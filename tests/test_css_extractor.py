import pytest
from css_extractor import extract_all_css   # <-- ADD THIS LINE

def test_extract_style_tag():
    html = "<style>body{color:red}</style>"
    css = extract_all_css(html)
    assert "body{color:red}" in css[0]

def test_inline_style():
    html = '<div style="margin:0">text</div>'
    css = extract_all_css(html)
    # The function wraps inline style with { }, so check for "margin:0"
    assert any("margin:0" in c for c in css)

def test_link_stylesheet():
    html = '<link rel="stylesheet" href="http://evil.com/style.css">'
    css = extract_all_css(html)
    assert any("LINK: http://evil.com/style.css" in c for c in css)

def test_import_statement():
    html = '<style>@import url("http://evil.com/print.css");</style>'
    css = extract_all_css(html)
    assert any("import" in c.lower() for c in css)