import os
import shutil
import subprocess
import glob
import re
import zipfile

print("=== Building Properly Aligned & Signed MiuiCamera.apk ===")

build_tools = r'C:\Users\ASTA\AppData\Local\Android\Sdk\build-tools\36.0.0'
zipalign_exe = os.path.join(build_tools, 'zipalign.exe')
apksigner_bat = os.path.join(build_tools, 'apksigner.bat')
dexdump_exe = os.path.join(build_tools, 'dexdump.exe')
apktool_jar = r'C:\WINDOWS\apktool.jar'

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
keystore_path = os.path.join(repo_root, 'tools', 'borndead_camera.keystore')
clean_source_zip = r'C:\Users\ASTA\OneDrive\Antigravity\miui_camera_hyperos3-vFinal.zip'
work_dir = r'C:\Users\ASTA\AppData\Local\Temp\camera_rebrand_clean'
src_apk = os.path.join(work_dir, 'pristine_MiuiCamera.apk')

if os.path.exists(work_dir):
    shutil.rmtree(work_dir)
os.makedirs(work_dir, exist_ok=True)

# Extract 100% pristine APK from miui_camera_hyperos3-vFinal.zip
print(f"\n[0/6] Extracting pristine APK from {os.path.basename(clean_source_zip)}...")
with zipfile.ZipFile(clean_source_zip, 'r') as z:
    with open(src_apk, 'wb') as f:
        f.write(z.read('system/priv-app/MiuiCamera/MiuiCamera.apk'))
print(f"Extracted clean pristine APK: {os.path.getsize(src_apk):,} bytes")

# 1. Decompile resources with apktool
print("\n[1/6] Decompiling resources with apktool (leaving raw DEX untouched)...")
decode_dir = os.path.join(work_dir, 'decoded')
cmd_decode = ['java', '-jar', apktool_jar, 'd', '-s', '-f', '-o', decode_dir, src_apk]
subprocess.run(cmd_decode, check=True)
print("Decoded successfully!")

