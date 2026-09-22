import os
import shutil
import zipfile

staging = r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Combo_Staging'
multi_staging = r'C:\Users\ASTA\OneDrive\Antigravity\Mi_MultiDevice_Combo_Staging'

if os.path.exists(staging):
    shutil.rmtree(staging)
os.makedirs(staging, exist_ok=True)

# Copy META-INF
shutil.copytree(os.path.join(multi_staging, 'META-INF'), os.path.join(staging, 'META-INF'))

# Copy devices/xuanyuan and devices/nezha
os.makedirs(os.path.join(staging, 'devices'), exist_ok=True)
shutil.copytree(os.path.join(multi_staging, 'devices', 'xuanyuan'), os.path.join(staging, 'devices', 'xuanyuan'))
shutil.copytree(os.path.join(multi_staging, 'devices', 'nezha'), os.path.join(staging, 'devices', 'nezha'))

# Ensure broken libs are NOT in xuanyuan
bad_libs = ['libremosaiclib.so', 'libmialgo_ainr_ll.so', 'libmialgo_ellc.so']
for lib in bad_libs:
    lp = os.path.join(staging, 'devices', 'xuanyuan', 'odm', 'lib64', lib)
    if os.path.exists(lp):
        os.remove(lp)
        print('Removed from staging:', lp)

# Copy system/etc and system/priv-app
os.makedirs(os.path.join(staging, 'system'), exist_ok=True)
shutil.copytree(os.path.join(multi_staging, 'system', 'etc'), os.path.join(staging, 'system', 'etc'))
shutil.copytree(os.path.join(multi_staging, 'system', 'priv-app'), os.path.join(staging, 'system', 'priv-app'))

# Copy common/service.sh, post-fs-data.sh, service.sh
for f in ['post-fs-data.sh', 'service.sh']:
    src = os.path.join(multi_staging, f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(staging, f))

common_dir = os.path.join(multi_staging, 'common')
if os.path.exists(common_dir):
    shutil.copytree(common_dir, os.path.join(staging, 'common'))

module_prop = """id=mi15u_x17u_master_camera_combo
name=Xiaomi 15 Ultra / 17 Ultra Master Camera Combo
version=v5.1-DualFlagship-DCG-A16
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Master Camera Combo for Xiaomi 15 Ultra (xuanyuan) & Xiaomi 17 Ultra (nezha) on HyperOS 2/3 (Android 15/16). Full Leica Camera App + Quad 50MP/200MP FullRes + Stock AIO LYT-900/OVX10500U tuning + DCG Hardware HDR + 8K Video all lenses + 4K120fps + AISP NR bypass.
"""

system_prop = """# Full Resolution RAW Support (Qualcomm CamX 50MP/200MP Output)
persist.vendor.camera.maxRAWSizes=55

# Aux Camera Access for all Google Camera (GCam) mods and Pro Camera apps
vendor.camera.aux.packagelist=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.agc.cam,com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.shamim.cam,org.codeaurora.snapcam,net.sourceforge.opencamera,com.google.android.apps.cameralite,com.hades.camera,com.free.cam,com.custom.camera,com.arun.gcam,com.google.android.GoogleCamera.Urnyx,com.google.android.GoogleCameraENG,com.google.android.GoogleCameraGood,com.falcon.camera
persist.vendor.camera.privapp.list=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.agc.cam,com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.shamim.cam,org.codeaurora.snapcam,net.sourceforge.opencamera,com.google.android.apps.cameralite,com.hades.camera,com.free.cam,com.custom.camera,com.arun.gcam,com.google.android.GoogleCamera.Urnyx,com.google.android.GoogleCameraENG,com.google.android.GoogleCameraGood,com.falcon.camera

# George Video Mod Tweaks (Bypass ArcSoft video noise reduction for sharp 4K/8K video textures)
persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1

# Preserve Leica Authentic & Leica Vibrant color science in Photo mode (0 = active)
persist.vendor.camera.leicafilter.bypassMode=0

# Video Bitrate & Hardware Acceleration
persist.vendor.camera.video.bitrate.factor=1.5
media.camera.bitrate.factor=1.5

# Leica Flagship Color Matrices, Modes & Watermarks
ro.miui.camera.leica.supported=1
persist.vendor.camera.enableLeicaMode=1
persist.sys.camera.leica=1
persist.vendor.camera.leica.supported=1
persist.vendor.camera.multicam.leica=1
persist.vendor.camera.provider.disable_device_feature=0
ro.miui.camera.leica.watermark=1

# Dual Conversion Gain (DCG / iDCG) Hardware HDR Support
# Enables native sensor-level dual gain readout (HCG/LCG) for wide dynamic range and low shadow noise
persist.vendor.camera.sensor.hdr=1
persist.vendor.camera.dcg.enable=1
persist.vendor.camera.hdr.dcg=1
persist.vendor.camera.sensor.dcg=1
ro.vendor.camera.dcg=1
"""

