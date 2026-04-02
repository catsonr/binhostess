#!/bin/sh

# SERVER SCRIPT
# concatinates the client's /etc/portage/make.conf (which was renamed client-make.conf), with /etc/portage/binhostess-make.conf
# (assumes existance of /etc/portage/binhostess-make.conf !)

echo "[BINHOSTESS::meow] concatinating /etc/portage.make.conf with /etc/binhostess-make.conf"

cat etc-portage/client-make.conf etc-portage/binhostess-make.conf > etc-portage/make.conf

echo "[BINHOSTESS::meow] concatinated"
