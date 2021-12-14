import logging
from typing import List, Dict, Optional

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument as PDFMinerDocument
from pdfminer.pdfdocument import (PDFPasswordIncorrect, PDFSyntaxError)
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

from .page import Page


logger = logging.getLogger(__name__)


def process_metadata(metadata: dict) -> dict:
    for k, v in metadata.items():
        try:
            metadata[k] = v.decode('ascii')
        except AttributeError:
            pass
    return metadata


class Document:
    def __init__(self, filepath: str, password: Optional[str] = None) -> None:
        self.filepath = filepath
        self.password = password
        self.pages = []

        self.fp = open(filepath, 'rb')
        self.parser = PDFParser(self.fp)

        self._extract_pdf_pages()
        self.metadata = self._extract_pdf_metadata()

    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return f'PDF from {self.filepath}'

    def _extract_pdf_pages(self) -> None:
        rsrcmgr = PDFResourceManager(caching=False)
        device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        try:
            for page in PDFPage.get_pages(self.fp,
                                          None,
                                          maxpages=None,
                                          password=self.password,
                                          caching=False,
                                          check_extractable=True):
                page.rotate = page.rotate % 360
                interpreter.process_page(page)
                self.pages.append(device.get_result())
        except Exception as e:
            raise Exception(f'Unable to parse PDF pages due to "{e}"')
        self.pages = [Page(page, i, self.filepath) for i, page in enumerate(self.pages)]

    def _extract_pdf_metadata(self) -> Dict[str, str]:
        try:
            doc = PDFMinerDocument(self.parser)
        except (ValueError, PDFPasswordIncorrect, PDFSyntaxError) as e:
            logger.error(f'Unable to extract PDF metadata due to {e}')
            return {}
        raw_metadata = doc.info[0] if len(doc.info) == 1 else {}
        return process_metadata(raw_metadata)

    def get_text(self) -> str:
        return '\n\n'.join([x.text for x in self.pages])

    def get_metadata(self) -> dict:
        return self.metadata
