# Lab 02 — STP Root Bridge Election and Loop Prevention

**Date completed:** October 21, 2026  
**Platform:** Cisco Packet Tracer, Cisco 2960 switches  
**Protocol observed:** Per-VLAN Spanning Tree (PVST), IEEE 802.1D STP (`spanning-tree mode pvst`; `protocol ieee`)  
**Lab file:** `Lab-02-STP-Root-Bridge-and-Loop-Prevention.pkt`

## Objective

Build a redundant three-switch Layer 2 topology; identify STP root, designated, and alternate ports; deliberately change the VLAN 10 root bridge; observe how the blocked path changes; and verify behavior during a controlled link shutdown and restoration.

## Topology

```text
                 S1
              /      \
       Fa0/1 /        \ Fa0/3
            /          \
       Fa0/1             Fa0/1
         S2 ------------- S3
        Fa0/5           Fa0/2
```

Physical link mapping (unambiguous):

| Link | Endpoint A | Endpoint B |
| --- | --- | --- |
| Existing inter-switch trunk | S1 Fa0/1 | S2 Fa0/1 |
| New inter-switch trunk | S1 Fa0/3 | S3 Fa0/1 |
| New inter-switch trunk | S2 Fa0/5 | S3 Fa0/2 |

The prior Router-on-a-Stick topology's router, end hosts, and other connections were left in place. This lab focuses on **VLAN 10 (SALES)** STP behavior. The new S3 switch had VLANs 1 and 10 active, but VLAN 20 was **not** created on S3. This experiment does **not** demonstrate VLAN 20 connectivity through S3.

## Configuration

### S3 — verified running configuration excerpts

The following commands appeared in S3's supplied `show running-config` output:

```cisco
hostname S3
spanning-tree mode pvst
spanning-tree extend system-id
spanning-tree vlan 10 priority 4096
!
interface FastEthernet0/1
 switchport mode trunk
!
interface FastEthernet0/2
 switchport mode trunk
```

S3's `show vlan brief` separately verified that VLAN **10 / SALES** existed and was **active**. It was not listed as a separate VLAN declaration in the supplied running configuration; on this switching platform, VLAN database information may be stored separately.

### S1 and S2 — verified state

`show interfaces trunk` confirmed the new links S1 Fa0/3 and S2 Fa0/5 were operational **802.1Q trunks**, native VLAN 1, permitting VLAN 10. The existing S1 Fa0/1–S2 Fa0/1 link also remained a trunk. Full running configurations for S1 and S2 were not captured for this README, so no further commands are claimed as verified.

## Verification and results

### 1. Initial VLAN 10 root bridge: S1

Before changing bridge priorities, the switches' `show spanning-tree vlan 10` outputs established:

- **S1 was the root:** `This bridge is the root`.
- The relevant displayed priority components were equal at **32778** (32768 base priority + VLAN 10 extended system ID).
- **S1 MAC:** `0003.E423.EEB7`; **S2 MAC:** `0090.2B95.C895`; **S3 MAC:** `0060.4772.46D3`.
- With equal priorities, **S1 had the lowest MAC address** and won the root election.
- **S2 Fa0/1:** Root / Forwarding, root path cost 19.
- **S3 Fa0/1:** Root / Forwarding, root path cost 19.
- **S2 Fa0/5:** Alternate / Blocking for VLAN 10. **S3 Fa0/2:** Designated / Forwarding. S2 and S3 tied on root path cost 19; S3's lower Bridge ID won the designated-port election for their segment.

### 2. Change the VLAN 10 root to S3

On S3, the following setting was confirmed in the running configuration:

```cisco
spanning-tree vlan 10 priority 4096
```

Observed `show spanning-tree vlan 10` results after convergence:

| Switch | Root ID priority / address | Root path cost | Relevant VLAN 10 port roles |
| --- | --- | ---: | --- |
| S1 | 4106 / `0060.4772.46D3` | 19 | Fa0/3 **Root FWD**; Fa0/1 **Desg FWD** |
| S2 | 4106 / `0060.4772.46D3` | 19 | Fa0/5 **Root FWD**; Fa0/1 **Altn BLK** |
| S3 | 4106 / `0060.4772.46D3` | 0 (root) | Fa0/1 **Desg FWD**; Fa0/2 **Desg FWD** |

**Why the root priority displays as 4106:** the configured priority **4096** plus the VLAN 10 extended system ID gives **4106**.

After S3 became root, S1 and S2 each used their direct FastEthernet link toward S3 with cost 19. On the S1–S2 segment, both switches advertised an equal root path cost, so S1's lower Bridge ID made **S1 Fa0/1 designated/forwarding**, leaving **S2 Fa0/1 alternate/blocked** to avoid a Layer 2 loop.

### 3. Controlled link failure and restoration

- **Test action:** Administratively shut down **S1 Fa0/1**, the direct S1–S2 trunk, in the separate practice file.
- **Observed on S2:** `show spanning-tree vlan 10` no longer displayed Fa0/1 among operational STP interfaces. S2 Fa0/5 remained **Root / Forwarding**, and S3 remained root with cost 19.
- **Interpretation:** Shutting down S1's interface took the physical S1–S2 link down. S2 Fa0/1 did **not** transition to designated/forwarding while the link was unavailable. Communication could still use the S1–S3–S2 switching path, though end-to-end host connectivity was **not retested** during this specific failure.
- **Restoration:** S1 Fa0/1 was re-enabled. The subsequent S2 STP output showed **Fa0/1 Alternate / Blocking**, **Fa0/5 Root / Forwarding**, and S3 still serving as the root bridge.
- **End state:** The original physical link was restored and the VLAN 10 spanning tree again had a blocked redundant path. A dedicated `.pkt` copy was saved after restoration.

## What broke / What fixed it

This was a **planned failure simulation**, not a diagnosed accidental configuration fault. Shutting down S1 Fa0/1 intentionally removed the direct switch-to-switch link. Re-enabling it restored the physical connection, after which STP reconverged and blocked S2 Fa0/1 as the redundant path. No unrelated fault was discovered or repaired.

## Key takeaways

1. STP elects the **lowest Bridge ID** as root: priority first, then MAC address when priorities tie.
2. Each non-root switch selects a root port by the **lowest total path cost** to the root, followed by STP tie-breakers as needed.
3. Designated ports on a segment are selected using advertised root-path information and Bridge ID tie-breakers; equal costs between S1 and S2 caused S1 to win.
4. An **alternate/blocked** STP port is not the same as a port whose **physical link is down**.
5. Changing the root bridge may change the topology's forwarding and blocked interfaces without recabling the network.
6. `show spanning-tree vlan 10` reveals the root ID, local Bridge ID, root path cost, port roles and port states; `show interfaces trunk` shows trunk and VLAN forwarding summaries.

## Scope and evidence limitations

- Verified from actual pasted **S1/S2/S3 `show spanning-tree vlan 10`**, **S1/S2/S3 `show interfaces trunk`**, **S3 `show vlan brief`**, and **S3 `show running-config`** output shared during this lab.
- No measured STP convergence-time benchmark was performed; no claim is made about failover milliseconds or packet-loss duration.
- RSTP was **not** configured or tested here; the outputs show traditional IEEE STP/PVST.
- End-to-end ping tests were not repeated during the failure experiment.
- The Packet Tracer file was saved locally; its separate upload to this repository is pending.

## Next lab

Compare STP with **Rapid PVST+ / RSTP**, including edge ports, alternate ports, and observed convergence during a controlled change.
