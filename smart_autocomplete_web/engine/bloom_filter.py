from dataclasses import dataclass
from typing import Iterable

def _hash_with_seed(s: str, seed: int) -> int:
    h = seed
    for ch in s:
        h = (h * 131 + ord(ch)) & 0xFFFFFFFF
    return h

@dataclass
class BloomFilter:
    m: int = 50000
    k: int = 5

    def __post_init__(self) -> None:
        self._bits = bytearray(self.m // 8 + 1)

    def _set_bit(self, idx: int) -> None:
        self._bits[idx // 8] |= (1 << (idx % 8))

    def _get_bit(self, idx: int) -> int:
        return (self._bits[idx // 8] >> (idx % 8)) & 1

    def _indexes(self, item: str) -> Iterable[int]:
        for i in range(self.k):
            hv = _hash_with_seed(item, seed=0x9E3779B9 + i * 97)
            yield hv % self.m

    def add(self, item: str) -> None:
        item = item.lower()
        for idx in self._indexes(item):
            self._set_bit(idx)

    def might_contain(self, item: str) -> bool:
        item = item.lower()
        return all(self._get_bit(idx) == 1 for idx in self._indexes(item))
