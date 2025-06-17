from fastapi import APIRouter, Query, UploadFile, File, HTTPException
from app.storage import load_chunks, save_chunks, save_index
from app.semantic_linker import build_index, find_similar, search_index
from app.embedder import embed_query ,embed_chunks
from app.extractor import pdf_pages_extractor
from app.chunker import chunk_pages
import os

router = APIRouter()

chunks = None
index = None

@router.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    global chunks, index  # ✅ declare this FIRST

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    os.makedirs("data/uploads", exist_ok=True)
    file_location = os.path.join("data/uploads", file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    pages = pdf_pages_extractor(file_location)
    processed_chunks = chunk_pages(pages)
    processed_chunks = embed_chunks(processed_chunks)
    index = build_index(processed_chunks)
    links = find_similar(processed_chunks, index)

    for i, chunk in enumerate(processed_chunks):
        chunk["related_chunks"] = links.get(i, [])

    save_chunks(processed_chunks)
    save_index(index)

    chunks = processed_chunks  # 🔁 update global reference

    return {
        "message": f"{file.filename} uploaded and processed.",
        "chunks": len(chunks)
    }

def ensure_chunks_loaded():
    global chunks, index
    if chunks is None or index is None:
        chunks = load_chunks()
        index = build_index(chunks)

@router.get("/chunks")
def get_all_chunks():
    ensure_chunks_loaded()
    return chunks

@router.get("/chunk/{chunk_id}")
def get_chunk(chunk_id: int):
    ensure_chunks_loaded()
    return chunks[chunk_id] if 0 <= chunk_id < len(chunks) else {"error": "Invalid chunk_id"}

@router.get("/related_chunks")
def get_related_chunks(chunk_id: int = Query(...)):
    ensure_chunks_loaded()
    return chunks[chunk_id].get("related_chunks", [])

@router.get("/search")
def semantic_search(query: str):
    ensure_chunks_loaded()
    vector = embed_query(query)
    results = search_index(vector, index, chunks)
    return results
