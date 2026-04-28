import os
import shutil

keep_basenames = {
    'en.json', 'en.js', 'en-GB.js',
    'pt-pt.json', 'pt-pt.js', 'pt-PT.js', 'pt.json', 'pt.js'
}

count = 0

# Find all locale directories
for root, dirs, files in os.walk('/c/Projects/OnlyOffice/Source'):
    if os.path.basename(root).lower() == 'locale':
        for f in files:
            if f not in keep_basenames:
                fp = os.path.join(root, f)
                os.remove(fp)
                count += 1
                print(f'  Deleted: {fp}')

print(f'\nDeleted {count} locale files total')

# Handle template directories
tpl = '/c/Projects/OnlyOffice/Source/desktopeditors/desktop-apps/common/templates'
if os.path.isdir(tpl):
    for d in os.listdir(tpl):
        dp = os.path.join(tpl, d)
        if os.path.isdir(dp) and d not in ('EN', 'PT'):
            shutil.rmtree(dp)
            print(f'Removed template dir: {d}')
    print('Template cleanup done')

print('All done!')
