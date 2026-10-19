#!/usr/bin/env python3
"""Subnet calculator — CCNA speed drill.

Usage:
    python3 subnet_calc.py 192.168.10.0/24
    python3 subnet_calc.py 10.0.0.0 255.255.255.192

Prints: network, broadcast, first/last usable, usable host count,
wildcard mask, and the /prefix. Standard library only.
"""

import ipaddress
import sys


def describe(cidr: str) -> None:
    net = ipaddress.ip_network(cidr, strict=False)
    hosts = list(net.hosts())
    print(f"Network:        {net.network_address}")
    print(f"Broadcast:      {net.broadcast_address}")
    print(f"Prefix:         /{net.prefixlen}")
    print(f"Subnet mask:    {net.netmask}")
    print(f"Wildcard mask:  {net.hostmask}")
    if hosts:
        print(f"First usable:   {hosts[0]}")
        print(f"Last usable:    {hosts[-1]}")
        print(f"Usable hosts:   {len(hosts)}")
    else:
        print("No usable host addresses in this subnet.")


def main(argv: list[str]) -> int:
    if len(argv) == 2 and "/" in argv[1]:
        cidr = argv[1]
    elif len(argv) == 3:
        cidr = f"{argv[1]}/{argv[2]}"
    else:
        print(__doc__)
        return 2
    try:
        describe(cidr)
    except ValueError as exc:
        print(f"Invalid input: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
