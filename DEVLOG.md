# Development Log – The Torchbearer

**Student Name:** ___Alan Vo________________________
**Student ID:** _______132574829____________________

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – [5/11]: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

I'll implement Dijkstra first since the search depends on correct distances, 
and I'll test it on the spec's illustration graph before wiring up the recursive search. 
The parts I expect to be hardest are the lower-bound pruning logic and ensuring backtracking 
correctly restores state between recursive calls.

---

## Entry 2 – [5/11]: [Pruning]

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

Fix: Only compute a lower bound when relics_remaining is non-empty.
Previously the bound was checked before the base case, causing completed
routes to be pruned. Now the base case runs first and only partial routes
are subject to pruning.

---

## Entry 3 – [Date]: [Short description]

_Your entry here._

---

## Entry 4 – [Date]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

_Your entry here._

---

## Final Entry – [Date]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | |
| Part 2: Precomputation Design | |
| Part 3: Algorithm Correctness | |
| Part 4: Search Design | |
| Part 5: State and Search Space | |
| Part 6: Pruning | |
| Part 7: Implementation | |
| README and DEVLOG writing | |
| **Total** | |
