import pytest
from models import Finding
from risk_scoring import calculate_risk_score

def make_finding(risk_level: str) -> Finding:
    return Finding(
        technique="dummy",
        snippet="dummy",
        risk_level=risk_level,
        paper_section="dummy",
        description="dummy",
        mitigation="dummy"
    )

class TestRiskScoring:

    def test_no_findings_no_boosts(self):
        risk = calculate_risk_score([], [])
        assert risk["score"] == 0
        assert risk["label"] == "Safe"
        assert risk["base_total"] == 0
        assert risk["boost_total"] == 0

    def test_single_critical(self):
        findings = [make_finding("Critical")]
        risk = calculate_risk_score(findings, [])
        assert risk["base_total"] == 40
        assert risk["boost_total"] == 0
        assert risk["score"] == 40
        assert risk["label"] == "High"

    def test_single_high(self):
        findings = [make_finding("High")]
        risk = calculate_risk_score(findings, [])
        assert risk["base_total"] == 25
        assert risk["score"] == 25
        assert risk["label"] == "Moderate"

    def test_multiple_findings(self):
        findings = [make_finding("Critical"), make_finding("High"), make_finding("Medium")]
        risk = calculate_risk_score(findings, [])
        assert risk["base_total"] == 40 + 25 + 15
        assert risk["score"] == 80
        assert risk["label"] == "Critical"

    def test_with_boosts(self):
        findings = [make_finding("Critical")]
        boosts = [{"description": "test", "boost": 20}]
        risk = calculate_risk_score(findings, boosts)
        assert risk["base_total"] == 40
        assert risk["boost_total"] == 20
        assert risk["score"] == 60
        assert risk["label"] == "High"

    def test_score_capped_at_100(self):
        findings = [make_finding("Critical")] * 3
        boosts = [{"description": "x", "boost": 50}]
        risk = calculate_risk_score(findings, boosts)
        assert risk["score"] == 100
        assert risk["label"] == "Critical"

    def test_medium_risk_boundary(self):
        findings = [make_finding("Medium")] * 2  # 30
        risk = calculate_risk_score(findings, [])
        assert risk["score"] == 30
        assert risk["label"] == "Moderate"

        findings = [make_finding("Medium")]  # 15
        risk = calculate_risk_score(findings, [])
        assert risk["score"] == 15
        assert risk["label"] == "Moderate"

    def test_high_risk_boundary(self):
        findings = [make_finding("High")] * 3  # 75
        risk = calculate_risk_score(findings, [])
        assert risk["score"] == 75
        assert risk["label"] == "Critical"

        findings = [make_finding("High")] * 2  # 50
        risk = calculate_risk_score(findings, [])
        assert risk["score"] == 50
        assert risk["label"] == "High"