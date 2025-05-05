#!/usr/bin/env sh


docker tag langflow:1.4.0 ghcr.io/enmaca/docker-images/langflow:latest
docker push ghcr.io/enmaca/docker-images/langflow:latest