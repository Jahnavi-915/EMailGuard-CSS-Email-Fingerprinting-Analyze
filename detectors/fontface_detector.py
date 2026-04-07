import re
from models import Finding
from typing import List


def detect_fontface(css_snippets: List[str]) -> List[Finding]:
    findings = []

    for css in css_snippets:
        # Check for @font-face
        if not re.search(r'@font-face', css, re.IGNORECASE):
            continue

        # Extract all URLs inside
        urls = re.findall(r'url\([\'"]?([^\'")]+)[\'"]?\)', css, re.IGNORECASE)

        for url in urls:
            # Ignore safe data URLs
            if url.lower().startswith("data:"):
                continue

            findings.append(Finding(
                technique="@font-face Remote Font Loading",
                snippet=css[:200] + "..." if len(css) > 200 else css,
                risk_level="High",
                paper_section="Section IV-B",
                description="Loads external font resource which can be used for tracking and fingerprinting.",
                mitigation="Disallow external font loading or proxy font requests."
            ))
            break  # avoid duplicate findings per snippet

    return findings