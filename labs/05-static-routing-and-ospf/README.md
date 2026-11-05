# Lab 05 — IPv4/IPv6 Static Routing and OSPFv2 Troubleshooting

**Completed:** November 4, 2026  
**Platform:** Cisco Packet Tracer (Cisco IOS)  
**Project file:** [Lab 05 Static Routing and OSPF.pkt](./Lab%2005%20Static%20Routing%20and%20OSPF.pkt)  
**Plain-language summary:** [SUMMARY.md](./SUMMARY.md)

## Objective

Build a two-router network from scratch, verify IPv4 and IPv6 static routing between separate LANs, then enable single-area OSPFv2 and demonstrate that both routers learn the remote IPv4 LAN dynamically. Troubleshoot routing failures using interface status, routing tables, neighbor state, and the OSPF link-state database (LSDB).

This is a self-directed CCNA study lab, not a production deployment.

## Topology and addressing

```text
PC1 ── R1 Gi0/0/1 ── R1 Gi0/0/0 ══ R2 Gi0/0/0 ── R2 Gi0/0/1 ── PC2
       LAN 10               WAN 10.0.12.0/30               LAN 20
```

| Device | Interface | IPv4 | IPv6 |
| --- | --- | --- | --- |
| R1 | Gi0/0/0 (WAN) | `10.0.12.1/30` | `2001:DB8:12::1/64` |
| R1 | Gi0/0/1 (LAN) | `192.168.10.1/24` | `2001:DB8:10::1/64` |
| R2 | Gi0/0/0 (WAN) | `10.0.12.2/30` | `2001:DB8:12::2/64` |
| R2 | Gi0/0/1 (LAN) | `192.168.20.1/24` | `2001:DB8:20::1/64` |
| PC1 | Ethernet | `192.168.10.10/24` | `2001:DB8:10::10/64` |
| PC2 | Ethernet | `192.168.20.10/24` | `2001:DB8:20::10/64` |

PC1's tested default gateways: IPv4 `192.168.10.1`; IPv6 `2001:DB8:10::1`. PC2 uses the R2 LAN as its local network. IPv6 example addresses use the documentation prefix `2001:DB8::/32`, suitable for a simulated lab.

## Stage 1 — IPv4 interface addressing

Configured the two routers' WAN and LAN interfaces and gave the PCs separate `/24` LAN addresses. Verified R1's WAN/LAN interfaces were **up/up** and that R1 could ping R2 on `10.0.12.2`. An initial WAN ping returned 4/5 responses, then a subsequent test returned 5/5; initial address resolution was a likely factor but not independently proved.

## Stage 2 — IPv4 static routing

Installed reciprocal routes to the remote LANs. The effective route commands were:

```cisco
! On R1: reach PC2's LAN through R2's WAN address
ip route 192.168.20.0 255.255.255.0 10.0.12.2

! On R2: reach PC1's LAN through R1's WAN address
ip route 192.168.10.0 255.255.255.0 10.0.12.1
```

Verified on R1: `S 192.168.20.0/24 [1/0] via 10.0.12.2`.  
Verified on R2: `S 192.168.10.0/24 [1/0] via 10.0.12.1`.

**Result:** PC1 pinged PC2's IPv4 address `192.168.20.10`, **4/4 replies**.

**Initial error:** A first attempt used host address `192.168.20.10` with a `/24` mask and the wrong next hop. IOS returned `%Inconsistent address and mask`. Correcting the destination to the network prefix and using the reachable WAN next hop fixed the configuration.

## Stage 3 — IPv6 static routing

Enabled IPv6 forwarding with `ipv6 unicast-routing`, configured IPv6 addresses on router interfaces and PCs, and installed the routes below. These are the effective routing statements confirmed by `show ipv6 route`:

```cisco
! R1
ipv6 route 2001:DB8:20::/64 2001:DB8:12::2

! R2
ipv6 route 2001:DB8:10::/64 2001:DB8:12::1
```

R1 reported:

```text
S 2001:DB8:20::/64 [1/0]
  via 2001:DB8:12::2
```

R2 reported:

```text
S 2001:DB8:10::/64 [1/0]
  via 2001:DB8:12::1
```

**What broke:** R2 initially lacked a return static route, and PC1 had the wrong IPv6 gateway, `2001:DB8:12::1` (R1's WAN interface, not on PC1's LAN). The first end-to-end IPv6 test failed **0/4**. PC1 could ping its local router's LAN address `2001:DB8:10::1` **4/4**, isolating the local address and gateway configuration.

**Fix:** Added R2's route back to `2001:DB8:10::/64`, then corrected PC1's IPv6 default gateway to `2001:DB8:10::1`.

**Final result:**

```text
PC1> ping 2001:DB8:20::10
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
```

