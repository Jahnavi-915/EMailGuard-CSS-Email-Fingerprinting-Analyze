import pytest
from models import Finding
from correlation_engine import CorrelationEngine

# Helper to create a Finding with just technique name
def make_finding(technique: str) -> Finding:
    return Finding(
        technique=technique,
        snippet="dummy snippet",
        risk_level="High",
        paper_section="dummy",
        description="dummy",
        mitigation="dummy"
    )

class TestCorrelationEngine:

    def test_no_findings(self):
        engine = CorrelationEngine([])
        insights = engine.get_correlation_insights()
        assert insights == []

    def test_single_technique_no_correlation(self):
        findings = [make_finding("External @import Chain")]
        engine = CorrelationEngine(findings)
        insights = engine.get_correlation_insights()
        # No sequence or pair matched because need multiple
        assert insights == []

    def test_sequence_supports_media_calc(self):
        findings = [
            make_finding("@supports Conditional Resource Loading"),
            make_finding("@media Conditional with URL"),
            make_finding("CSS calc() Expression")
        ]
        engine = CorrelationEngine(findings)
        insights = engine.get_correlation_insights()
        assert len(insights) == 1
        assert insights[0]["description"] == "Progressive probing: @supports -> @media -> calc()"
        assert insights[0]["boost"] == 15

    def test_sequence_requires_order(self):
        # Wrong order: calc before media
        findings = [
            make_finding("CSS calc() Expression"),
            make_finding("@media Conditional with URL"),
            make_finding("@supports Conditional Resource Loading")
        ]
        engine = CorrelationEngine(findings)
        insights = engine.get_correlation_insights()
        # The sequence rule requires @supports -> @media -> calc() in that order.
        # Since order is wrong, no match.
        assert not any(ins["description"] == "Progressive probing: @supports -> @media -> calc()" for ins in insights)

    def test_chain_import_and_media(self):
        findings = [
            make_finding("External @import Chain"),
            make_finding("@media Conditional with URL")
        ]
        engine = CorrelationEngine(findings)
        insights = engine.get_correlation_insights()
        # Should match both sequence and chain? Sequence requires @import then @media? Actually sequence rule "Chain: @import external -> @media exfiltration" is in SEQUENCE_RULES.
        # But there's also a CHAIN_RULE for same pair. We'll check that at least one is found.
        assert any(ins["description"] == "Chain: @import external -> @media exfiltration" for ins in insights)
        # Also should see the pair chain (duplicate but deduped)
        assert any(ins["description"] == "@import chain + any remote resource loading" for ins in insights)

    def test_container_and_calc(self):
        findings = [
            make_finding("@container Query with Exfiltration"),
            make_finding("CSS calc() Expression")
        ]
        engine = CorrelationEngine(findings)
        insights = engine.get_correlation_insights()
        assert any(ins["description"] == "Container + calc combination" for ins in insights)
        assert any(ins["boost"] == 10 for ins in insights if ins["description"] == "Container + calc combination")

    def test_font_and_supports(self):
        findings = [
            make_finding("@font-face Remote Font Loading"),
            make_finding("@supports Conditional Resource Loading")
        ]
        engine = CorrelationEngine(findings)
        insights = engine.get_correlation_insights()
        assert any(ins["description"] == "Font + supports probe" for ins in insights)

    def test_multiple_chains_deduplication(self):
        # Same pair triggers both sequence and chain rules – but should be deduped by description.
        findings = [
            make_finding("External @import Chain"),
            make_finding("@media Conditional with URL")
        ]
        engine = CorrelationEngine(findings)
        insights = engine.get_correlation_insights()
        # There are two different descriptions for this pair: 
        # "Chain: @import external -> @media exfiltration" (sequence rule) and 
        # "@import chain + any remote resource loading" (chain rule).
        # They are different descriptions, so both appear. That's acceptable.
        # But we test that no duplicate of the same description.
        descriptions = [ins["description"] for ins in insights]
        assert len(descriptions) == len(set(descriptions))

    def test_empty_findings_returns_empty(self):
        engine = CorrelationEngine([])
        assert engine.get_correlation_insights() == []