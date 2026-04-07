import re
from models import Finding
from typing import List


def detect_supports(css_snippets: List[str]) -> List[Finding]:
    findings = []

    for css in css_snippets:
        # Check for @supports
        if not re.search(r'@supports', css, re.IGNORECASE):
            continue

        # Extract blocks inside @supports
        supports_pattern = r'@supports\s*\([^)]+\)\s*\{((?:[^{}]|\{[^{}]*\})*)\}'

        blocks = re.findall(supports_pattern, css, re.IGNORECASE | re.DOTALL)

        for block in blocks:
            if re.search(r'url\([^)]+\)', block, re.IGNORECASE):
                findings.append(Finding(
                    technique="@supports Conditional Resource Loading",
                    snippet=f"@supports ... {{ {block[:100]} }}",
                    risk_level="Critical",
                    paper_section="Section IV-C",
                    description="Uses feature detection to conditionally load external resources, enabling fingerprinting.",
                    mitigation="Avoid conditional resource loading or sanitize CSS."
                ))
                break  # avoid duplicates

    return findings