from dataclasses import dataclass
from typing import List

@dataclass
class Finding:
    technique: str
    snippet: str
    risk_level: str   # "Critical", "High", "Medium", "Low"
    paper_section: str
    description: str
    mitigation: str