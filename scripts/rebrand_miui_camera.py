import os
import shutil
import zipfile
import re
import hashlib
import zlib
import subprocess
import glob

print("=== Starting MiuiCamera.apk Rebranding & Custom Build ===")

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
staging_apk = r'C:\Users\ASTA\OneDrive\Antigravity\Clean_Camera_Payload_Staging\system\priv-app\MiuiCamera\MiuiCamera.apk'
build_dir = r'C:\Users\ASTA\AppData\Local\Temp\camera_mod_workspace'
keystore_path = os.path.join(repo_root, 'tools', 'borndead_camera.keystore')
os.makedirs(os.path.dirname(keystore_path), exist_ok=True)

jdk_bin = r'C:\Program Files\Eclipse Adoptium\jdk-25.0.4.101-hotspot\bin'
keytool_exe = os.path.join(jdk_bin, 'keytool.exe')
jarsigner_exe = os.path.join(jdk_bin, 'jarsigner.exe')
apktool_jar = r'C:\WINDOWS\apktool.jar'

if os.path.exists(build_dir):
    shutil.rmtree(build_dir)
os.makedirs(build_dir, exist_ok=True)

# 1. Decompile APK resources
print("\n[1/6] Decompiling APK resources with apktool...")
cmd_decode = ['java', '-jar', apktool_jar, 'd', '-s', '-f', '-o', build_dir, staging_apk]
res = subprocess.run(cmd_decode, capture_output=True, text=True)
if res.returncode != 0:
    print(f"Error decoding APK: {res.stderr}")
    exit(1)
print("Decoded successfully!")

# 2. Modify XML string resources in all languages
print("\n[2/6] Modifying localized string resources...")
strings_modified_count = 0
for str_file in glob.glob(os.path.join(build_dir, 'res', 'values*', 'strings.xml')):
    with open(str_file, 'r', encoding='utf-8', errors='ignore') as fp:
        content = fp.read()

    orig = content
    # Replace mod title and description
    if 'values-ru' in str_file or 'values-uk' in str_file:
        content = re.sub(r'<string name="pref_mod_title">[^<]*</string>',
                         '<string name="pref_mod_title">Описание модификации [Модификация: borndead]</string>', content)
        content = re.sub(r'<string name="pref_mod_label">[^<]*</string>',
                         '<string name="pref_mod_label">"Xiaomi Master Camera Leica 5.0 by borndead\\nTelegram: @Mi_Master_Camera_Combo"</string>', content)
    else:
        content = re.sub(r'<string name="pref_mod_title">[^<]*</string>',
                         '<string name="pref_mod_title">Modification Description [Build Author: borndead]</string>', content)
        content = re.sub(r'<string name="pref_mod_label">[^<]*</string>',
                         '<string name="pref_mod_label">"Xiaomi Master Camera Leica 5.0 by borndead\\nTelegram: @Mi_Master_Camera_Combo"</string>', content)

    # General cleanup of author handles in strings
    content = content.replace('@itzdfplayer_stash', '@Mi_Master_Camera_Combo')
    content = content.replace('@itzdfplayer', 'borndead')
    content = content.replace('HolyBear', 'borndead')

    if content != orig:
        with open(str_file, 'w', encoding='utf-8', newline='\n') as fp:
            fp.write(content)
        strings_modified_count += 1

print(f"Updated {strings_modified_count} strings.xml resource files!")

# Helper to fix DEX checksum and SHA1
def patch_dex_header(dex_path, old_b, new_b):
    if len(old_b) != len(new_b):
        raise ValueError(f"Byte replacement must be exact same length: {len(old_b)} vs {len(new_b)}")
    with open(dex_path, 'rb') as fp:
        data = bytearray(fp.read())
    
    count = 0
    idx = 0
    while True:
        idx = data.find(old_b, idx)
        if idx == -1: break
        data[idx:idx+len(new_b)] = new_b
        count += 1
        idx += len(new_b)
    
    if count > 0:
        # Recompute SHA-1 signature (bytes 12..31) from bytes 32..end
        sha1 = hashlib.sha1(data[32:]).digest()
        data[12:32] = sha1
        # Recompute Adler-32 checksum (bytes 8..11) from bytes 12..end
        adler = zlib.adler32(data[12:]) & 0xffffffff
        data[8:12] = adler.to_bytes(4, 'little')
        
        with open(dex_path, 'wb') as fp:
            fp.write(data)
        print(f"Patched {count} occurrences in {os.path.basename(dex_path)} & recalculated checksum!")
    else:
        print(f"No occurrences of {old_b} found in {os.path.basename(dex_path)}")

