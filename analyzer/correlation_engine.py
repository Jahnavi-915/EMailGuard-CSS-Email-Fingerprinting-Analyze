# correlation_engine.py
from typing import List, Dict, Any
from models import Finding

class CorrelationEngine:
    """
    Rule-based correlation engine to detect multi-stage fingerprinting chains.
    """

    # Define sequences that indicate progressive fingerprinting
    SEQUENCE_RULES = [
        {
            "name": "Progressive probing: @supports -> @media -> calc()",
            "sequence": ["@supports Conditional Resource Loading", "@media Conditional with URL", "CSS calc() Expression"],
            "boost": 15
        },
        {
            "name": "Chain: @import external -> @media exfiltration",
            "sequence": ["External @import Chain", "@media Conditional with URL"],
            "boost": 20
        },
        {
            "name": "Container + calc combination",
            "sequence": ["@container Query with Exfiltration", "CSS calc() Expression"],
            "boost": 10
        },
        {
            "name": "Font + supports probe",
            "sequence": ["@font-face Remote Font Loading", "@supports Conditional Resource Loading"],
            "boost": 12
        }
    ]

    # Chains (two findings that together are dangerous)
    CHAIN_RULES = [
        {
            "name": "@import chain + any remote resource loading",
            "pair": ["External @import Chain", "@media Conditional with URL"],
            "boost": 20,
            "or_alternative": ["External @import Chain", "@container Query with Exfiltration"]
        },
        {
            "name": "Multiple remote font + media exfiltration",
            "pair": ["@font-face Remote Font Loading", "@media Conditional with URL"],
            "boost": 15
        }
    ]

    def __init__(self, findings: List[Finding]):
        self.findings = findings
        self.technique_names = [f.technique for f in findings]

    def detect_sequences(self) -> List[Dict[str, Any]]:
        """Detect ordered sequences of techniques."""
        insights = []
        for rule in self.SEQUENCE_RULES:
            seq = rule["sequence"]
            # Check if all techniques in seq appear in order (not necessarily consecutive)
            idx = 0
            for tech in seq:
                if tech in self.technique_names[idx:]:
                    idx = self.technique_names.index(tech, idx) + 1
                else:
                    break
            else:
                # All found in order
                insights.append({
                    "description": rule["name"],
                    "boost": rule["boost"]
                })
        return insights

    def detect_chains(self) -> List[Dict[str, Any]]:
        """Detect unordered dangerous pairs."""
        insights = []
        for rule in self.CHAIN_RULES:
            if "pair" in rule:
                if rule["pair"][0] in self.technique_names and rule["pair"][1] in self.technique_names:
                    insights.append({
                        "description": rule["name"],
                        "boost": rule["boost"]
                    })
            if "or_alternative" in rule:
                alt = rule["or_alternative"]
                if alt[0] in self.technique_names and alt[1] in self.technique_names:
                    insights.append({
                        "description": rule["name"],
                        "boost": rule["boost"]
                    })
        return insights

    def get_correlation_insights(self) -> List[Dict[str, Any]]:
        """Return all correlation insights with their boosts."""
        all_insights = []
        all_insights.extend(self.detect_sequences())
        all_insights.extend(self.detect_chains())
        # Remove duplicates based on description
        unique = []
        seen = set()
        for ins in all_insights:
            if ins["description"] not in seen:
                seen.add(ins["description"])
                unique.append(ins)
        return unique