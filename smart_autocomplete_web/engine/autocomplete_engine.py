from dataclasses import dataclass
from typing import List, Literal, Optional

from .bloom_filter import BloomFilter
from .trie import Trie
from .radix_tree import RadixTree

Mode = Literal["trie", "radix", "contains"]

@dataclass
class AutocompleteEngine:
    mode: Mode = "trie"
    bloom_m: int = 50000
    bloom_k: int = 5

    def __post_init__(self) -> None:
        self.bloom = BloomFilter(m=self.bloom_m, k=self.bloom_k)
        self.trie: Optional[Trie] = Trie() if self.mode == "trie" else None
        self.radix: Optional[RadixTree] = RadixTree() if self.mode == "radix" else None
        self.words: List[str] = []

    def build(self, words: List[str]) -> None:
        self.words = words
        for w in words:
            w = w.strip().lower()
            if not w:
                continue
            self.bloom.add(w)
            if self.trie:
                self.trie.insert(w)
            if self.radix:
                self.radix.insert(w)

    def suggest(self, prefix: str, topk: int = 10) -> List[str]:
        prefix = prefix.strip().lower()
        if not prefix:
            return []

        # Trie mode (prefix-based)
        if self.mode == "trie" and self.trie:
            return self.trie.autocomplete(prefix, topk=topk)

        # Radix mode (prefix-based)
        if self.mode == "radix" and self.radix:
            return self.radix.autocomplete(prefix, topk=topk)

        # Contains mode (substring-based search)
        if self.mode == "contains":
            results = []
            for word in self.words:
                if prefix in word:
                    results.append(word)
            return results[:topk]

        return []
