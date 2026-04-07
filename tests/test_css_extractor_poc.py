import pytest
from eml_parser import parse_eml
from css_extractor import extract_all_css
from pathlib import Path


POC_FOLDER = Path("test_samples/paper_pocs")


@pytest.mark.parametrize("eml_file", [
    "minimal.eml",
    "officedetect.eml",
    "osdetect.eml",
    "printdetect.eml",
    "styledetect.eml"
])
def test_css_extraction_on_pocs(eml_file):
    path = POC_FOLDER / eml_file

    # Skip if file missing
    if not path.exists():
        pytest.skip(f"{eml_file} not found")

    # 🔹 Step 1: Parse email
    html, metadata = parse_eml(str(path))

    # ✅ Parser checks
    assert html is not None
    assert isinstance(html, str)
    assert len(html.strip()) > 0

    # 🔹 Step 2: Extract CSS
    css = extract_all_css(html)

    # ✅ CSS extractor checks
    assert isinstance(css, list)

    # Some PoCs may have minimal CSS, so allow >= 0 but check meaningful case
    if len(css) > 0:
        # Ensure extracted snippets are valid strings
        assert all(isinstance(c, str) for c in css)

        # Ensure at least one snippet has some non-empty content
        assert any(len(c.strip()) > 0 for c in css)