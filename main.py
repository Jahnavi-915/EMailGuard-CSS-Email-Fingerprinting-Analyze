import argparse
from eml_parser import parse_eml
from css_extractor import extract_all_css

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

    if args.verbose:
        print("\n" + "="*50)
        print("EMAIL METADATA")
        print("="*50)
        for k, v in metadata.items():
            print(f"{k}: {v}")
        print("\n" + "="*50)
        print(f"EXTRACTED CSS SNIPPETS ({len(css_snippets)})")
        print("="*50)
        for i, css in enumerate(css_snippets, 1):
            print(f"\n--- Snippet {i} ---")
            # Truncate long CSS for readability
            print(css[:500] + ("..." if len(css) > 500 else ""))

    # Step 3: Detectors (Week 2) – placeholder
    findings = []

    if args.summary:
        print("\nRisk score: N/A (detectors not implemented yet)")
    else:
        print(f"\nAnalysis complete. Found {len(css_snippets)} CSS snippet(s).")
        if not args.verbose:
            print("Use --verbose to see details.")

    return 0

if __name__ == '__main__':
    exit(main())