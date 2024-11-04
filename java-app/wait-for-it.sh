#!/usr/bin/env bash
host=$1
port=$2
timeout=${3:-30}

for ((i=1;i<=timeout;i++)); do
    nc -z "$host" "$port" && echo "$host:$port is available" && exit 0
    echo "Waiting for $host:$port... $i seconds elapsed"
    sleep 1
done

echo "$host:$port did not become available within $timeout seconds"
exit 1
