#!/usr/bin/env bash
IMAGE_NAME="diceroller:latest"
case "$1" in
    build)
        echo "building $IMAGE_NAME for usage on port 8000"
        docker build -t diceroller:latest -f ./docker/diceroller.dockerfile .
        ;;
    run)
        echo "running $IMAGE_NAME on port 8000"
        docker run -it --rm -p 8000:8000 diceroller:latest
        ;;
    *)
        echo "usage: $0 {build|run}"
        exit 1
        ;;
esac