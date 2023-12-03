# README.md for NATS OpenAI Proxy

## Introduction

NATS OpenAI Proxy is a Python-based command-line tool designed to facilitate interactions between client applications and OpenAI's GPT models using NATS as a messaging server. It serves as a proxy, accepting chat requests from a NATS queue, querying OpenAI's GPT models with these requests, and then sending the responses back to the client via NATS, with added support for NATS nkeys and TLS encryption for secure communication.

## What is NATS OpenAI Proxy?

NATS OpenAI Proxy integrates the advanced natural language processing capabilities of OpenAI's GPT models into various applications through a robust, scalable messaging system, NATS. The tool is especially useful for applications requiring secure, scalable, distributed, and asynchronous communication.

## Why NATS OpenAI Proxy?

The tool simplifies the complexity involved in interfacing client applications with OpenAI's GPT models. By leveraging NATS with nkeys and TLS support, it provides a secure, reliable, and scalable way to handle communication between clients and AI models.

## How It Works

NATS OpenAI Proxy listens on a specified NATS subject (channel) for messages. Upon receiving a message, it processes the chat request through an OpenAI GPT model and sends back the response via NATS. It supports NATS nkeys for authentication and TLS for secure communication.

## Requirements

- Python 3.6+
- `nats.py`
- `openai`
- `pyyaml`
- `argparse`
- `nkeys`

## Installation

Install the required Python packages using pip:

```bash
pip install nats.py openai pyyaml argparse nkeys
```

## Configuration

Configuration is managed through a `config.yaml` file. The default configuration includes:

- NATS server URL
- OpenAI API key
- NATS subject to listen on
- OpenAI GPT model (engine) to use
- NATS nkey seed file (for authentication)
- TLS configuration for NATS (certificate, key, and CA file)

## Command-Line Arguments

- `--config`: Path to the configuration file. Default: `config.yaml`
- `--nats_server`: Specify the NATS server address.
- `--openai_api_key`: Provide the OpenAI API key.
- `--subject`: Set the NATS subject to listen on for incoming requests.
- `--engine`: Choose the OpenAI GPT model for processing requests.
- `--nkey_seed_file`: Path to the NATS nkey seed file for authentication.
- `--tls_cert`: Path to the TLS certificate file.
- `--tls_key`: Path to the TLS key file.
- `--tls_ca`: Path to the TLS CA file (optional).

These arguments allow for overriding the default configuration or the settings specified in `config.yaml`.

## NATS, OpenAI, and Security

NATS provides the messaging infrastructure with added security features like nkeys and TLS, ensuring authenticated and encrypted communication. OpenAI's GPT models offer advanced AI capabilities. OpenAINATSProxy bridges these technologies, ensuring secure and intelligent message handling.

## Getting Started

1. Configure the `config.yaml` file with your NATS, OpenAI details, and security settings.

```
nats:
  server: "nats://localhost:4222"
  subject: "openai_requests"
  nkey_seed_file: "path/to/nkey_seed_file"
  tls:
    enabled: true
    cert: "path/to/cert.pem"
    key: "path/to/key.pem"
    ca: "path/to/ca.pem" # Optional
```
2. Run the application using `python nats-openai-proxy.py`.

### Start NATS
```bash
$ nats-server -D
[687918] 2023/12/03 21:22:36.982451 [INF] Starting nats-server
[687918] 2023/12/03 21:22:36.982594 [INF]   Version:  2.10.6
[687918] 2023/12/03 21:22:36.982603 [INF]   Git:      [77e4ac6]
[687918] 2023/12/03 21:22:36.982613 [DBG]   Go build: go1.21.4
[687918] 2023/12/03 21:22:36.982616 [INF]   Name:     NCY5TPJTMAUBVVGAYZEAMUDQ3WAMW3FVZM2TISSMJ5DBLNGOUEZ5MAQP
[687918] 2023/12/03 21:22:36.982625 [INF]   ID:       NCY5TPJTMAUBVVGAYZEAMUDQ3WAMW3FVZM2TISSMJ5DBLNGOUEZ5MAQP
[687918] 2023/12/03 21:22:36.982645 [DBG] Created system account: "$SYS"
[687918] 2023/12/03 21:22:36.983350 [INF] Listening for client connections on 0.0.0.0:4222
[687918] 2023/12/03 21:22:36.983371 [DBG] Get non local IPs for "0.0.0.0"
[687918] 2023/12/03 21:22:36.983612 [DBG]   ip=149.28.127.156
[687918] 2023/12/03 21:22:36.983648 [DBG]   ip=172.17.0.1
[687918] 2023/12/03 21:22:36.983695 [INF] Server is ready
[687918] 2023/12/03 21:22:36.984544 [DBG] maxprocs: Leaving GOMAXPROCS=2: CPU quota undefined
```

