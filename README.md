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

| # | Lab | What it proves | Topology diagram | Status |
|---|-----|----------------|------------------|--------|
| 01 | [Router-on-a-Stick: Inter-VLAN Routing](labs/01-router-on-a-stick-inter-vlan-routing/) | Two separate department networks, one router connection, full two-way communication | [View diagram](labs/01-router-on-a-stick-inter-vlan-routing/SUMMARY.md#topology-at-a-glance) | ✅ Complete |
| 02 | [STP Root Bridge Election and Loop Prevention](labs/02-stp-root-bridge-and-loop-prevention/) | Redundant switch links kept loop-free; the backup path moves on command and survives a link failure test | [View diagram](labs/02-stp-root-bridge-and-loop-prevention/SUMMARY.md#topology-at-a-glance) | ✅ Complete |
| 03 | [Extended ACLs: Selective Inter-VLAN Filtering](labs/03-extended-acls/) | A firewall-style rule on the router that blocks one specific computer from reaching another — and nothing else | [View diagram](labs/03-extended-acls/SUMMARY.md#topology-at-a-glance) | ✅ Complete |
| 04 | [EtherChannel (LACP): Link Aggregation and STP Failover](labs/04-etherchannel/) | Two switch cables operate as one logical trunk; one cable fails without dropping the Port-channel, and STP reroutes around a separate failure | [View diagram](labs/04-etherchannel/SUMMARY.md#topology-at-a-glance) | ✅ Complete |
| 05 | [IPv4/IPv6 Static Routing and OSPFv2 Troubleshooting](labs/05-static-routing-and-ospf/) | Dual-stack static routes, OSPF adjacency and LAN advertisements, diagnosing a missing OSPF route using LSAs, and verified PC-to-PC pings | [View diagram](labs/05-static-routing-and-ospf/SUMMARY.md#topology-at-a-glance) | ✅ Complete |

Each lab folder includes its Packet Tracer project file so reviewers can open the actual network in Cisco Packet Tracer.

Each lab has a **recruiter-friendly visual topology** and a short interview explanation at the top of both its **SUMMARY.md** and technical **README.md**. Start with a diagram to see the devices, links, and purpose; open the `.pkt` file for the actual simulated network.

## How every lab is documented

1. **Objective** — what the lab proves
2. **Visual topology + 20-second recruiter explanation** — a GitHub-rendered Mermaid diagram, device/link labels, and a plain-language interview pitch
3. **Configuration** — the actual commands I ran (passwords removed)
4. **What broke** — the fault, in my own words
5. **What fixed it** — the troubleshooting steps, in order
6. **Verification** — the proof it works (pings, status reports)
7. **Takeaway** — the one thing I'll remember under exam pressure

Template (use for every future lab): [lab-writeup-template.md](labs/_template/lab-writeup-template.md). New labs must include a visual diagram in both the README and SUMMARY, based on the verified project topology.

## Python automation

The [python-automation](python-automation/) folder holds small scripts that
automate the repetitive parts of lab work — starting points for real network
automation habits, not copy-pasted examples. It currently includes a subnet
calculator I built to drill the address math the CCNA demands.
