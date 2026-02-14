from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class TrieNode:
    children: Dict[str, "TrieNode"] = field(default_factory=dict)
    is_end: bool = False

class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        word = word.lower()
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_end = True

    def autocomplete(self, prefix: str, topk: int = 10) -> List[str]:
        prefix = prefix.lower()
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]

        results: List[str] = []

        def dfs(cur: TrieNode, path: str) -> None:
            if len(results) >= topk:
                return
            if cur.is_end:
                results.append(path)
            for c in sorted(cur.children.keys()):
                dfs(cur.children[c], path + c)

        dfs(node, prefix)
        return results
