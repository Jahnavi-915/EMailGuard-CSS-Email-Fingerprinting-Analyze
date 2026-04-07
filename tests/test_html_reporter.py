import os
import tempfile
import pytest
from models import Finding
from reporter.html_reporter import generate_html_report

def test_generate_html_report_creates_file():
    findings = [
        Finding(
            technique="Test Technique",
            snippet="test snippet",
            risk_level="High",
            paper_section="Test section",
            description="Test description",
            mitigation="Test mitigation"
        )
    ]
    metadata = {"subject": "Test Email", "from": "test@example.com", "date": "2024-01-01"}
    risk = {"score": 50, "label": "High", "base_total": 30, "boost_total": 20}
    correlation_insights = [{"description": "Test correlation", "boost": 10}]

    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        output_path = tmp.name

    try:
        generate_html_report(findings, metadata, risk, correlation_insights, output_path)
        assert os.path.exists(output_path)
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        assert "EMailGuard" in content
        assert "Test Email" in content
        assert "Test Technique" in content
        assert "High" in content
        assert "Test correlation" in content
    finally:
        if os.path.exists(output_path):
            os.unlink(output_path)