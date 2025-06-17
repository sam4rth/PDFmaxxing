import faiss
import numpy as np

def build_index(chunks, dim = 384):
    embedding_matrix = np.array([chunk["embedding"] for chunk in chunks]).astype("float32")
    
    index = faiss.IndexFlatL2(dim)
    index.add(embedding_matrix)
    return index

def find_similar(chunks, index, k = 5):
    embedding_matrix = np.array([chunk["embedding"] for chunk in chunks]).astype("float32")
    
    D, I = index.search(embedding_matrix, k + 1)  # +1 to skip self match
    links = {}

    for i, neighbors in enumerate(I):
        links[i] = [int(n) for n in neighbors if n != i]  # skip self
    return links