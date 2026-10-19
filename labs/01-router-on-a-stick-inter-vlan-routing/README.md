# Lab 01 — Router-on-a-Stick: Inter-VLAN Routing

**Date:** 2026-10-18
**Status:** 🟡 Partially documented — final evidence capture pending (see §8)
**Tool:** Cisco Packet Tracer
**Topics:** 802.1Q trunking, router subinterfaces, inter-VLAN routing

## 1. Objective

Route traffic between VLANs through a single router interface using 802.1Q
subinterfaces, and prove end-to-end connectivity between hosts in different
VLANs.

## 2. Topology

```
                        802.1Q trunk (VLANs 10, 20)
                  S1 Fa0/1 <------------------> S1 Fa0/1... (S2 Fa0/1)
                     |                                |
  R1 G0/0/0 <---+    | Fa0/2: PC2 (VLAN 10)            | Fa0/2: PC3 (VLAN 20)
  (trunk, port   |    |        192.168.10.2            |        (IP TBD)
   TBD on S1) ---+    + VLAN 10 PC: 192.168.10.3 (S2, port TBD)
   .10: 192.168.10.1/24
   .20: 192.168.20.1/24
```

| Device | Interface / Port | VLAN | IP address |
|--------|------------------|------|------------|
| R1 | G0/0/0.10 | 10 | 192.168.10.1/24 |
| R1 | G0/0/0.20 | 20 | 192.168.20.1/24 |
| R1 | G0/0/0 (parent) | trunk | no IP (see §4) |
| PC2 | S1 Fa0/2 | 10 | 192.168.10.2/24 |
| PC (VLAN 10) | S2 (port TBD) | 10 | 192.168.10.3/24 |
| PC3 | S2 Fa0/2 | 20 | not yet recorded |
| S1 ↔ S2 | Fa0/1 ↔ Fa0/1 | trunk, 802.1Q, VLANs 10+20 | — |

## 3. Configuration

Recovered excerpts (post-fix state). Full running-configs still pending — see §8.

### R1

```
interface GigabitEthernet0/0/0
 no ip address
!
interface GigabitEthernet0/0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
!
interface GigabitEthernet0/0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
```

### S1 / S2

```
! TODO: full running-configs pending capture
! Known: S1 Fa0/1 <-> S2 Fa0/1 trunk, 802.1Q, VLANs 10 and 20
! Known: S1 Fa0/2 access VLAN 10; S2 Fa0/2 access VLAN 20
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
3. Re-tested pings after the correction.

## 6. Verification

- Same-VLAN connectivity: 4/4 pings successful (recorded).
- Inter-VLAN final tests: **outstanding**.
- VLAN/trunk verification (`show vlan brief`, `show interfaces trunk`): **outstanding**.

## 7. Takeaway

On a router-on-a-stick, the physical trunk interface stays unnumbered — the
moment you IP it, you've told the router the wrong story about where each
VLAN's gateway lives.

## 8. Evidence still needed

- [ ] Full `show running-config` from R1, S1, and S2 (passwords stripped)
- [ ] `show vlan brief` and `show interfaces trunk` from both switches
- [ ] Final inter-VLAN ping tests (e.g. PC2 ↔ PC3, 192.168.10.3 ↔ VLAN 20 host)
- [ ] PC3's IP address; S2 port for the 192.168.10.3 PC; R1↔S1 trunk port ID

**This entry is not fully verified until the above is captured.**
