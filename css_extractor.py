from bs4 import BeautifulSoup
import re
from typing import List

def extract_all_css(html: str) -> List[str]:
    soup = BeautifulSoup(html, 'html.parser')
    css_snippets = []

    # <style> tags
    for style_tag in soup.find_all('style'):
        if style_tag.string:
            css_snippets.append(style_tag.string)

    # inline styles
    for tag in soup.find_all(style=True):
        css_snippets.append(f"{{ {tag['style']} }}")

    # <link rel="stylesheet">
    for link in soup.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            css_snippets.append(f"/* LINK: {href} */")

    # @import statements (also inside existing CSS)
    all_css = "\n".join(css_snippets)
    import_pattern = r'@import\s+url\([\'"]?([^\'"\)]+)[\'"]?\)'
    imports = re.findall(import_pattern, all_css, re.IGNORECASE)
    for imp in imports:
        css_snippets.append(f"@import url({imp});")

    return css_snippets