# risk_scoring.py
from typing import List, Dict, Any
from models import Finding

# Base scores – increased to reflect real risk
BASE_SCORES = {
    "Critical": 40,
    "High": 25,
    "Medium": 15,
    "Low": 8
}

def calculate_risk_score(findings: List[Finding], correlation_insights: List[Dict[str, Any]]) -> dict:
    """
    Returns:
        {
            "score": int (0-100),
            "label": str,
            "base_total": int,
            "boost_total": int
        }
    """
    base_total = sum(BASE_SCORES.get(f.risk_level, 0) for f in findings)
    boost_total = sum(ins.get("boost", 0) for ins in correlation_insights)
    raw_score = base_total + boost_total
    score = min(100, max(0, raw_score))

    # Adjusted thresholds – more sensitive to fingerprinting
    if score <= 10:
        label = "Safe"
    elif score <= 30:
        label = "Moderate"
    elif score <= 60:
        label = "High"
    else:
        label = "Critical"

    return {
        "score": score,
        "label": label,
        "base_total": base_total,
        "boost_total": boost_total
    }