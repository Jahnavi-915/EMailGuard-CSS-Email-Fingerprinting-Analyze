import os
from eml_parser import parse_eml

folder = "test_samples/paper_pocs"

for file in os.listdir(folder):
    if file.endswith(".eml"):
        path = os.path.join(folder, file)
        print(f"\n=== Testing: {file} ===")

        html, metadata = parse_eml(path)

        if html:
            print("✅ HTML extracted")
            print(f"Subject: {metadata.get('subject')}")
        else:
            print("❌ No HTML found")