# CCNA Lab Portfolio

Hands-on networking labs, documented the way I'd walk a recruiter through them:
what I built, what broke, and how I fixed it.

**Stack:** Cisco Packet Tracer · IOS CLI · Python (network automation)

## Labs

| # | Lab | Focus | Status |
|---|-----|-------|--------|
| 01 | [Router-on-a-Stick: Inter-VLAN Routing](labs/01-router-on-a-stick-inter-vlan-routing/) | 802.1Q subinterfaces, inter-VLAN connectivity | Complete |
| 02 | [STP Root Bridge Election and Loop Prevention](labs/02-stp-root-bridge-and-loop-prevention/) | PVST, root elections, port roles, link-failure testing | Complete |

## Lab write-up format

Every lab follows the same template
([template](labs/_template/lab-writeup-template.md)):

1. **Objective** — what the lab proves
2. **Topology** — devices, addressing, how it's wired
3. **Configuration** — the actual commands I ran
4. **What broke** — the fault, in my own words
5. **What fixed it** — the troubleshooting steps, in order
6. **Verification** — the proof it works (pings, show commands)
7. **Takeaway** — the one thing I'll remember under exam pressure

## Python automation

The [python-automation](python-automation/) folder holds small scripts that
automate the boring parts of lab work — starting points for real NetDevOps
habits, not copy-pasted examples.
