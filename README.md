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

## Installation

Install the required Python packages using pip:

```bash
pip install nats.py openai pyyaml argparse
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
3. Override configuration settings as needed using command-line arguments.

## Contributions and Support

Contributions are welcome. Submit issues and pull requests through GitHub. For support, use the project's issue tracker.

## License

NATS OpenAI Proxy is released under the [MIT License](LICENSE).

---

This revised README includes the necessary information about the added NATS nkeys and TLS features, ensuring users understand the enhanced security capabilities of the OpenAINATSProxy tool.