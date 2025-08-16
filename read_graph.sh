#!/bin/bash

if [ -z "${MEMORY_FILE_PATH}" ]; then
    echo "MEMORY_FILE_PATH is not set"
    exit 1
fi

[ -f "${MEMORY_FILE_PATH}" ] || { echo "Memory file not found"; exit 1; }
which npx || { echo "npx is not installed"; exit 1; }

printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"read_graph","arguments":{}}}' |  npx @modelcontextprotocol/server-memory > memory.json