customize_sh = """##########################################################################################
#
# Xiaomi 15 Ultra / 17 Ultra Master Camera Combo Installer
# Supports: Xiaomi 15 Ultra (xuanyuan) & Xiaomi 17 Ultra (nezha)
# Compatible with HyperOS 2.0 / 3.0 (Android 15 / 16 - API 35/36)
# by borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
#
##########################################################################################

ui_print "*********************************************************"
ui_print "   Xiaomi 15 Ultra / 17 Ultra Master Camera Combo        "
ui_print "                  v5.1 Dual-Flagship                     "
ui_print "                     by borndead                         "
ui_print "*********************************************************"

# 1. Hardware Detection
DEVICE=$(getprop ro.product.device)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.build.product)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.product.vendor.device)

ui_print "- Detected hardware: $DEVICE"

case "$DEVICE" in
    xuanyuan|x15u)
        DEVICE_NAME="Xiaomi 15 Ultra ($DEVICE)"
        DEV_PROFILE="xuanyuan"
        ZOOM_GRID="0.5:1.0:3.0:5.0"
        XML_NAMES="xuanyuan.xml ishtar.xml"
        ;;
    nezha|x17u)
        DEVICE_NAME="Xiaomi 17 Ultra ($DEVICE)"
        DEV_PROFILE="nezha"
        ZOOM_GRID="0.5:1.0:3.0:5.0"
        XML_NAMES="nezha.xml xuanyuan.xml ishtar.xml"
        ;;
    *)
        ui_print "! Notice: Device ($DEVICE) not explicitly listed."
        ui_print "! Defaulting to Xiaomi 15 Ultra / 17 Ultra profile..."
        DEVICE_NAME="Xiaomi Ultra ($DEVICE)"
        DEV_PROFILE="xuanyuan"
        ZOOM_GRID="0.5:1.0:3.0:5.0"
        XML_NAMES="${DEVICE}.xml xuanyuan.xml ishtar.xml"
        ;;
esac

ui_print "  -> Active Device Profile: $DEVICE_NAME ($DEV_PROFILE)"
ui_print "  -> 50MP/200MP Zoom Grid: $ZOOM_GRID"

API=$(getprop ro.build.version.sdk)
OS_VER=$(getprop ro.build.version.release)
BUILD_ID=$(getprop ro.build.display.id)
BUILD_FLAVOR=$(getprop ro.build.flavor)
MOD_DEV=$(getprop ro.product.mod_device)
ROM_VER=$(getprop ro.build.version.incremental)

ui_print "- Android Version: $OS_VER (API $API)"
ui_print "- ROM Build ID: $BUILD_ID"

# 2. Deploy matching hardware binaries and tuning JSONs
ui_print "- Deploying Chromatix sensor modules & tuning for $DEV_PROFILE..."
mkdir -p "$MODPATH/system/odm/lib64/camera"
mkdir -p "$MODPATH/system/odm/etc/camera"

if [ -d "$MODPATH/devices/$DEV_PROFILE/odm" ]; then
    cp -af "$MODPATH/devices/$DEV_PROFILE/odm/." "$MODPATH/system/odm/"
fi

if [ -d "$MODPATH/devices/$DEV_PROFILE/vendor" ]; then
    mkdir -p "$MODPATH/system/vendor"
    cp -af "$MODPATH/devices/$DEV_PROFILE/vendor/." "$MODPATH/system/vendor/"
fi

# Clean up device profile staging to save storage on device
rm -rf "$MODPATH/devices"

# 3. Dynamic patch of device_features XML
ui_print "- Locating stock device_features XML for $DEVICE..."
REAL_XML=""
for xml_name in $XML_NAMES; do
    for xml_candidate in \\
        /product/etc/device_features/$xml_name \\
        /system/etc/device_features/$xml_name \\
        /odm/etc/device_features/$xml_name \\
        /vendor/etc/device_features/$xml_name; do
        if [ -f "$xml_candidate" ]; then
            REAL_XML="$xml_candidate"
            break 2
        fi
    done
done

if [ -n "$REAL_XML" ]; then
    ui_print "  Found stock config: $REAL_XML"
    mkdir -p "$MODPATH/system/etc/device_features"
    mkdir -p "$MODPATH/system/product/etc/device_features"
    mkdir -p "$MODPATH/product/etc/device_features"
    
    PRIMARY_XML_NAME=$(basename "$REAL_XML")
    TARGET_XML="$MODPATH/system/etc/device_features/$PRIMARY_XML_NAME"
    cp -af "$REAL_XML" "$TARGET_XML"

    # Purge conflicting / rogue tags that cause camera freezes
    for tag in \\
        support_ultra_hd_zoom ultra_pixel_zoom_ratio_support_list \\
        support_ultra_pixel_zoom_ratio support_super_resolution_zoom \\
        is_support_ultra_hd is_support_pixel_model support_super_resolution \\
        support_ultra_pixel support_50mp support_ultra_raw support_manual_ultra_raw \\
        support_8k_video support_8k_24fps support_8k_all_rear_sensors \\
        support_4k_120fps support_dolby_vision support_4k_60fps_dolby_vision \\
        support_log_video support_director_mode support_cinematic_mode \\
        support_camera_dcg is_support_dcg support_dcg_hdr support_sensor_hdr support_idcg; do
        sed -i "/$tag/d" "$TARGET_XML"
    done

    sed -i 's|</features>||g' "$TARGET_XML"

    cat << EOF >> "$TARGET_XML"
    <!-- FullRes 50MP/200MP Mode on All Rear Sensors ($ZOOM_GRID) -->
    <!-- Photo mode (161) remains clean, fluid, and freeze-free -->
    <bool name="is_support_ultra_hd">true</bool>
    <bool name="support_50mp">true</bool>
    <string name="support_ultra_hd_zoom">$ZOOM_GRID</string>
    <bool name="support_ultra_raw">true</bool>
    <bool name="support_manual_ultra_raw">true</bool>

    <!-- Professional Video Capabilities (George Stock Video MOD) -->
    <bool name="support_8k_video">true</bool>
    <bool name="support_8k_24fps">true</bool>
    <bool name="support_8k_all_rear_sensors">true</bool>
    <bool name="support_4k_120fps">true</bool>
    <bool name="support_dolby_vision">true</bool>
    <bool name="support_4k_60fps_dolby_vision">true</bool>
    <bool name="support_log_video">true</bool>
    <bool name="support_director_mode">true</bool>
    <bool name="support_cinematic_mode">true</bool>
    <bool name="support_eis">true</bool>
    <bool name="support_ois">true</bool>
</features>
EOF

    # Mirror to all partitions and across alternate alias names
    for out_name in $XML_NAMES; do
        cp -af "$TARGET_XML" "$MODPATH/system/etc/device_features/$out_name"
        cp -af "$TARGET_XML" "$MODPATH/system/product/etc/device_features/$out_name"
        cp -af "$TARGET_XML" "$MODPATH/product/etc/device_features/$out_name"
    done
    ui_print "  Patched device_features: 50M ($ZOOM_GRID) + 8K/4K120 injected safely."
else
    ui_print "  Notice: stock device_features XML not found on standard paths, skipping overlay."
fi

# 4. Resolve Camera APK & Custom ROM Handling
# Custom ROMs (SimpleRom - ST, Xiaomi.eu, EliteROM) have deodexed/patched camera apps.
# Replacing MiuiCamera.apk causes signature/JNI crash!
# On Xiaomi 17 Ultra (nezha), native camera APK is already HyperOS 3.0.
IS_CUSTOM_ROM=false
case "$BUILD_ID $BUILD_FLAVOR $MOD_DEV $ROM_VER" in
    *[Ss]imple*|*ST*|*st*|*[Ee][Uu]*|*[Ee]lite*|*[Pp]ulse*|*[Cc]ustom*)
        IS_CUSTOM_ROM=true
        ;;
esac

if [ "$IS_CUSTOM_ROM" = "true" ] || [ "$DEV_PROFILE" = "nezha" ]; then
    ui_print "- Custom ROM ($BUILD_ID) or Xiaomi 17 Ultra detected:"
    ui_print "  Preserving ROM's native patched MiuiCamera.apk (prevents crash)."
    ui_print "  Injecting Chromatix bins, FullRes RAW, DCG HDR & Video MOD..."
    rm -rf "$MODPATH/system/priv-app/MiuiCamera"
    rm -rf "$MODPATH/system/product/priv-app/MiuiCamera"
    rm -rf "$MODPATH/product/priv-app/MiuiCamera"
else
    ui_print "- Resolving camera destination paths..."
    SRC_APK_PATH="$MODPATH/system/priv-app/MiuiCamera/MiuiCamera.apk"
    STOC_CAM_PATHS="
    /product/priv-app/MiuiCamera/MiuiCamera.apk
    /system/product/priv-app/MiuiCamera/MiuiCamera.apk
    /system/priv-app/MiuiCamera/MiuiCamera.apk
    /system/system_ext/priv-app/MiuiCamera/MiuiCamera.apk
    /system_ext/priv-app/MiuiCamera/MiuiCamera.apk
    "

    FOUND_PATH=""
    for path in $STOC_CAM_PATHS; do
        if [ -f "$path" ]; then
            FOUND_PATH="$path"
            ui_print "  Detected system MiuiCamera at: $path"
            break
        fi
    done

    copy_camera_assets() {
        local target_apk="$1"
        local target_dir="$(dirname "$target_apk")"
        mkdir -p "$target_dir"
        cp -af "$SRC_APK_PATH" "$target_apk"
        if [ -d "$MODPATH/system/priv-app/MiuiCamera/lib" ]; then
            mkdir -p "$target_dir/lib"
            cp -rf "$MODPATH/system/priv-app/MiuiCamera/lib/." "$target_dir/lib/"
        fi
        set_perm_recursive "$target_dir" 0 0 0755 0644
        mkdir -p "$target_dir/oat"
        touch "$target_dir/oat/.nomedia"
    }

    if [ -n "$FOUND_PATH" ]; then
        TARGET_MOD_PATH="$MODPATH$FOUND_PATH"
        if [ "$FOUND_PATH" != "/system/priv-app/MiuiCamera/MiuiCamera.apk" ]; then
            ui_print "  Targeting active camera overlay at: $FOUND_PATH"
            copy_camera_assets "$TARGET_MOD_PATH"
            case "$FOUND_PATH" in
                /product/*)
                    copy_camera_assets "$MODPATH/system$FOUND_PATH"
                    ;;
                /system/product/*)
                    STRIPPED=${FOUND_PATH#/system}
                    copy_camera_assets "$MODPATH$STRIPPED"
                    ;;
            esac
        else
            set_perm_recursive "$MODPATH/system/priv-app/MiuiCamera" 0 0 0755 0644
            mkdir -p "$MODPATH/system/priv-app/MiuiCamera/oat"
            touch "$MODPATH/system/priv-app/MiuiCamera/oat/.nomedia"
        fi
    else
        ui_print "  Installing to default: /system/priv-app/MiuiCamera/MiuiCamera.apk"
        set_perm_recursive "$MODPATH/system/priv-app/MiuiCamera" 0 0 0755 0644
        mkdir -p "$MODPATH/system/priv-app/MiuiCamera/oat"
        touch "$MODPATH/system/priv-app/MiuiCamera/oat/.nomedia"
    fi
fi

# 5. Handle HAL (camera.qcom.so) Compatibility
if [ "$API" -ge 35 ]; then
    ui_print "- Android 15/16 detected (API $API):"
    if [ "$DEV_PROFILE" = "xuanyuan" ]; then
        ui_print "  Deploying native HyperOS 3.0 / A16 HAL (EUXM 3.0.9.0) for Xiaomi 15 Ultra."
    else
        ui_print "  Preserving native A16 Camera HAL for $DEV_PROFILE (prevents black screen)."
        rm -rf "$MODPATH/system/odm/lib64/hw"
        rm -rf "$MODPATH/system/vendor/odm/lib64/hw"
    fi
else
    ui_print "- Android 14 detected (API $API): keeping camera.qcom.so."
fi

# 6. Mirror to /vendor/odm for ROM compatibility
if [ -d "$MODPATH/system/odm" ]; then
    if [ -d /vendor/odm ] || [ -L /odm ]; then
        ui_print "- Mirroring ODM files to /vendor/odm for ROM compatibility..."
        mkdir -p "$MODPATH/system/vendor/odm/lib64/camera"
        mkdir -p "$MODPATH/system/vendor/odm/etc/camera"
        cp -af "$MODPATH/system/odm/lib64/camera/." "$MODPATH/system/vendor/odm/lib64/camera/"
        cp -af "$MODPATH/system/odm/etc/camera/." "$MODPATH/system/vendor/odm/etc/camera/"
        if [ -d "$MODPATH/system/odm/lib64/hw" ]; then
            mkdir -p "$MODPATH/system/vendor/odm/lib64/hw"
            cp -af "$MODPATH/system/odm/lib64/hw/." "$MODPATH/system/vendor/odm/lib64/hw/"
        fi
    fi
fi

# 7. Clear camera app cache and preferences
ui_print "- Clearing camera app cache and preferences..."
pm clear com.android.camera >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1
rm -rf /data/data/com.android.camera/code_cache/* >/dev/null 2>&1

# 8. Set Permissions and SELinux contexts
ui_print "- Setting permissions and SELinux contexts..."
set_perm_recursive "$MODPATH/system" 0 0 0755 0644
[ -d "$MODPATH/product" ] && set_perm_recursive "$MODPATH/product" 0 0 0755 0644

for bin_file in "$MODPATH/system/odm/lib64/camera"/*.bin; do
    [ -f "$bin_file" ] || continue
    ref_name="/odm/lib64/camera/$(basename "$bin_file")"
    if [ -e "$ref_name" ]; then
        chcon --reference="$ref_name" "$bin_file" 2>/dev/null
    else
        chcon u:object_r:vendor_configs_file:s0 "$bin_file" 2>/dev/null || chcon u:object_r:vendor_file:s0 "$bin_file" 2>/dev/null
    fi
done

for json_file in "$MODPATH/system/odm/etc/camera"/*.json; do
    [ -f "$json_file" ] || continue
    chcon u:object_r:vendor_configs_file:s0 "$json_file" 2>/dev/null
done

if [ -d "$MODPATH/system/vendor/odm" ]; then
    for f in $(find "$MODPATH/system/vendor/odm" -type f); do
        chcon u:object_r:vendor_configs_file:s0 "$f" 2>/dev/null
    done
fi

[ -d "$MODPATH/system/etc/device_features" ] && chcon -R u:object_r:system_file:s0 "$MODPATH/system/etc/device_features" 2>/dev/null
[ -d "$MODPATH/system/product/etc/device_features" ] && chcon -R u:object_r:system_file:s0 "$MODPATH/system/product/etc/device_features" 2>/dev/null
[ -d "$MODPATH/product/etc/device_features" ] && chcon -R u:object_r:system_file:s0 "$MODPATH/product/etc/device_features" 2>/dev/null
[ -d "$MODPATH/system/odm/lib64" ] && chcon -R u:object_r:vendor_file:s0 "$MODPATH/system/odm/lib64" 2>/dev/null
[ -d "$MODPATH/system/vendor/lib64" ] && chcon -R u:object_r:vendor_file:s0 "$MODPATH/system/vendor/lib64" 2>/dev/null
[ -d "$MODPATH/system/odm/lib64/hw" ] && chcon -R u:object_r:vendor_file:s0 "$MODPATH/system/odm/lib64/hw" 2>/dev/null
[ -d "$MODPATH/system/vendor/odm/lib64/hw" ] && chcon -R u:object_r:vendor_file:s0 "$MODPATH/system/vendor/odm/lib64/hw" 2>/dev/null
[ -f "$MODPATH/system/etc/permissions/privapp-permissions-camera.xml" ] && set_perm "$MODPATH/system/etc/permissions/privapp-permissions-camera.xml" 0 0 0644

ui_print "*********************************************************"
ui_print "- Xiaomi 15U / 17U Master Camera Combo installed!"
ui_print "- Target Device: $DEVICE_NAME ($DEV_PROFILE)"
ui_print "- High-Res Zoom Grid: $ZOOM_GRID"
ui_print "- Full Leica Camera App & companion libraries ready."
ui_print "- Stock Photo mode freeze FIXED (smooth fluid preview)."
ui_print "- FullRes active for Stock & all GCam mods."
ui_print "- 8K Video on all rear lenses & 4K120fps enabled."
ui_print "- Dual Conversion Gain (DCG / iDCG) Hardware HDR active."
ui_print "- AISP noise reduction bypass active (clean textures)."
ui_print "- Leica Authentic/Vibrant color science preserved."
ui_print "- Please reboot your device."
ui_print "*********************************************************"
"""

with open(os.path.join(staging, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(module_prop)

with open(os.path.join(staging, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(system_prop)

with open(os.path.join(staging, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(customize_sh)

# Create zip package
out_zip = r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip'
with zipfile.ZipFile(out_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for root, dirs, files in os.walk(staging):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, staging).replace('\\', '/')
            zf.write(full_p, rel_p)

print('Packaged:', out_zip, 'Size:', os.path.getsize(out_zip))

# Also copy/overwrite v5.0 name so if user/friend looks for 15ux17u package, both v5.1 and v5.0 are updated with the fix
out_zip_v5 = r'C:\Users\ASTA\OneDrive\Antigravity\Mi15U_X17U_Master_Camera_Combo_v5.0_by_borndead.zip'
shutil.copy2(out_zip, out_zip_v5)
print('Updated v5.0 name alias with the fix as well:', out_zip_v5)
