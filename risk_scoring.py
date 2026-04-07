# risk_scoring.py
from typing import List, Dict, Any
from models import Finding

BASE_SCORES = {
    "Critical": 30,
    "High": 15,
    "Medium": 8,
    "Low": 3
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
    boost_total = sum(ins.get("boost", 0) for ins in correlation_insights)  # .get() for safety
    raw_score = base_total + boost_total
    score = min(100, raw_score)

    if score <= 20:
        label = "Safe"
    elif score <= 45:
        label = "Moderate"
    elif score <= 70:
        label = "High"
    else:
        label = "Critical"

    return {
        "score": score,
        "label": label,
        "base_total": base_total,
        "boost_total": boost_total
    }