# 3. Patch classes.dex and classes7.dex
print("\n[3/6] Patching DEX bytecode and fixing headers...")
dex_main = os.path.join(build_dir, 'classes.dex')
dex_7 = os.path.join(build_dir, 'classes7.dex')

# Replace telegram link (exact 34 bytes)
old_tg = b"https://t.me/itzdfplayer_stash/847"
new_tg = b"http://t.me/Mi_Master_Camera_Combo"
patch_dex_header(dex_main, old_tg, new_tg)

# Replace author github label (exact 18 bytes)
old_gh = b"GitHub@ItzDFPlayer"
new_gh = b"GitHub@borndead   "
patch_dex_header(dex_7, old_gh, new_gh)

# 4. Rebuild APK with apktool
print("\n[4/6] Rebuilding APK with apktool...")
rebuilt_apk = os.path.join(build_dir, 'rebuilt_MiuiCamera.apk')
cmd_build = ['java', '-jar', apktool_jar, 'b', '-f', '-o', rebuilt_apk, build_dir]
res_build = subprocess.run(cmd_build, capture_output=True, text=True)
if res_build.returncode != 0:
    print(f"Error rebuilding APK: {res_build.stderr}")
    exit(1)
print(f"Rebuilt APK created successfully ({os.path.getsize(rebuilt_apk):,} bytes)!")

# 5. Generate Keystore & Sign APK
print("\n[5/6] Signing APK with custom developer keystore...")
if not os.path.exists(keystore_path):
    print("Generating new borndead_camera.keystore...")
    cmd_genkey = [
        keytool_exe, '-genkeypair', '-v',
        '-keystore', keystore_path,
        '-alias', 'master_camera',
        '-keyalg', 'RSA', '-keysize', '2048',
        '-validity', '10000',
        '-storepass', 'mastercamera123',
        '-keypass', 'mastercamera123',
        '-dname', 'CN=borndead, OU=MasterCamera, O=Leica, L=Global, ST=World, C=US'
    ]
    subprocess.run(cmd_genkey, check=True)

# Sign APK
cmd_sign = [
    jarsigner_exe,
    '-sigalg', 'SHA256withRSA',
    '-digestalg', 'SHA-256',
    '-keystore', keystore_path,
    '-storepass', 'mastercamera123',
    rebuilt_apk,
    'master_camera'
]
res_sign = subprocess.run(cmd_sign, capture_output=True, text=True)
if res_sign.returncode != 0:
    print(f"Error signing APK: {res_sign.stderr}")
    exit(1)
print("Signed successfully!")

# Verify Signature
cmd_verify = [jarsigner_exe, '-verify', rebuilt_apk]
res_verify = subprocess.run(cmd_verify, capture_output=True, text=True)
if 'jar verified' in res_verify.stdout:
    print("[PASS] APK signature verified: 100% valid!")
else:
    print(f"Signature verification warning: {res_verify.stdout}")

# 6. Deploy new MiuiCamera.apk to all staging targets
print("\n[6/6] Deploying signed MiuiCamera.apk to all staging repositories...")
staging_dirs = [
    r'C:\Users\ASTA\OneDrive\Antigravity\Clean_Camera_Payload_Staging\system\priv-app\MiuiCamera',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi_MultiDevice_Combo_Staging\system\priv-app\MiuiCamera',
    r'C:\Users\ASTA\OneDrive\Antigravity\Universal_Full_Staging\system\priv-app\MiuiCamera',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi13U_Full_Staging\system\priv-app\MiuiCamera',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi14U_Full_Staging\system\priv-app\MiuiCamera',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_Full_Staging\system\priv-app\MiuiCamera',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Combo_Staging\system\priv-app\MiuiCamera',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15_Full_Staging\system\priv-app\MiuiCamera',
    r'C:\Users\ASTA\OneDrive\Antigravity\X17U_Full_Staging\system\priv-app\MiuiCamera'
]

for sdir in staging_dirs:
    if os.path.exists(sdir):
        dest_apk = os.path.join(sdir, 'MiuiCamera.apk')
        shutil.copy2(rebuilt_apk, dest_apk)
        print(f"Updated: {dest_apk} ({os.path.getsize(dest_apk):,} bytes)")

print("\n=== ALL STAGING DIRECTORIES EQUIPPED WITH REBRANDED & SIGNED MiuiCamera.apk ===")
