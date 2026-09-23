import os
import re

scripts_dir = os.path.dirname(os.path.abspath(__file__))

print(f"Cleaning build scripts in: {scripts_dir}")

for fname in os.listdir(scripts_dir):
    if not fname.endswith('.py') or fname in ('clean_module_authors.py', 'update_build_scripts_author.py'):
        continue
    fpath = os.path.join(scripts_dir, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()

    orig = content
    # Replace author=borndead (feat. ...) with author=borndead
    content = re.sub(r'author=borndead\s*\([^\)]+\)', 'author=borndead', content)
    # Also in customize.sh ui_print or comments: (feat. itzdfplayer...)
    content = re.sub(r'\(feat\.[^\)]+\)', '', content)
    content = re.sub(r'feat\.\s*(itzdfplayer|amitkattal|georgekiarie|qualcomm)[^\n"]*', '', content, flags=re.IGNORECASE)

    if content != orig:
        with open(fpath, 'w', encoding='utf-8', newline='\n') as fp:
            fp.write(content)
        print(f"[UPDATED] {fname}")
    else:
        print(f"[UNCHANGED] {fname}")

print("\n=== BUILD SCRIPTS CLEANED ===")
