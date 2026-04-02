#!/bin/sh

# SERVER SCRIPT
# creates the server's docker gentoo instance named "gentoo"

# stolen from:
# https://stackoverflow.com/questions/1885525/how-do-i-prompt-a-user-for-confirmation-in-bash-script
read -p "[BINHOSTESS::init] initializing binhostess! this will remove any existing containers. would you like to continue? [y/n]" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
fi

echo "[BINHOSTESS::init] removing existing gentoo file system ..."
docker compose down -v

echo "[BINHOSTESS::init] creating new gentoo file system ..."
docker compose up -d

echo "[BINHOSTESS::init] performing initial 'emerge --sync'"
docker compose exec gentoo emerge --sync

read -p "[BINHOSTESS::init] would you like to emerge @world? [y/n]" -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1
fi

docker compose exec -it gentoo emerge --ask @world
