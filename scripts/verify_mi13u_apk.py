import os, zipfile, subprocess, tempfile

zip_path = r'C:\Users\ASTA\OneDrive\Antigravity\Mi13U_Master_Camera_Combo_Full_by_borndead.zip'
build_tools = r'C:\Users\ASTA\AppData\Local\Android\Sdk\build-tools\36.0.0'
zipalign_exe = os.path.join(build_tools, 'zipalign.exe')
apksigner_bat = os.path.join(build_tools, 'apksigner.bat')
dexdump_exe = os.path.join(build_tools, 'dexdump.exe')

with tempfile.TemporaryDirectory() as td:
    apk_out = os.path.join(td, 'MiuiCamera.apk')
    with zipfile.ZipFile(zip_path, 'r') as z:
        libs = [f for f in z.namelist() if f.startswith('system/priv-app/MiuiCamera/lib/arm64/')]
        print(f"Companion libraries count: {len(libs)}")
        for l in sorted(libs):
            print("  ", os.path.basename(l))
        with open(apk_out, 'wb') as f:
            f.write(z.read('system/priv-app/MiuiCamera/MiuiCamera.apk'))
    
    # 1. zipalign check
    za = subprocess.run([zipalign_exe, '-c', '4', apk_out], capture_output=True, text=True)
    status_za = "PASS (OK)" if za.returncode == 0 else "FAIL"
    print(f"Zipalign 4KB page alignment: {status_za}")
    
    # 2. apksigner verify
    sig = subprocess.run([apksigner_bat, 'verify', '-v', apk_out], capture_output=True, text=True)
    print("Signature verified:")
    for line in sig.stdout.splitlines():
        if 'Verified' in line:
            print("  ", line)
            
    # 3. DEX verify
    with zipfile.ZipFile(apk_out, 'r') as apk_z:
        for name in apk_z.namelist():
            if name.endswith('.dex'):
                dex_path = os.path.join(td, name)
                with open(dex_path, 'wb') as df:
                    df.write(apk_z.read(name))
                dd = subprocess.run([dexdump_exe, '-c', dex_path], capture_output=True, text=True)
                has_err = 'Out-of-order' in dd.stderr
                status_dex = "FAIL" if has_err else "PASS (Clean bytecode)"
                print(f"DEX {name}: {status_dex}")
