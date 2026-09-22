import os
import shutil
import zipfile

# 1. Clean post-fs-data.sh in both stagings
clean_post_fs_data = """#!/system/bin/sh
# post-fs-data.sh - Safe initialization without policy tampering
# Prevents Magisk Safe Mode and preserves root on all firmwares
MODDIR=${0%/*}
"""

multi_staging = r'C:\Users\ASTA\OneDrive\Antigravity\Mi_MultiDevice_Combo_Staging'
ishtar_staging = r'C:\Users\ASTA\OneDrive\Antigravity\Mi13U_Master_Combo_Staging'

for stg in [multi_staging, ishtar_staging]:
    p = os.path.join(stg, 'post-fs-data.sh')
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(clean_post_fs_data)
    print(f'Cleaned post-fs-data.sh in: {stg}')

# 2. Update customize.sh in ishtar_staging to preserve native APK on Android 14
cust_13u_path = os.path.join(ishtar_staging, 'customize.sh')
with open(cust_13u_path, 'r', encoding='utf-8') as f:
    cust_13u = f.read()

# Add A14 / HOS 1.0 safeguard before copy_camera_assets
target_cam_str = '# 4. Resolve system Camera APK installation path'
replacement_cam_str = """# 4. Resolve system Camera APK installation path
# On Android 14 (HyperOS 1.0 / API <= 34), preserving native Leica Camera APK prevents black screen!
if [ "$API" -le 34 ]; then
    ui_print "- Android 14 / HyperOS 1.0 detected (API $API):"
    ui_print "  Preserving native Leica Camera APK (prevents black screen on HOS 1.0)."
    rm -rf "$MODPATH/system/priv-app/MiuiCamera"
    rm -rf "$MODPATH/system/product/priv-app/MiuiCamera"
    rm -rf "$MODPATH/product/priv-app/MiuiCamera"
else
"""

if 'if [ "$API" -le 34 ]; then' not in cust_13u:
    # find where APK install logic ends and close the else block
    old_end = """    ui_print "  Installing to default: /system/priv-app/MiuiCamera/MiuiCamera.apk"
    set_perm_recursive "$MODPATH/system/priv-app/MiuiCamera" 0 0 0755 0644
    mkdir -p "$MODPATH/system/priv-app/MiuiCamera/oat"
    touch "$MODPATH/system/priv-app/MiuiCamera/oat/.nomedia"
fi

# 5. Handle ODM / Vendor partition layout"""

    new_end = """    ui_print "  Installing to default: /system/priv-app/MiuiCamera/MiuiCamera.apk"
    set_perm_recursive "$MODPATH/system/priv-app/MiuiCamera" 0 0 0755 0644
    mkdir -p "$MODPATH/system/priv-app/MiuiCamera/oat"
    touch "$MODPATH/system/priv-app/MiuiCamera/oat/.nomedia"
fi
fi

# 5. Handle ODM / Vendor partition layout"""

    cust_13u = cust_13u.replace(target_cam_str, replacement_cam_str).replace(old_end, new_end)
    with open(cust_13u_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(cust_13u)
    print('Updated customize.sh in ishtar_staging.')

# Repackage 13U combo
out_13u_v51 = r'C:\Users\ASTA\OneDrive\Antigravity\Mi13U_Master_Camera_Combo_v5.1_by_borndead.zip'
out_13u_v50 = r'C:\Users\ASTA\OneDrive\Antigravity\Mi13U_Master_Camera_Combo_v5.0_by_borndead.zip'
with zipfile.ZipFile(out_13u_v51, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for root, dirs, files in os.walk(ishtar_staging):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, ishtar_staging).replace('\\', '/')
            zf.write(full_p, rel_p)

shutil.copy2(out_13u_v51, out_13u_v50)
print('Packaged 13U combo:', out_13u_v51, 'Size:', os.path.getsize(out_13u_v51))

# 3. Update customize.sh in multi_staging
cust_multi_path = os.path.join(multi_staging, 'customize.sh')
with open(cust_multi_path, 'r', encoding='utf-8') as f:
    cust_multi = f.read()

# Make sure for ishtar, camera.qcom.so is never copied on Android 14 either
old_hal_check = """if [ "$API" -ge 35 ]; then
    ui_print "- Android 15/16 detected (API $API):"
    if [ "$DEV_PROFILE" = "xuanyuan" ]; then
        ui_print "  Deploying native HyperOS 3.0 / A16 HAL (EUXM 3.0.9.0) for Xiaomi 15 Ultra."
    else
        ui_print "  Preserving native A16 Camera HAL (prevents black screen)."
        ui_print "  FullRes unlocked via Chromatix bins + maxRAWSizes."
        rm -rf "$MODPATH/system/odm/lib64/hw"
        rm -rf "$MODPATH/system/vendor/odm/lib64/hw"
    fi
else
    ui_print "- Android 14 detected (API $API): keeping patched camera.qcom.so."
fi"""

new_hal_check = """if [ "$API" -ge 35 ]; then
    ui_print "- Android 15/16 detected (API $API):"
    if [ "$DEV_PROFILE" = "xuanyuan" ]; then
        ui_print "  Deploying native HyperOS 3.0 / A16 HAL (EUXM 3.0.9.0) for Xiaomi 15 Ultra."
    else
        ui_print "  Preserving native A16 Camera HAL for $DEV_PROFILE (prevents black screen)."
        rm -rf "$MODPATH/system/odm/lib64/hw"
        rm -rf "$MODPATH/system/vendor/odm/lib64/hw"
    fi
else
    ui_print "- Android 14 detected (API $API):"
    if [ "$DEV_PROFILE" = "ishtar" ]; then
        ui_print "  Preserving native A14 Camera HAL for Xiaomi 13 Ultra (prevents black screen)."
        rm -rf "$MODPATH/system/odm/lib64/hw"
        rm -rf "$MODPATH/system/vendor/odm/lib64/hw"
    fi
fi"""

if old_hal_check in cust_multi:
    cust_multi = cust_multi.replace(old_hal_check, new_hal_check)
    with open(cust_multi_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(cust_multi)
    print('Updated HAL handling in multi_staging customize.sh.')

# Repackage Universal Combo
out_universal = r'C:\Users\ASTA\OneDrive\Antigravity\Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip'
with zipfile.ZipFile(out_universal, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for root, dirs, files in os.walk(multi_staging):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, multi_staging).replace('\\', '/')
            zf.write(full_p, rel_p)

print('Packaged Universal combo:', out_universal, 'Size:', os.path.getsize(out_universal))
