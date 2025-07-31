#!/usr/bin/env sh
VERSION=$(grep '^version *= *"' pyproject.toml | sed 's/.*"\(.*\)".*/\1/')

echo "Pushing version $VERSION to Docker Hub and GitHub Container Registry"

docker tag langflow:$VERSION ghcr.io/enmaca/docker-images/langflow:latest
docker push ghcr.io/enmaca/docker-images/langflow:latest