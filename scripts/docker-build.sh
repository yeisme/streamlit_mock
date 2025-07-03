#!/bin/bash

version=${1:-latest}

docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t yeisme0123/streamlit_mock:latest \
    -t yeisme0123/streamlit_mock:${version} \
    -f Dockerfile \
    .
