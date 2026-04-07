import argparse
from eml_parser import parse_eml
from css_extractor import extract_all_css
from detectors.import_detector import detect_import_rules
from detectors.media_detector import detect_media_queries
from detectors.container_detector import detect_container_queries
from detectors.calc_detector import detect_calc
from detectors.fontface_detector import detect_fontface
from detectors.supports_detector import detect_supports
from correlation_engine import CorrelationEngine
from risk_scoring import calculate_risk_score
from reporter.html_reporter import generate_html_report

def main():
    parser = argparse.ArgumentParser(description="EMailGuard - CSS Email Fingerprinting Analyzer")
    parser.add_argument('--input', required=True, help='Path to .eml file')
    parser.add_argument('--output', default='report.html', help='Output HTML report path')
    parser.add_argument('--verbose', action='store_true', help='Print findings to console')
    parser.add_argument('--summary', action='store_true', help='Only print risk score')
    args = parser.parse_args()

    # Step 1: Parse email
    html, metadata = parse_eml(args.input)
    if html is None:
        print("Error: No HTML part found in the email.")
        return 1

    # Step 2: Extract CSS
    css_snippets = extract_all_css(html)

    # Step 3: Run detectors
    findings = []
    findings.extend(detect_import_rules(css_snippets))
    findings.extend(detect_media_queries(css_snippets))
    findings.extend(detect_container_queries(css_snippets))
    findings.extend(detect_calc(css_snippets))
    findings.extend(detect_fontface(css_snippets))
    findings.extend(detect_supports(css_snippets))

    # Deduplicate findings
    unique_findings = {}
    for f in findings:
        key = (f.technique, f.snippet.strip())
        if key not in unique_findings:
            unique_findings[key] = f
    findings = list(unique_findings.values())

    # Step 4: Correlation
    corr_engine = CorrelationEngine(findings)
    correlation_insights = corr_engine.get_correlation_insights()

    # Step 5: Risk scoring
    risk = calculate_risk_score(findings, correlation_insights)

    # Step 6: Output
    if args.verbose:
        print("\n" + "="*60)
        print("EMAIL METADATA")
        print("="*60)
        for k, v in metadata.items():
            print(f"{k}: {v}")
        print("\n" + "="*60)
        print(f"FINDINGS ({len(findings)})")
        print("="*60)
        for i, f in enumerate(findings, 1):
            print(f"\n--- Finding {i} ---")
            print(f"Technique: {f.technique}")
            print(f"Risk: {f.risk_level}")
            print(f"Paper: {f.paper_section}")
            print(f"Snippet: {f.snippet[:200]}...")
            print(f"Mitigation: {f.mitigation}")

        print("\n" + "="*60)
        print("CORRELATION INSIGHTS")
        print("="*60)
        for ins in correlation_insights:
            print(f"- {ins['description']} (Boost: +{ins['boost']})")

        print("\n" + "="*60)
        print(f"RISK SCORE: {risk['score']}/100 ({risk['label']})")
        print(f"  Base total: {risk['base_total']} | Boost total: {risk['boost_total']}")
        print("="*60)

    if args.summary:
        print(f"{risk['label']} ({risk['score']}/100)")
    else:
        # Generate HTML report
        generate_html_report(findings, metadata, risk, correlation_insights, args.output)
        print(f"\nAnalysis complete. HTML report saved to: {args.output}")

    return 0

if __name__ == '__main__':
    exit(main())