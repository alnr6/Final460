# CS 460 Algorithms: Final Programming Assignment
## The Torchbearer

**Semester:** Spring 2026
**Instructor:** Manju Muralidharan Priya
**Total Points:** 100

---

## The World

Deep beneath the Ashenmoor Mountains lies a dungeon that has swallowed every adventurer who
entered without a plan. Torchlit corridors branch unpredictably. Portcullises, underground
rivers, and collapsed archways mean most passages run in only one direction. You cannot assume
you can retrace your steps.

You are writing the navigation engine for the Torchbearer: a magical construct sent into the
dungeon by the Adventurers Guild. The Torchbearer starts at the dungeon entrance, must visit
a fixed set of relic chambers to retrieve cursed artifacts, and must escape through the one
safe exit before its torch burns out. Every corridor costs torch fuel to traverse.

Your engine must find the route that collects every relic for the minimum total torch fuel.
Dead Torchbearers are expensive. Wasted fuel is unacceptable.

---

## The Problem, Formally

The dungeon is modeled as a **weighted, directed graph** `G = (V, E)`.

- Each node in `V` is a dungeon location: a chamber, a junction, a trap room.
- Each directed edge `(u, v)` has a nonnegative integer weight: the torch fuel cost to
  travel from `u` to `v`. Not every passage goes both directions.
- The Torchbearer starts at a fixed **entrance** node `S`.
- A set `M = {R1, R2, ..., Rk}` of **relic chambers** must each be visited at least once.
- The Torchbearer must finish at a fixed **exit** node `T`.

The Torchbearer **may** pass through any dungeon node as an intermediate stop. The cheapest
path between two relic chambers may route through many other rooms along the way.

**Goal:** find a walk from `S`, visiting every node in `M` at least once, ending at `T`,
with minimum total torch fuel cost.

---

## Concrete Illustration

This example clarifies the structure of the problem only. It does not suggest any particular
implementation approach.

**Entrance:** S | **Relic chambers:** B, C, D | **Exit:** T

After computing cheapest inter-location travel costs, suppose you have:

| From \ To | B   | C   | D   | T   |
|-----------|-----|-----|-----|-----|
| S         | 1   | 2   | 2   | --  |
| B         | --  | 100 | 1   | 1   |
| C         | 1   | --  | 100 | 1   |
| D         | 1   | 1   | --  | 100 |

Two possible routes:

- Route 1: S -> B -> D -> C -> T &nbsp; total fuel = 1 + 1 + 1 + 1 = **4**
- Route 2: S -> C -> B -> D -> T &nbsp; total fuel = 2 + 1 + 1 + 1 = **5**

Both collect every relic. Both end at T. Their total costs differ. Knowing cheapest
point-to-point travel costs alone does not tell you which collection order is optimal.

---

## How This Assignment Works

Every written question in Parts 1 through 6 has a corresponding function in
`torchbearer.py` and a corresponding section in `README.md`. The three are
deliberately linked: your written reasoning in the README explains the design decisions
your code implements. Graders cross-reference all three.

The structure is:

| Part | README Section | Function in torchbearer.py |
|---|---|---|
| 1: Problem Analysis | Part 1: Problem Analysis | `explain_problem()` |
| 2a: Source Selection | Part 2a: Source Selection | `select_sources()` |
| 2b: Distance Storage | Part 2b: Distance Storage | `run_dijkstra()` |
| 2c: Complexity | Part 2c: Complexity | `precompute_distances()` |
| 3: Correctness | Part 3: Correctness | `dijkstra_invariant_check()` |
| 4: Search Design | Part 4: Search Design | `explain_search()` |
| 5a: State | Part 5a: State Representation | `find_optimal_route()` |
| 5b: Data Structure | Part 5b: Data Structure | `find_optimal_route()` |
| 5c: Search Space | Part 5c: Search Space | `_explore()` |
| 6a: Best-So-Far | Part 6a: Best-So-Far | `_explore()` |
| 6b: Lower Bound | Part 6b: Lower Bound | `_explore()` |
| 6c: Pruning Correctness | Part 6c: Pruning Correctness | `_explore()` |

---

## Deliverables

Create a **public GitHub repository** for this project and submit the repository URL on Canvas. All three files below must be present at the root of the repository. A missing file earns zero for its section.

| File | Contents |
|---|---|
| `torchbearer.py` | Your complete implementation |
| `README.md` | Written answers, one section per part |
| `DEVLOG.md` | Development log with at least four dated entries |

**Submission checklist before you paste the link on Canvas:**
- Repository is set to public (graders must be able to access it without signing in)
- All three files are at the root of the repo, not inside a subfolder
- The link you submit goes to the repository, not to an individual file
- Commit history reflects your actual development process and aligns with your DEVLOG entries

