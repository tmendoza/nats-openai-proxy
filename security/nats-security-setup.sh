#!/bin/bash

# This is a script that walks thru the securitty setup process for NATS.  This is a PITA so I coded it up quickly for you
# This is using a self-signed cert.  The info in here is my own personal test info.  
# PLEASE REPLACE!  THIS IS JUST A EXAMPLE OF WHAT TO DO!
#
# NOTE: Make sure you have the 'conf' file generated.  You may also need to copy them to the current directory of change
#       the paths in the script to their location.  There are examples in the templates directory of the repo.

rm -f *.pem *.crt *.srl *.key *.csr

# Generate the CA's rpivate key (ca-key.pem) and a self-signed certificate (ca-cert.pem)
# openssl req -x509 -newkey rsa:4096 -days 365 -keyout ca-key.pem -out ca-cert.pem -subj "/C=US/ST=Illinois/L=Chicago/O='Bloom, Inc.'/OU=Infrastructure/CN=clueelf.io/emailAddress=commercial@tonymendoza.us"

openssl req -x509 \
            -sha256 -days 356 \
            -nodes \
            -newkey rsa:2048 \
            -subj "/CN=clueelf.io/C=US/ST=Illinois/L=Chicago" \
            -keyout rootCA.key -out rootCA.crt 


# Generate Server side private key
openssl genrsa -out server.key 2048

# Generate Client side private key 
openssl genrsa -out client.key 2048

# Generate Server's certificate signing request (CSR)
openssl req -new -key server.key -out server.csr -config server-csr.conf

# Generate Client's certificate signing request (CSR)
openssl req -new -key client.key -out client.csr -config client-csr.conf

# Use the CA's private key to sign the server & client's CSR and get back the signed certificate

# Server Side
openssl x509 -req \
    -in server.csr \
    -CA rootCA.crt -CAkey rootCA.key \
    -CAcreateserial -out server.crt \
    -days 365 \
    -sha256 -extfile cert.conf

# Client Side
openssl x509 -req \
    -in client.csr \
    -CA rootCA.crt -CAkey rootCA.key \
    -CAcreateserial -out client.crt \
    -days 365 \
    -sha256 

# Launch the NATS Server
# nats-server --tls --tlscert=server.crt --tlskey=server.key --tlscacert=rootCA.crt --tlsverify

# Launch the NATS Client
# nats bench --tlsca=rootCA.crt --tlscert=client.crt --tlskey=client.key \
#    benchsubject --pub 1 --sub 10 --server=nats://127.0.0.1:4222

