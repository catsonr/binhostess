#!/bin/sh

# SERVER SCRIPT
# copies the /etc/portage/ of client to server's docker gentoo instance "gentoo"
# over SSH using rsync
# and also renames make.conf to client-make.conf!
#
# where CLIENT is some "user@ip"

CLIENT=$1

echo "[BINHOSTESS::sync] syncing etc/porgate's!"
rsync -avP --delete --exclude='gnupg/' --exclude='binrepos.conf/' "$CLIENT:/etc/portage/" etc-portage
rsync -avP "$CLIENT:/var/lib/portage/world" var-lib-portage-world

mv etc-portage/make.conf etc-portage/client-make.conf

echo "[BINHOSTESS::sync] synced"

sh meow.sh
