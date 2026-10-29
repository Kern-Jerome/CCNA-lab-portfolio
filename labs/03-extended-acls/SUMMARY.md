# Lab 03 in Plain Language — One Computer Blocked, Everyone Else Through

**The task.** In Lab 01, the Sales and HR networks could reach each other
freely. Real networks need finer control than that: sometimes one specific
computer must be kept away from one specific machine, while everyone else's
work continues untouched. I added that kind of rule — a filter on the router
called an access control list — and proved it blocked exactly the one
conversation it was aimed at, and nothing more.

**The setup.** The same router and department networks as Lab 01: Sales
(192.168.10.0) and HR (192.168.20.0) connected through one Cisco router in
Packet Tracer, with two Sales computers and one HR computer in the test.

**What I did.**

1. **Wrote the rule.** One Sales computer (192.168.10.2) is denied from
   pinging the HR computer (192.168.20.2). Every other kind of traffic, from
   every other computer, is explicitly allowed through.
2. **Placed it where it works best.** The filter sits on the router port
   where Sales traffic arrives — as close to the source as possible, so
   blocked traffic is dropped before it crosses the network.
3. **Tested both directions of the claim.** The blocked computer's pings
   failed completely (0 of 4 replies, with the router reporting the
   destination unreachable), while the same computer could still reach other
   addresses, and the second Sales computer could still reach the HR
   computer. The router's own match counters agreed: the deny rule counted
   exactly the blocked attempts, and the allow rule counted the traffic that
   passed.
4. **Reversed it cleanly.** I removed the rule from the router port without
   deleting the rule itself, then verified the block was gone and the
   original traffic flowed again — the standard way to undo a network change
   without destroying the policy you might need later.

**What broke.** One real mistake, mine: while removing the rule, I typed the
removal command in a way that created a stray filter reference literally
named "no." I spotted it in the router's verification output, removed it
properly, and confirmed the final state was clean. It's documented in the
full write-up because it's the kind of slip that matters on real equipment —
and because catching it is the skill.

**What it proves.**

- I can filter traffic with surgical precision — one computer, one type of
  traffic — instead of blunt all-or-nothing blocking.
- I verify a security rule from both sides: proof the forbidden traffic
  stops *and* proof the allowed traffic still flows.
- I make changes I can undo: apply, test, roll back, and confirm the
  rollback, leaving the network exactly as documented.

**A sample of the configuration** (the full write-up is in this folder's
README.md):

```
ip access-list extended 180
 10 deny icmp host 192.168.10.2 host 192.168.20.2
 20 permit ip any any
```

Line 10 is the block: ping traffic from the one Sales computer to the one HR
computer is denied. Line 20 is just as important — everything else is
explicitly permitted, so the rule changes only what it means to change.
