import re
from models import Finding
from typing import List

def detect_import_rules(css_snippets: List[str]) -> List[Finding]:
    findings = []
    pattern = r'@import\s+url\([\'"]?([^\'"\)]+)[\'"]?\)'
    
    for css in css_snippets:
        matches = re.findall(pattern, css, re.IGNORECASE)
        for url in matches:
            # Only flag external imports (not data: URLs)
            if not url.startswith('data:'):
                findings.append(Finding(
                    technique="External @import Chain",
                    snippet=f"@import url({url});",
                    risk_level="Critical",
                    paper_section="Section IV-B, VIII-C2",
                    description="Loads external CSS file. Can be chained to bypass sanitization and exfiltrate data.",
                    mitigation="Convert to inline styles or use a proxy that inlines all resources (Section IX-B)."
                ))
    return findings