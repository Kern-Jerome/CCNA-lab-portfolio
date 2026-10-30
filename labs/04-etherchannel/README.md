# Lab 04 — EtherChannel (LACP): Link Aggregation, Redundancy, and STP

**Completed:** October 29, 2026  
**Platform:** Cisco Packet Tracer (Cisco IOS, Cisco 2960 switches)  
**Lab file:** [Lab 04 EtherChannel.pkt](./Lab%2004%20EtherChannel.pkt)  
**Plain-language summary:** [SUMMARY.md](./SUMMARY.md)

## Objective

Build a two-link **Layer 2 EtherChannel using LACP** between switches S1 and S2. Confirm that the two physical cables operate as one logical **Port-channel 1 (Po1)**, preserve 802.1Q trunking, test loss and restoration of a member link, and observe how **Spanning Tree Protocol (STP)** handles the logical interface during a separate upstream link failure.

This is a self-directed CCNA study lab, not a production deployment.

## Topology

The project extends my [Lab 02 STP topology](../02-stp-root-bridge-and-loop-prevention/). S1, S2, and S3 form a redundant triangle. R1 and the existing PCs remain connected.

```text
                      R1
                       |
                       S1 ======= S2
                        \         /
                         \       /
                            S3

        S1—S2: two physical FastEthernet links
               bundled into one LACP Port-channel (Po1)
        S1—S3 and S2—S3: separate existing STP paths
```

| Connection | Side A | Side B | Purpose |
| --- | --- | --- | --- |
| EtherChannel member 1 | S1 Fa0/1 | S2 Fa0/1 | Existing 802.1Q trunk |
| EtherChannel member 2 | S1 Fa0/4 | S2 Fa0/6 | New 802.1Q trunk |
| S1–S3 | S1 Fa0/3 | S3 Fa0/1 | Existing redundant path |
| S2–S3 | S2 Fa0/5 | S3 Fa0/2 | Existing direct root path for VLAN 10 |
| S1–R1 | S1 Gi0/1 | R1 Gi0/0/0 | Existing router-on-a-stick connection |

The interface mapping was confirmed using `show cdp neighbors` and `show interfaces status` before recabling. The new FastEthernet interfaces were operating at **100 Mbps, full duplex**.

## Configuration

### 1. Prepare the new physical links as trunks

Both existing Fa0/1 interfaces were already 802.1Q trunks. The new interfaces initially belonged to access VLAN 1, so they were changed to trunk mode before enabling LACP.

**S1:**

```cisco
configure terminal
interface FastEthernet0/4
 switchport mode trunk
end
```

**S2:**

```cisco
configure terminal
interface FastEthernet0/6
 switchport mode trunk
end
```

`show interfaces <interface> switchport` confirmed trunk mode, **native VLAN 1**, and **all VLANs allowed** on the newly added ports, matching the existing Fa0/1 trunks.

### 2. Enable LACP active mode and assign Port-channel 1

The commands below reflect the configuration performed during the lab. The existing Fa0/1 interfaces were added after the initial one-member Port-channel was discovered during verification.

**S1:**

```cisco
configure terminal
interface FastEthernet0/4
 channel-protocol lacp
 channel-group 1 mode active
exit
interface FastEthernet0/1
 channel-protocol lacp
 channel-group 1 mode active
end
```

**S2:**

```cisco
configure terminal
interface FastEthernet0/6
 channel-protocol lacp
 channel-group 1 mode active
exit
interface FastEthernet0/1
 channel-protocol lacp
 channel-group 1 mode active
end
```

**Active + active** allows LACP negotiation on both ends. The two 100 Mbps links form a logical bundle for redundancy and load distribution; this does **not** imply a single flow can necessarily use both links' combined bandwidth.

## Verification and results

### 1. EtherChannel summary: both members bundled

**S1:**

```text
S1# show etherchannel summary
1      Po1(SU)           LACP   Fa0/4(P) Fa0/1(P)
```

**S2:**

```text
S2# show etherchannel summary
1      Po1(SU)           LACP   Fa0/6(P) Fa0/1(P)
```

- **S** = Layer 2 Port-channel.
- **U** = Port-channel in use.
- **P** = physical interface bundled into the Port-channel.

The presence of **both member interfaces with `(P)`** matters: `Po1(SU)` by itself does not prove that all intended members joined.

### 2. Trunk operation

On both switches, `show interfaces trunk` reported:

```text
Port        Mode    Encapsulation  Status    Native vlan
Po1         on      802.1q         trunking  1

Port        Vlans allowed on trunk
Po1         1-1005

Port        Vlans allowed and active in management domain
Po1         1,10,20
```

For VLAN 10, STP treated **Po1 as one logical port**, rather than assigning independent STP roles to each physical member.

### 3. VLAN 10 STP baseline

S3 was the root bridge for VLAN 10, with reported Root ID priority **4106** and MAC **0060.4772.46D3**.

