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

Each lab folder also holds the Packet Tracer project file, so a reviewer with
Packet Tracer can open the exact network I built.

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
