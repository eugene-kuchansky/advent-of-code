import sys
from collections import defaultdict


def read_data() -> list[tuple[str, str]]:
    raw_data = sys.stdin.read()
    connections = []
    for line in raw_data.strip().split("\n"):
        a, b = line.split("-")
        connections.append((a, b))

    return connections


def calc1(connections: list[tuple[str, str]]) -> int:
    result = 0

    inter_connections = defaultdict(set)
    for a, b in connections:
        inter_connections[a].add(b)
        inter_connections[b].add(a)

    triples = set()
    for comp, connects_to in inter_connections.items():
        for other_comp in connects_to:
            common = inter_connections[comp].intersection(inter_connections[other_comp])
            for common_comp in common:
                t = tuple(sorted([comp, object, common_comp]))
                triples.add(t)

    for triple in triples:
        for comp in triple:
            if comp[0] == "t":
                result += 1
                break

    return result


def bron_kerbosch(current_clique, candidates, explored, graph, cliques):
    if not candidates and not explored:
        cliques.append(current_clique)
        return

    for v in list(candidates):
        bron_kerbosch(
            current_clique.union({v}),
            candidates.intersection(graph[v]),
            explored.intersection(graph[v]),
            graph,
            cliques,
        )
        candidates.remove(v)
        explored.add(v)


def calc2(connections: list[tuple[str, str]]) -> str:
    result = 0

    inter_connections = defaultdict(set)
    for a, b in connections:
        inter_connections[a].add(b)
        inter_connections[b].add(a)

    cliques = []
    bron_kerbosch(
        current_clique=set(),
        candidates=set(inter_connections.keys()),
        explored=set(),
        graph=inter_connections,
        cliques=cliques,
    )

    max_clique = 0
    clique = None
    for c in cliques:
        if len(c) > max_clique:
            max_clique = len(c)
            clique = c
    result = ",".join(sorted(clique))
    return result


if __name__ == "__main__":
    connections = read_data()
    print(calc1(connections))
    print(calc2(connections))
