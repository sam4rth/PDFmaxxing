from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed_chunks(chunks):
    texts = [chunk["text"] for chunk in chunks]
    vectors = model.encode(texts)
    
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = vectors[i].tolist()  # convert from np array to list
    return chunks

def embed_query(query):
    return model.encode([query])[0]