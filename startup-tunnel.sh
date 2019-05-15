#! /bin/bash

wait_for_response()
{
    while ! nc -z response 8000;
    do sleep 1;
    done;
}

echo "[INFO] Waiting for response"
wait_for_response
echo "[INFO] Response found. Initiating tunnel."

/cloudflare/cloudflared tunnel