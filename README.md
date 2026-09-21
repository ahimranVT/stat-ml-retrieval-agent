# stat-ml-retrieval-agent

A retrieval-augmented generation (RAG) system for querying machine learning
and statistics research, built around a retriever I fine-tuned myself rather
than an off-the-shelf embedding model. The end goal is an agent that can
answer questions about recent `stat.ML` research on arXiv, with a retrieval
component that's measurably better than a generic baseline, and a CI/CD
pipeline that catches performance regressions automatically.

I'm building this to go deeper on retrieval work I did during my ML Engineer
internship at Netsol (a RAG chatbot POC), and to get hands-on with the
agentic/tool-use patterns that a lot of current AI engineering roles expect.

## Status

🚧 **In progress.** I'm building this step by step and documenting results as
I go, rather than dumping a finished project at the end. See the roadmap
below for where things currently stand.

- [x] Define task & pull corpus (arXiv `stat.ML` abstracts)
- [ ] Build eval set (hand-labeled query → relevant chunk pairs)
- [ ] Baseline retriever (BM25 / off-the-shelf embeddings) + recall@k
- [ ] Fine-tune embedding model in PyTorch
- [ ] Evaluate fine-tuned retriever vs. baseline
- [ ] Wrap retrieval + generation in LangChain
- [ ] Turn retrieval into a LangChain agent tool
- [ ] CI/CD eval harness (GitHub Actions)
- [ ] Deploy + write up final results

## Why this project

Most RAG demos online just call an off-the-shelf embedding model and stop
there. I wanted to actually understand and measure the difference fine-tuning
makes on a specific domain, rather than assume it — so this project is
structured around a real baseline-vs-fine-tuned comparison, not just "it
works."

## Data

- **Source:** [arXiv API](https://arxiv.org/help/api), `stat.ML` category
  (Statistics - Machine Learning)
- **Unit:** paper abstracts, chunked into 1–2 pieces each
- **Size:** ~600 abstracts / ~[N] chunks *(update once corpus is finalized)*
- **Eval set:** hand-labeled query → correct-chunk pairs *(in progress)*

## Planned architecture

```
query --> retriever (fine-tuned embedding model) --> top-k chunks
      --> LangChain agent (decides: search docs? answer directly?)
      --> LLM generates grounded answer
```

CI/CD runs the retrieval eval (recall@k, MRR) on every push and fails the
build if performance drops below a set threshold — the idea being that a
retriever silently getting worse should be caught the same way a broken
test would be.

## Tech stack

- **PyTorch** / sentence-transformers — embedding model fine-tuning
- **LangChain** — retrieval pipeline + agent/tool orchestration
- **GitHub Actions** — automated eval on every push
- **Python** for everything else (data pulling, eval scripts)

## Results

*To be filled in as the project progresses — baseline vs. fine-tuned
retrieval metrics will go here once Step 4 (evaluation) is complete.*

| Model                               | Recall@5 | Recall@10 | MRR |
| ----------------------------------- | -------- | --------- | --- |
| Baseline (off-the-shelf embeddings) | –        | –         | –   |
| Fine-tuned                          | –        | –         | –   |

## Setup

bash

```bash
git clone https://github.com/<your-username>/stat-ml-retrieval-agent.git
cd stat-ml-retrieval-agent
pip install -r requirements.txt
python src/ingest/pull_arxiv_corpus.py
```

## Repo structure

```
stat-ml-retrieval-agent/
├── data/               # corpus + eval set (JSON)
├── src/
│   ├── ingest/         # pulling & chunking arXiv data
│   ├── retrieval/      # baseline + fine-tuned retriever, eval scripts
│   └── training/       # PyTorch fine-tuning code
├── tests/              # eval harness for CI
└── .github/workflows/  # CI/CD config
```

## Notes / lessons learned

*(I'll add short notes here as I hit real problems and fix them — e.g.
chunking edge cases, training gotchas, retrieval failures — since that's
often more interesting to a reader than the polished final result.)*
