import os
import shutil

app_dir = r"c:/Projects/OnlyOffice/app/editors"

# We only want to keep EN, PT, and default.
keep_prefixes = ('en', 'pt', 'default')

def prune_locales(root_path):
    for root, dirs, files in os.walk(root_path):
        # We process directories named 'locale', 'locales', 'help', 'lang', 'languages', 'translations'
        if os.path.basename(root).lower() in ('locale', 'locales', 'lang', 'languages', 'translations'):
            # It's a directory containing locales... wait, some locales are files (e.g. JSON), some are dirs
            # If files are named like 'en.json', 'pt-BR.json', etc.
            for file in files:
                name, ext = os.path.splitext(file)
                if not name.lower().startswith(keep_prefixes) and name.lower() != 'default':
                    # remove it
                    try:
                        os.remove(os.path.join(root, file))
                    except:
                        pass
        
        # Or if the directories inside are entirely languages
        if os.path.basename(root).lower() in ('help', 'dict', 'dictionaries'):
            for d in dirs[:]:
                if not d.lower().startswith(keep_prefixes) and d.lower() != 'default':
                    dir_path = os.path.join(root, d)
                    try:
                        shutil.rmtree(dir_path)
                        dirs.remove(d) # Don't traverse
                    except:
                        pass

prune_locales(app_dir)
print("Pruned locales and languages from editors.")
