import re
from models import Finding
from typing import List

def detect_container_queries(css_snippets: List[str]) -> List[Finding]:
    findings = []
    font_units = ['ch', 'ex', 'ic', 'cap']
    
    for css in css_snippets:
        # Check if this snippet contains @container
        if not re.search(r'@container', css, re.IGNORECASE):
            continue
        
        # Check for URL exfiltration inside any @container block
        container_pattern = r'@container\s*\([^)]+\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}'
        url_found = False
        for block in re.findall(container_pattern, css, re.IGNORECASE | re.DOTALL):
            if re.search(r'url\([^)]+\)', block, re.IGNORECASE):
                findings.append(Finding(
                    technique="@container Query with Exfiltration",
                    snippet=f"@container ... {{ {block[:100]} }}",
                    risk_level="Critical",
                    paper_section="Section IV-A, Listing 1",
                    description="Container query conditionally loads a remote resource based on container size.",
                    mitigation="Preload resources or rewrite to inline styles (Section IX-B)."
                ))
                url_found = True
                break
        
        if not url_found:
            # Simple substring check for font units (case-insensitive)
            css_lower = css.lower()
            if any(unit in css_lower for unit in font_units):
                findings.append(Finding(
                    technique="@container Query with Font-Relative Units",
                    snippet=css[:200] + "..." if len(css) > 200 else css,
                    risk_level="High",
                    paper_section="Section IV-A1",
                    description="Uses font-relative units (ch, ex, ic, cap) to detect installed fonts without remote loading.",
                    mitigation="Disable remote fonts or use a proxy that inlines resources (Section IX-B)."
                ))
    
    return findings