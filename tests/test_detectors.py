import pytest
from detectors.import_detector import detect_import_rules
from detectors.media_detector import detect_media_queries
from detectors.container_detector import detect_container_queries

def test_import_detector():
    css = ["@import url('http://evil.com/style.css');"]
    findings = detect_import_rules(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "Critical"

def test_import_ignores_data_url():
    css = ["@import url('data:text/css,...');"]
    findings = detect_import_rules(css)
    assert len(findings) == 0

def test_media_detector():
    css = ["@media (max-width: 600px) { body { background-image: url('/small'); } }"]
    findings = detect_media_queries(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "Critical"

def test_media_no_url():
    css = ["@media (max-width: 600px) { body { color: red; } }"]
    findings = detect_media_queries(css)
    assert len(findings) == 0

def test_container_detector_with_url():
    css = ["@container (width > 100px) { div { background-image: url('/wide'); } }"]
    findings = detect_container_queries(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "Critical"

def test_container_with_font_units():
    css = ["@container (width > 7.5px) { p { width: 1cap; } }"]
    findings = detect_container_queries(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "High"