## Stage 4 — Single-area OSPFv2

Enabled OSPF process 1, area 0, on the WAN; added each router's LAN to OSPF; and made the LAN interfaces passive so they could be advertised without sending Hellos to PCs. The final R1 OSPF process configuration was confirmed with `show running-config`:

```cisco
router ospf 1
 router-id 192.168.10.1
 log-adjacency-changes
 passive-interface GigabitEthernet0/0/1
 network 10.0.12.0 0.0.0.3 area 0
 network 192.168.10.0 0.0.0.255 area 0
```

On R2, `show ip ospf interface` confirmed Gi0/0/0 in **area 0** with one adjacent neighbor and Gi0/0/1 in **area 0** with `No Hellos (Passive interface)`. R2's router ID was `192.168.20.1`.

### OSPF adjacency

R1 reported:

```text
Neighbor ID     Pri   State     Dead Time   Address       Interface
192.168.20.1      1   FULL/DR   00:00:31    10.0.12.2     GigabitEthernet0/0/0
```

`FULL/DR` means the adjacency is fully formed and R2 was acting as Designated Router at that point. Earlier, R1 had been DR and R2 BDR; both were valid roles during the lab.

### Administrative distance versus OSPF

While the IPv4 static routes remained installed, R1 selected `S 192.168.20.0/24 [1/0]` rather than an OSPF route to the same prefix. Default administrative distances are **1 for static** and **110 for OSPF**. After removing the IPv4 static routes, the goal was to install OSPF-learned LAN routes on both routers.

### Difficult failure: FULL neighbor but no OSPF LAN route

After removing R1's static route, its table had no route to `192.168.20.0/24`, despite a FULL OSPF adjacency.

Diagnosis used:

```cisco
show ip ospf neighbor
show ip ospf interface
show ip protocols
show running-config
show ip ospf database
show ip ospf database router
show ip ospf database network
show ip ospf
show ip route
```

Observed evidence:

1. R1 and R2 exchanged OSPF information; R2's Router LSA included `192.168.20.0/24`.
2. A leftover `area 0 virtual-link 10.0.12.2` statement was inappropriate for this single-area design. Attempts to remove it directly did not persist in the simulated running configuration. R1's OSPF process was rebuilt with the intended configuration.
3. After rebuilding, R1 had one area with two interfaces and a FULL adjacency, but its Router LSA still initially advertised only the LAN stub network, omitted the WAN transit network, and carried an unexpected ABR flag.
4. R2's Network LSA correctly listed both routers as attached to `10.0.12.0/30`, and both databases agreed on the incomplete version of R1's Router LSA.
5. Resetting the OSPF process with `clear ip ospf process` restored FULL adjacency but **did not** initially resolve the missing route.
6. Finally, administratively shutting down and re-enabling R1's WAN interface triggered updated Router LSAs. R1's Router LSA then included both its LAN stub network and the WAN transit network, and the OSPF route installed correctly.

The exact original cause of the incomplete LSA was not proved; stale simulator/protocol state was a possibility. The observed solution was the controlled WAN-interface reinitialization, not repeated guessing.

### Final dynamic-route and connectivity verification

**R1 (learned R2's LAN):**

```text
O 192.168.20.0/24 [110/2] via 10.0.12.2, GigabitEthernet0/0/0
```

**R2 (learned R1's LAN):**

```text
O 192.168.10.0/24 [110/2] via 10.0.12.1, GigabitEthernet0/0/0
```

**PC1 to PC2, IPv4, after both original IPv4 static routes were removed:**

```text
PC1> ping 192.168.20.10
Packets: Sent = 4, Received = 4, Lost = 0 (0% loss)
Round-trip: minimum 0 ms, maximum 9 ms, average 3 ms
```

This validates end-to-end IPv4 connectivity using OSPF-learned routes. The IPv6 static routes remained configured separately; the IPv6 connectivity test was completed earlier in the lab.

## CCNA skills demonstrated

- IPv4 and IPv6 subnet/interface addressing and gateway selection
- Configuring, verifying, and troubleshooting reciprocal static routes
- Enabling IPv6 forwarding and interpreting IPv6 route-table codes
- Establishing an OSPFv2 area 0 neighbor adjacency
- Using passive interfaces while advertising LAN networks
- Interpreting `FULL/DR`, DR/BDR roles, OSPF AD 110 and path cost
- Distinguishing the OSPF LSDB from routes actually installed in the RIB
- Reading Router LSAs and Network LSAs to troubleshoot inconsistent topology
- Verifying routing outcomes with actual PC-to-PC ping results

## Project-file and evidence status

This write-up is based on IOS and PC command outputs recorded during the study session. The Packet Tracer project file supplied after the session is included in this directory. A separate reopen-and-reverify test of that uploaded project file is not claimed.
