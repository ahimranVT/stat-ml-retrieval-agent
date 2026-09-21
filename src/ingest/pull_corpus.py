"""
Pulls abstracts from arXiv's stat.ML category and saves them as a ready-for-retrieval chunked
corpus

Usage:
    pip install arxiv --break-system-packages
    python pull_corpus.py

Output:
    corpus.json  ->  [{"chunk_id": "chunk_0001", "text": "..."}]
"""

import json
import time
from typing import List, Dict, Any
import xml.etree.ElementTree as ET

ARXIV_API = "http://export.arxiv.org/api/query"
CATEGORY = "cat:stat.ML"
MAX_RESULTS_PER_CALL = 100
TOTAL_DOCUMENTS = 600

NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
}

# Get the root for a single batch of entries
def fetch_batch(start:int, max_results:int)-> ET.element:
    return

# Get the arxiv id, title and summary for entries
def parse_entries(root:ET.Element)-> List[Dict[str,str]]:
    return

# Break the abstracts down into chunks and return them
def chunk_abstract(title:str, summary:str, max_chars:int=600)-> List[str]:
    return
    

def main():

    entries = []
    start = 0

    print(f'Pulling ~{TOTAL_DOCUMENTS} abstracts from category {CATEGORY}')

    while len(entries) < TOTAL_DOCUMENTS:

        root = fetch_batch(start, MAX_RESULTS_PER_CALL)
        batch = parse_entries(root)

        if not batch:
            print(f'No more results retrieved. Stopping early')

        entries.extend(batch)
        start += MAX_RESULTS_PER_CALL

        print(f'Fetched {len(entries)} entries so far ...')

        time.sleep(3)

    corpus = []
    chunk_counter = 1

    for entry in entries:
        for chunk_text in chunk_abstract(entry['title'], entry['summary']):

            corpus.append({
                'chunk_id': f'chunk_{chunk_counter:04d}',
                'text': chunk_text,
                'source_paper_id': entry['id'],
                'source_title': entry['title']
            })

            chunk_counter += 1
  
    with open("corpus.json", "w") as f:
        json.dump(corpus, f, indent=2)
    
    print(f"\nSaved {len(corpus)} chunks from {len(entries)} papers to corpus.json")
    

if __name__ == "__main__":
    main()