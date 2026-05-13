"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: _______Alan Vo____________________
Student ID:   _______132574829___________

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.

    """
    return (
         "Why a single shortest-path run from S is not enough: "
        "Dijkstra from S tells us the cheapest cost to reach every node, but it cannot "
        "decide which relic to visit first — the ordering of relic visits is a decision "
        "it never makes.\n\n"

        "What decision remains after all inter-location costs are known: "
        "Even with a complete table of cheapest costs between every pair of relevant "
        "locations, we still must decide the order in which the relics are visited, "
        "since different orderings produce different total costs.\n\n"

        "Why this requires a search over orders: "
        "Because the optimal total cost depends on the sequence in which relics are "
        "collected, and no local greedy rule reliably identifies the globally cheapest "
        "sequence, the engine must search over the space of all possible relic orderings."
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.

    We run Dijkstra from the spawn and from every relic.
    The exit node is never a source because we only ever travel *to* it,
    never *from* it to another required location.

    """
    sources = set()
    sources.add(spawn)
    for r in relics:
        sources.add(r)
    sources.add(exit_node)
    return list(sources)


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    Standard Dijkstra with a binary min-heap.
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0

    # Min-heap entries are (cost, node).
    heap = [(0, source)]

    while heap:
        cost_u, u = heapq.heappop(heap)

        if cost_u > dist[u]:
            continue

        for v, edge_cost in graph[u]:
            new_cost = dist[u] + edge_cost
            if new_cost < dist[v]:
                dist[v] = new_cost
                heapq.heappush(heap, (new_cost, v))

    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    We run one Dijkstra per source node (spawn + each relic).
    This gives us O((k+1) * (m log n)) total precomputation time.
    """
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for src in sources:
        dist_table[src] = run_dijkstra(graph, src)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    """
    return (
        "Part 3a - Invariant explanation:\n"
        "Finalized nodes (in S): Every node u that has been extracted from the heap has "
        "dist[u] equal to the true shortest-path cost from the source; no future "
        "relaxation can improve it.\n"
        "Non-finalized nodes (not in S): dist[v] holds the cost of the cheapest "
        "path discovered so far from the source to v, where all intermediate nodes "
        "on that path belong to S.\n\n"

        "Part 3b - Why each phase holds:\n"
        "Initialization: Before any iteration, dist[source] = 0 and dist[v] = inf for "
        "all other v; the set S is empty, so the invariant holds vacuously for S, and "
        "every non-S estimate reflects the best (and only) discovered path so far.\n"
        "Maintenance: The node u with the minimum dist[u] is finalized because all edge "
        "weights are nonnegative, meaning no undiscovered path through any node outside "
        "S can arrive at u more cheaply than the direct best-known estimate; adding u "
        "to S and relaxing its outgoing edges updates non-S estimates to reflect any "
        "newly discovered shorter paths whose interior now lies entirely in S.\n"
        "Termination: When the heap is empty, every reachable node is in S with its "
        "true shortest-path distance, and unreachable nodes retain dist = inf.\n\n"

        "Part 3c - Why correctness matters for routing:\n"
        "If any precomputed distance is wrong, the planner's cost estimates for "
        "candidate routes will be wrong, potentially causing it to discard the true "
        "optimal route or select a suboptimal one."
            
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    
    """
    return (
        "Why Greedy Fails:\n"
        "Failure mode: A greedy algorithm always travels to the nearest uncollected "
        "relic next; this local choice can force an expensive detour later that a "
        "different ordering would have avoided entirely.\n"
        "Counter-example setup: Using the spec illustration — S→B costs 1, S→C costs 2, "
        "S→D costs 2; from B, going to D costs 1 and to T costs 1.\n"
        "What greedy picks: Greedy from S picks B first (cheapest at cost 1), then must "
        "decide between C and D; if it then picks the nearest remaining relic the total "
        "may be suboptimal depending on the next step.\n"
        "What optimal picks: The optimal route S→B→D→C→T costs 4 total by ordering "
        "relics to avoid expensive cross-edges.\n"
        "Why greedy loses: The cheapest next step locally can force a high-cost edge "
        "later; greedy never looks ahead to consider how the current choice affects "
        "remaining travel costs.\n\n"

        "What the Algorithm Must Explore:\n"
        "The algorithm must explore every possible order in which the relics can be "
        "visited, because only by comparing all orderings (or pruning provably "
        "suboptimal ones) can it guarantee the globally cheapest route."
    
    )


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    TODO
    """
        # best[0] = best cost found so far; best[1] = corresponding relic order.
    best = [float('inf'), []]

    # relics_remaining is a set for O(1) membership, add, and remove (backtrack).
    relics_remaining = set(relics)

    _explore(
        dist_table=dist_table,
        current_loc=spawn,
        relics_remaining=relics_remaining,
        relics_visited_order=[],
        cost_so_far=0.0,
        exit_node=exit_node,
        best=best,
    )

    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.
    """
    # Pruning: Lower-bound check.
    # At this point we know cost_so_far (fuel burned to reach current_loc).
    # The cheapest we could possibly finish is: cost_so_far plus the
    # shortest path from current_loc to ANY remaining relic (we must visit
    # at least one more before reaching the exit) plus the cheapest path
    # from that relic to the exit.  We use the minimum over all remaining
    # relics as the lower bound on future cost.
    #
    # This lower bound never overestimates because it assumes the best
    # possible next relic AND the cheapest possible exit leg — ignoring
    # all other remaining relics.  Any complete route must pay at least
    # this much on top of cost_so_far.
    #
    # Safety guarantee: if lower_bound >= best[0], then even the most
    # optimistic completion of this branch cannot beat the best solution
    # already found.  Therefore no optimal solution is discarded by this
    # pruning step; it only eliminates branches that are provably
    # non-improving.
    
    if relics_remaining:
        current_dists = dist_table.get(current_loc, {})
        min_future = float('inf')
        for r in relics_remaining:
            to_r = current_dists.get(r, float('inf'))
            from_r = dist_table.get(r, {}).get(exit_node, float('inf'))
            min_future = min(min_future, to_r + from_r)
        lower_bound = cost_so_far + min_future
        if lower_bound >= best[0]:
            return
    else:
        cost_to_exit = dist_table.get(current_loc, {}).get(exit_node, float('inf'))
        total_cost = cost_so_far + cost_to_exit
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = list(relics_visited_order)
        return
    
    current_dists = dist_table.get(current_loc, {})
    for next_relic in list(relics_remaining):
        travel_cost = current_dists.get(next_relic, float('inf'))
        if travel_cost == float('inf'):
            continue  # next_relic is unreachable from here; skip.

        new_cost = cost_so_far + travel_cost

        # Best-so-far pruning: abandon if cost already exceeds best known.
        if new_cost >= best[0]:
            continue

        # Choose this relic next (modify state).
        relics_remaining.remove(next_relic)
        relics_visited_order.append(next_relic)

        _explore(
            dist_table=dist_table,
            current_loc=next_relic,
            relics_remaining=relics_remaining,
            relics_visited_order=relics_visited_order,
            cost_so_far=new_cost,
            exit_node=exit_node,
            best=best,
        )

        # Backtrack (restore state for the next candidate).
        relics_visited_order.pop()
        relics_remaining.add(next_relic)


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
