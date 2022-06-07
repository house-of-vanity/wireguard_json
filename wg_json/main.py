import subprocess
import json
import sys
from typing import NamedTuple, TypedDict
 
cmd = ["/usr/bin/wg", "show", "all", "dump"] 
proc = subprocess.Popen(cmd,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE,
    universal_newlines=True
)
stdout, stderr = proc.communicate()

class Peer(TypedDict):
    preshared_key: str
    endpoint: str
    latest_handshake: int
    transfer_rx: int
    transfer_tx: int
    persistent_keepalive: bool
    allowed_ips: list

class Interface(TypedDict):
    name: str
    private_key: str
    public_key: str
    listen_port: int
    fwmark: str
    peers: list

class Wireguard(TypedDict):
    interfaces: dict
 
wg_state = Wireguard({})

def main():
    for v in stdout.split('\n'):
        args = v.split('\t')
        if len(args) == 5:
            interface = Interface(
                    name = args[0],
                    private_key = args[1],
                    public_key = args[2],
                    listen_port = args[3],
                    fwmark = args[4],
                    peers = [])
            wg_state[interface['name']] = interface
        elif len(args) == 9:
            allowed_ips = args[4].replace(' ', '').split(',')
            peer = Peer(
                    preshared_key= args[1],
                    endpoint = args[3],
                    latest_handshake = int(args[5]),
                    transfer_rx = int(args[6]),
                    transfer_tx = int(args[7]),
                    persistent_keepalive = args[8],
                    allowed_ips = allowed_ips)
            wg_state[args[0]]['peers'].append(peer)
        else:
            continue
    print(json.dumps(wg_state))

main()
