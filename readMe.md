# Looking for GPRD compliant solution for extraction

Spacy est une bibliothèque puissante pour le traitement du langage naturel, mais elle n'inclut pas de fonctionnalités intégrées pour l'extraction de texte à partir de fichiers PDF ou d'images. Cependant, vous pouvez combiner Spacy avec d'autres bibliothèques pour accomplir ces tâches. Voici comment vous pouvez le faire :

### 1. Extraction de Texte à partir de PDF

Pour extraire du texte à partir de fichiers PDF, vous pouvez utiliser des bibliothèques comme `PyMuPDF` (également connue sous le nom de `fitz`) ou `pdfplumber`.

#### Utilisation de PyMuPDF (fitz)

```bash
pip install pymupdf
```

```python
import fitz  # PyMuPDF
import spacy

# Charger le modèle Spacy
nlp = spacy.load("en_core_web_sm")

# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

# Chemin vers le fichier PDF
pdf_path = "path/to/your/document.pdf"

# Extraire le texte
pdf_text = extract_text_from_pdf(pdf_path)

# Traiter le texte avec Spacy
doc = nlp(pdf_text)

# Exemple : Imprimer les entités nommées
for ent in doc.ents:
    print(ent.text, ent.label_)
```

#### Utilisation de pdfplumber

```bash
pip install pdfplumber
```

```python
import pdfplumber
import spacy

# Charger le modèle Spacy
nlp = spacy.load("en_core_web_sm")

# Fonction pour extraire le texte d'un PDF
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Chemin vers le fichier PDF
pdf_path = "path/to/your/document.pdf"

# Extraire le texte
pdf_text = extract_text_from_pdf(pdf_path)

# Traiter le texte avec Spacy
doc = nlp(pdf_text)

# Exemple : Imprimer les entités nommées
for ent in doc.ents:
    print(ent.text, ent.label_)
```

### 2. Extraction de Texte à partir d'Images

Pour extraire du texte à partir d'images, vous pouvez utiliser Tesseract OCR via la bibliothèque `pytesseract`.

#### Installation de Tesseract OCR

- **Sur Linux :**
  ```bash
  sudo apt-get install tesseract-ocr
  ```

- **Sur macOS :**
  ```bash
  brew install tesseract
  ```

- **Sur Windows :**
  Téléchargez le programme d'installation à partir de [ce lien](https://github.com/UB-Mannheim/tesseract/wiki) et ajoutez Tesseract à votre PATH.

#### Utilisation de pytesseract

```bash
pip install pytesseract pillow
```

```python
import pytesseract
from PIL import Image
import spacy

# Charger le modèle Spacy
nlp = spacy.load("en_core_web_sm")

# Fonction pour extraire le texte d'une image
def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

# Chemin vers le fichier image
image_path = "path/to/your/image.png"

# Extraire le texte
image_text = extract_text_from_image(image_path)

# Traiter le texte avec Spacy
doc = nlp(image_text)

# Exemple : Imprimer les entités nommées
for ent in doc.ents:
    print(ent.text, ent.label_)
```

### Conclusion

En combinant Spacy avec des bibliothèques telles que `PyMuPDF` ou `pdfplumber` pour les PDF et `pytesseract` pour les images, vous pouvez extraire du texte de divers formats de fichiers et ensuite utiliser les puissantes fonctionnalités de traitement du langage naturel de Spacy pour analyser ce texte.


# Extract both text and images from pdf, word, pptx...

To extract both text from content and text from images within PDF, Word, and PPTX documents, you will need a combination of libraries. Here’s a comprehensive approach for each document type:

### PDF Documents

**Library Combination: PyMuPDF (fitz) + pytesseract**

1. **Extract Text Content using PyMuPDF**
2. **Extract Text from Images using pytesseract**

**Installation:**
```bash
pip install pymupdf pytesseract pillow
```

**Example Code:**
```python
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            # Extract text content
            text += page.get_text()
            # Extract images and perform OCR
            for img in page.get_images(full=True):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image = Image.open(io.BytesIO(image_bytes))
                text += pytesseract.image_to_string(image)
    return text

print(extract_text_from_pdf('example.pdf'))
```

### Word Documents

**Library Combination: python-docx + pytesseract**

1. **Extract Text Content using python-docx**
2. **Extract Text from Images using pytesseract**

**Installation:**
```bash
pip install python-docx pytesseract pillow
```

**Example Code:**
```python
from docx import Document
import pytesseract
from PIL import Image
import io

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    # Extract images and perform OCR
    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            image = Image.open(io.BytesIO(rel.target_part.blob))
            text += pytesseract.image_to_string(image)
    return text

print(extract_text_from_docx('example.docx'))
```

### PowerPoint Presentations

**Library Combination: python-pptx + pytesseract**

1. **Extract Text Content using python-pptx**
2. **Extract Text from Images using pytesseract**

**Installation:**
```bash
pip install python-pptx pytesseract pillow
```

**Example Code:**
```python
from pptx import Presentation
import pytesseract
from PIL import Image
import io

def extract_text_from_pptx(pptx_path):
    prs = Presentation(pptx_path)
    text = ""
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text += shape.text
            if shape.shape_type == 13:  # Image shape type
                image = shape.image
                image_bytes = image.blob
                image = Image.open(io.BytesIO(image_bytes))
                text += pytesseract.image_to_string(image)
    return text

print(extract_text_from_pptx('example.pptx'))
```

### Summary

By combining `PyMuPDF`, `python-docx`, and `python-pptx` with `pytesseract`, you can extract both the text content and text from images in PDF, Word, and PowerPoint documents. This approach ensures you capture all textual data within your documents, regardless of whether it’s in standard text format or embedded within images.

These libraries can be run on-premises or within your Azure infrastructure, ensuring that your data remains secure and under your control.