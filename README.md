# binhostess

binhostess (**binhost** **e**merge **s**yncing **s**ervice) is a client-server service that allows
gentoo users to emerge (install) a package first on a more power full machine (server), then copy
the compiled binary to the target machine (client).

gentoo's [binhost](https://wiki.gentoo.org/wiki/Gentoo_Binary_Host_Quickstart) already provides this
functionality; binhostess simply sits on top of portage and keeps both machines synchronized and
emerging for you!

hence, "**emerge syncing service.**"

## requirements

the client (target machine) requires:

 - a working gentoo install
 - rsync
 - python3 (or any static http site to host `var-cache-binpkgs/`

the server (faster machine) requires:

 - docker
 - python3

*note that the server need not be running gentoo!*

## usage

### set

**set** is not yet implemented. it is to be used to configure binhostess. see
`/etc/portage/binhostess.conf`

#### set fields

`server-host` the user and ip for server. e.g.: `cassie@192.168.0.1`

`server-path` the location for the gentoo docker container. e.g.: `~/.binhostess`

binhostess needs to be both *synchronized* and *initialized* before being used.

### sync

**sync** copies `/etc/portage/` (directory), `/var/lib/portage/world`, and
`/var/lib/portage/world_sets` (files) to the server. this allows the client and server's respective
portages to be configured the same, meaning they both produce and use the same binaries!

### init

**init** installs a gentoo instance into the directory `gentoo/`; containerized inside of docker.
here you can additionally emerge @world.

## emerge

to emerge a package, simply prepend `binhostess` to any given emerge command. e.g.:

`binhostess emerge "--ask app-editors/vim"`

**for now, you must wrap any emerge arguments in quotes. sorry!**

this will first emerge on the serer, creating a binary per the client's configuration (like
`/etc/portage/make.conf`). the server then opens an http server to host the binary, the client runs
the emerge command, portage's binhost detects this server and installs the binary. the http server
is then closed.
