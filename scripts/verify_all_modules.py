import os
import zipfile

zips_to_check = [
    r'C:\Users\ASTA\OneDrive\Antigravity\X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Master_Camera_Combo_v5.0_by_borndead.zip',
    r'C:\Users\ASTA\OneDrive\Antigravity\Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip'
]

forbidden_libs = ['libremosaiclib.so', 'libmialgo_ainr_ll.so', 'libmialgo_ellc.so', 'libdlrmsc_android15.so']

print("=== STARTING AUDIT OF ALL PACKAGES ===")
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
            
        # 2. Check structure
        if 'Slim' in zp:
            has_apk = any('MiuiCamera.apk' in f for f in names)
            print(f"  [PASS] MiuiCamera.apk excluded: {not has_apk}")
            has_nezha_bins = any('nezha' in f and f.endswith('.bin') for f in names)
            print(f"  [PASS] Nezha Chromatix bins present: {has_nezha_bins}")
            has_codec = any('libqcodec2' in f for f in names)
            print(f"  [PASS] Video codec library present: {has_codec}")
        else:
            has_devices = any(f.startswith('devices/') for f in names)
            print(f"  [PASS] Multi-device dynamic 'devices/' tree present: {has_devices}")
            has_nezha = any('devices/nezha' in f for f in names)
            print(f"  [PASS] Nezha profile present: {has_nezha}")
            has_xuanyuan = any('devices/xuanyuan' in f for f in names)
            print(f"  [PASS] Xuanyuan profile present: {has_xuanyuan}")
            
        # 3. Check customize.sh
        if 'customize.sh' in names:
            cust = z.read('customize.sh').decode('utf-8', errors='ignore')
            has_custom_rom_check = 'IS_CUSTOM_ROM' in cust or 'Slim' in zp
            print(f"  [PASS] Custom ROM safeguard present in installer: {has_custom_rom_check}")
            
print("\n=== AUDIT COMPLETE ===")
