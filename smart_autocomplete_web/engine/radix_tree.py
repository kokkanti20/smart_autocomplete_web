from dataclasses import dataclass, field
from typing import Dict, List

def _lcp(a: str, b: str) -> int:
    n = min(len(a), len(b))
    i = 0
    while i < n and a[i] == b[i]:
        i += 1
    return i

@dataclass
class RadixNode:
    children: Dict[str, "RadixNode"] = field(default_factory=dict)
    is_end: bool = False

class RadixTree:
    def __init__(self) -> None:
        self.root = RadixNode()

    def insert(self, word: str) -> None:
        word = word.lower()
        node = self.root
        rest = word

        while True:
            for edge, child in list(node.children.items()):
                common = _lcp(edge, rest)
                if common == 0:
                    continue

                if common == len(edge):
                    node = child
                    rest = rest[common:]
                    if rest == "":
                        node.is_end = True
                        return
                    break

                # split
                prefix = edge[:common]
                old_suffix = edge[common:]
                new_suffix = rest[common:]

                mid = RadixNode()
                del node.children[edge]
                node.children[prefix] = mid

                mid.children[old_suffix] = child

                if new_suffix == "":
                    mid.is_end = True
                else:
                    mid.children[new_suffix] = RadixNode(is_end=True)
                return

            else:
                node.children[rest] = RadixNode(is_end=True)
                return

    def autocomplete(self, prefix: str, topk: int = 10) -> List[str]:
        prefix = prefix.lower()
        node = self.root
        rest = prefix
        built = ""

        while rest:
            matched = False
            for edge, child in node.children.items():
                common = _lcp(edge, rest)
                if common == 0:
                    continue

                # prefix ends inside this edge
                if common == len(rest):
                    built += rest
                    remainder = edge[common:]
                    # collect from child, but we already consumed remainder as part of the path
                    return self._collect(child, built + remainder, topk)

                # consume full edge
                if common == len(edge):
                    built += edge
                    node = child
                    rest = rest[common:]
                    matched = True
                    break

            if not matched:
                return []

        return self._collect(node, built, topk)

    def _collect(self, start: RadixNode, prefix: str, topk: int) -> List[str]:
        results: List[str] = []

        def dfs(node: RadixNode, cur: str) -> None:
            if len(results) >= topk:
                return
            if node.is_end:
                results.append(cur)
            for edge in sorted(node.children.keys()):
                dfs(node.children[edge], cur + edge)

        dfs(start, prefix)
        return results
