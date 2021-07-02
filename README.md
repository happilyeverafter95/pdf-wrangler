# pdf-wrangler

This is a PDFMiner wrapper used to simplify extraction. More functionalities to come to make it a more general purpose PDF utility tool.

## Usage

```
from wrangler import Document

pdf_document = Document('path/to/pdf', password='optional password')

# to access pdf metadata
pdf_document.metadata

# to access pdf text & images by pages (iterable)
pdf_document.pages
```