### Start the Openai Proxy Service
```bash
$ python3 src/nats-openai-proxy.py --config ./config/config.yaml 
INFO:root:Connected to NATS Server
INFO:root:Listening for requests on 'openai_requests'
```

### Make a request to Openai through the NATS queue 'openai_requests' using the [nats cli](https://github.com/nats-io/natscli)
```bash
$ nats request 'openai_requests' "List the last 10 presidents" --timeout=20000ms
21:24:08 Sending request on "openai_requests"
21:24:16 Received with rtt 8.183064673s
As of August 2021:

1. Joe Biden (2021-present)
2. Donald Trump (2017-2021)
3. Barack Obama (2009-2017)
4. George W. Bush (2001-2009)
5. Bill Clinton (1993-2001)
6. George H. W. Bush (1989-1993)
7. Ronald Reagan (1981-1989)
8. Jimmy Carter (1977-1981)
9. Gerald Ford (1974-1977)
10. Richard Nixon (1969-1974)

```

3. Override configuration settings as needed using command-line arguments.

### Start the OpanAI Proxy service using a different model (engine) and enable debugging
```
$ python3 src/nats-openai-proxy.py --config ./config/config.yaml --engine gpt-3.5-turbo-0613 --debug true
DEBUG:asyncio:Using selector: EpollSelector
INFO:root:Connected to NATS Server
INFO:root:Listening for requests on 'openai_requests'
INFO:root:Handling request 'List the last 10 presidents'
DEBUG:root:Making call to OpenAI...
DEBUG:root:Using OpenAI Key: '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'
DEBUG:httpx:load_ssl_context verify=True cert=None trust_env=True http2=False
DEBUG:httpx:load_verify_locations cafile='/etc/ssl/certs/ca-certificates.crt'
DEBUG:openai._base_client:Request options: {'method': 'post', 'url': '/chat/completions', 'files': None, 'json_data': {'messages': [{'role': 'user', 'content': 'List the last 10 presidents'}], 'model': 'gpt-3.5-turbo-0613'}}
DEBUG:httpcore.connection:connect_tcp.started host='api.openai.com' port=443 local_address=None timeout=5.0 socket_options=None
DEBUG:httpcore.connection:connect_tcp.complete return_value=<httpcore._backends.sync.SyncStream object at 0x7f69f356ae90>
DEBUG:httpcore.connection:start_tls.started ssl_context=<ssl.SSLContext object at 0x7f69f34bf2c0> server_hostname='api.openai.com' timeout=5.0
DEBUG:httpcore.connection:start_tls.complete return_value=<httpcore._backends.sync.SyncStream object at 0x7f69f356ae60>
DEBUG:httpcore.http11:send_request_headers.started request=<Request [b'POST']>
DEBUG:httpcore.http11:send_request_headers.complete
DEBUG:httpcore.http11:send_request_body.started request=<Request [b'POST']>
DEBUG:httpcore.http11:send_request_body.complete
DEBUG:httpcore.http11:receive_response_headers.started request=<Request [b'POST']>
DEBUG:httpcore.http11:receive_response_headers.complete return_value=(b'HTTP/1.1', 200, b'OK', [(b'Date', b'Sun, 03 Dec 2023 21:35:33 GMT'), (b'Content-Type', b'application/json'), (b'Transfer-Encoding', b'chunked'), (b'Connection', b'keep-alive'), (b'access-control-allow-origin', b'*'), (b'Cache-Control', b'no-cache, must-revalidate'), (b'openai-model', b'gpt-3.5-turbo-0613'), (b'openai-organization', b'tony-mendoza-inc'), (b'openai-processing-ms', b'2251'), (b'openai-version', b'2020-10-01'), (b'strict-transport-security', b'max-age=15724800; includeSubDomains'), (b'x-ratelimit-limit-requests', b'5000'), (b'x-ratelimit-limit-tokens', b'80000'), (b'x-ratelimit-limit-tokens_usage_based', b'80000'), (b'x-ratelimit-remaining-requests', b'4999'), (b'x-ratelimit-remaining-tokens', b'79976'), (b'x-ratelimit-remaining-tokens_usage_based', b'79976'), (b'x-ratelimit-reset-requests', b'12ms'), (b'x-ratelimit-reset-tokens', b'18ms'), (b'x-ratelimit-reset-tokens_usage_based', b'18ms'), (b'x-request-id', b'a5f2c2ba533b009a4abf9124675c9229'), (b'CF-Cache-Status', b'DYNAMIC'), (b'Set-Cookie', b'__cf_bm=XbPt9eLt2Saxv0eQSBITK9WDaPcCXU8uSuAvZ.T.ASo-1701639333-0-AccnD2Uml+j4/CLCPIz7MulQYPP3t3GdDRHDELqh4to/jNe6ndsn6PVk38zTSN3q5R3TsmtsqabSmY2bKE6Q3s4=; path=/; expires=Sun, 03-Dec-23 22:05:33 GMT; domain=.api.openai.com; HttpOnly; Secure; SameSite=None'), (b'Set-Cookie', b'_cfuvid=uIbo3X1.zOB.h3WqKBa5ucd1SgdVibhR_N6HEx3QEbo-1701639333093-0-604800000; path=/; domain=.api.openai.com; HttpOnly; Secure; SameSite=None'), (b'Server', b'cloudflare'), (b'CF-RAY', b'82fef0978c5c60b3-ORD'), (b'Content-Encoding', b'gzip'), (b'alt-svc', b'h3=":443"; ma=86400')])
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
DEBUG:httpcore.http11:receive_response_body.started request=<Request [b'POST']>
DEBUG:httpcore.http11:receive_response_body.complete
DEBUG:httpcore.http11:response_closed.started
DEBUG:httpcore.http11:response_closed.complete
DEBUG:openai._base_client:HTTP Request: POST https://api.openai.com/v1/chat/completions "200 OK"
DEBUG:root:Returned completion: '1. Donald Trump (2017-2021)
2. Barack Obama (2009-2017)
3. George W. Bush (2001-2009)
4. Bill Clinton (1993-2001)
5. George H.W. Bush (1989-1993)
6. Ronald Reagan (1981-1989)
7. Jimmy Carter (1977-1981)
8. Gerald Ford (1974-1977)
9. Richard Nixon (1969-1974)
10. Lyndon B. Johnson (1963-1969)'
DEBUG:root:Publishing results back to client... 1. Donald Trump (2017-2021)
2. Barack Obama (2009-2017)
3. George W. Bush (2001-2009)
4. Bill Clinton (1993-2001)
5. George H.W. Bush (1989-1993)
6. Ronald Reagan (1981-1989)
7. Jimmy Carter (1977-1981)
8. Gerald Ford (1974-1977)
9. Richard Nixon (1969-1974)
10. Lyndon B. Johnson (1963-1969)
```


## Contributions and Support

Contributions are welcome. Submit issues and pull requests through GitHub. For support, use the project's issue tracker.

## License

NATS OpenAI Proxy is released under the [MIT License](LICENSE).

---

This revised README includes the necessary information about the added NATS nkeys and TLS features, ensuring users understand the enhanced security capabilities of the OpenAINATSProxy tool.