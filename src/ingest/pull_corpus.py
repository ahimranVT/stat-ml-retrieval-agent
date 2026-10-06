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
import urllib.parse, urllib.request
from typing import List, Dict
import xml.etree.ElementTree as ET

ARXIV_API = "http://export.arxiv.org/api/query"
CATEGORY = "cat:stat.ML"
MAX_RESULTS_PER_CALL = 100
TOTAL_DOCUMENTS = 600

NAMESPACES = {
    "atom": "http://www.w3.org/2005/Atom",
}

# Get the root for a single batch of entries
def fetch_batch(start:int, max_results:int)-> ET.Element:

    params = {
        'search_query': CATEGORY,
        'start': start,
        'max_results': max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as resp:
        raw = resp.read()

    return ET.fromstring(raw)

# Get the arxiv id, title and summary for entries
def parse_entries(root:ET.Element)-> List[Dict[str,str]]:

    entries = []

    for entry in root.findall("atom:entry", NAMESPACES):

        try:
            entry_info = {
                'arxiv_id':entry.find('atom:id', NAMESPACES).text.strip(),
                'title': entry.find('atom:title', NAMESPACES).text.strip().replace("\n", " "),
                'summary': entry.find('atom:summary', NAMESPACES).text.strip().replace("\n", " "),
            }

        except AttributeError:
            print("[skipped] entry missing required field in (id, title, summary)")
            continue

        entries.append(entry_info)

    return entries

# Break the abstracts down into chunks and return them
def split_recursive(text:str, max_chars:int=600)-> List[str]:

    if len(text) <= max_chars:
        return [text]     

    sentences = text.split(". ")

    if len(sentences) <=1:
        return [text]

    mid = len(sentences) // 2

    c1 = ". ".join(sentences[:mid]).strip()
    c2 = ". ".join(sentences[mid:]).strip()

    return split_recursive(c1, max_chars) + split_recursive(c2, max_chars)    

def main():

    entries = []
    start = 0

    print(f'Pulling ~{TOTAL_DOCUMENTS} abstracts from category {CATEGORY}')

    while len(entries) < TOTAL_DOCUMENTS:

        root = fetch_batch(start, MAX_RESULTS_PER_CALL)
        batch = parse_entries(root)

        if not batch:
            print(f'No more results retrieved. Stopping early')
            break

        entries.extend(batch)
        start += MAX_RESULTS_PER_CALL

        print(f'Fetched {len(entries)} entries so far ...')

        time.sleep(3)

    corpus = []
    chunk_counter = 1

    for entry in entries:
        full_text = entry['title'] + '. ' + entry['summary']
        
        for chunk_text in split_recursive(full_text):

            corpus.append({
                'chunk_id': f'chunk_{chunk_counter:04d}',
                'text': chunk_text,
                'source_paper_id': entry['arxiv_id'],
                'source_title': entry['title']
            })

            chunk_counter += 1
  
    with open("corpus.json", "w") as f:
        json.dump(corpus, f, indent=2)
    
    print(f"\nSaved {len(corpus)} chunks from {len(entries)} papers to corpus.json")
    

if __name__ == "__main__":
    main()