**On commit history:** Your Git commit history is part of your submission. Graders will check that commit timestamps and messages correspond to the dated entries in your DEVLOG. A DEVLOG that describes four sessions of work but a repository with a single commit is an academic integrity flag. Commit as you go, after completing each part, after fixing a bug, after a significant design change. Commit messages should be descriptive enough to match the work described in the corresponding DEVLOG entry.

Do not submit a zip file. Do not submit screenshots of code. Do not submit a private repository, private repos will not be graded.

---

## Part 1: Understanding the Problem (6 points)

*The Guild's cartographers have mapped every corridor. The Torchbearer's first problem is
not reading the map, it is deciding what to do with it.*

Document your understanding in `README.md` under **"Part 1: Problem Analysis"**.
This section should read like a short developer note, not an essay.
Use bullet points. Each bullet is one to two sentences maximum.
These answers also go into `explain_problem()` in your code.

Your three bullets must address:

1. Why a single shortest-path run from S is not sufficient, name the specific decision
   it cannot make.
2. What structural decision remains after all inter-location travel costs are known.
3. In one sentence: why this problem is a search over orders, not a single computation.

The README template shows the exact format expected.

---

## Part 2: Precomputation Design (10 points)

*Before the Torchbearer takes a single step, the engine pre-loads a map of the cheapest
routes between every location it might ever care about.*

Document your design in `README.md` under **"Part 2: Precomputation Design"** with
sub-sections 2a, 2b, 2c. Use tables and bullet points. No prose paragraphs.
These sections correspond to `select_sources()`, `run_dijkstra()`, and
`precompute_distances()` in your code.

### Part 2a: Source Selection (4 points)

Fill in the source-selection table in the README template. For each source node type,
provide a one-line reason. Two rows minimum.

### Part 2b: Distance Storage (3 points)

Fill in the distance-storage table in the README template. Five fields: data structure
name, what keys represent, what values represent, lookup time complexity, and why O(1)
lookup is achievable. One entry per field, no paragraph required.

### Part 2c: Precomputation Complexity (3 points)

Fill in the four complexity bullets in the README template: number of Dijkstra runs,
cost per run, total complexity, and a one-line justification. Let n = |V|, m = |E|,
k = |M|. Single shortest-path run costs O(m log n).

---

## Part 3: Shortest-Path Correctness (12 points)

*The engine only works if the distances it has are real. A wrong distance means the
Torchbearer wastes fuel or never finds the exit.*

Document your understanding in `README.md` under **"Part 3: Algorithm Correctness"**
with sub-sections 3a, 3b, 3c. Use bullets throughout. No paragraphs.
These answers also go into `dijkstra_invariant_check()` in your code.

Consider one run of Dijkstra's algorithm from source `x`. Let `S` be the set of nodes
whose shortest-path distances have been finalized. Let `dist[v]` be the current estimate
for node `v`. The following invariant holds at the start of every main loop iteration:

> For every vertex v in S, dist[v] is the true shortest-path distance from x to v.
> For every vertex u not in S, dist[u] is the length of the shortest discovered path
> from x to u whose internal vertices all lie in S.

### Part 3a: Invariant Explanation (4 points)

Two bullets in the README template: one for finalized nodes, one for non-finalized nodes.
Do not copy the invariant text verbatim. One to two sentences per bullet.

### Part 3b: Invariant Maintenance (6 points)

Three bullets in the README template, one per phase:
- **Initialization:** why the invariant holds before the first iteration.
- **Maintenance:** why finalizing the min-dist node is always correct. Your bullet must
  explicitly name nonnegative edge weights as part of the argument.
- **Termination:** what the invariant guarantees when the algorithm finishes.

One to three sentences per bullet is sufficient.

### Part 3c: Why Correctness Matters (2 points)

One sentence in the README template connecting correct shortest-path distances to
correct routing decisions by the Torchbearer's planner.

---

## Part 4: From Distances to Search (6 points)

*The Torchbearer knows how much fuel every corridor costs. It still does not know which
relic to go for first and that decision changes everything.*

Document your analysis in `README.md` under **"Part 4: Search Design"** with two
sub-sections: "Why Greedy Fails" and "What the Algorithm Must Explore."
Use the five-bullet format shown in the README template. No paragraphs.
These answers also go into `explain_search()` in your code.

**Why Greedy Fails:** Five bullets covering the failure mode, a concrete counter-example
with specific node names or costs (you may use the illustration from the spec), what greedy
picks, what optimal picks, and why greedy loses. One to two sentences per bullet.

**What the Algorithm Must Explore:** One bullet. Must use the word **order**.

---

## Part 5: State and Search Space (10 points)

*Every step of the search, the engine needs to know exactly where it is, what it has
collected, and how much fuel it has burned. Without all three, it cannot make correct
decisions.*

Document your design in `README.md` under **"Part 5: State and Search Space"** with
sub-sections 5a, 5b, 5c. Use tables and bullets throughout.
These sections correspond to `find_optimal_route()` and `_explore()` in your code.

### Part 5a: State Representation (4 points)

