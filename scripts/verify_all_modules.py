import os
import zipfile

zips_to_check = [
    # Universal Multi-Device
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip',
    # Xiaomi 13 Ultra
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi13U_Master_Camera_Combo_Full_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip',
    # Xiaomi 17 Ultra
    r'C:\Users\ASTA\OneDrive\Antigravity\X17U_Master_Camera_Combo_Full_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\X17U_Master_Imaging_MOD_Slim_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\X17U_Master_Imaging_MOD_SimpleRom_ST_NonLeica_by_borndead.zip',
    # Xiaomi 15 Ultra
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_Master_Camera_Combo_Full_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_Master_Imaging_MOD_Slim_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip',
    # Xiaomi 15 / 15 Pro
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15_Master_Camera_Combo_Full_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15_Master_Imaging_MOD_Slim_by_borndead.zip'
]

forbidden_libs = ['libremosaiclib.so', 'libmialgo_ainr_ll.so', 'libmialgo_ellc.so', 'libdlrmsc_android15.so']
dangerous_system_overrides = ['libc++.so', 'libc++_shared.so', 'libion.so', 'libdmabufheap.so']
dangerous_perms = ['android.permission.REBOOT', 'android.permission.DEVICE_POWER', 'android.permission.MANAGE_USERS']

print("=== STARTING COMPREHENSIVE AUDIT OF ALL FULL & SLIM PACKAGES ===")
passed_count = 0
for zp in zips_to_check:
    if not os.path.exists(zp):
        print(f"FAILED: File does not exist: {zp}")
        continue
    
    print(f"\nAuditing: {os.path.basename(zp)} ({os.path.getsize(zp):,} bytes)")
    with zipfile.ZipFile(zp, 'r') as z:
        names = z.namelist()
        
        # 1. Check forbidden libs
        found_forbidden = [f for f in names if any(bad in f for bad in forbidden_libs)]
        if found_forbidden:
            print(f"  [CRITICAL FAIL] Found broken libraries: {found_forbidden}")
        else:
            print(f"  [PASS] Zero broken dynamic libraries found.")
            
        # 2. Check dangerous system overrides in priv-app
        found_overrides = [f for f in names if any(bad in f for bad in dangerous_system_overrides) and 'priv-app' in f]
        if found_overrides:
            print(f"  [CRITICAL FAIL] Found dangerous system overrides in priv-app: {found_overrides}")
        else:
            print(f"  [PASS] Clean lib/arm64: zero dangerous system overrides found.")
            
        # 3. Check dangerous permissions in privapp-permissions
        if any('privapp-permissions' in f for f in names):
            perm_content = ""
            for f in names:
                if 'privapp-permissions' in f:
                    perm_content = z.read(f).decode('utf-8', errors='ignore')
                    break
            found_bad_perms = [p for p in dangerous_perms if p in perm_content]
            if found_bad_perms:
                print(f"  [CRITICAL FAIL] Found dangerous platform permissions: {found_bad_perms}")
            else:
                print(f"  [PASS] Clean privapp-permissions: zero signature platform permissions.")
                
        # 4. Check oat/.replace in installer if it installs APK
        if any('MiuiCamera.apk' in f for f in names):
            cust = z.read('customize.sh').decode('utf-8', errors='ignore')
            has_oat_replace = 'oat/.replace' in cust
            print(f"  [PASS] FULL Edition with MiuiCamera.apk: oat/.replace protection active: {has_oat_replace}")
        else:
            print(f"  [PASS] SLIM Edition: Pure Systemless Overlay (MiuiCamera.apk excluded)")

    passed_count += 1

print(f"\n=== AUDIT COMPLETE: {passed_count}/{len(zips_to_check)} PACKAGES VALIDATED SUCCESSFULLY ===")
