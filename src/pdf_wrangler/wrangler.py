import datetime
import base64
import logging
from io import BytesIO
from typing import List, Dict, Optional

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTFigure, LTImage, LTPage
from pdfminer.pdfdocument import PDFDocument as PDFMinerDocument
from pdfminer.pdfdocument import (PDFPasswordIncorrect, PDFSyntaxError)
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


logger = logging.getLogger(__name__)


def process_metadata(metadata: dict) -> dict:
    for k, v in metadata.items():
        try:
            metadata[k] = v.decode('ascii')
        except AttributeError:
            pass
        if 'date' in k.lower():
            try:
                date_field = v.replace('D:', '')
                metadata[k] = datetime.datetime.strptime(date_field,'%Y%m%d%H%M%S%z').strftime('%D %H:%M')
            except Exception as e:
                # TODO: make exception handling more strict
                logger.warn(f'Unable to parse date field {v} due to {e}')
    return metadata


class Page:
    def __init__(self, raw_page: LTPage, page_num: int, filepath: str) -> None:
        self.page_num = page_num
        self.filepath = filepath
        self.text = self.extract_text(raw_page)
        self.images = self.extract_images_from_page(raw_page, [])

    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return f'PDF page {self.page_num} for {self.filepath}'

    def extract_text(self, page: LTPage) -> str:
        try:
            return page.groups[0].get_text()
        except:
            # TODO: stricter exception handling, logging error message
            return ''

    def extract_images_from_page(self, page: LTPage, images: List[LTImage]) -> List[LTImage]:
        for lt_obj in page:
            if isinstance(lt_obj, LTImage):
                if lt_obj.stream:
                    images.append(lt_obj)
            elif isinstance(lt_obj, LTFigure):
                self.extract_images_from_pdf_obj(lt_obj, images)
        return images


class Document:
    def __init__(self, filepath: str, password: Optional[str] = None) -> None:
        self.filepath = filepath
        self.buffered = BytesIO()
        self.buffered.write(base64.b64decode(self.read_file()))
        self.password = password
        self.pages = []
        self.extract_pdf_pages()
        self.metadata = self.extract_pdf_metadata()

    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return f'PDF from {self.filepath}'

    def read_file(self) -> None:
        with open(self.filepath, 'rb') as f:
            return base64.b64encode(f.read())

    def extract_pdf_pages(self) -> None:
        self.buffered.seek(0)
        rsrcmgr = PDFResourceManager(caching=False)
        device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        try:
            for page in PDFPage.get_pages(self.buffered,
                                          None,
                                          maxpages=None,
                                          password=self.password,
                                          caching=False,
                                          check_extractable=True):
                page.rotate = page.rotate % 360
                interpreter.process_page(page)
                self.pages.append(device.get_result())
        except Exception as e:
            # TODO: make exception handling more strict
            raise Exception(f'Unable to parse PDF pages due to {e}')
        device.close()
        self.parse_pdf_pages()    

    def parse_pdf_pages(self) -> None:
        self.pages = [Page(page, i, self.filepath) for i, page in enumerate(self.pages)]

    def extract_pdf_metadata(self) -> Dict[str, str]:
        parser = PDFParser(self.buffered)
        try:
            doc = PDFMinerDocument(parser)
        except (ValueError, PDFPasswordIncorrect, PDFSyntaxError):
            return {}
        raw_metadata = doc.info[0] if len(doc.info) == 1 else {}
        return process_metadata(raw_metadata)
