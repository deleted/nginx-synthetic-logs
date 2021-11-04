#!/bin/bash
docker build -t generate_nginx_logs . && docker run --rm generate_nginx_logs
