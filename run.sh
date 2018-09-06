#!/bin/bash
BASEDIR="$(realpath `dirname $0`)"

if [ "$1" == "sleep" ]; then
    exec sleep infinity
    exit 0
fi

if [ "$1" == "shell" ]; then
    PYTHONPATH="." ipython3 || exit $?
    exit 0
fi

if [ "$1" == "tests" ]; then
    shift
    cd "$BASEDIR"
    PYTHONPATH="." py.test $@ || exit $?
    cd -
fi

if [ "$1" == "download" ]; then
    cd klima
    python downloader.py
    cd -
fi
