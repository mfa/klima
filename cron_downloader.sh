#!/bin/sh

set -e

(
    cd ~/klima
    docker run --rm -v `pwd`:/opt/code --name klima-downloader klima download
)
