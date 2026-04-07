import re
from models import Finding
from typing import List

def detect_import_rules(css_snippets: List[str]) -> List[Finding]:
    findings = []
    patterns = [
        r'@import\s+url\([\'"]?([^\'"\)]+)[\'"]?\)',
        r'@import\s+[\'"]([^\'"]+)[\'"]'
    ]
    for css in css_snippets:
        for pattern in patterns:
            matches = re.findall(pattern, css, re.IGNORECASE)
            for url in matches:
                if not url.startswith('data:'):
                    findings.append(Finding(
                        technique="External @import Chain",
                        snippet=f"@import {url}",
                        risk_level="Critical",
                        paper_section="Section IV-B, VIII-C2",
                        description="Loads external CSS file. Can be chained to bypass sanitization and exfiltrate data.",
                        mitigation="Convert to inline styles or use a proxy that inlines all resources (Section IX-B)."
                    ))
    return findings