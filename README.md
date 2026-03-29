# binhostess

binhostess (**binhost** **e**merge **s**yncing **s**ervice) is a client-server service
that allows gentoo users to emerge a package on a different machine, where the
binary is then copied to the original target machine.

gentoo's [binhost](https://wiki.gentoo.org/wiki/Gentoo_Binary_Host_Quickstart)
already provides this functionality; binhostess sits on top of portage and keeps
both machines synchronized for you! hence, "emerge syncing service."

## requirements

docker
