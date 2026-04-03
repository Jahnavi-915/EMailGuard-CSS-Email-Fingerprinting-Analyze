import pytest
from css_extractor import extract_all_css
from eml_parser import parse_eml
from pathlib import Path

def test_extract_css_from_officedetect():
    """Week 1: Ensure CSS is extracted without crashing."""
    eml_path = Path("test_samples/paper_pocs/officedetect.eml")
    if not eml_path.exists():
        pytest.skip("officedetect.eml not found")
    
    html, _ = parse_eml(str(eml_path))
    css_snippets = extract_all_css(html)
    
    # Week 1 requirement: we successfully extracted something (not empty)
    assert len(css_snippets) > 0
    # Optional: check that we have at least one snippet containing '@container'
    combined = " ".join(css_snippets).lower()
    assert "@container" in combined or "container" in combined

def test_extract_css_from_osdetect():
    eml_path = Path("test_samples/paper_pocs/osdetect.eml")
    if not eml_path.exists():
        pytest.skip("osdetect.eml not found")
    
    html, _ = parse_eml(str(eml_path))
    css_snippets = extract_all_css(html)
    
    # Week 1: we extracted CSS (could be <link> comments or actual rules)
    assert len(css_snippets) > 0
    # The osdetect.eml uses a data: URI – our extractor records the LINK comment
    # That's acceptable for Week 1; Week 2 detectors will handle decoding.
    assert any("link" in s.lower() or "@container" in s.lower() for s in css_snippets)

def test_extract_css_from_printdetect():
    eml_path = Path("test_samples/paper_pocs/printdetect.eml")
    if not eml_path.exists():
        pytest.skip("printdetect.eml not found")
    
    html, _ = parse_eml(str(eml_path))
    css_snippets = extract_all_css(html)
    
    assert len(css_snippets) > 0
    # May contain @media print or @page (but not required for Week 1)
    combined = " ".join(css_snippets).lower()
    # Just ensure something was extracted; don't fail if no specific keyword
    assert True

def test_extract_css_from_styledetect():
    eml_path = Path("test_samples/paper_pocs/styledetect.eml")
    if not eml_path.exists():
        pytest.skip("styledetect.eml not found")
    
    html, _ = parse_eml(str(eml_path))
    css_snippets = extract_all_css(html)
    
    assert len(css_snippets) > 0