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


# Other solutions to study
To extract text from various types of files (PDF, PPTX, Word, Markdown, HTML, Outlook, Teams, etc.) both from text content and text included in images (using OCR), you have a few options that can be deployed on-premises or within an Azure environment. Here's an overview of tools and libraries that can help you achieve this, without sending your data to an external API:

### Tools and Libraries for On-Premises or Azure Deployment

#### 1. **Apache Tika**
Apache Tika is a versatile library for extracting text from various file formats including PDF, Word, PPTX, HTML, and more. It can be run on-premises or in an Azure VM.

**Installation and Usage:**
```bash
pip install tika
```

```python
from tika import parser

# Parse PDF
parsed = parser.from_file('example.pdf')
print(parsed['content'])

# Parse Word document
parsed = parser.from_file('example.docx')
print(parsed['content'])

# Parse PPTX
parsed = parser.from_file('example.pptx')
print(parsed['content'])
```

#### 2. **PyMuPDF (fitz) for PDF**
For PDF extraction, PyMuPDF is highly efficient and straightforward.

**Installation and Usage:**
```bash
pip install pymupdf
```

```python
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

print(extract_text_from_pdf('example.pdf'))
```

#### 3. **python-docx for Word Documents**
To work with Word documents, `python-docx` is a reliable choice.

**Installation and Usage:**
```bash
pip install python-docx
```

```python
from docx import Document

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

print(extract_text_from_docx('example.docx'))
```

#### 4. **python-pptx for PowerPoint Presentations**
`python-pptx` is used for extracting text from PPTX files.

**Installation and Usage:**
```bash
pip install python-pptx
```

```python
from pptx import Presentation

def extract_text_from_pptx(pptx_path):
    prs = Presentation(pptx_path)
    text_runs = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text_runs.append(shape.text)
    return "\n".join(text_runs)

print(extract_text_from_pptx('example.pptx'))
```

#### 5. **pytesseract for OCR**
To extract text from images within documents, use Tesseract OCR via `pytesseract`.

**Installation and Usage:**
```bash
pip install pytesseract pillow
```

```python
import pytesseract
from PIL import Image

# Ensure Tesseract is installed and added to your PATH
def extract_text_from_image(image_path):
    return pytesseract.image_to_string(Image.open(image_path))

print(extract_text_from_image('example.png'))
```

### Deployment on Azure

You can run these libraries on Azure Virtual Machines or Azure Kubernetes Service (AKS) for scalable and secure deployment. Ensure that your environment is configured to handle the necessary libraries and dependencies.

### LangChain and LlamaIndex

LangChain and LlamaIndex are primarily frameworks for building language models and integrating them with various data sources and pipelines. While they can help orchestrate and integrate different components of an NLP pipeline, they do not inherently provide the text extraction capabilities out of the box. However, they can be used in conjunction with the aforementioned libraries to build comprehensive NLP solutions.

### Conclusion

For an on-premises or Azure-based solution to extract text from various document types, you can leverage the following libraries:
- **Apache Tika**: For a broad range of file types.
- **PyMuPDF (fitz)**: For PDF files.
- **python-docx**: For Word documents.
- **python-pptx**: For PowerPoint presentations.
- **pytesseract**: For OCR on images.

By using these libraries, you ensure that your data processing remains within your control, and you do not need to send data to external APIs. For deployment, consider using Azure Virtual Machines or Azure Kubernetes Service to maintain a secure and scalable environment.