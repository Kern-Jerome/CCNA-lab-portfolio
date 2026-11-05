# CCNA Lab Portfolio — Kern Jerome

Hands-on Cisco networking labs that I built, configured, and tested myself in
Cisco Packet Tracer while preparing for the **CCNA exam (December 2026)**. I'm
preparing for entry-level IT and networking roles, and this repo is my proof
of work: every lab shows the setup, the configuration I actually ran, and the
tests that prove it works.

These are self-directed study labs, not employer projects — the point is that
the skills in them are the real, day-one skills of a junior network role.

**Stack:** Cisco Packet Tracer · Cisco IOS command line · Python

## What these labs demonstrate

- **Keeping departments separate, but connected.** Splitting one network into
  isolated groups (here, Sales and HR) so traffic stays apart — then letting a
  router pass traffic between them on purpose. This is the setup behind
  everyday requests like "Sales shouldn't see HR's files, but both need the
  printer."
- **Backup connections that don't crash the network.** Linking switches with
  spare cables so one failure doesn't take the office down — and proving the
  spare path waits in reserve instead of sending traffic around in an endless
  loop.
- **Combining redundant switch links with LACP.** Bundling two physical
  cables into one logical trunk, verifying both members, and checking that
  the Port-channel stays up when one member fails.
- **Static and dynamic routing.** Configuring IPv4/IPv6 static routes, then moving IPv4 routing to OSPF and troubleshooting a FULL adjacency that initially failed to install a LAN route.
- **Verification, not assumptions.** Every lab ends with tests: connectivity
  checks from every computer, plus the switches' and router's own status
  reports, quoted in the write-ups.
- **Honest troubleshooting notes.** Each lab states plainly what went wrong —
  or says so when nothing did — instead of polishing the story.

## Labs

| # | Lab | What it proves | Status |
|---|-----|----------------|--------|
| 01 | [Router-on-a-Stick: Inter-VLAN Routing](labs/01-router-on-a-stick-inter-vlan-routing/) | Two separate department networks, one router connection, full two-way communication | ✅ Complete |
| 02 | [STP Root Bridge Election and Loop Prevention](labs/02-stp-root-bridge-and-loop-prevention/) | Redundant switch links kept loop-free; the backup path moves on command and survives a link failure test | ✅ Complete |
| 03 | [Extended ACLs: Selective Inter-VLAN Filtering](labs/03-extended-acls/) | A firewall-style rule on the router that blocks one specific computer from reaching another — and nothing else | ✅ Complete |
| 04 | [EtherChannel (LACP): Link Aggregation and STP Failover](labs/04-etherchannel/) | Two switch cables operate as one logical trunk; one cable fails without dropping the Port-channel, and STP reroutes around a separate failure | ✅ Complete |
| 05 | [IPv4/IPv6 Static Routing and OSPFv2 Troubleshooting](labs/05-static-routing-and-ospf/) | Dual-stack static routes, OSPF adjacency and LAN advertisements, diagnosing a missing OSPF route using LSAs, and verified PC-to-PC pings | ✅ Complete — project file upload pending |
| 05 | [IPv4/IPv6 Static Routing and OSPF Troubleshooting](labs/05-static-routing-and-ospf/) | Two-router dual-stack network; working static routes; OSPF neighbor/LSA troubleshooting; verified dynamic routes and end-to-end pings | ✅ Lab complete · `.pkt` upload pending |

Lab folders include the original Packet Tracer project file where available, so reviewers can open the exact network built. **Lab 05's write-ups are published, but its `.pkt` project file is still pending upload.**

New to the details? Each lab has a one-page **SUMMARY.md** in plain language.
The full technical write-up is the README.md beside it.

## How every lab is documented

1. **Objective** — what the lab proves
2. **Topology** — devices, addressing, how it's wired
3. **Configuration** — the actual commands I ran (passwords removed)
4. **What broke** — the fault, in my own words
5. **What fixed it** — the troubleshooting steps, in order
6. **Verification** — the proof it works (pings, status reports)
7. **Takeaway** — the one thing I'll remember under exam pressure

Template: [lab-writeup-template.md](labs/_template/lab-writeup-template.md)

## Python automation

The [python-automation](python-automation/) folder holds small scripts that
automate the repetitive parts of lab work — starting points for real network
automation habits, not copy-pasted examples. It currently includes a subnet
calculator I built to drill the address math the CCNA demands.