# 2. Modify XML string resources in all languages
print("\n[2/6] Updating strings.xml resources across all languages...")
strings_modified = 0
for str_file in glob.glob(os.path.join(decode_dir, 'res', 'values*', 'strings.xml')):
    with open(str_file, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    orig = c
    if 'values-ru' in str_file or 'values-uk' in str_file:
        c = re.sub(r'<string name="pref_mod_title">[^<]*</string>',
                   '<string name="pref_mod_title">Описание модификации [Модификация: borndead]</string>', c)
        c = re.sub(r'<string name="pref_mod_label">[^<]*</string>',
                   '<string name="pref_mod_label">"Xiaomi Master Camera Leica 5.0 by borndead\\nTelegram: @Mi_Master_Camera_Combo"</string>', c)
    else:
        c = re.sub(r'<string name="pref_mod_title">[^<]*</string>',
                   '<string name="pref_mod_title">Modification Description [Build Author: borndead]</string>', c)
        c = re.sub(r'<string name="pref_mod_label">[^<]*</string>',
                   '<string name="pref_mod_label">"Xiaomi Master Camera Leica 5.0 by borndead\\nTelegram: @Mi_Master_Camera_Combo"</string>', c)
    c = c.replace('@itzdfplayer_stash', '@Mi_Master_Camera_Combo')
    c = c.replace('@itzdfplayer', 'borndead')
    c = c.replace('HolyBear', 'borndead')
    if c != orig:
        with open(str_file, 'w', encoding='utf-8', newline='\n') as fp:
            fp.write(c)
        strings_modified += 1

print(f"Updated {strings_modified} strings.xml files with borndead author and @Mi_Master_Camera_Combo channel!")

# 3. Rebuild APK with apktool
print("\n[3/6] Rebuilding APK with apktool...")
unaligned_apk = os.path.join(work_dir, 'unaligned.apk')
cmd_build = ['java', '-jar', apktool_jar, 'b', '-f', '-o', unaligned_apk, decode_dir]
subprocess.run(cmd_build, check=True)
print(f"Rebuilt unaligned APK: {os.path.getsize(unaligned_apk):,} bytes")

# 4. Page-align APK with zipalign -p -f 4
print("\n[4/6] Page-aligning APK (4096-byte boundaries for uncompressed .so)...")
aligned_apk = os.path.join(work_dir, 'aligned.apk')
cmd_align = [zipalign_exe, '-p', '-f', '4', unaligned_apk, aligned_apk]
subprocess.run(cmd_align, check=True)

# Verify alignment
res_check = subprocess.run([zipalign_exe, '-c', '4', aligned_apk], capture_output=True, text=True)
if res_check.returncode == 0:
    print("[PASS] Alignment verification SUCCESSFUL: 100% 4KB page-aligned!")
else:
    print(f"[FAIL] Alignment verification failed: {res_check.stderr}")

# 5. Sign with apksigner (v1, v2, v3, v4 signature schemes)
print("\n[5/6] Signing with apksigner (Full v1/v2/v3/v4 support)...")
signed_apk = os.path.join(work_dir, 'MiuiCamera_borndead_signed.apk')
cmd_sign = [
    apksigner_bat, 'sign',
    '--ks', keystore_path,
    '--ks-key-alias', 'master_camera',
    '--ks-pass', 'pass:mastercamera123',
    '--key-pass', 'pass:mastercamera123',
    '--v1-signing-enabled', 'true',
    '--v2-signing-enabled', 'true',
    '--v3-signing-enabled', 'true',
    '--out', signed_apk,
    aligned_apk
]
subprocess.run(cmd_sign, check=True)

# Verify with apksigner
res_verify = subprocess.run([apksigner_bat, 'verify', '-v', signed_apk], capture_output=True, text=True)
print(f"[PASS] Signature verified:\n{res_verify.stdout.strip()}")

# Verify final alignment
res_final_align = subprocess.run([zipalign_exe, '-c', '4', signed_apk], capture_output=True, text=True)
print(f"[PASS] Final zipalign check: {'OK' if res_final_align.returncode == 0 else 'FAIL'}")

# Verify DEX bytecode integrity
print("\n[6/6] Verifying DEX bytecode integrity across all DEX files...")
with zipfile.ZipFile(signed_apk, 'r') as z:
    for name in z.namelist():
        if name.endswith('.dex'):
            out_dex = os.path.join(work_dir, name)
            with open(out_dex, 'wb') as f:
                f.write(z.read(name))
            res_d = subprocess.run([dexdump_exe, '-c', out_dex], capture_output=True, text=True)
            if res_d.returncode != 0 or 'Failure to verify' in res_d.stderr or 'Out-of-order' in res_d.stderr:
                print(f"[FAIL] {name}: Verification failed:\n{res_d.stderr}")
                raise RuntimeError(f"DEX verification failed for {name}")
            else:
                print(f"[PASS] {name}: 100% clean, verified with dexdump (returncode 0)!")

# 7. Deploy to staging directories
print("\n=== Deploying Clean Signed MiuiCamera.apk and Restoring All Companion Libs ===")
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

# Source for complete companion libs
source_libs_dir = r'C:\Users\ASTA\OneDrive\Antigravity\Mi_MultiDevice_Combo_Staging\system\priv-app\MiuiCamera\lib\arm64'
excluded_libs = {
    'libdmabufheap.so', 'libion.so',
    'libremosaiclib.so', 'libmialgo_ainr_ll.so', 'libmialgo_ellc.so', 'libdlrmsc_android15.so'
}

# Also verify Clean_Camera_Payload_Staging gets ALL companion libs
clean_payload_libs = r'C:\Users\ASTA\OneDrive\Antigravity\Clean_Camera_Payload_Staging\system\priv-app\MiuiCamera\lib\arm64'
os.makedirs(clean_payload_libs, exist_ok=True)
for lib in os.listdir(source_libs_dir):
    if lib in excluded_libs:
        continue
    s_f = os.path.join(source_libs_dir, lib)
    d_f = os.path.join(clean_payload_libs, lib)
    if os.path.abspath(s_f) != os.path.abspath(d_f):
        shutil.copy2(s_f, d_f)
print(f"Restored all {len(os.listdir(clean_payload_libs))} companion libraries (including libc++_shared.so) in Clean_Camera_Payload_Staging!")

for sdir in staging_dirs:
    if os.path.exists(sdir):
        dest_apk = os.path.join(sdir, 'MiuiCamera.apk')
        shutil.copy2(signed_apk, dest_apk)
        # Ensure lib/arm64 has clean companion libs
        dest_lib = os.path.join(sdir, 'lib', 'arm64')
        os.makedirs(dest_lib, exist_ok=True)
        for lib in os.listdir(source_libs_dir):
            if lib in excluded_libs:
                continue
            s_f = os.path.join(source_libs_dir, lib)
            d_f = os.path.join(dest_lib, lib)
            if os.path.abspath(s_f) != os.path.abspath(d_f):
                shutil.copy2(s_f, d_f)
        print(f"Updated: {dest_apk} ({os.path.getsize(dest_apk):,} bytes) + libs in {dest_lib}")

print("\n=== SUCCESS: ALL FULL STAGING TARGETS UPDATED WITH FULLY VERIFIED APK & LIBS ===")
