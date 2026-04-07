# detectors/container_detector.py
import re
from models import Finding
from typing import List

def detect_container_queries(css_snippets: List[str]) -> List[Finding]:
    findings = []
    font_units = ['ch', 'ex', 'ic', 'cap']
    
    for css in css_snippets:
        # Find all @container occurrences with proper brace matching
        pos = 0
        while True:
            # Look for '@container' followed by optional condition and '{'
            match = re.search(r'@container\s*(\([^)]*\))?\s*\{', css[pos:], re.IGNORECASE)
            if not match:
                break
            
            start = pos + match.start()
            brace_start = start + match.end() - pos - 1  # position of '{'
            
            # Find matching closing brace
            depth = 1
            i = brace_start + 1
            while i < len(css) and depth > 0:
                if css[i] == '{':
                    depth += 1
                elif css[i] == '}':
                    depth -= 1
                i += 1
            
            block = css[brace_start:i]  # includes the braces and content
            
            # Check for URL exfiltration
            if re.search(r'url\([^)]+\)', block, re.IGNORECASE):
                findings.append(Finding(
                    technique="@container Query with Exfiltration",
                    snippet=block[:200] + ("..." if len(block) > 200 else ""),
                    risk_level="Critical",
                    paper_section="Section IV-A, Listing 1",
                    description="Container query conditionally loads a remote resource based on container size.",
                    mitigation="Preload resources or rewrite to inline styles (Section IX-B)."
                ))
            # Check for font-relative units
            elif any(unit in block.lower() for unit in font_units):
                findings.append(Finding(
                    technique="@container Query with Font-Relative Units",
                    snippet=block[:200] + ("..." if len(block) > 200 else ""),
                    risk_level="High",
                    paper_section="Section IV-A1",
                    description="Uses font-relative units (ch, ex, ic, cap) to detect installed fonts without remote loading.",
                    mitigation="Disable remote fonts or use a proxy that inlines resources (Section IX-B)."
                ))
            else:
                # Generic container query fingerprinting (like OS detection)
                findings.append(Finding(
                    technique="@container Query (Size-based Fingerprinting)",
                    snippet=block[:200] + ("..." if len(block) > 200 else ""),
                    risk_level="Medium",
                    paper_section="Section IV-A",
                    description="Container query can leak container dimensions (e.g., scrollbar width) for fingerprinting.",
                    mitigation="Consider rewriting container queries to static styles or use a proxy that inlines resources."
                ))
            
            pos = i  # continue after this block
    
    return findings