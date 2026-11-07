# CCNA Networking Lab Portfolio

**Hands-on Cisco Packet Tracer projects** | Studying for the CCNA (target: December 2026)

I build small networks, configure Cisco devices, test whether they work, and document what I learned. Each project includes an easy-to-follow diagram, real test results, and the saved Packet Tracer file.

**Start here:** Choose a lab below. Open **Diagram & simple explanation** to understand the setup without needing to know Cisco commands. Open **Technical details** for configurations, troubleshooting, and evidence.

## The six labs

| Lab | The problem I solved | Explore |
| --- | --- | --- |
| **01 — Connect two departments** · Router-on-a-Stick, Inter-VLAN Routing | Keep Sales and HR on separate networks while allowing communication through a router. | [Diagram & simple explanation](labs/01-router-on-a-stick-inter-vlan-routing/SUMMARY.md) · [Technical details](labs/01-router-on-a-stick-inter-vlan-routing/README.md) |
| **02 — Prevent network loops** · Spanning Tree (STP) | Add backup connections between switches without letting traffic circulate endlessly. | [Diagram & simple explanation](labs/02-stp-root-bridge-and-loop-prevention/SUMMARY.md) · [Technical details](labs/02-stp-root-bridge-and-loop-prevention/README.md) |
| **03 — Control network access** · Extended ACLs | Block one specific computer's ping traffic while allowing the other tested traffic. | [Diagram & simple explanation](labs/03-extended-acls/SUMMARY.md) · [Technical details](labs/03-extended-acls/README.md) |
| **04 — Keep a switch connection available** · EtherChannel (LACP) | Combine two cables into one logical connection and verify it stays up when one member is disabled. | [Diagram & simple explanation](labs/04-etherchannel/SUMMARY.md) · [Technical details](labs/04-etherchannel/README.md) |
| **05 — Route traffic between networks** · Static Routing & OSPF | Configure IPv4 and IPv6 routing, then troubleshoot why a router wasn't learning a route automatically. | [Diagram & simple explanation](labs/05-static-routing-and-ospf/SUMMARY.md) · [Technical details](labs/05-static-routing-and-ospf/README.md) |
| **06 — Give addresses across networks and share an outside address** · DHCP Relay & NAT/PAT | Let PCs obtain IPv4 addresses from a remote DHCP server, then verify two clients sharing a router outside IPv4 address. | [Diagram & simple explanation](labs/06-dhcp-relay-and-nat-pat/SUMMARY.md) · [Technical details](labs/06-dhcp-relay-and-nat-pat/README.md) |

## How to read each project

- **Diagram:** What is connected to what. Labels show the networks and important links.
- **Problem and solution:** What I was trying to make the network do, in everyday language.
- **Proof:** Actual ping results or device status from the test—not just a claim that it worked.
- **Troubleshooting:** What failed, how I investigated, and what changed.
- **Technical details and project file:** Cisco configuration and the editable `.pkt` simulation.

### A few useful terms

- **Router:** Connects different networks.
- **Switch:** Connects devices within a local network.
- **VLAN:** A way to make separate logical networks on switches.
- **Ping:** A quick test of whether one device can reach another.

**Tools used:** Cisco Packet Tracer · Cisco IOS command line

These are **self-directed training projects**, not production or employer networks. I describe only tests I performed. Some labs verify device status and failover behavior rather than end-to-end traffic or performance measurements.

## Also in this repository

- [Python automation exercises](python-automation/) — small scripts for networking practice.
- [Reusable lab documentation template](labs/_template/lab-writeup-template.md) — the format for future projects.
