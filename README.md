# binhostess

binhostess (**binhost** **e**merge **s**yncing **s**ervice) is a client-server service that allows
gentoo users to emerge (install) a package first on a more powerful machine (server), then copy
the compiled binary to the target machine (client).

gentoo's [binhost](https://wiki.gentoo.org/wiki/Gentoo_Binary_Host_Quickstart) already provides this
functionality; binhostess simply sits on top of portage and keeps both machines synchronized and
emerging for you!

hence, "**emerge syncing service.**"

## requirements

the client (target machine) requires:

 - ssh
 - a working gentoo install
 - rsync
 - python3

the server (faster machine) requires:

 - ssh
 - docker
 - python3

*note that the server need not be running gentoo!*

## usage

### set

**set** is not yet implemented. it is used to configure binhostess. for now, you can configure
binhostess by editing `/etc/portage/binhostess.conf`

#### set fields

`server_host` the user and ip for server. e.g.: `cassie@192.168.0.1`

`server_path` the location where binhostess will be installed. e.g.: `~/.binhostess`

for this user, their file would look like:
```
server_host=cassie@192.168.0.1
server_path=~/.binhostess
```

binhostess needs to be both *initialized* and *synchronized* before being used.

### init

**init** installs a gentoo instance into the directory `gentoo/`; containerized inside of docker, as
well as writes the binhost file `/etc/portage/binrepos.conf/binhostess.conf` so the client's portage
knows how to find the server. if the server is not running for one reason or the other, init will
start it.

### sync

**sync** copies `/etc/portage/` (directory), `/var/lib/portage/world`, and
`/var/lib/portage/world_sets` (files) to the server. this allows the client and server's respective
portages to be configured the same, meaning they both produce and use the same binaries!

here you can additionally `emerge --sync`

## emerge

to emerge a package, simply prepend `binhostess` to any given emerge command. e.g.:

`binhostess emerge "--ask app-editors/vim"`

**for now, you must wrap any emerge arguments in quotes. sorry!**

this will first emerge on the serer, creating a binary per the client's configuration (like
`/etc/portage/make.conf`). the server then opens an http server to host the binary, the client runs
the emerge command, portage's binhost detects this server and installs the binary. the http server
is then closed.

## maintenance

binhostess keeps the client and server *synchronized*, not working. so long as you follow sensible
[portage maintenance](https://wiki.gentoo.org/wiki/Portage/Help/Maintaining_a_Gentoo_system)
binhostess will be able to produce compatible binaries with your target machine.
