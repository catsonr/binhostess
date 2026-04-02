# binhostess

binhostess (**binhost** **e**merge **s**yncing **s**ervice) is a client-server service that allows
gentoo users to emerge a package on a different machine (server), where the binary is then copied to
the original target machine (client).

gentoo's [binhost](https://wiki.gentoo.org/wiki/Gentoo_Binary_Host_Quickstart) already provides this
functionality; binhostess sits on top of portage and keeps both machines synchronized and emerging
for you!

hence, "emerge syncing service."

## requirements

 - docker
 - rsync
 - python3 (or any static http site to host `var-cache-binpkgs/`

## usage

binhostess needs to be both *synchronized* and *initialized* before being used.

### sync.sh

`sync.sh` copies the `/etc/portage/` (and other related files) from `client` to `server`. if you
haven't used binhostess in a while you can synchronize from the server

`server $ sh sync.sh user@client-ip`

the server's gentoo instance now matches the client.

### init.sh

`init.sh` installs a gentoo instance into the directory `gentoo/`; containerized inside of docker.
here you can additionally emerge @world.

**NOTE:** for now, init.sh assumes a very specific stage3. please replace the link in init.sh with
your desired stage3 tar.gz. 

## hosting

to host the server's compiled binaries in `var/cache/binpkgs`, simply run `sh host.sh`

on the client, please create `/etc/portage/binrepos.conf/binhostess` with the contents:
```
[binhostess]
priority=1
sync-uri=http://user@server-ip:8322
location=/var/cache/binhost/binhostess
verify-signature=false
```

## emerging

to emerge a package, first emerge on the server

`server $ docker compose exec gentoo emerge package`

and then on the client

`client $ emerge --getbinpkg package`

the package is now emerged. hopefully much quicker than if it was compiled on client!
