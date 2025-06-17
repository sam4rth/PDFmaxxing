import nltk
nltk.download('punkt_tab')

def chunk_pages(pages):
    chunks = []
    for page in pages:
        paragraphs = page["text"].split("\n\n")
        for p in paragraphs:
            p = p.strip()
            if len(p) > 50:
                sentences = nltk.sent_tokenize(p)
                chunks.append({
                    "page": page["page"],
                    "text": p,
                    "sentences": sentences
                })
    return chunks