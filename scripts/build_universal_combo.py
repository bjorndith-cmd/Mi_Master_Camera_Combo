import os
import shutil
import zipfile

staging = r'C:\Users\ASTA\OneDrive\Antigravity\Mi_MultiDevice_Combo_Staging'

# Update customize.sh in Mi_MultiDevice_Combo_Staging
customize_path = os.path.join(staging, 'customize.sh')
with open(customize_path, 'r', encoding='utf-8') as f:
    cust = f.read()

# Check vendor copy
if 'devices/$DEV_PROFILE/vendor' not in cust:
    old_deploy = '''if [ -d "$MODPATH/devices/$DEV_PROFILE/odm" ]; then
    cp -af "$MODPATH/devices/$DEV_PROFILE/odm/." "$MODPATH/system/odm/"
fi'''
    new_deploy = '''if [ -d "$MODPATH/devices/$DEV_PROFILE/odm" ]; then
    cp -af "$MODPATH/devices/$DEV_PROFILE/odm/." "$MODPATH/system/odm/"
fi

if [ -d "$MODPATH/devices/$DEV_PROFILE/vendor" ]; then
    mkdir -p "$MODPATH/system/vendor"
    cp -af "$MODPATH/devices/$DEV_PROFILE/vendor/." "$MODPATH/system/vendor/"
fi'''
    cust = cust.replace(old_deploy, new_deploy)

# Custom ROM & Nezha preservation check
old_cam_resolv = '''# 4. Resolve system Camera APK installation path
ui_print "- Resolving camera destination paths..."
SRC_APK_PATH="$MODPATH/system/priv-app/MiuiCamera/MiuiCamera.apk"'''

new_cam_resolv = '''# 4. Resolve system Camera APK & Custom ROM Handling
BUILD_ID=$(getprop ro.build.display.id)
BUILD_FLAVOR=$(getprop ro.build.flavor)
MOD_DEV=$(getprop ro.product.mod_device)
ROM_VER=$(getprop ro.build.version.incremental)

IS_CUSTOM_ROM=false
case "$BUILD_ID $BUILD_FLAVOR $MOD_DEV $ROM_VER" in
    *[Ss]imple*|*ST*|*st*|*[Ee][Uu]*|*[Ee]lite*|*[Pp]ulse*|*[Cc]ustom*)
        IS_CUSTOM_ROM=true
        ;;
esac

if [ "$IS_CUSTOM_ROM" = "true" ] || [ "$DEV_PROFILE" = "nezha" ]; then
    ui_print "- Custom ROM ($BUILD_ID) or Xiaomi 17 Ultra detected:"
    ui_print "  Preserving ROM's native patched MiuiCamera.apk (prevents crash)."
    ui_print "  Deploying Chromatix hardware modules, FullRes RAW, DCG HDR & Video MOD."
    rm -rf "$MODPATH/system/priv-app/MiuiCamera"
    rm -rf "$MODPATH/system/product/priv-app/MiuiCamera"
    rm -rf "$MODPATH/product/priv-app/MiuiCamera"
else
ui_print "- Resolving camera destination paths..."
SRC_APK_PATH="$MODPATH/system/priv-app/MiuiCamera/MiuiCamera.apk"'''

if 'IS_CUSTOM_ROM' not in cust:
    cust = cust.replace(old_cam_resolv, new_cam_resolv)
    # close the else block after copy_camera_assets handling
    old_else_end = '''    set_perm_recursive "$MODPATH/system/priv-app/MiuiCamera" 0 0 0755 0644
    mkdir -p "$MODPATH/system/priv-app/MiuiCamera/oat"
    touch "$MODPATH/system/priv-app/MiuiCamera/oat/.nomedia"
fi

# 4. Handle HAL (camera.qcom.so) Compatibility'''

    new_else_end = '''    set_perm_recursive "$MODPATH/system/priv-app/MiuiCamera" 0 0 0755 0644
    mkdir -p "$MODPATH/system/priv-app/MiuiCamera/oat"
    touch "$MODPATH/system/priv-app/MiuiCamera/oat/.nomedia"
fi
fi

# 4. Handle HAL (camera.qcom.so) Compatibility'''
    cust = cust.replace(old_else_end, new_else_end)

with open(customize_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(cust)
print('Updated customize.sh in staging.')

# Package Universal Combo
out_zip = r'C:\Users\ASTA\OneDrive\Antigravity\Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip'
print('Creating zip:', out_zip)
with zipfile.ZipFile(out_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for root, dirs, files in os.walk(staging):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, staging).replace('\\', '/')
            zf.write(full_p, rel_p)

print('Packaged Universal:', out_zip, 'Size:', os.path.getsize(out_zip))
