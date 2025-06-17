# backend/run_pipeline.py
import os
from app.extractor import pdf_pages_extractor
from app.chunker import chunk_pages
from app.embedder import embed_chunks
from app.semantic_linker import build_index, find_similar
from app.storage import save_chunks

BASE_DIR = os.path.dirname(__file__)
PDF_PATH = os.path.join(BASE_DIR, "turing.pdf")

pages = pdf_pages_extractor(PDF_PATH)
chunks = chunk_pages(pages)
chunks = embed_chunks(chunks)

index = build_index(chunks)
semantic_links = find_similar(chunks, index)

for i, chunk in enumerate(chunks):
    chunk["related_chunks"] = semantic_links.get(i, [])

save_chunks(chunks)
print(f"✅ Saved {len(chunks)} chunks. First chunk:\n{chunks[0]}")
