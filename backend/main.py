# 📁 backend/
# │   ├── 📁 app/
# │   │   ├── __init__.py
# │   │   ├── extractor.py          # PDF parsing with PyMuPDF
# │   │   ├── chunker.py            # Chunking logic (NLP/NLTK)
# │   │   ├── embedder.py           # Embedding generator using SBERT
# │   │   ├── linker.py             # Semantic linking using FAISS
# │   │   ├── models.py             # Pydantic models
# │   │   ├── storage.py            # Save/load JSON, DB, etc.
# │   │   └── routes.py             # FastAPI routes
# │   │
# │   ├── main.py                   # FastAPI entrypoint
# │   ├── requirements.txt
# │   ├── README.md
# │   └── data/                     # Local storage for processed PDFs

import os
from app.extractor import pdf_pages_extractor
from app.chunker import chunk_pages
from app.embedder import embed_chunks
from app.semantic_linker import build_index, find_similar
from app.storage import save_chunks, load_chunks

BASE_DIR = os.path.dirname(__file__)  # folder of this script
PDF_PATH = os.path.join(BASE_DIR, "turing.pdf")

pages = pdf_pages_extractor(PDF_PATH)

chunks = chunk_pages(pages)

chunks = embed_chunks(chunks)

index = build_index(chunks)
semantic_links = find_similar(chunks, index)

for i, chunk in enumerate(chunks):
    chunk["related_chunks"] = semantic_links.get(i, [])

save_chunks(chunks)
print(f"First embedding:\n{chunks[0]}...")