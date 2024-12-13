# Simple API

## About

Simple API is a test task.

## Cerbos policy test

To check policy you can run a few possible commands

- run the follow command
    
    ```
    docker run --rm --name cerbos_test -t -v ./cerbos/:/cerbos_data \
       ghcr.io/cerbos/cerbos:latest compile --tests=/cerbos_data/tests /cerbos_data/policies
    ```