import os
import fitz as f

BASE_DIR = os.path.dirname(__file__)  # folder of this script
PDF_PATH = os.path.join(BASE_DIR, "turing.pdf")

doc = f.open(PDF_PATH)
for page in doc:
    text = page.get_text()
    print(text)