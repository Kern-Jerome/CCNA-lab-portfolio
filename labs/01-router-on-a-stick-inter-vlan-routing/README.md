# Lab 01 — Router-on-a-Stick: Inter-VLAN Routing

**Date:** 2026-10-18
**Tool:** Cisco Packet Tracer
**Topics:** 802.1Q trunking, router subinterfaces, inter-VLAN routing

## 1. Objective

Route traffic between VLANs through a single router interface using 802.1Q
subinterfaces, and prove end-to-end connectivity between hosts in different
VLANs.

## 2. Topology

One router connected via a trunk link to a switch; hosts spread across
multiple VLANs on the switch.

> Configs below are placeholders — paste the actual commands and addressing
> from the Packet Tracer session before marking this complete.

## 3. Configuration

```
! TODO: paste router subinterface config (encapsulation dot1Q, IP per VLAN)
! TODO: paste switch trunk + access-port config
```

## 4. What broke

The parent (physical) interface on the router had been assigned an IP address,
which broke the subinterface design — the physical interface on a
router-on-a-stick trunk should carry no IP; each subinterface owns its VLAN's
gateway address.

## 5. What fixed it

1. Removed the IP address from the parent physical interface.
2. Confirmed each subinterface had the correct `encapsulation dot1Q <vlan>`
   and gateway IP for its VLAN.
3. Re-tested inter-VLAN pings after the correction.

## 6. Verification

- 4/4 inter-VLAN pings succeeded after the fix.
- TTL behavior across routed hops confirmed and understood.

## 7. Takeaway

On a router-on-a-stick, the physical trunk interface stays unnumbered — the
moment you IP it, you've told the router the wrong story about where each
VLAN's gateway lives.
