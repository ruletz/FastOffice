import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# the logo in OnlyOffice is normally an SVG or a class.
# let's look for elements that might represent the branding
m = re.search(r'<div[^>]*class=[\'"][^\'"]*logo[^\'"]*[\'"][^>]*>.*?</div\s*>', text, re.IGNORECASE | re.DOTALL)
if m:
    print("Found div with logo:")
    print(m.group(0)[:500])

m = re.search(r'<svg[^>]*class=[\'"][^\'"]*logo[^\'"]*[\'"][^>]*>.*?</svg>', text, re.IGNORECASE | re.DOTALL)
if m:
    print("\nFound svg with logo:")
    print(m.group(0)[:500])

