# Lab 01 — Router-on-a-Stick: Inter-VLAN Routing

**Date:** 2026-10-18 · **Completed and verified:** 2026-10-19
**Status:** ✅ Complete and verified
**Tool:** Cisco Packet Tracer
**Topics:** 802.1Q trunking, router subinterfaces, inter-VLAN routing

## 1. Objective

Route traffic between VLANs through a single router interface using 802.1Q
subinterfaces, and prove end-to-end connectivity between hosts in different
VLANs.

## 2. Topology

Physical topology confirmed via CDP.

```
                    802.1Q trunk
  [R1 G0/0/0] <------------------> [S1 Gi0/1]
                                        |
                                 Fa0/1 | trunk (802.1Q)
                                        |
                                   [S2 Fa0/1]
```

| Device | Port | VLAN | IP address / gateway |
|--------|------|------|----------------------|
| R1 | G0/0/0.10 | 10 (SALES) | 192.168.10.1/24 |
| R1 | G0/0/0.20 | 20 (HR) | 192.168.20.1/24 |
| R1 | G0/0/0 (parent) | trunk | unnumbered |
| SALES PC 1 | S1 Fa0/2 | 10 | 192.168.10.2/24, gw 192.168.10.1 |
| SALES PC 2 | S2 Fa0/3 | 10 | 192.168.10.3/24, gw 192.168.10.1 |
| HR PC | S2 Fa0/2 | 20 | 192.168.20.2/24, gw 192.168.20.1 |
| S1 ↔ S2 | Fa0/1 ↔ Fa0/1 | trunk, 802.1Q, VLANs 1/10/20 | — |
| R1 ↔ S1 | G0/0/0 ↔ Gi0/1 | trunk, 802.1Q | — |

## 3. Configuration

### R1 — running-config captured 2026-10-19

IOS 16.6.4 · hostname R1 · running-config 834 bytes.

```
hostname R1
!
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
!
interface GigabitEthernet0/0/1
 shutdown
!
interface GigabitEthernet0/0/2
 shutdown
!
interface Vlan1
 shutdown
```

### S1 — running-config captured 2026-10-19

IOS 15.0 · hostname S1 · running-config 1173 bytes · PVST spanning-tree mode.

```
hostname S1
!
spanning-tree mode pvst
!
interface FastEthernet0/1
 switchport mode trunk
!
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 10
!
interface GigabitEthernet0/1
 switchport mode trunk
!
interface Vlan1
 no ip address
 shutdown
```

### S2 — running-config captured 2026-10-19

IOS 15.0 · hostname S2 · PVST spanning-tree mode.

```
hostname S2
!
spanning-tree mode pvst
!
interface FastEthernet0/1
 switchport mode trunk
!
interface FastEthernet0/2
 switchport mode access
 switchport access vlan 20
!
interface FastEthernet0/3
 switchport mode access
 switchport access vlan 10
```

## 4. What broke

No troubleshooting cycle was documented for this lab — the configuration was
built and verified cleanly end-to-end.

## 5. What fixed it

Nothing to fix. The verification evidence below is the proof.

## 6. Verification

**Connectivity tests (all 4/4 replies, 0% loss):**

| Test | Result |
|------|--------|
| SALES PC 1 → 192.168.10.1 (gateway) | 4/4 ✅ |
| HR PC → 192.168.20.1 (gateway) | 4/4 ✅ |
| HR PC → SALES PC 1 (192.168.10.2) | 4/4 ✅ |
| SALES PC 1 → HR PC (192.168.20.2) | 4/4 ✅ |
| SALES PC 2 → 192.168.10.1 (gateway) | 4/4 ✅ |
| SALES PC 2 → HR PC (192.168.20.2) | 4/4 ✅ |

**Supporting evidence:**
- R1 routing table confirms connected routes for 192.168.10.0/24 and
  192.168.20.0/24.
- `show ip interface brief` on R1: parent G0/0/0 and both subinterfaces up/up;
  G0/0/1, G0/0/2, and Vlan1 administratively down.
- `show vlan brief` on S1/S2: VLAN 10 (SALES) and VLAN 20 (HR) active.
- `show interfaces trunk`: S1 Fa0/1, S1 Gi0/1, and S2 Fa0/1 all operational
  802.1Q trunks, native VLAN 1, allowing VLANs 1–1005, with VLANs 1/10/20 in
  spanning-tree forwarding state.
- `show interfaces status`: S1 Fa0/2 (access VLAN 10) and S2 Fa0/2 (VLAN 20) /
  Fa0/3 (VLAN 10) connected, full duplex, 100 Mbps.
- CDP confirmed the physical topology in §2.

## 7. Takeaway

- VLANs separate Layer 2 broadcast domains.
- Router subinterfaces use 802.1Q encapsulation to route between VLANs over
  one physical router link.
- Trunk links must carry the required VLANs end-to-end.
- Successful gateway pings verify local VLAN-to-router connectivity;
  cross-VLAN host pings provide end-to-end evidence of inter-VLAN routing.

## 8. Evidence captured

- [x] Full `show running-config` from R1, S1, S2
- [x] `show ip interface brief` on R1
- [x] `show vlan brief` / `show interfaces trunk` / `show interfaces status` on S1 and S2
- [x] CDP neighbor verification of the physical topology
- [x] Gateway ping tests from every host
- [x] Cross-VLAN host ping tests (both directions)
- [x] R1 connected routes for both VLAN subnets
