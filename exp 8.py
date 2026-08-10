import heapq

INF = float('inf')


def reduce_matrix(mat):
    """Reduce matrix and return reduced matrix and reduction cost."""

    n = len(mat)
    m = [row[:] for row in mat]
    cost = 0

    # Row reduction
    for i in range(n):
        row_min = min(m[i])

        if row_min != INF and row_min > 0:
            cost += row_min

            for j in range(n):
                if m[i][j] != INF:
                    m[i][j] -= row_min

    # Column reduction
    for j in range(n):
        col_min = min(m[i][j] for i in range(n))

        if col_min != INF and col_min > 0:
            cost += col_min

            for i in range(n):
                if m[i][j] != INF:
                    m[i][j] -= col_min

    return m, cost


def tsp_branch_and_bound(cost):
    """TSP using Branch and Bound."""

    n = len(cost)

    # Initial matrix reduction
    reduced_matrix, initial_cost = reduce_matrix(cost)

    # Priority queue:
    # (lower_bound, current_cost, current_city, path, matrix)
    pq = []

    heapq.heappush(
        pq,
        (initial_cost, 0, 0, [0], reduced_matrix)
    )

    best_cost = INF
    best_path = None

    while pq:

        lower_bound, current_cost, current_city, path, matrix = heapq.heappop(pq)

        # Prune if bound is already worse
        if lower_bound >= best_cost:
            continue

        # If all cities are visited
        if len(path) == n:

            if cost[current_city][0] != INF:

                total_cost = (
                    current_cost
                    + cost[current_city][0]
                )

                if total_cost < best_cost:
                    best_cost = total_cost
                    best_path = path + [0]

            continue

        # Branch to unvisited cities
        for next_city in range(n):

            if next_city in path:
                continue

            if cost[current_city][next_city] == INF:
                continue

            new_matrix = [row[:] for row in matrix]

            # Prevent returning to current city
            for j in range(n):
                new_matrix[current_city][j] = INF

            # Prevent visiting next city again
            for i in range(n):
                new_matrix[i][next_city] = INF

            # Prevent premature return to source
            new_matrix[next_city][0] = INF

            # Reduce new matrix
            reduced, reduction_cost = reduce_matrix(new_matrix)

            new_cost = (
                current_cost
                + cost[current_city][next_city]
            )

            new_lower_bound = (
                new_cost
                + reduction_cost
            )

            if new_lower_bound < best_cost:

                heapq.heappush(
                    pq,
                    (
                        new_lower_bound,
                        new_cost,
                        next_city,
                        path + [next_city],
                        reduced
                    )
                )

    return best_path, best_cost


# --- 5-City Cost Matrix ---

cost = [
    [INF, 10, 8, 9, 7],
    [10, INF, 10, 5, 6],
    [8, 10, INF, 8, 9],
    [9, 5, 8, INF, 6],
    [7, 6, 9, 6, INF]
]

n = 5

cities = ['A', 'B', 'C', 'D', 'E']


# --- Run Branch and Bound ---

best_path, best_cost = tsp_branch_and_bound(cost)


# --- Display Cost Matrix ---

print('5-City TSP - Cost Matrix:')

print(
    f'{"":>4}',
    ' '.join(f'{c:>5}' for c in cities)
)

for i, row in enumerate(cost):

    r = [
        'INF' if x == INF else str(x)
        for x in row
    ]

    print(
        f'{cities[i]:>4}',
        ' '.join(f'{v:>5}' for v in r)
    )


# --- Display Result ---

print(
    f'\nOptimal Tour: '
    f'{" -> ".join(cities[i] for i in best_path)}'
)

print(f'Minimum Cost: {best_cost}')


# --- Path Verification ---

print('\nPath verification:')

for i in range(n):

    u = best_path[i]
    v = best_path[i + 1]

    print(
        f' {cities[u]} -> {cities[v]}: '
        f'cost = {cost[u][v]}'
    )