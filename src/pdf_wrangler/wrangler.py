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
from pdfminer.psparser import PSLiteral

from PIL import Image


logger = logging.getLogger(__name__)


def process_metadata(metadata: dict) -> dict:
    for k, v in metadata.items():
        try:
            metadata[k] = v.decode('ascii')
        except AttributeError:
            pass
    return metadata


class PDFImage:
    def __init__(self, image: LTImage, num_image: int, page_num: int) -> None:
        self.__num_image = num_image + 1
        self.__page_num = page_num
        try:
            channel = self._get_image_mode(image)
            image_rawdata = image.stream.get_rawdata()
            self.image = Image.frombytes(channel, image.srcsize, image_rawdata)
        except Exception as e:
            logger.warn(f'Unable to extract image {num_image} from page {page_num} due to "{e}"')
            self.image = None

    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return f'PDF image {self.__num_image} on page {self.__page_num}'

    def _get_image_mode(self, image: LTImage) -> str:
        mode = image.stream.attrs.get('ColorSpace', PSLiteral('DeviceGray')).name
        if mode == 'DeviceRGB':
            return 'RGB'
        elif mode == 'DeviceGray' and image.stream.attrs.get('BitsPerComponent', 8) ==1:
            return '1'
        return 'L'

    def save(self, filepath: str) -> None:
        self.image.save(filepath)


class Page:
    def __init__(self, raw_page: LTPage, __page_num: int, filepath: str) -> None:
        self.__page_num = __page_num + 1
        self.filepath = filepath

        try:
            self.text = raw_page.groups[0].get_text()
        except:
            # TODO: stricter exception handling
            self.text = ''

        self.images = self.extract_images_from_page(raw_page)

    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return f'PDF page {self.__page_num} for {self.filepath}'

    def get_text(self) -> str:
        return self.text

    def extract_raw_images(self, page: LTPage, images: List[LTImage]) -> List[LTImage]:
        for lt_obj in page:
            if isinstance(lt_obj, LTImage):
                if lt_obj.stream:
                    images.append(lt_obj)
            elif isinstance(lt_obj, LTFigure):
                self.extract_raw_images(lt_obj, images)
        return images

    def extract_images_from_page(self, page: LTPage) -> list:
        return [PDFImage(im, i, self.__page_num) for i, im in enumerate(self.extract_raw_images(page, []))]


class Document:
    def __init__(self, filepath: str, password: Optional[str] = None) -> None:
        self.filepath = filepath
        self.buffered = BytesIO()
        self.buffered.write(base64.b64decode(self._read_file()))
        self.password = password
        self.pages = []
        self._extract_pdf_pages()
        self.metadata = self._extract_pdf_metadata()

    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return f'PDF from {self.filepath}'

    def _read_file(self) -> None:
        with open(self.filepath, 'rb') as f:
            return base64.b64encode(f.read())

    def _extract_pdf_pages(self) -> None:
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
            raise Exception(f'Unable to parse PDF pages due to "{e}"')
        device.close()
        self.pages = [Page(page, i, self.filepath) for i, page in enumerate(self.pages)]

    def _extract_pdf_metadata(self) -> Dict[str, str]:
        parser = PDFParser(self.buffered)
        try:
            doc = PDFMinerDocument(parser)
        except (ValueError, PDFPasswordIncorrect, PDFSyntaxError):
            return {}
        raw_metadata = doc.info[0] if len(doc.info) == 1 else {}
        return process_metadata(raw_metadata)

    def get_text(self) -> str:
        return '\n\n'.join([x.text for x in self.pages])

    def get_metadata(self) -> dict:
        return self.metadata
