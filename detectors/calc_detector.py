import re
from models import Finding
from typing import List


def detect_calc(css_snippets: List[str]) -> List[Finding]:
    findings = []

    for css in css_snippets:
        # Detect calc() usage (case-insensitive)
        if re.search(r'calc\s*\(', css, re.IGNORECASE):
            findings.append(Finding(
                technique="CSS calc() Expression",
                snippet=css[:200] + "..." if len(css) > 200 else css,
                risk_level="High",
                paper_section="Section V-A",
                description="Use of calc() allows dynamic layout computation, which can be abused for fingerprinting by adapting styles based on device/environment.",
                mitigation="Avoid dynamic CSS expressions or sanitize inputs to prevent leakage of layout-dependent information."
            ))

    return findings