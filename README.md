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

# to access full pdf text
pdf_document.get_text()

# print text by pdf page
for page in pdf_document.pages:
    print(page.get_text())

# to access pdf images by page
page_1_images = pdf_document.pages[0].images

# get first image bytes representation
page_1_images[0].stream.get_data()
```

## Installation

To install, run:
```
pip install pdf-wrangler
```