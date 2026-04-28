import os
import re

path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/app.js'

with open(path, 'r', encoding='utf8') as f:
    text = f.read()

def find_context(term):
    print(f"\n--- Searching for {term} ---")
    matches = list(re.finditer(r'.{0,100}' + term + r'.{0,100}', text, re.IGNORECASE))
    for i, m in enumerate(matches[:5]):
        print(f"Match {i+1}: {m.group(0)}")

find_context(r'clouds*')
find_context(r'collaboration')
find_context(r'plugins')
find_context(r'protection')
find_context(r'title.*?align')
find_context(r'toolbar')

