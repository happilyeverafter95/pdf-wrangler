# pdf-wrangler

PDFMiner wrapper used to simplify PDF extraction. More functionalities to come to make it a more general purpose PDF utility tool.

## Document Module

The `Document` module provides a class with the same name used to represent a PDF document. The primary `pages` attribute contains extracted text and images compatible with [Pillow Images](https://pillow.readthedocs.io/en/stable/reference/Image.html).

PDF metadata can also be accessed through the `metadata` attribute.

## Example Usage

```
from pdf_wrangler import Document

pdf_document = Document('path/to/pdf', password='optional password')

# to access pdf metadata
pdf_document.metadata

# to access pdf text & images by pages (iterable)
pdf_document.pages

# text on the first page
pdf_document.pages[0].text
```

## Installation

To install, run:
```
pip install pdf-wrangler
```