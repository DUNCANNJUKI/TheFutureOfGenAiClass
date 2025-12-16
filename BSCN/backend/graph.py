"""
Minimal graph model to simulate JAC walkers deterministically.
Nodes have type and props; edges have type.
Walkers operate over this graph object.
"""
from collections import defaultdict, deque
from typing import Dict, List, Any, Tuple

class Node:
    def __init__(self, nid: str, ntype: str, props: Dict[str, Any]=None):
        self.id = nid
        self.type = ntype
        self.props = props or {}

class Edge:
    def __init__(self, src: str, dst: str, etype: str, props: Dict[str, Any]=None):
        self.src = src
        self.dst = dst
        self.type = etype
        self.props = props or {}

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.adj: Dict[str, List[Edge]] = defaultdict(list)
        self.rev: Dict[str, List[Edge]] = defaultdict(list)

    def add_node(self, nid: str, ntype: str, props: Dict[str, Any]=None):
        self.nodes[nid] = Node(nid, ntype, props)

    def add_edge(self, src: str, dst: str, etype: str, props: Dict[str, Any]=None):
        e = Edge(src, dst, etype, props)
        self.adj[src].append(e)
        self.rev[dst].append(e)

    def get_node(self, nid: str) -> Node:
        return self.nodes.get(nid)

    def neighbors(self, nid: str, etype: str=None) -> List[str]:
        res = []
        for e in self.adj.get(nid, []):
            if etype is None or e.type == etype:
                res.append(e.dst)
        return res

    def incoming(self, nid: str, etype: str=None) -> List[str]:
        res = []
        for e in self.rev.get(nid, []):
            if etype is None or e.type == etype:
                res.append(e.src)
        return res

    def find_paths(self, start: str, target_type: str, max_depth: int=3) -> List[List[str]]:
        # BFS up to depth, return node id paths that end in node.type == target_type
        paths = []
        q = deque([[start]])
        while q:
            path = q.popleft()
            if len(path)-1 > max_depth:
                continue
            last = path[-1]
            node = self.nodes.get(last)
            if node and node.type == target_type and last != start:
                paths.append(path)
            for e in self.adj.get(last, []):
                if e.dst in path:
                    continue
                q.append(path + [e.dst])
        return paths
