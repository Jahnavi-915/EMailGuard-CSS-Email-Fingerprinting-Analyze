import re
from models import Finding
from typing import List

def detect_supports(css_snippets: List[str]) -> List[Finding]:
    findings = []
    for css in css_snippets:
        pos = 0
        while True:
            match = re.search(r'@supports\s*([^{]+)\{', css[pos:], re.IGNORECASE)
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
                    technique="@supports Conditional Resource Loading",
                    snippet=block[:200] + ("..." if len(block) > 200 else ""),
                    risk_level="Critical",
                    paper_section="Section IV-C",
                    description="Uses feature detection to conditionally load a remote resource.",
                    mitigation="Avoid conditional resource loading or sanitize CSS."
                ))
            else:
                findings.append(Finding(
                    technique="@supports Query (Feature Detection)",
                    snippet=block[:200] + ("..." if len(block) > 200 else ""),
                    risk_level="Medium",
                    paper_section="Section IV-C2",
                    description="Feature detection can be used for fingerprinting even without exfiltration.",
                    mitigation="Consider removing @supports queries or using a proxy."
                ))
            pos = i
    return findings