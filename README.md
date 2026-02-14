# Smart Text Search & Autocomplete Web Application

A web-based autocomplete system built using advanced data structures:

- Trie (Prefix Tree)
- Radix Tree (Compressed Trie)
- Bloom Filter (Probabilistic Membership Check)

This project demonstrates efficient prefix-based search and compares different data structures in a real-time web application.

## 🚀 Features

- Live autocomplete suggestions
- Trie-based prefix search
- Radix Tree (compressed trie) search
- Optional substring search (Contains mode)
- Bloom Filter membership check
- Performance timing (in milliseconds)
- Modern glassmorphism UI
- Large English dictionary dataset support


## 🧠 Technologies Used

- Python 3
- Flask (Web Framework)
- HTML, CSS, JavaScript
- Trie Data Structure
- Radix Tree
- Bloom Filter



## 📂 Project Structure

smart_autocomplete_web/
│
├── app.py
├── requirements.txt
├── data/
│ └── words.txt
├── engine/
│ ├── autocomplete_engine.py
│ ├── trie.py
│ ├── radix_tree.py
│ ├── bloom_filter.py
│ └── loader.py
├── templates/
│ └── index.html
└── static/
└── images/
└── bg.jpg



## ⚙️ Installation & Setup

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Run Application
python app.py

4️⃣ Open Browser

Go to:

http://127.0.0.1:5000


### If using GitHub Codespaces:

Open Ports tab

Click port 5000

Open in browser
