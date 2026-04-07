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
        assert risk["base_total"] == 30
        assert risk["boost_total"] == 0
        assert risk["score"] == 30
        assert risk["label"] == "Moderate"  # 30 is Moderate (21-45)

    def test_single_high(self):
        findings = [make_finding("High")]
        risk = calculate_risk_score(findings, [])
        assert risk["base_total"] == 15
        assert risk["score"] == 15
        assert risk["label"] == "Safe"

    def test_multiple_findings(self):
        findings = [make_finding("Critical"), make_finding("High"), make_finding("Medium")]
        risk = calculate_risk_score(findings, [])
        assert risk["base_total"] == 30 + 15 + 8  # 53
        assert risk["score"] == 53
        assert risk["label"] == "High"  # 46-70 is High

    def test_with_boosts(self):
        findings = [make_finding("Critical")]  # 30
        boosts = [{"description": "test", "boost": 20}]
        risk = calculate_risk_score(findings, boosts)
        assert risk["base_total"] == 30
        assert risk["boost_total"] == 20
        assert risk["score"] == 50
        assert risk["label"] == "High"

    def test_score_capped_at_100(self):
        findings = [make_finding("Critical")] * 4  # 120 base
        boosts = [{"description": "x", "boost": 50}]
        risk = calculate_risk_score(findings, boosts)
        assert risk["score"] == 100
        assert risk["label"] == "Critical"

    def test_medium_risk_boundary(self):
        # 20 -> Safe, 21 -> Moderate
        findings = [make_finding("Medium")] * 2  # 8+8=16, still Safe
        risk = calculate_risk_score(findings, [])
        assert risk["score"] == 16
        assert risk["label"] == "Safe"

        findings = [make_finding("Medium")] * 3  # 24
        risk = calculate_risk_score(findings, [])
        assert risk["score"] == 24
        assert risk["label"] == "Moderate"

    def test_high_risk_boundary(self):
        # 45 -> Moderate, 46 -> High
        findings = [make_finding("High")] * 3  # 45
        risk = calculate_risk_score(findings, [])
        assert risk["score"] == 45
        assert risk["label"] == "Moderate"

        findings = [make_finding("High")] * 4  # 60
        risk = calculate_risk_score(findings, [])
        assert risk["score"] == 60
        assert risk["label"] == "High"