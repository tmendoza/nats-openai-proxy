import asyncio
import openai
import yaml
import logging
import argparse

import nats
from nats.aio.client import Client as NATS
from nats.aio.nkeys import NKeys
import ssl

# Rest of the application code...

class OpenAINATSProxy:
    def __init__(self, config):
        self.config = config
        self.nc = NATS()

    # Setup NATS connection with nkeys and TLS
    async def secure_connect_to_nats():
        options = {
            "servers": config["nats"]["server"],
            "name": "OpenAINATSProxy"
        }

        # Configure nkeys if provided
        if "nkey_seed_file" in config["nats"]:
            with open(config["nats"]["nkey_seed_file"]) as f:
                seed = f.read()
            nk = NKeys.from_seed(seed.encode())
            options["nkeys_seed"] = seed
            options["signature_cb"] = lambda nonce: nk.sign(nonce.encode())

        # Configure TLS if enabled
        if config["nats"]["tls"]["enabled"]:
            context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(
                certfile=config["nats"]["tls"]["cert"],
                keyfile=config["nats"]["tls"]["key"]
            )
            if "ca" in config["nats"]["tls"]:
                context.load_verify_locations(cafile=config["nats"]["tls"]["ca"])
            options["tls"] = context

        # Connect to NATS
        await nats.connect(**options)

    async def connect_to_nats(self):
        try:
            await self.nc.connect(servers=[self.config['nats_server']])
            logging.info("Connected to NATS Server")
        except Exception as e:
            logging.error(f"Failed to connect to NATS server: {e}")
            exit(1)

    async def listen_for_requests(self):
        subject = self.config.get('subject', 'chat_requests')
        await self.nc.subscribe(subject, cb=self.handle_request)
        logging.info(f"Listening for requests on '{subject}'")

    async def handle_request(self, msg):
        data = msg.data.decode()
        try:
            response = self.query_openai(data)
            await self.nc.publish(msg.reply, response.encode())
        except Exception as e:
            logging.error(f"Error handling request: {e}")
            await self.nc.publish(msg.reply, b"Error processing request")

    def query_openai(self, prompt):
        openai.api_key = self.config['openai_api_key']
        response = openai.Completion.create(engine=self.config.get('engine', "text-davinci-004"), prompt=prompt)
        return response.choices[0].text.strip()

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
    parser.add_argument("--nkey_seed_file", help="Path to the NATS nkey seed file for authentication.")
    parser.add_argument("--tls_cert", help="Path to the TLS certificate file.")
    parser.add_argument("--tls_key", help="Path to the TLS key file.")
    parser.add_argument("--tls_ca", help="Path to the TLS CA file (optional).")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    # Load configuration file
    config = load_config(args.config)

    """
    nats:
    server: "nats://localhost:4222"
    subject: "openai_requests"
    openai_api_key: "your-openai-api-key"
    engine: "text-davinci-004"
    nkey_seed_file: "path/to/nkey_seed_file"
    tls:
        enabled: true
        cert: "path/to/cert.pem"
        key: "path/to/key.pem"
        ca: "path/to/ca.pem" # Optional
    """
    # Override config with CLI arguments if provided
    if args.nats.server:
        config['nats.server'] = args.nats.server
    if args.nats.openai_api_key:
        config['nats.openai_api_key'] = args.nats.openai_api_key
    if args.nats.subject:
        config['nats.subject'] = args.nats.subject
    if args.nats.engine:
        config['nats.engine'] = args.nats.engine
    if args.nats.nkey_seed_file:
        config['nats.nkey_seed_file'] = args.nats.nkey_seed_file
    if args.nats.tls.enabled:
        config['nats.tls.enabled'] = args.nats.tls.enabled
    if args.nats.tls.cert:
        config['nats.tls.cert'] = args.nats.tls.cert
    if args.nats.tls.key:
        config['nats.tls.key'] = args.nats.tls.key
    if args.nats.tls.ca:
        config['nats.tls.ca'] = args.nats.tls.ca

    # Setup logging
    logging.basicConfig(level=logging.INFO)

    # Run the service
    proxy = OpenAINATSProxy(config)
    asyncio.run(proxy.run())
