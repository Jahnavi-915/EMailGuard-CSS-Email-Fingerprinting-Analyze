import re
from models import Finding
from typing import List

def detect_fontface(css_snippets: List[str]) -> List[Finding]:
    findings = []
    for css in css_snippets:
        # Match @font-face blocks (handles nested braces)
        matches = re.finditer(r'@font-face\s*\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}', css, re.IGNORECASE | re.DOTALL)
        for match in matches:
            block = match.group(1)
            # Find all src: url(...) inside block
            url_matches = re.findall(r'src:\s*url\([\'"]?([^\'"\)]+)[\'"]?\)', block, re.IGNORECASE)
            for url in url_matches:
                # Ignore data: URLs (base64 embedded fonts)
                if not url.startswith('data:'):
                    findings.append(Finding(
                        technique="@font-face Remote Font Loading",
                        snippet=block[:200] + ("..." if len(block) > 200 else ""),
                        risk_level="High",
                        paper_section="Section IV-B",
                        description="Remote font loading enables font fingerprinting.",
                        mitigation="Disallow external font loading or proxy font requests."
                    ))
                    break  # Only add one finding per @font-face block
    return findings