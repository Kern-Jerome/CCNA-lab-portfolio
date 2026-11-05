# Lab 03 — Block one ping test while leaving other traffic available

**In one sentence:** I created a targeted router rule that stopped one Sales computer from pinging one HR computer, without blocking the other tested connections.

## Topology at a glance

```mermaid
flowchart LR
  pc2["Sales PC2<br/>192.168.10.2<br/>Tested blocked source"]
  pc4["Sales PC4<br/>192.168.10.3<br/>Tested permitted source"]
  pc3["HR PC3<br/>192.168.20.2<br/>Target"]
  s1["S1 switch"]
  s2["S2 switch"]
  r1["R1 router<br/>ACL 180 inbound on VLAN 10<br/>Routes between VLANs"]
  pc2 ---|"VLAN 10"| s1
  pc4 ---|"VLAN 10"| s2
  pc3 ---|"VLAN 20"| s2
  s2 ---|"802.1Q trunk"| s1
  s1 ---|"802.1Q trunk"| r1
```

**How to read it:** The diagram shows where the rule was **applied during testing**. Its interface assignment was removed at the end. This lab tested ICMP (ping), not a complete security policy.

## What I changed

- Created an access control list (ACL): a rule that filters network traffic.
- Applied the rule to incoming Sales traffic on the router.
- Tested blocked traffic, allowed traffic, and the result after removing the rule.

## What I verified

- Blocked Sales PC → HR PC ping: **0 out of 4 replies**.
- Second Sales PC → HR PC ping: **4 out of 4 replies**. The blocked Sales PC could still ping the HR gateway.
- After removing the ACL from the interface, the originally blocked ping succeeded **4 out of 4 times**.

## What went wrong — and how I handled it

During removal, I accidentally created an ACL reference named `no`. I identified it in router output, removed the incorrect assignment, and verified that the intended traffic worked again.

## Why it matters

A narrowly targeted rule can stop one kind of traffic without cutting off every device or service.

## Open the files

- [Technical write-up: configuration, commands, and evidence](./README.md)
- [Open the Packet Tracer project](./Lab%2003%20Extended%20ACLs.pkt)

**Note:** This is a simulated learning project, not a production deployment.
