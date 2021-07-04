# pdf-wrangler

PDFMiner wrapper used to simplify PDF extraction. More functionalities to come to make it a more general purpose PDF utility tool.

## Document class

The `Document` class is used to represent a PDF document. It contains functionality to access the raw text by page, PDF metadata and images in the form of PDFMiner's `LTImage` objects.

## Example Usage

```
from pdf_wrangler import Document

pdf_document = Document('path/to/pdf', password='optional password')

# to access pdf metadata
pdf_document.get_metadata()

# to access pdf text
pdf_document.get_text()

# to access pdf text on first page
pdf_document.pages[0].get_text()
```

## Installation

To install, run:
```
pip install pdf-wrangler
```