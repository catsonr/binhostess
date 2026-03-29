#!/bin/sh

# actually, just going raw fs is way too dangerous. using docker...

echo "[BINHOSTESS::init] removing previous gentoo filesystem ..."
sudo rm -rf gentoo

echo "[BINHOSTESS::init] getting stage3 ..."
wget https://mirror.leaseweb.com/gentoo/releases/x86/autobuilds/current-stage3-i686-ssemath-t64-openrc/stage3-i686-ssemath-t64-openrc-20260324T164601Z.tar.xz

echo "[BINHOSTESS::init] unzipping stage3 ..."
mkdir gentoo
sudo tar xpf stage3-*.tar.xz --xattrs-include='*.*' --numeric-owner -C gentoo
sudo mv stage3-*.tar.xz gentoo

echo "[BINHOSTESS::init] done!"
