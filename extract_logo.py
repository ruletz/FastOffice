import codecs
import re

html_path = 'c:/Projects/OnlyOffice/app/index.html'

with codecs.open(html_path, 'r', 'utf8') as f:
    text = f.read()

# Look for 'idx-about-cut-logo'. Let's extract 1500 chars around it
m = re.search(r'idx-about-cut-logo', text)
output = ""
if m:
    start = max(0, m.start() - 200)
    end = min(len(text), m.start() + 1500)
    output += "CONTEXT AROUND idx-about-cut-logo:\n" + text[start:end] + "\n\n"

# Search for the word 'ONLYOFFICE' near any 'logo' 
# or search for '.logo ' pattern
m2 = re.search(r'idx-ver-logo', text)
if m2:
    start = max(0, m2.start() - 200)
    end = min(len(text), m2.start() + 1500)
    output += "CONTEXT AROUND idx-ver-logo:\n" + text[start:end] + "\n\n"

with codecs.open("c:/Projects/OnlyOffice/logo_context.txt", "w", "utf8") as out:
    out.write(output)
