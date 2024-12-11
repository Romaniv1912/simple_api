# Simple API

## About

Simple API is a test task.

## Cerbos policy test

To check policy you can run a few possible commands

- run ```PolicyTest``` from config, _**need to build image before**_
- run the follow commands
    
    ```
    docker run --rm --name cerbos_test -t -v ./cerbos/:/cerbos_data \
       ghcr.io/cerbos/cerbos:latest compile --tests=/cerbos_data/tests /cerbos_data/policies
    ```
    
    or, _**need to build image before**_
    
    ```
    docker run --rm --name cerbos_test cerbos:latest \
       compile --tests=/cerbos_data/tests /cerbos_data/policies
    ```