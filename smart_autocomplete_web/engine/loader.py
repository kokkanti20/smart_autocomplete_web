from typing import List

def load_words(path: str) -> List[str]:
    words: List[str] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            w = line.strip().lower()
            if w:
                words.append(w)
    return words
