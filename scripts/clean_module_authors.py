import os
import zipfile
import tempfile
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
releases_dir = os.path.join(repo_root, 'releases')

print(f"Scanning releases directory: {releases_dir}")

for zname in sorted(os.listdir(releases_dir)):
    if not zname.endswith('.zip'):
        continue
    zpath = os.path.join(releases_dir, zname)
    modified = False

    with tempfile.TemporaryDirectory() as td:
        with zipfile.ZipFile(zpath, 'r') as z:
            z.extractall(td)

        # 1. Clean module.prop
        mprop = os.path.join(td, 'module.prop')
        if os.path.exists(mprop):
            with open(mprop, 'r', encoding='utf-8', errors='ignore') as fp:
                lines = fp.readlines()
            new_lines = []
            for line in lines:
                if line.startswith('author='):
                    if line.strip() != 'author=borndead':
                        line = 'author=borndead\n'
                        modified = True
                new_lines.append(line)
            with open(mprop, 'w', encoding='utf-8', newline='\n') as fp:
                fp.writelines(new_lines)

        # 2. Clean customize.sh
        mcust = os.path.join(td, 'customize.sh')
        if os.path.exists(mcust):
            with open(mcust, 'r', encoding='utf-8', errors='ignore') as fp:
                ccontent = fp.read()

            orig_c = ccontent
            # Remove any (feat. ...)
            ccontent = re.sub(r'\(feat\.[^\)]+\)', '', ccontent)
            # Remove any "feat. itzdfplayer..."
            ccontent = re.sub(r'feat\.\s*(itzdfplayer|amitkattal|georgekiarie|qualcomm)[^\n"]*', '', ccontent, flags=re.IGNORECASE)
            # Clean up extra spaces around "by borndead"
            ccontent = re.sub(r'by borndead\s+', 'by borndead ', ccontent)

            if ccontent != orig_c:
                modified = True
                with open(mcust, 'w', encoding='utf-8', newline='\n') as fp:
                    fp.write(ccontent)

        if modified:
            with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as zout:
                for root, dirs, files in os.walk(td):
                    for file in files:
                        fp = os.path.join(root, file)
                        rp = os.path.relpath(fp, td).replace('\\', '/')
                        zout.write(fp, rp)
            print(f"[UPDATED] {zname} -> author strictly set to borndead")
        else:
            print(f"[UNCHANGED] {zname} already clean")

print("\n=== ALL RELEASE ZIP FILES UPDATED WITH author=borndead ===")