| Switch | Relevant interface | Observed VLAN 10 role/state |
| --- | --- | --- |
| S1 | Fa0/3 | **Root / Forwarding** toward S3 |
| S1 | Po1 | **Designated / Forwarding** |
| S2 | Fa0/5 | **Root / Forwarding** toward S3 |
| S2 | Po1 | **Alternate / Blocking** |

On S2, `show interfaces trunk` listed Po1 as forwarding VLANs **1 and 20**, but not VLAN **10**. This is an **STP forwarding decision**, not an LACP failure: the physical EtherChannel remained bundled and operational.

### 4. Test A — one EtherChannel member fails

I administratively shut down **S1 Fa0/4** while leaving Fa0/1 and Po1 untouched.

```cisco
configure terminal
interface FastEthernet0/4
 shutdown
```

Observed during the shutdown:

```text
S1: Po1(SU)  LACP  Fa0/4(D) Fa0/1(P)
S2: Po1(SU)  LACP  Fa0/6(D) Fa0/1(P)
```

**Result:** Po1 remained up with **Fa0/1 as the surviving bundled member**. The failed interfaces showed `(D)` for down; the healthy interfaces retained `(P)`.

After `no shutdown` on S1 Fa0/4, S1 again showed:

```text
Po1(SU)  LACP  Fa0/4(P) Fa0/1(P)
```

This test confirmed **bundle survival at the interface/LACP level**. It was not a separate end-to-end traffic or throughput test.

### 5. Test B — the direct STP root path fails

Separately, I shut down **S2 Fa0/5**, its direct link toward root switch S3, and checked `show spanning-tree vlan 10`.

**During failure:**

```text
Root ID   Cost 31
          Port 27(Port-channel1)

Interface  Role  Sts  Cost
Fa0/3      Desg  FWD  19
Po1        Root  FWD  12
```

**Result:** Po1 changed from **Alternate / Blocking** to **Root / Forwarding**. S2 reached S3 through **S1**, with an observed total root path cost of **31**:

- S2's Po1 to S1: **12**
- S1's path to root S3: **19**
- Total: **12 + 19 = 31**

This is **total root path cost**; the interface's local cost alone is not the entire STP root-port selection calculation.

After restoring S2 Fa0/5, an early check showed `Fa0/5 Root LIS`: STP had selected the root port, but the port was still **Listening**. A later check confirmed full convergence:

```text
Root ID   Cost 19
          Port 5(FastEthernet0/5)

Interface  Role  Sts  Cost
Fa0/5      Root  FWD  19
Po1        Altn  BLK  12
```

**Result:** S2 returned to its lower-cost direct path to S3. The root port finished transitioning to **Forwarding**, and Po1 returned to its **Alternate / Blocking** role for VLAN 10. The observed protocol was **IEEE STP (`protocol ieee`)**; I did not measure a numerical convergence time.

## What went wrong — and how I fixed it

1. **Initially configured only one member on each switch.** The first LACP checks showed `Po1(SU)` with S1 `Fa0/4(P)` and S2 `Fa0/6(P)`, but **Fa0/1 was missing**. I configured Fa0/1 with LACP active on both switches and repeated verification until **both members displayed `(P)`**.
2. **Saw a temporary standalone member.** S1 initially displayed `Fa0/1(I)` immediately after its configuration. A subsequent check, after both ends had been configured and LACP negotiated, showed `Fa0/1(P)`.
3. **Checked STP before it fully reconverged.** After restoring S2 Fa0/5, I first observed `Root LIS` rather than `Root FWD`. I allowed the transition to complete and verified **Root / Forwarding** before accepting the restored state.
4. **Refined my STP reasoning.** The root path changed from a direct **cost 19** path to an indirect **cost 31** path during the failure. The correct comparison is total path cost to the root, not just one interface's local cost or port priority.

These are actual lab mistakes and observations, not injected production incidents.

## Configuration persistence

Both switches returned `Building configuration... [OK]` after `copy running-config startup-config`. I saved and reopened **Lab 04 EtherChannel.pkt**, and a post-reopen S1 check again displayed:

```text
Po1(SU)  LACP  Fa0/1(P) Fa0/4(P)
```

The original Packet Tracer project is included in this directory for review.

## CCNA skills demonstrated

- Identifying interfaces and physical neighbors using CDP and interface status
- Preparing compatible 802.1Q EtherChannel member trunks
- Configuring **LACP active/active** and adding interfaces to a Port-channel
- Reading `show etherchannel summary` flags `S`, `U`, `P`, `I`, and `D`
- Verifying trunk mode, native VLAN, and active/allowed VLANs
- Understanding STP's treatment of a logical Port-channel
- Differentiating physical member failure, LACP operational state, and per-VLAN STP blocking
- Testing failure, restoration, convergence, and saved configuration persistence

**Scope:** Verification was based on the actual Packet Tracer command outputs and screenshots captured during this lab. No measured throughput, convergence duration, or end-to-end packet-loss result is claimed for the failure scenarios.
