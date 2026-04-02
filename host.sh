#!/bin/sh

echo "[BINHOSTESS::host] starting server ..."

python3 -m http.server 8322 --directory var-cache-binpkgs

echo "[BINHOSTESS::host] stopping server ..."
