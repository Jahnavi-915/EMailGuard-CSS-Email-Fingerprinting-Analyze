import pytest
from models import Finding
from detectors.import_detector import detect_import_rules
from detectors.media_detector import detect_media_queries
from detectors.container_detector import detect_container_queries
from detectors.calc_detector import detect_calc
from detectors.fontface_detector import detect_fontface
from detectors.supports_detector import detect_supports

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
    css = ["@media (max-width: 600px) { body { background-image: url('http://evil.com'); } }"]
    findings = detect_media_queries(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "Critical"

def test_media_no_url():
    # Now our detector flags media without URL as Medium (fingerprinting)
    css = ["@media (max-width: 600px) { body { color: red; } }"]
    findings = detect_media_queries(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "Medium"

def test_container_detector_with_url():
    css = ["@container (width > 100px) { div { background: url('http://evil.com'); } }"]
    findings = detect_container_queries(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "Critical"

def test_container_with_font_units():
    css = ["@container (width > 100px) { div { width: 10ch; } }"]
    findings = detect_container_queries(css)
    # Should detect as High or at least Medium
    assert len(findings) >= 1
    assert findings[0].risk_level in ["High", "Medium"]

def test_calc_detection():
    css = ["width: calc(100% - 20px);"]
    findings = detect_calc(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "High"

def test_calc_no_detection():
    css = ["width: 100px;"]
    findings = detect_calc(css)
    assert len(findings) == 0

def test_fontface_detection():
    css = ["@font-face { src: url('http://evil.com/font.woff'); }"]
    findings = detect_fontface(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "High"

def test_fontface_ignore_data_url():
    css = ["@font-face { src: url('data:font/woff;base64,...'); }"]
    findings = detect_fontface(css)
    assert len(findings) == 0

def test_supports_detection():
    css = ["@supports (display: grid) { div { background: url('http://evil.com'); } }"]
    findings = detect_supports(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "Critical"

def test_supports_no_url():
    css = ["@supports (display: grid) { body { color: red; } }"]
    findings = detect_supports(css)
    assert len(findings) == 1
    assert findings[0].risk_level == "Medium"