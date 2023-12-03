import asyncio
import openai
import yaml
import logging
import argparse

import nats, nkeys
from nats.aio.client import Client as NATS
import ssl

# Rest of the application code...

class OpenAINATSProxy:
    def __init__(self, config):
        self.config = config
        self.nc = NATS()


    async def connect_to_nats(self):
        options = {
            "servers": config["nats"]["server"],
            "name": "OpenAINATSProxy"
        }

        # Configure nkeys if provided
        if config["nats"]["nkey"]["enabled"]:
            if "seed_file" in config["nats"]["nkey"]:
                with open(config["nats"]["nkey"]["seed_file"]) as f:
                    seed = f.read()
                nk = nkeys.from_seed(seed.encode())
                options["nkeys_seed"] = seed
                options["signature_cb"] = lambda nonce: nk.sign(nonce.encode())

        # Configure TLS if enabled
        if config["nats"]["tls"]["enabled"]:
            context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH)
            
            if "ca" in config["nats"]["tls"]:
                context.load_verify_locations(cafile=config["nats"]["tls"]["ca"])
            
            context.load_cert_chain(
                certfile=config["nats"]["tls"]["cert"],
                keyfile=config["nats"]["tls"]["key"]
            )
            options["tls"] = context

        try:
            await self.nc.connect(**options)
            logging.info("Connected to NATS Server")
        except Exception as e:
            logging.error(f"Failed to connect to NATS server: {e}")
            exit(1)

    async def listen_for_requests(self):
        # subject = self.config.get('subject', 'chat_requests')
        subject = self.config['nats']['subject']
        await self.nc.subscribe(subject, cb=self.handle_request)
        logging.info(f"Listening for requests on '{subject}'")

    async def handle_request(self, msg):
        data = msg.data.decode()
        logging.info(f"Handling request '{data}'")
        try:
            logging.debug("Making call to OpenAI...")
            response = self.query_openai(data)
            logging.debug(f"Publishing results back to client... {response}")
            await self.nc.publish(msg.reply, response.encode())
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            await self.nc.publish(msg.reply, b"Error processing request")

    def query_openai(self, prompt):
        # optional; defaults to `os.environ['OPENAI_API_KEY']`
        openai.api_key = self.config['nats']['openai_api_key']
        logging.debug(f"Using OpenAI Key: '{openai.api_key}'")

        completion = openai.chat.completions.create(
            model= self.config['nats']['engine'],
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        logging.debug(f"Returned completion: '{completion.choices[0].message.content}'")
        return completion.choices[0].message.content

    async def run(self):
        await self.connect_to_nats()
        await self.listen_for_requests()

def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def parse_arguments():
    parser = argparse.ArgumentParser(description="OpenAI-NATS Proxy Service")
    parser.add_argument("--config", help="Path to the configuration file", default="config.yaml")
    parser.add_argument("--nats_server", help="NATS server address")
    parser.add_argument("--openai_api_key", help="OpenAI API key")
    parser.add_argument("--subject", help="NATS subject to listen on")
    parser.add_argument("--engine", help="OpenAI engine to use")
    parser.add_argument("--nkey_enabled", help="NATS Nkey tokens enabled.", default=False)
    parser.add_argument("--nkey_seed_file", help="Path to the NATS nkey seed file for authentication.")
    parser.add_argument("--tls_enabled", help="NATS TLS Security enabled.  Default = false", default=False)
    parser.add_argument("--tls_cert", help="Path to the TLS certificate file.")
    parser.add_argument("--tls_key", help="Path to the TLS key file.")
    parser.add_argument("--tls_ca", help="Path to the TLS CA file (optional).")
    parser.add_argument("--debug", help="Enable debug logging (optional).  Default = false", default=False)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Load configuration file
    config = load_config(args.config)


    # Override config with CLI arguments if provided
    if args.nats_server:
        config['nats']['server'] = args.nats_server
    if args.openai_api_key:
        config['nats']['openai_api_key'] = args.openai_api_key
    if args.subject:
        config['nats']['subject'] = args.subject
    if args.engine:
        config['nats']['engine'] = args.engine
    if args.nkey_enabled:
        config['nats']['nkey']['enabled'] = args.nkey_enabled
    if args.nkey_seed_file:
        config['nats']['nkey']['seed_file'] = args.nkey_seed_file
    if args.tls_enabled:
        config['nats']['tls']['enabled'] = args.tls_enabled
    if args.tls_cert:
        config['nats']['tls']['cert'] = args.tls_cert
    if args.tls_key:
        config['nats']['tls']['key'] = args.tls_key
    if args.tls_ca:
        config['nats']['tls']['ca'] = args.tls_ca


    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Run the service
    loop = asyncio.get_event_loop()
    loop.run_until_complete(OpenAINATSProxy(config).run())
    loop.run_forever()
    loop.close()

