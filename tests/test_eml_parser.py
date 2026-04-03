import pytest
from eml_parser import parse_eml
from pathlib import Path

def test_parse_paper_poc_officedetect():
    """Test that officedetect.eml parses and returns HTML."""
    eml_path = Path("test_samples/paper_pocs/officedetect.eml")
    if not eml_path.exists():
        pytest.skip("officedetect.eml not found")
    
    html, metadata = parse_eml(str(eml_path))
    assert html is not None
    assert "html" in html.lower()
    assert metadata['subject'] is not None  # subject may be present

def test_parse_paper_poc_osdetect():
    eml_path = Path("test_samples/paper_pocs/osdetect.eml")
    if not eml_path.exists():
        pytest.skip("osdetect.eml not found")
    
    html, metadata = parse_eml(str(eml_path))
    assert html is not None
    assert "calc" in html or "container" in html.lower()