#!/usr/bin/env python3

# binhostess.py is the client-side CLI for binhostess

import time
import argparse
import subprocess
import sys
from pathlib import Path
from dataclasses import dataclass, fields

HERE = Path(__file__).parent

# --- config ---

# /etc/portage/binhostess.conf object
@dataclass
class Conf:
    server_host: str = ""
    server_path: str = ""

    @staticmethod
    def path() -> Path:
        return Path("/etc/portage/binhostess.conf")

    @classmethod
    def load(cls) -> "Conf":

        conf = cls()
        try:
            for line in cls.path().read_text().splitlines():
                line = line.strip()
                if line.startswith("#"):
                    continue
                elif "=" in line:
                    k, v = line.split("=", 1)
                    k, v = k.strip(), v.strip().strip('"')
                    if k in { f.name for f in fields(cls) }:
                        setattr(conf, k, v)

        except FileNotFoundError:
            print("[binhostess::Conf::load] could not find /etc/portage/binhostess.conf !")
        
        return conf

    def save(self) -> None:
        lines = [ f'{f.name}={getattr(self, f.name)}' for f in fields(self) ]
        self.path().write_text("\n".join(lines) + "\n")

    def user(self) -> str:
        return self.server_host.split('@')[0]
    def ip(self) -> str:
        return self.server_host.split('@')[-1]

# --- util functions ---

# runs a shell command on client
def run(args, **kwargs):
    kwargs.setdefault("check", True)
    return subprocess.run(args, **kwargs)

# runs a shell command on server
def remote(cmd, **kwargs):
    conf = Conf.load()
    run(["ssh", "-t", conf.server_host, f"cd {conf.server_path} && {cmd}"], **kwargs)

# generates the string to be saved at /etc/portage/binrepos.conf/binhostess.conf
def repo_str() -> str:
    conf = Conf.load()
    return f"[binhostess]\npriority=8322\nsync-uri=http://{conf.ip()}:8322\nlocation=/var/cache/binhost/binhostess\nverify_signature=false\n"

# writes /etc/portage/binrepos.conf/binhostess
def repo():
    run(["sudo", "tee", "/etc/portage/binrepos.conf/binhostess.conf"], input=repo_str(), text=True, stdout=subprocess.DEVNULL)

# --- subcommands ---

# prints out the current binhostess config
def get():
    print(Conf.load())

# sets binhostess.conf values
# e.g.: `set server-host user@192.168.0.1`
def set(args):
    pass

# syncs server with client. namely:
# /etc/portage/ (excluding gnupg/ and binrepos.conf/binhostess.conf),
# /var/lib/portage/world, and 
# /var/lib/portage/world_sets
def sync(args):
    conf = Conf.load()
    host = conf.server_host
    path = conf.server_path
    dest = f"{host}:{path}"

    # push /etc/portage
    print(f"[BINHOSTESS::sync] copying /etc/portage to {dest}/etc-portage ...")
    run([
        "rsync", "-avP", "--delete",
        "--exclude=gnupg/",
        "--exclude=binrepos.conf/binhostess.conf",
        "--exclude=binhostess.conf",
        "/etc/portage",
        f"{dest}/etc-portage"
    ])

    # push var/lib/portage/world and var/lib/portage/world_sets
    print(f"[BINHOSTESS::sync] copying /var/lib/portage/world and /var/lib/portage/world_sets to {dest}/var-lib-portage ...")
    run([
        "rsync", "-avP",
        "/var/lib/portage/world",
        "/var/lib/portage/world_sets",
        f"{dest}/var-lib-portage/"
    ])

    # cat client-make.conf with binhostess-make.conf
    print(f"[BINHOSTESS::sync] concatinating client-make.conf with server-make.conf ...")
    run([
        "ssh", host,
        f"cd {path}/etc-portage && "
        "mv make.conf client-make.conf && "
        "cat client-make.conf binhostess-make.conf > make.conf"
    ])

    print("[BINHOSTESS::sync] synchronized!")

# creates gentoo docker container
def init(args):
    conf = Conf.load()

    answer = input("[BINHOSTESS::init] would you like to remove any existing docker containers? [y/n] ")
    if answer.lower() == "y" or answer.lower() == "yes":
        print("[BINHOSTESS::init] closing container ...")
        remote("docker compose down -v")

    print("[BINHOSTESS::init] starting container \"gentoo\"...")
    remote("docker compose up -d")

    print("[BINHOSTESS::init] performing 'emerge --sync' ...")
    remote("docker compose exec gentoo emerge --sync", check=False)

    print("[BINHOSTESS::init] writing /etc/portage/binrepos.conf/binhostess.conf ...")
    repo()

    print("[BINHOSTESS::init] initialization complete. ready to emerge!")

    answer = input("[BINHOSTESS::init] would you like to emerge @world ? [y/n] ")
    if answer.lower() != "y" and answer.lower() != "yes":
        return

    remote("docker compose exec -it gentoo emerge --ask @world")

def emerge(args):
    conf = Conf.load()

    print(f"[BINHOSTESS::emerge] performing 'emerge {args.args}' on {conf.server_host} ...")
    remote(f"docker compose exec gentoo emerge {args.args}", check=False)

    print(f"[BINHOSTESS::emerge] opening binhost http server at {conf.ip()}:8322 ...")
    http_server = subprocess.Popen([
        "ssh", "-t", conf.server_host, f"cd {conf.server_path} && python3 -m http.server 8322 --directory var-cache-binpkgs",
    ], stdout=subprocess.DEVNULL)

    s = 4
    print(f"[BINHOSTESS::emerge] waiting {s} seconds for binhost http server to start ...")
    time.sleep(s)

    print(f"[BINHOSTESS::emerge] performing 'emerge {args.args}' !")
    run(["sudo", "emerge", "--getbinpkg", *args.args.split()], check=False)

    print("[BINHOSTESS::emerge] closing binhost http server ...")
    http_server.terminate()
    http_server.wait()

# executes a shell command inside of the docker container
def exec(args):
    conf = Conf.load()
    host = conf.server_host
    path = conf.server_path
    run(["ssh", "-t", host, f"cd {path} && docker compose exec gentoo {args.cmd}"])

# --- entrypoint ---

def main():
    parser = argparse.ArgumentParser(prog="binhostess")

    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("get",  help="print the current config")
    sub.add_parser("set",  help="configure binhostess")
    sub.add_parser("sync", help="synchronize the server with client")
    sub.add_parser("init", help="(re)installs gentoo docker image on server")

    emerge_parser = sub.add_parser("emerge", help="emerge on server and copy to client!")
    emerge_parser.add_argument("args", help="the arguments to give to both emerges")

    exec_parser = sub.add_parser("exec", help="[debug] execute a shell command inside docker image")
    exec_parser.add_argument("cmd", help="command to run inside docker container (wrapped in quotes)")

    args = parser.parse_args()

    if args.command == "get":
        get()
    elif args.command == "set":
        set(args)
    elif args.command == "sync":
        sync(args)
    elif args.command == "init":
        init(args)
    elif args.command == "emerge":
        emerge(args)
    elif args.command == "exec":
        exec(args)

if __name__ == "__main__":
    main()