Fill in the state-representation table in the README template. Three rows: current
location, relics collected, fuel so far. The variable name column must match exactly
what you use in `torchbearer.py`. Graders cross-reference this table against your code.

### Part 5b: Data Structure for Visited Relics (3 points)

Fill in the data-structure table in the README template. Five rows: structure name,
check-membership complexity, mark-collected complexity, unmark complexity, and why
this structure fits. One entry per row.

### Part 5c: Worst-Case Search Space (3 points)

Two bullets: the worst-case count in terms of k = |M|, and a one-line justification.

---

## Part 6: Pruning (8 points)

*A Torchbearer that explores every possible route wastes time the Guild does not have.
The engine must cut deadend plans early without ever cutting the optimal plan.*

Document your pruning design in `README.md` under **"Part 6: Pruning"** with sub-sections
6a, 6b, 6c. Use the bullet formats shown in the README template.
These answers correspond directly to the pruning logic inside `_explore()`.

### Part 6a: Best-So-Far Tracking (3 points)

Three bullets: what is tracked, when it is used, and what it lets the algorithm skip.
One to two sentences per bullet.

### Part 6b: Lower Bound Estimation (3 points)

Three bullets: what information is available at the current state, what the lower bound
accounts for, and why it never overestimates. One to two sentences per bullet.

### Part 6c: Pruning Correctness (2 points)

One to two bullets explaining why abandoning a branch that cannot beat best-so-far is
guaranteed to never discard the optimal solution.

---

## Part 7: Code Requirements

Implement your solution in `torchbearer.py` using the provided starter template.

**Rules:**
- Implement every function marked `TODO`. Do not change any function signature.
- Do not remove or rename required functions.
- You may add private helper functions.
- Variable names in `torchbearer.py` must match the names defined in README Part 5a.
- The pruning safety comment inside `_explore()` is required and is graded separately.

Code correctness is auto-graded. Code quality is graded manually. See rubric for breakdown.

---

## README Requirements

Your `README.md` must contain these headings in this exact order:

```
# The Torchbearer

## Part 1: Problem Analysis
## Part 2: Precomputation Design
### Part 2a: Source Selection
### Part 2b: Distance Storage
### Part 2c: Precomputation Complexity
## Part 3: Algorithm Correctness
### Part 3a: Invariant Explanation
### Part 3b: Invariant Maintenance
### Part 3c: Why Correctness Matters
## Part 4: Search Design
## Part 5: State and Search Space
### Part 5a: State Representation
### Part 5b: Data Structure for Visited Relics
### Part 5c: Worst-Case Search Space
## Part 6: Pruning
### Part 6a: Best-So-Far Tracking
### Part 6b: Lower Bound Estimation
### Part 6c: Pruning Correctness
## References
```

Missing or renamed headings will not receive credit for that section.
The References section must list any external resources consulted. If none, write
"Lecture notes only."

---

## DEVLOG Requirements

`DEVLOG.md` must contain at least **four dated entries** including:
- An initial plan written before any code is written
- At least one entry describing a bug or wrong assumption and how you resolved it
- An entry after implementation is complete describing what you would change with more time
- A final entry with a per-part time estimate

Two to five sentences per entry is sufficient. Graders check that entries reflect genuine
iterative work across multiple sessions.

---

## Grading Summary

| Section | Points |
|---|---|
| Part 1: Problem Analysis (README) | 6 |
| Part 2a: Source Selection (README) | 4 |
| Part 2b: Distance Storage (README) | 3 |
| Part 2c: Complexity (README) | 3 |
| Part 3: Algorithm Correctness (README) | 12 |
| Part 4: Search Design (README) | 6 |
| Part 5a-c: State and Search Space (README) | 10 |
| Part 6a-c: Pruning (README) | 8 |
| `run_dijkstra` correctness (auto-graded) | 6 |
| `precompute_distances` correctness (auto-graded) | 5 |
| `find_optimal_route` + `_explore` correctness (auto-graded) | 10 |
| `solve` pipeline correctness (auto-graded) | 5 |
| Code quality: comments and naming (manual) | 6 |
| Pruning comment accuracy (manual) | 4 |
| README structure and completeness | 4 |
| DEVLOG completeness | 4 |
| Explanation functions present and non-empty | 4 |
| **Total** | **100** |

---

## Academic Integrity

This assignment assesses your individual understanding of algorithm design and implementation.

- You may use course materials, lecture notes, and the assigned textbook.
- You may not use generative AI tools to produce written answers or code for submission.
- You may not share or copy code with other students.
- You may discuss high-level concepts with classmates, but all writing and all code must
  be your own.

Disclose any external resource in the References section: name the resource, identify which
part it was used for, and explain how you verified the result. Failure to disclose is an
academic integrity violation.

I reserve the right to ask any student to explain their implementation verbally or in writing.
Being unable to explain your own code is grounds for an academic integrity review.
