#!/usr/bin/env bash
# wait-for-it.sh from https://github.com/vishnubob/wait-for-it
# Usage: wait-for-it.sh host:port -- command args

set -e

host=$(echo $1 | cut -d: -f1)
port=$(echo $1 | cut -d: -f2)
shift

while ! nc -z $host $port; do
  echo "Waiting for $host:$port..."
  sleep 1
done

exec "$@"
