import re
from models import Finding
from typing import List

def detect_media_queries(css_snippets: List[str]) -> List[Finding]:
    findings = []
    for css in css_snippets:
        pos = 0
        while True:
            # Match @media ... { ... } with proper brace matching
            match = re.search(r'@media\s*([^{]+)\{', css[pos:], re.IGNORECASE)
            if not match:
                break
            start = pos + match.start()
            brace_start = start + match.end() - pos - 1
            depth = 1
            i = brace_start + 1
            while i < len(css) and depth > 0:
                if css[i] == '{':
                    depth += 1
                elif css[i] == '}':
                    depth -= 1
                i += 1
            block = css[brace_start:i]
            if re.search(r'url\([^)]+\)', block, re.IGNORECASE):
                findings.append(Finding(
                    technique="@media Conditional with URL",
                    snippet=block[:200] + ("..." if len(block) > 200 else ""),
                    risk_level="Critical",
                    paper_section="Section III-B, IV-A3",
                    description="Uses viewport dimensions to conditionally load a remote resource, exfiltrating the result.",
                    mitigation="Preload all conditional resources (Section IX-B)."
                ))
            else:
                # Still a potential fingerprinting attempt
                findings.append(Finding(
                    technique="@media Query (Size-based Fingerprinting)",
                    snippet=block[:200] + ("..." if len(block) > 200 else ""),
                    risk_level="Medium",
                    paper_section="Section III-B",
                    description="Media query can leak viewport dimensions for fingerprinting even without remote resource loading.",
                    mitigation="Consider using a proxy that inlines styles or disables media queries."
                ))
            pos = i
    return findings