# pdf-wrangler

PDFMiner wrapper used to simplify PDF extraction and other PDF utilities.

## Document class

The `Document` class is used to represent a PDF document. It contains functionality to access the raw text by page, PDF metadata and images in the form of PDFMiner's `LTImage` object.

## Example Usage

```
from pdf_wrangler import Document

pdf_document = Document('path/to/pdf.pdf')

# to access pdf metadata
pdf_document.get_metadata()

# to access pdf text
pdf_document.get_text()

# print text by pdf page
for page in pdf_document.pages:
    print(page.get_text())
```

## Installation

To install, run:
```
pip install pdf-wrangler
```