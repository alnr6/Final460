# The Torchbearer

**Student Name:** Alan Vo
**Student ID:** _______132574829_____________
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  Dijkstra from S yields the minimum cost to reach every dungeon node, but it cannot decide *which relic to visit first* — the choice of relic ordering is a decision it never makes.

- **What decision remains after all inter-location costs are known:**
  Even with a complete table of cheapest costs between every pair of relevant locations, we must still determine the **order** in which to visit the relics, since different orderings produce different total fuel costs.

- **Why this requires a search over orders (one sentence):**
  No local greedy rule reliably identifies the globally cheapest sequence, so the engine must search the space of all possible relic orderings to guarantee an optimal result.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| Entrance node (`spawn`) | The Torchbearer starts here, so we need cheapest costs *from* spawn to every relic and exit. |
| Each relic chamber (`relics`) | After collecting a relic the Torchbearer travels onward, so we need cheapest costs *from* each relic to every other relic and to the exit. |

The exit node (`exit_node`) is **not** a source: the Torchbearer only ever travels *to* the exit, never *from* it to another required location.

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | Nested Dictionary (`dict[node, float]]`) |
|  What the keys represent | Source node (outer key); destination node (inner key) |
| What the values represent | Minimum fuel cost from the source node to the destination node (`float('inf')` if unreachable) |
| Lookup time complexity | O(1) average |
| Why O(1) lookup is possible | Python dictionaries are hash maps; both outer and inner lookups hash the node key in constant expected time. |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** `k + 1` - one from `spawn`, one from each of the `k` relic nodes.
- **Cost per run:** `O(m log n)` - standard Dijkstra with a binary min-heap over `n` nodes and `m` edges.
- **Total complexity:** `O((k + 1) · m log n)`
- **Justification (one line):** each of the `k + 1` sources nodes requires one independent Dijkstra traversal of the full graph, and the results are storted directly in the nested dictionary for O(1) retrieval.

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
    Every node `u` extracted from the priority queue has `dist[u]` equal to the true minimum-cost path from the source; this value is locked and will not change.

- **For nodes not yet finalized (not in S):**
  `dist[v]` holds the cost of the *cheapest path found so far* from the source to `v`; that path's internal nodes all belong to `S`, but a cheaper route through future finalized nodes may still exist.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  `dist[source] = 0` (correct: the trivial path costs zero) and `dist[v] = ∞` for all other nodes (correct: no paths have been discovered yet); `S` is empty so the finalized-node clause holds vacuously.

- **Maintenance : why finalizing the min-dist node is always correct:**
  The node `u` with the smallest `dist[u]` among non-S nodes is selected. Because all edge weights are **nonnegative**, any alternative path to `u` that passes through a node outside `S` must cost at least as much as `dist[u]` (it would first have to reach some non-S node, paying at least `dist[u]`). Therefore `dist[u]` is already optimal, and adding `u` to `S` preserves the invariant. Relaxing `u`'s outgoing edges then updates non-S estimates with newly discovered paths whose interiors now lie in `S`.

- **Termination : what the invariant guarantees when the algorithm ends:**
  When the heap is empty every reachable node is in `S` with its confirmed shortest-path distance; unreachable nodes retain `dist = ∞`.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

If any precomputed inter-location distance is incorrect, the planner's cost estimates for candidate relic orderings will be wrong potentially causing it to discard the true optimal route or select a more expensive one.

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** Greedily picking the nearest uncollected relic at each step minimizes the *immediate* travel cost but ignores how that choice affects the cost of all remaining legs.
- **Counter-example setup:** Using the spec illustration - S-B costs 1, S-C costs 2, S-D costs 2; from B, D costs 1 and T costs 1; from D, C costs 1 and T costs 100; from C, T costs 1.
- **What greedy picks:** reedy chooses B first (cheapest from S at cost 1), then D (cheapest from B at cost 1), then C (cheapest from D at cost 1), then T (from C at cost 1) - total = **4**, which happens to be optimal in this example.
- **What optimal picks:** The same route S,B,D,C,T at total cost 4 is optimal; a different ordering such as S,B,D,C,T costs 5, showing ordering matters.
- **Why greedy loses:** In general, choosing the nearest relic next can strand the Torchbearer far from the exit or force it across an expensive edge later; greedy has no mechanism to detect this until it's too late to recover.

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- The algorithm must explore every possible **order** in which the `k` relics can be visited — and use pruning to eliminate orderings that cannot yield a better total cost than the best complete route found so far.

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | `current_loc` | `node` | The dungeon chamber the Torchbearer is currently standing in |
| Relics already collected | `relics_visited_order` | `relics_remaining` | `list[node]` / `set[node]` |
| Fuel cost so far | `cost_so_far` | `float` | Total torch fuel burned from spawn to `current_loc` following the chosen relic order|

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
