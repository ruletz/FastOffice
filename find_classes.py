import codecs
import re

app_path = 'c:/Projects/OnlyOffice/app/editors/web-apps/apps/documenteditor/main/app.js'
with codecs.open(app_path, 'r', 'utf8') as f:
    text = f.read()

matches = re.findall(r'cls:\s*[\'\"]([^\'\"]*header[^\'\"]*)[\'\"]', text)
print('cls matches:', set(matches))

logo_matches = re.findall(r'cls:\s*[\'\"]([^\'\"]*logo[^\'\"]*)[\'\"]', text)
print('logo matches:', set(logo_matches))

cloud_matches = re.findall(r'cls:\s*[\'\"]([^\'\"]*cloud[^\'\"]*)[\'\"]', text)
print('cloud matches:', set(cloud_matches))

