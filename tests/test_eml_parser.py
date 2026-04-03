import pytest
from eml_parser import parse_eml

def test_parse_real_eml(tmp_path):
    # Create a minimal .eml file for testing
    eml_content = b"""From: test@example.com
Subject: Test
MIME-Version: 1.0
Content-Type: text/html; charset="utf-8"

<html><body>Hello</body></html>
"""
    eml_file = tmp_path / "test.eml"
    eml_file.write_bytes(eml_content)
    html, meta = parse_eml(str(eml_file))
    assert "Hello" in html
    assert meta['subject'] == "Test"