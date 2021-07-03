from pathlib import Path

import pytest
from src.pdf_wrangler import Document


@pytest.mark.parametrize('filepath, expected_pages', [
    (Path('tests/fixtures/resume_pdf.pdf'), 1),
]
)
def test_number_of_pages_extracted(filepath: Path, expected_pages: int) -> None:
    document = Document(filepath)
    assert len(document.pages) == expected_pages
