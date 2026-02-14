from flask import Flask, render_template, request, jsonify
import time

from engine.loader import load_words
from engine.autocomplete_engine import AutocompleteEngine

app = Flask(__name__)

# ----------------------------
# Load dataset
# ----------------------------
WORDS_PATH = "data/words.txt"
WORDS = load_words(WORDS_PATH)

# ----------------------------
# Initialize Engines
# ----------------------------
ENGINE_TRIE = AutocompleteEngine(mode="trie")
ENGINE_TRIE.build(WORDS)

ENGINE_RADIX = AutocompleteEngine(mode="radix")
ENGINE_RADIX.build(WORDS)

ENGINE_CONTAINS = AutocompleteEngine(mode="contains")
ENGINE_CONTAINS.build(WORDS)


# ----------------------------
# Home Route
# ----------------------------
@app.route("/")
def home():
    return render_template("index.html", total_words=len(WORDS))


# ----------------------------
# API Route
# ----------------------------
@app.route("/api/suggest")
def suggest():
    prefix = request.args.get("q", "").strip()
    mode = request.args.get("mode", "trie").strip().lower()
    topk = request.args.get("topk", "10")

    try:
        topk = int(topk)
    except ValueError:
        topk = 10

    if mode == "radix":
        engine = ENGINE_RADIX
    elif mode == "contains":
        engine = ENGINE_CONTAINS
    else:
        engine = ENGINE_TRIE

    # Bloom check (full word existence only)
    bloom_result = engine.bloom.might_contain(prefix) if prefix else False

    start = time.perf_counter()
    suggestions = engine.suggest(prefix, topk)
    end = time.perf_counter()

    return jsonify({
        "suggestions": suggestions,
        "bloom_maybe_exists": bloom_result,
        "time_ms": round((end - start) * 1000, 4),
        "count": len(suggestions)
    })


# ----------------------------
# Run Server
# ----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
