#!/bin/sh

set -e

git pull

# build new image for cron
docker build --tag=klima .
