import logging
from typing import List

from pdfminer.layout import LTImage, LTPage, LTFigure


class Page:
    def __init__(self, raw_page: LTPage, __page_num: int, filepath: str) -> None:
        self.__page_num = __page_num + 1
        self.filepath = filepath

        try:
            self.text = raw_page.groups[0].get_text()
        except Exception as e:
            logger.error(f'Could not extract text from page due to {e}')
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

    def extract_images_from_page(self, page: LTPage) -> List[LTImage]:
        return self.extract_raw_images(page, [])
