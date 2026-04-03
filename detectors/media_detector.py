import re
from models import Finding
from typing import List

def detect_media_queries(css_snippets: List[str]) -> List[Finding]:
    findings = []
    # Detect @media rules that contain both a condition (width, height, etc.) and a url()
    media_pattern = r'@media\s*\([^)]+\)\s*\{([^}]*)\}'
    
    for css in css_snippets:
        matches = re.findall(media_pattern, css, re.IGNORECASE | re.DOTALL)
        for block in matches:
            if re.search(r'url\([^)]+\)', block, re.IGNORECASE):
                findings.append(Finding(
                    technique="@media Conditional with URL",
                    snippet=f"@media ... {{ {block[:100]} }}",
                    risk_level="Critical",
                    paper_section="Section III-B, IV-A3",
                    description="Uses viewport dimensions to conditionally load a remote resource, exfiltrating the result.",
                    mitigation="Preload all conditional resources (Section IX-B)."
                ))
    return findings