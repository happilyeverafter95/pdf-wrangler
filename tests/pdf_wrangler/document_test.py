from pathlib import Path

import pytest
from src.pdf_wrangler import Document


@pytest.mark.parametrize('filepath, text', [
    (Path('tests/fixtures/resume_pdf.pdf'),
    'FirstnameNAME\nBorn on dd/mm/yyyy in City\nAdress, Postal Code City, Country\n\uf10b xx.xx.xx.xx.xx\n| \uf0e0 ﬁrst'),
]
)
def test_text_extraction_first_100_characters(filepath: Path, text: str) -> None:
    document = Document(filepath)
    assert document.get_text()[:100] == text
