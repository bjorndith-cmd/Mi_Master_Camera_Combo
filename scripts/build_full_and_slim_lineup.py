import os
import shutil
import zipfile

print("=== Building Dual-Tier (FULL & SLIM) Module Lineup for All Devices ===")

root_antigravity = r'C:\Users\ASTA\OneDrive\Antigravity'
repo_releases = r'C:\Users\ASTA\OneDrive\Документы\GitHub\Mi_Master_Camera_Combo\releases'
os.makedirs(repo_releases, exist_ok=True)

multi_staging = os.path.join(root_antigravity, 'Mi_MultiDevice_Combo_Staging')
payload_staging = os.path.join(root_antigravity, 'Clean_Camera_Payload_Staging')

# -------------------------------------------------------------
# 1. PREPARE CLEAN CAMERA PAYLOAD (Purging broken/conflicting libs)
# -------------------------------------------------------------
if os.path.exists(payload_staging):
    shutil.rmtree(payload_staging)
os.makedirs(os.path.join(payload_staging, 'system', 'priv-app', 'MiuiCamera', 'lib', 'arm64'), exist_ok=True)
os.makedirs(os.path.join(payload_staging, 'system', 'etc', 'permissions'), exist_ok=True)

# Copy MiuiCamera.apk
src_apk = os.path.join(multi_staging, 'system', 'priv-app', 'MiuiCamera', 'MiuiCamera.apk')
shutil.copy2(src_apk, os.path.join(payload_staging, 'system', 'priv-app', 'MiuiCamera', 'MiuiCamera.apk'))

# Copy companion libraries excluding system overriding libs (libc++, libion, libdmabufheap)
src_libs = os.path.join(multi_staging, 'system', 'priv-app', 'MiuiCamera', 'lib', 'arm64')
bad_libs = {'libc++.so', 'libc++_shared.so', 'libion.so', 'libdmabufheap.so'}
for lib_name in os.listdir(src_libs):
    if lib_name not in bad_libs:
        shutil.copy2(
            os.path.join(src_libs, lib_name),
            os.path.join(payload_staging, 'system', 'priv-app', 'MiuiCamera', 'lib', 'arm64', lib_name)
        )

# Safe privapp-permissions-camera.xml (purged REBOOT, DEVICE_POWER, MANAGE_USERS)
safe_perm_xml = """<?xml version="1.0" encoding="utf-8"?>
<permissions>
    <privapp-permissions package="com.android.camera">
        <permission name="android.permission.WRITE_SECURE_SETTINGS" />
        <permission name="android.permission.REAL_GET_TASKS" />
        <permission name="android.permission.START_ACTIVITIES_FROM_BACKGROUND" />
        <permission name="android.permission.INTERACT_ACROSS_USERS" />
        <permission name="android.permission.MEDIA_CONTENT_CONTROL" />
        <permission name="android.permission.SYSTEM_CAMERA" />
        <permission name="android.permission.CAMERA_SEND_SYSTEM_EVENT" />
        <permission name="android.permission.CONTROL_DISPLAY_BRIGHTNESS" />
        <permission name="android.permission.STATUS_BAR" />
        <permission name="android.permission.UPDATE_APP_OPS_STATS" />
        <permission name="android.permission.PACKAGE_USAGE_STATS" />
        <permission name="android.permission.RECORD_AUDIO" />
        <permission name="android.permission.ACCESS_FINE_LOCATION" />
        <permission name="android.permission.CAMERA" />
        <permission name="android.permission.MODIFY_AUDIO_SETTINGS" />
        <permission name="android.permission.CAPTURE_AUDIO_OUTPUT" />
    </privapp-permissions>
</permissions>
"""
with open(os.path.join(payload_staging, 'system', 'etc', 'permissions', 'privapp-permissions-camera.xml'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(safe_perm_xml)
print(f"[OK] Clean Camera Payload ready in: {payload_staging}")

# Common safe post-fs-data.sh
common_post_fs_data = """#!/system/bin/sh
# post-fs-data.sh - Safe initialization without policy tampering
# Prevents Magisk Safe Mode and preserves root on all firmwares
MODDIR=${0%/*}
"""

# Common system.prop (Base)
common_system_prop = """# Full Resolution RAW Support (Qualcomm CamX 50MP/200MP Output)
persist.vendor.camera.maxRAWSizes=55

# Aux Camera Access for all Google Camera (GCam) mods and Pro Camera apps
vendor.camera.aux.packagelist=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.google.android.GoogleCamera.BigKaka,com.google.android.GoogleCamera.Urnyx,com.google.android.GoogleCameraENG,com.google.android.GoogleCameraGood,com.google.android.apps.cameralite,com.agc.cam,com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.agc.gcam96,org.codeaurora.snapcam,com.samsung.android.scan3d,com.samsung.android.ruler,com.ss.android.ugc.aweme,com.android.mgc,com.shamim.cam,net.sourceforge.opencamera,com.hades.camera,com.free.cam,com.custom.camera,com.arun.gcam,com.falcon.camera
persist.vendor.camera.privapp.list=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.google.android.GoogleCamera.BigKaka,com.google.android.GoogleCamera.Urnyx,com.google.android.GoogleCameraENG,com.google.android.GoogleCameraGood,com.google.android.apps.cameralite,com.agc.cam,com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.agc.gcam96,org.codeaurora.snapcam,com.samsung.android.scan3d,com.samsung.android.ruler,com.ss.android.ugc.aweme,com.android.mgc,com.shamim.cam,net.sourceforge.opencamera,com.hades.camera,com.free.cam,com.custom.camera,com.arun.gcam,com.falcon.camera

# George Video Mod Tweaks (Bypass ArcSoft video noise reduction for sharp 4K/8K textures)
persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1

# Video Bitrate & Hardware Acceleration
persist.vendor.camera.video.bitrate.factor=1.5
media.camera.bitrate.factor=1.5

# Dual Conversion Gain (DCG) Hardware HDR Activation
persist.vendor.camera.dcg.enable=1
persist.vendor.camera.hdr.dcg=1
persist.vendor.camera.sensor.hdr=1
ro.vendor.camera.dcg=1
persist.vendor.camera.sensor.idcg=1

# Leica Color Science & Offline Processing Fix
ro.miui.camera.leica.supported=1
persist.vendor.camera.enableLeicaMode=1
persist.sys.camera.leica=1
persist.vendor.camera.leica.supported=1
persist.vendor.camera.multicam.leica=1
persist.vendor.camera.provider.disable_device_feature=0
ro.miui.camera.leica.watermark=1
persist.vendor.camera.cloud.enable=0
persist.sys.camera.leica_essential.cloud=0
"""

def create_zip(staging_dir, zip_path):
    print(f"Creating: {os.path.basename(zip_path)}...")
    with zipfile.ZipFile(zip_path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for root, dirs, files in os.walk(staging_dir):
            for file in files:
                full_p = os.path.join(root, file)
                rel_p = os.path.relpath(full_p, staging_dir).replace('\\', '/')
                zf.write(full_p, rel_p)
    sz = os.path.getsize(zip_path)
    print(f"  -> Generated: {sz:,} bytes")
    # Mirror to repo releases
    repo_copy = os.path.join(repo_releases, os.path.basename(zip_path))
    shutil.copy2(zip_path, repo_copy)

# -------------------------------------------------------------
# 2. BUILD UNIVERSAL FULL & UNIVERSAL SLIM
# -------------------------------------------------------------
uni_full_staging = os.path.join(root_antigravity, 'Universal_Full_Staging')
uni_slim_staging = os.path.join(root_antigravity, 'Universal_Slim_Staging')

for stg in [uni_full_staging, uni_slim_staging]:
    if os.path.exists(stg):
        shutil.rmtree(stg)
    os.makedirs(stg, exist_ok=True)
    # Copy META-INF
    shutil.copytree(os.path.join(multi_staging, 'META-INF'), os.path.join(stg, 'META-INF'))
    # Copy devices/ directory tree
    shutil.copytree(os.path.join(multi_staging, 'devices'), os.path.join(stg, 'devices'))
    # Copy scripts
    with open(os.path.join(stg, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_post_fs_data)
    with open(os.path.join(stg, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write("#!/system/bin/sh\n")
    with open(os.path.join(stg, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_system_prop)

# Add clean camera payload to Universal FULL
shutil.copytree(os.path.join(payload_staging, 'system'), os.path.join(uni_full_staging, 'system'))

# Module prop for Universal FULL
with open(os.path.join(uni_full_staging, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi_master_camera_combo_universal_full
name=Xiaomi Master Camera Combo (Universal FULL Edition)
version=v5.8-Universal-FULL-A16
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Universal Full Flagship Camera Suite for Xiaomi 13U, 14U, 15, 15 Pro, 15U & 17U on HyperOS 1/2/3 (Android 14/15/16). Full Leica Camera APK + oat/.replace protection + Quad-50M/200M FullRes + Variable Aperture + Stock AIO 104 LYT-900 tuning + DCG Hardware HDR + George 8K video on all lenses + 4K120fps + offline processing.
""")

# Module prop for Universal SLIM
with open(os.path.join(uni_slim_staging, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi_master_camera_combo_universal_slim
name=Xiaomi Master Camera Combo (Universal SLIM Edition)
version=v5.8-Universal-SLIM-A16
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Universal Pure Systemless Overlay for Xiaomi 13U, 14U, 15, 15 Pro, 15U & 17U on HyperOS 1/2/3. Zero Camera APK replacement (100% immune to signature mismatch bootloops!). Quad-50M/200M FullRes + Variable Aperture + Stock AIO 104 LYT-900 tuning + DCG Hardware HDR + George 8K all lenses + 4K120fps + Chromatix hardware sensor bins.
""")

# customize.sh for Universal FULL (Includes APK copy with oat/.replace)
uni_full_cust = """##########################################################################################
# Universal Multi-Device Master Camera Combo (FULL Edition with Leica Camera App)
# Fully compatible with HyperOS 2.0 / 3.0 (Android 15 / 16)
##########################################################################################

ui_print "*********************************************************"
ui_print "       Xiaomi Master Camera Combo (FULL Edition)         "
ui_print "   Leica Camera App + Quad-50M/200M + DCG HDR + 8K       "
ui_print "                     by borndead                         "
ui_print "*********************************************************"

DEVICE=$(getprop ro.product.device)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.build.product)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.product.vendor.device)
API=$(getprop ro.build.version.sdk)
[ -z "$API" ] && API=35
OS_VER=$(getprop ro.build.version.release)

case "$DEVICE" in
    ishtar)
        DEVICE_NAME="Xiaomi 13 Ultra"
        DEV_PROFILE="ishtar"
        ZOOM_GRID="0.5:1.0:3.2:5.0"
        XML_NAMES="ishtar.xml"
        ;;
    aurora)
        DEVICE_NAME="Xiaomi 14 Ultra"
        DEV_PROFILE="aurora"
        ZOOM_GRID="0.5:1.0:3.2:5.0"
        XML_NAMES="aurora.xml ishtar.xml"
        ;;
    dada)
        DEVICE_NAME="Xiaomi 15"
        DEV_PROFILE="dada"
        ZOOM_GRID="1.0"
        XML_NAMES="dada.xml ishtar.xml"
        ;;
    haotian)
        DEVICE_NAME="Xiaomi 15 Pro"
        DEV_PROFILE="dada"
        ZOOM_GRID="0.6:1.0:3.2:5.0"
        XML_NAMES="haotian.xml dada.xml ishtar.xml"
        ;;
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
        ui_print "! Unlisted device ($DEVICE). Applying flagship fallback profile..."
        DEVICE_NAME="Xiaomi Flagship ($DEVICE)"
        DEV_PROFILE="ishtar"
        ZOOM_GRID="0.5:1.0:3.2:5.0"
        XML_NAMES="${DEVICE}.xml ishtar.xml"
        ;;
esac

ui_print "- Target: $DEVICE_NAME ($DEV_PROFILE)"
ui_print "- Android: $OS_VER (API $API)"

# 1. Deploy matching hardware binaries
ui_print "- Deploying Chromatix sensor modules for $DEV_PROFILE..."
mkdir -p "$MODPATH/system/odm/lib64/camera"
mkdir -p "$MODPATH/system/odm/etc/camera"
[ -d "$MODPATH/devices/$DEV_PROFILE/odm" ] && cp -af "$MODPATH/devices/$DEV_PROFILE/odm/." "$MODPATH/system/odm/"
[ -d "$MODPATH/devices/$DEV_PROFILE/vendor" ] && mkdir -p "$MODPATH/system/vendor" && cp -af "$MODPATH/devices/$DEV_PROFILE/vendor/." "$MODPATH/system/vendor/"
rm -rf "$MODPATH/devices"

# 2. Dynamic patch of device_features XML
ui_print "- Patching device_features for $DEVICE..."
REAL_XML=""
for xml_name in $XML_NAMES; do
    for xml_cand in /product/etc/device_features/$xml_name /system/etc/device_features/$xml_name /odm/etc/device_features/$xml_name /vendor/etc/device_features/$xml_name; do
        if [ -f "$xml_cand" ]; then
            REAL_XML="$xml_cand"
            break 2
        fi
    done
done

if [ -n "$REAL_XML" ]; then
    mkdir -p "$MODPATH/system/etc/device_features"
    TARGET_XML="$MODPATH/system/etc/device_features/$(basename "$REAL_XML")"
    cp -af "$REAL_XML" "$TARGET_XML"

    for tag in \\
        support_ultra_hd_zoom ultra_pixel_zoom_ratio_support_list \\
        support_ultra_pixel_zoom_ratio support_super_resolution_zoom \\
        is_support_ultra_hd is_support_pixel_model support_super_resolution \\
        support_ultra_pixel support_50mp support_ultra_raw support_manual_ultra_raw \\
        support_camera_manual_aperture support_variable_aperture support_stepless_aperture \\
        support_8k_video support_8k_24fps support_8k_all_rear_sensors \\
        support_4k_120fps support_dolby_vision support_4k_60fps_dolby_vision \\
        support_log_video support_director_mode support_cinematic_mode \\
        support_camera_dcg is_support_dcg support_dcg_hdr support_sensor_hdr support_idcg \\
        support_cloud_process support_cloud_ai_process support_ultra_raw_cloud \\
        is_support_cloud_process support_cloud_photo_enhance support_ai_cloud \\
        support_cloud_sr support_cloud_super_resolution support_leica_essential_cloud \\
        support_leica_cloud support_aisp_cloud is_support_ultra_raw_cloud \\
        support_gallery_cloud_process; do
        sed -i "/$tag/d" "$TARGET_XML"
    done

    sed -i 's|</features>||g' "$TARGET_XML"

    cat << EOF >> "$TARGET_XML"
    <!-- Offline Processing Bypass (No Pink Noise / Cloud Delays) -->
    <bool name="support_cloud_process">false</bool>
    <bool name="support_cloud_ai_process">false</bool>
    <bool name="support_ultra_raw_cloud">false</bool>
    <bool name="is_support_cloud_process">false</bool>
    <bool name="support_cloud_photo_enhance">false</bool>
    <bool name="support_ai_cloud">false</bool>
    <bool name="support_cloud_sr">false</bool>
    <bool name="support_cloud_super_resolution">false</bool>
    <bool name="support_leica_essential_cloud">false</bool>
    <bool name="support_leica_cloud">false</bool>
    <bool name="support_aisp_cloud">false</bool>
    <bool name="is_support_ultra_raw_cloud">false</bool>
    <bool name="support_gallery_cloud_process">false</bool>

    <!-- FullRes 50MP/200MP Mode ($ZOOM_GRID) -->
    <bool name="is_support_ultra_hd">true</bool>
    <bool name="support_50mp">true</bool>
    <string name="support_ultra_hd_zoom">$ZOOM_GRID</string>
    <bool name="support_ultra_raw">true</bool>
    <bool name="support_manual_ultra_raw">true</bool>

    <!-- Variable Physical Aperture (F1.63 - F4.0) -->
    <bool name="support_camera_manual_aperture">true</bool>
    <bool name="support_variable_aperture">true</bool>
    <bool name="support_stepless_aperture">true</bool>

    <!-- Professional Video Capabilities -->
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

    <!-- Dual Conversion Gain (DCG) Hardware HDR -->
    <bool name="support_camera_dcg">true</bool>
    <bool name="is_support_dcg">true</bool>
    <bool name="support_dcg_hdr">true</bool>
    <bool name="support_sensor_hdr">true</bool>
    <bool name="support_idcg">true</bool>
</features>
EOF
    for out_name in $XML_NAMES; do
        cp -af "$TARGET_XML" "$MODPATH/system/etc/device_features/$out_name"
        mkdir -p "$MODPATH/system/product/etc/device_features"
        mkdir -p "$MODPATH/product/etc/device_features"
        cp -af "$TARGET_XML" "$MODPATH/system/product/etc/device_features/$out_name"
        cp -af "$TARGET_XML" "$MODPATH/product/etc/device_features/$out_name"
    done
fi

# 3. Full Leica Camera APK Deployment with oat/.replace protection
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
    # Anti-Bootloop: Hide system odex so ART doesn't checksum-fail
    mkdir -p "$target_dir/oat"
    touch "$target_dir/oat/.replace"
    touch "$target_dir/oat/.nomedia"
    touch "$target_dir/.replace"
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
        touch "$MODPATH/system/priv-app/MiuiCamera/oat/.replace"
        touch "$MODPATH/system/priv-app/MiuiCamera/oat/.nomedia"
        touch "$MODPATH/system/priv-app/MiuiCamera/.replace"
    fi
else
    set_perm_recursive "$MODPATH/system/priv-app/MiuiCamera" 0 0 0755 0644
    mkdir -p "$MODPATH/system/priv-app/MiuiCamera/oat"
    touch "$MODPATH/system/priv-app/MiuiCamera/oat/.replace"
    touch "$MODPATH/system/priv-app/MiuiCamera/oat/.nomedia"
fi

# 4. Mirror to /vendor/odm for ROM compatibility
if [ -d "$MODPATH/system/odm" ]; then
    if [ -d /vendor/odm ] || [ -L /odm ]; then
        mkdir -p "$MODPATH/system/vendor/odm/lib64/camera"
        mkdir -p "$MODPATH/system/vendor/odm/etc/camera"
        cp -af "$MODPATH/system/odm/lib64/camera/." "$MODPATH/system/vendor/odm/lib64/camera/"
        cp -af "$MODPATH/system/odm/etc/camera/." "$MODPATH/system/vendor/odm/etc/camera/"
    fi
fi

# 5. Purge stale dalvik-cache and camera app cache
ui_print "- Purging camera cache & dalvik state..."
rm -rf /data/dalvik-cache/*/*com.android.camera* >/dev/null 2>&1
rm -rf /data/system/package_cache/* >/dev/null 2>&1
pm clear com.android.camera >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1
rm -rf /data/data/com.android.camera/code_cache/* >/dev/null 2>&1
if [ -d /data/app ]; then
    rm -rf /data/app/~~*com.android.camera* >/dev/null 2>&1
    rm -rf /data/app/*com.android.camera* >/dev/null 2>&1
fi

# 6. Permissions and SELinux
set_perm_recursive "$MODPATH/system" 0 0 0755 0644
[ -d "$MODPATH/product" ] && set_perm_recursive "$MODPATH/product" 0 0 0755 0644
[ -f "$MODPATH/system/etc/permissions/privapp-permissions-camera.xml" ] && set_perm "$MODPATH/system/etc/permissions/privapp-permissions-camera.xml" 0 0 0644

ui_print "*********************************************************"
ui_print "- FULL Edition installed successfully!"
ui_print "- Full Leica Camera App ready with oat/.replace protection."
ui_print "- 50MP/200MP FullRes, George 8K Video & DCG HDR active."
ui_print "- Please reboot your device."
ui_print "*********************************************************"
"""
with open(os.path.join(uni_full_staging, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(uni_full_cust)

# customize.sh for Universal SLIM (NO APK)
uni_slim_cust = """##########################################################################################
# Universal Multi-Device Master Camera Combo (SLIM Edition - Pure Systemless Overlay)
# Zero Camera APK replacement - 100% immune to signature mismatch bootloops!
# Fully compatible with HyperOS 1.0, 2.0 & 3.0 (Android 14, 15 & 16)
##########################################################################################

ui_print "*********************************************************"
ui_print "       Xiaomi Master Camera Combo (SLIM Edition)         "
ui_print "   Pure Systemless Overlay (100% Anti-Bootloop Safe)     "
ui_print "   Quad-50M/200M + DCG HDR + 8K Video + Chromatix        "
ui_print "                     by borndead                         "
ui_print "*********************************************************"

DEVICE=$(getprop ro.product.device)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.build.product)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.product.vendor.device)
API=$(getprop ro.build.version.sdk)
[ -z "$API" ] && API=35
OS_VER=$(getprop ro.build.version.release)

case "$DEVICE" in
    ishtar)
        DEVICE_NAME="Xiaomi 13 Ultra"
        DEV_PROFILE="ishtar"
        ZOOM_GRID="0.5:1.0:3.2:5.0"
        XML_NAMES="ishtar.xml"
        ;;
    aurora)
        DEVICE_NAME="Xiaomi 14 Ultra"
        DEV_PROFILE="aurora"
        ZOOM_GRID="0.5:1.0:3.2:5.0"
        XML_NAMES="aurora.xml ishtar.xml"
        ;;
    dada)
        DEVICE_NAME="Xiaomi 15"
        DEV_PROFILE="dada"
        ZOOM_GRID="1.0"
        XML_NAMES="dada.xml ishtar.xml"
        ;;
    haotian)
        DEVICE_NAME="Xiaomi 15 Pro"
        DEV_PROFILE="dada"
        ZOOM_GRID="0.6:1.0:3.2:5.0"
        XML_NAMES="haotian.xml dada.xml ishtar.xml"
        ;;
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
        ui_print "! Unlisted device ($DEVICE). Applying flagship fallback profile..."
        DEVICE_NAME="Xiaomi Flagship ($DEVICE)"
        DEV_PROFILE="ishtar"
        ZOOM_GRID="0.5:1.0:3.2:5.0"
        XML_NAMES="${DEVICE}.xml ishtar.xml"
        ;;
esac

ui_print "- Target: $DEVICE_NAME ($DEV_PROFILE)"
ui_print "- Android: $OS_VER (API $API)"

# 1. Deploy matching hardware binaries
ui_print "- Deploying Chromatix sensor modules for $DEV_PROFILE..."
mkdir -p "$MODPATH/system/odm/lib64/camera"
mkdir -p "$MODPATH/system/odm/etc/camera"
[ -d "$MODPATH/devices/$DEV_PROFILE/odm" ] && cp -af "$MODPATH/devices/$DEV_PROFILE/odm/." "$MODPATH/system/odm/"
[ -d "$MODPATH/devices/$DEV_PROFILE/vendor" ] && mkdir -p "$MODPATH/system/vendor" && cp -af "$MODPATH/devices/$DEV_PROFILE/vendor/." "$MODPATH/system/vendor/"
rm -rf "$MODPATH/devices"

# 2. Dynamic patch of device_features XML
ui_print "- Patching device_features for $DEVICE..."
REAL_XML=""
for xml_name in $XML_NAMES; do
    for xml_cand in /product/etc/device_features/$xml_name /system/etc/device_features/$xml_name /odm/etc/device_features/$xml_name /vendor/etc/device_features/$xml_name; do
        if [ -f "$xml_cand" ]; then
            REAL_XML="$xml_cand"
            break 2
        fi
    done
done

if [ -n "$REAL_XML" ]; then
    mkdir -p "$MODPATH/system/etc/device_features"
    TARGET_XML="$MODPATH/system/etc/device_features/$(basename "$REAL_XML")"
    cp -af "$REAL_XML" "$TARGET_XML"

    for tag in \\
        support_ultra_hd_zoom ultra_pixel_zoom_ratio_support_list \\
        support_ultra_pixel_zoom_ratio support_super_resolution_zoom \\
        is_support_ultra_hd is_support_pixel_model support_super_resolution \\
        support_ultra_pixel support_50mp support_ultra_raw support_manual_ultra_raw \\
        support_camera_manual_aperture support_variable_aperture support_stepless_aperture \\
        support_8k_video support_8k_24fps support_8k_all_rear_sensors \\
        support_4k_120fps support_dolby_vision support_4k_60fps_dolby_vision \\
        support_log_video support_director_mode support_cinematic_mode \\
        support_camera_dcg is_support_dcg support_dcg_hdr support_sensor_hdr support_idcg \\
        support_cloud_process support_cloud_ai_process support_ultra_raw_cloud \\
        is_support_cloud_process support_cloud_photo_enhance support_ai_cloud \\
        support_cloud_sr support_cloud_super_resolution support_leica_essential_cloud \\
        support_leica_cloud support_aisp_cloud is_support_ultra_raw_cloud \\
        support_gallery_cloud_process; do
        sed -i "/$tag/d" "$TARGET_XML"
    done

    sed -i 's|</features>||g' "$TARGET_XML"

    cat << EOF >> "$TARGET_XML"
    <!-- Offline Processing Bypass (No Pink Noise / Cloud Delays) -->
    <bool name="support_cloud_process">false</bool>
    <bool name="support_cloud_ai_process">false</bool>
    <bool name="support_ultra_raw_cloud">false</bool>
    <bool name="is_support_cloud_process">false</bool>
    <bool name="support_cloud_photo_enhance">false</bool>
    <bool name="support_ai_cloud">false</bool>
    <bool name="support_cloud_sr">false</bool>
    <bool name="support_cloud_super_resolution">false</bool>
    <bool name="support_leica_essential_cloud">false</bool>
    <bool name="support_leica_cloud">false</bool>
    <bool name="support_aisp_cloud">false</bool>
    <bool name="is_support_ultra_raw_cloud">false</bool>
    <bool name="support_gallery_cloud_process">false</bool>

    <!-- FullRes 50MP/200MP Mode ($ZOOM_GRID) -->
    <bool name="is_support_ultra_hd">true</bool>
    <bool name="support_50mp">true</bool>
    <string name="support_ultra_hd_zoom">$ZOOM_GRID</string>
    <bool name="support_ultra_raw">true</bool>
    <bool name="support_manual_ultra_raw">true</bool>

    <!-- Variable Physical Aperture (F1.63 - F4.0) -->
    <bool name="support_camera_manual_aperture">true</bool>
    <bool name="support_variable_aperture">true</bool>
    <bool name="support_stepless_aperture">true</bool>

    <!-- Professional Video Capabilities -->
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

    <!-- Dual Conversion Gain (DCG) Hardware HDR -->
    <bool name="support_camera_dcg">true</bool>
    <bool name="is_support_dcg">true</bool>
    <bool name="support_dcg_hdr">true</bool>
    <bool name="support_sensor_hdr">true</bool>
    <bool name="support_idcg">true</bool>
</features>
EOF
    for out_name in $XML_NAMES; do
        cp -af "$TARGET_XML" "$MODPATH/system/etc/device_features/$out_name"
        mkdir -p "$MODPATH/system/product/etc/device_features"
        mkdir -p "$MODPATH/product/etc/device_features"
        cp -af "$TARGET_XML" "$MODPATH/system/product/etc/device_features/$out_name"
        cp -af "$TARGET_XML" "$MODPATH/product/etc/device_features/$out_name"
    done
fi

# 3. Pure Systemless Overlay Notice
ui_print "- SLIM Pure Systemless Overlay active."
ui_print "  ROM native Camera APK is preserved untouched."
ui_print "  100% immune to signature mismatch and odex bootloops."

# 4. Mirror to /vendor/odm for ROM compatibility
if [ -d "$MODPATH/system/odm" ]; then
    if [ -d /vendor/odm ] || [ -L /odm ]; then
        mkdir -p "$MODPATH/system/vendor/odm/lib64/camera"
        mkdir -p "$MODPATH/system/vendor/odm/etc/camera"
        cp -af "$MODPATH/system/odm/lib64/camera/." "$MODPATH/system/vendor/odm/lib64/camera/"
        cp -af "$MODPATH/system/odm/etc/camera/." "$MODPATH/system/vendor/odm/etc/camera/"
    fi
fi

# 5. Clear camera app cache
ui_print "- Clearing camera app cache..."
pm clear com.android.camera >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1
rm -rf /data/data/com.android.camera/code_cache/* >/dev/null 2>&1

# 6. Permissions and SELinux
set_perm_recursive "$MODPATH/system" 0 0 0755 0644
[ -d "$MODPATH/product" ] && set_perm_recursive "$MODPATH/product" 0 0 0755 0644

ui_print "*********************************************************"
ui_print "- SLIM Edition installed successfully!"
ui_print "- Pure Systemless Overlay ready (Zero APK modified)."
ui_print "- 50MP/200MP FullRes, George 8K Video & DCG HDR active."
ui_print "- Please reboot your device."
ui_print "*********************************************************"
"""
with open(os.path.join(uni_slim_staging, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(uni_slim_cust)

# Package Universal FULL
uni_full_zip = os.path.join(root_antigravity, 'Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip')
create_zip(uni_full_staging, uni_full_zip)
# Mirror for backward compatibility
legacy_uni = os.path.join(root_antigravity, 'Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip')
shutil.copy2(uni_full_zip, legacy_uni)
shutil.copy2(uni_full_zip, os.path.join(repo_releases, os.path.basename(legacy_uni)))

# Package Universal SLIM
uni_slim_zip = os.path.join(root_antigravity, 'Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip')
create_zip(uni_slim_staging, uni_slim_zip)

# -------------------------------------------------------------
# 3. BUILD DEDICATED FULL & SLIM FOR XIAOMI 13 ULTRA (ishtar)
# -------------------------------------------------------------
ishtar_full_stg = os.path.join(root_antigravity, 'Mi13U_Full_Staging')
ishtar_slim_stg = os.path.join(root_antigravity, 'Mi13U_Slim_Staging')

for stg in [ishtar_full_stg, ishtar_slim_stg]:
    if os.path.exists(stg):
        shutil.rmtree(stg)
    os.makedirs(stg, exist_ok=True)
    shutil.copytree(os.path.join(multi_staging, 'META-INF'), os.path.join(stg, 'META-INF'))
    with open(os.path.join(stg, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_post_fs_data)
    with open(os.path.join(stg, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write("#!/system/bin/sh\n")
    with open(os.path.join(stg, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_system_prop)
    # Copy ishtar sensor bins and aisp.json to system/odm
    os.makedirs(os.path.join(stg, 'system', 'odm', 'lib64', 'camera'), exist_ok=True)
    os.makedirs(os.path.join(stg, 'system', 'odm', 'etc', 'camera'), exist_ok=True)
    ishtar_bins = os.path.join(multi_staging, 'devices', 'ishtar', 'odm', 'lib64', 'camera')
    for b in os.listdir(ishtar_bins):
        if b.endswith('.bin'):
            shutil.copy2(os.path.join(ishtar_bins, b), os.path.join(stg, 'system', 'odm', 'lib64', 'camera', b))
    shutil.copy2(
        os.path.join(multi_staging, 'devices', 'ishtar', 'odm', 'etc', 'camera', 'aisp.json'),
        os.path.join(stg, 'system', 'odm', 'etc', 'camera', 'aisp.json')
    )

# Add Clean Camera Payload to 13U FULL
shutil.copytree(os.path.join(payload_staging, 'system', 'priv-app'), os.path.join(ishtar_full_stg, 'system', 'priv-app'))
shutil.copytree(os.path.join(payload_staging, 'system', 'etc', 'permissions'), os.path.join(ishtar_full_stg, 'system', 'etc', 'permissions'))

# Props
with open(os.path.join(ishtar_full_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi13u_master_camera_combo_full
name=Xiaomi 13 Ultra Master Camera Combo (FULL Edition)
version=v5.2-Full-AntiBootloop
versionCode=20260926
author=borndead (feat. amitkattal & GeorgeKiarie)
description=Dedicated FULL Leica Camera Suite for Xiaomi 13 Ultra (ishtar) on HyperOS 2/3 (Android 15/16). Full Leica Camera App + oat/.replace protection + Quad-50MP FullRes (0.5x, 1x, 3.2x, 5x) + DCG Hardware HDR + George 8K Video all lenses + 4K120fps + Chromatix IMX989/IMX858 hardware calibration bins.
""")

with open(os.path.join(ishtar_slim_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi13u_master_imaging_mod_slim
name=Xiaomi 13 Ultra Master Camera Combo (SLIM Edition)
version=v5.2-Slim-AntiBootloop
versionCode=20260926
author=borndead (feat. amitkattal & GeorgeKiarie)
description=Dedicated Pure Systemless Overlay for Xiaomi 13 Ultra (ishtar) on HyperOS 1/2/3. Zero Camera APK replacement (100% immune to signature mismatch bootloops on official Taiwan/Global ROMs!). Quad-50MP FullRes (0.5x, 1x, 3.2x, 5x) + DCG Hardware HDR + George 8K Video all lenses + 4K120fps + Chromatix IMX989/IMX858.
""")

# Build 13U FULL customize.sh
ishtar_full_cust = uni_full_cust.replace("Xiaomi Master Camera Combo (FULL Edition)", "Xiaomi 13 Ultra Master Camera Combo (FULL Edition)")
with open(os.path.join(ishtar_full_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(ishtar_full_cust)

# Build 13U SLIM customize.sh
ishtar_slim_cust = uni_slim_cust.replace("Xiaomi Master Camera Combo (SLIM Edition)", "Xiaomi 13 Ultra Master Camera Combo (SLIM Edition)")
with open(os.path.join(ishtar_slim_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(ishtar_slim_cust)

# Package 13U FULL
ishtar_full_zip = os.path.join(root_antigravity, 'Mi13U_Master_Camera_Combo_Full_by_borndead.zip')
create_zip(ishtar_full_stg, ishtar_full_zip)
# Mirror to v5.1 legacy
legacy_13u_v51 = os.path.join(root_antigravity, 'Mi13U_Master_Camera_Combo_v5.1_by_borndead.zip')
shutil.copy2(ishtar_full_zip, legacy_13u_v51)
shutil.copy2(ishtar_full_zip, os.path.join(repo_releases, os.path.basename(legacy_13u_v51)))

# Package 13U SLIM
ishtar_slim_zip = os.path.join(root_antigravity, 'Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip')
create_zip(ishtar_slim_stg, ishtar_slim_zip)
# Mirror to v1.0 slim legacy
legacy_13u_slim = os.path.join(root_antigravity, 'Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip')
shutil.copy2(ishtar_slim_zip, legacy_13u_slim)
shutil.copy2(ishtar_slim_zip, os.path.join(repo_releases, os.path.basename(legacy_13u_slim)))

# -------------------------------------------------------------
# 4. BUILD DEDICATED FULL & SLIM FOR XIAOMI 17 ULTRA (nezha)
# -------------------------------------------------------------
x17u_full_stg = os.path.join(root_antigravity, 'X17U_Full_Staging')
x17u_slim_stg = os.path.join(root_antigravity, 'X17U_Slim_Staging_New')

for stg in [x17u_full_stg, x17u_slim_stg]:
    if os.path.exists(stg):
        shutil.rmtree(stg)
    os.makedirs(stg, exist_ok=True)
    shutil.copytree(os.path.join(multi_staging, 'META-INF'), os.path.join(stg, 'META-INF'))
    with open(os.path.join(stg, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_post_fs_data)
    with open(os.path.join(stg, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write("#!/system/bin/sh\n")
    with open(os.path.join(stg, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_system_prop)
    # Copy nezha assets
    shutil.copytree(os.path.join(multi_staging, 'devices', 'nezha', 'odm'), os.path.join(stg, 'system', 'odm'))
    shutil.copytree(os.path.join(multi_staging, 'devices', 'nezha', 'vendor'), os.path.join(stg, 'system', 'vendor'))

shutil.copytree(os.path.join(payload_staging, 'system', 'priv-app'), os.path.join(x17u_full_stg, 'system', 'priv-app'))
shutil.copytree(os.path.join(payload_staging, 'system', 'etc', 'permissions'), os.path.join(x17u_full_stg, 'system', 'etc', 'permissions'))

with open(os.path.join(x17u_full_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=x17u_master_camera_combo_full
name=Xiaomi 17 Ultra Master Camera Combo (FULL Edition)
version=v5.2-Full-Nezha
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Dedicated FULL Leica Camera Suite for Xiaomi 17 Ultra (nezha) on HyperOS 3.0. Full Leica Camera APK + oat/.replace protection + genuine OVX10500U/HP9/JN5 Chromatix bins + DCG Hardware HDR + 8K video on all lenses + 4K120fps + Qualcomm libqcodec2_v4l2codec.so.
""")

with open(os.path.join(x17u_slim_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=x17u_master_imaging_mod_slim
name=Xiaomi 17 Ultra Master Camera Combo (SLIM Edition)
version=v1.1-Slim-Nezha
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Dedicated Pure Systemless Overlay for Xiaomi 17 Ultra (nezha) on HyperOS 3.0. Zero Camera APK replacement (100% immune to crashes on SimpleRom ST, EU, Elite!). OVX10500U/HP9/JN5 Chromatix bins + DCG Hardware HDR + 8K video all lenses + 4K120fps + Qualcomm libqcodec2_v4l2codec.so.
""")

x17u_full_cust = uni_full_cust.replace("Xiaomi Master Camera Combo (FULL Edition)", "Xiaomi 17 Ultra Master Camera Combo (FULL Edition)")
with open(os.path.join(x17u_full_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(x17u_full_cust)

x17u_slim_cust = uni_slim_cust.replace("Xiaomi Master Camera Combo (SLIM Edition)", "Xiaomi 17 Ultra Master Camera Combo (SLIM Edition)")
with open(os.path.join(x17u_slim_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(x17u_slim_cust)

x17u_full_zip = os.path.join(root_antigravity, 'X17U_Master_Camera_Combo_Full_by_borndead.zip')
create_zip(x17u_full_stg, x17u_full_zip)

x17u_slim_zip = os.path.join(root_antigravity, 'X17U_Master_Imaging_MOD_Slim_by_borndead.zip')
create_zip(x17u_slim_stg, x17u_slim_zip)
# Mirror to v1.0 slim legacy
legacy_17u_slim = os.path.join(root_antigravity, 'X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip')
shutil.copy2(x17u_slim_zip, legacy_17u_slim)
shutil.copy2(x17u_slim_zip, os.path.join(repo_releases, os.path.basename(legacy_17u_slim)))

# -------------------------------------------------------------
# 5. BUILD DEDICATED FULL & SLIM FOR XIAOMI 15 ULTRA (xuanyuan)
# -------------------------------------------------------------
x15u_full_stg = os.path.join(root_antigravity, 'Mi15U_Full_Staging')
x15u_slim_stg = os.path.join(root_antigravity, 'Mi15U_Slim_Staging')

for stg in [x15u_full_stg, x15u_slim_stg]:
    if os.path.exists(stg):
        shutil.rmtree(stg)
    os.makedirs(stg, exist_ok=True)
    shutil.copytree(os.path.join(multi_staging, 'META-INF'), os.path.join(stg, 'META-INF'))
    with open(os.path.join(stg, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_post_fs_data)
    with open(os.path.join(stg, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write("#!/system/bin/sh\n")
    with open(os.path.join(stg, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_system_prop)
    # Copy xuanyuan assets
    shutil.copytree(os.path.join(multi_staging, 'devices', 'xuanyuan', 'odm'), os.path.join(stg, 'system', 'odm'))

shutil.copytree(os.path.join(payload_staging, 'system', 'priv-app'), os.path.join(x15u_full_stg, 'system', 'priv-app'))
shutil.copytree(os.path.join(payload_staging, 'system', 'etc', 'permissions'), os.path.join(x15u_full_stg, 'system', 'etc', 'permissions'))

with open(os.path.join(x15u_full_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi15u_master_camera_combo_full
name=Xiaomi 15 Ultra Master Camera Combo (FULL Edition)
version=v5.2-Full-Xuanyuan
versionCode=20260926
author=borndead (feat. amitkattal & GeorgeKiarie)
description=Dedicated FULL Leica Camera Suite for Xiaomi 15 Ultra (xuanyuan) on HyperOS 2/3. Full Leica Camera APK + oat/.replace protection + Stock AIO 104 LYT-900 / HP9 200M tunings + native A16 Camera HAL + DCG Hardware HDR + 8K video on all lenses + 4K120fps.
""")

with open(os.path.join(x15u_slim_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi15u_master_imaging_mod_slim
name=Xiaomi 15 Ultra Master Camera Combo (SLIM Edition)
version=v1.1-Slim-Xuanyuan
versionCode=20260926
author=borndead (feat. amitkattal & GeorgeKiarie)
description=Dedicated Pure Systemless Overlay for Xiaomi 15 Ultra (xuanyuan) on HyperOS 2/3. Zero Camera APK replacement (100% immune to signature mismatch bootloops!). Stock AIO 104 LYT-900 / HP9 200M Chromatix tunings + native A16 HAL + DCG Hardware HDR + 8K video all lenses + 4K120fps.
""")

x15u_full_cust = uni_full_cust.replace("Xiaomi Master Camera Combo (FULL Edition)", "Xiaomi 15 Ultra Master Camera Combo (FULL Edition)")
with open(os.path.join(x15u_full_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(x15u_full_cust)

x15u_slim_cust = uni_slim_cust.replace("Xiaomi Master Camera Combo (SLIM Edition)", "Xiaomi 15 Ultra Master Camera Combo (SLIM Edition)")
with open(os.path.join(x15u_slim_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(x15u_slim_cust)

x15u_full_zip = os.path.join(root_antigravity, 'Mi15U_Master_Camera_Combo_Full_by_borndead.zip')
create_zip(x15u_full_stg, x15u_full_zip)

x15u_slim_zip = os.path.join(root_antigravity, 'Mi15U_Master_Imaging_MOD_Slim_by_borndead.zip')
create_zip(x15u_slim_stg, x15u_slim_zip)

# -------------------------------------------------------------
# 6. BUILD DEDICATED FULL & SLIM FOR XIAOMI 15 / 15 PRO (dada/haotian)
# -------------------------------------------------------------
mi15_full_stg = os.path.join(root_antigravity, 'Mi15_Full_Staging')
mi15_slim_stg = os.path.join(root_antigravity, 'Mi15_Slim_Staging')

for stg in [mi15_full_stg, mi15_slim_stg]:
    if os.path.exists(stg):
        shutil.rmtree(stg)
    os.makedirs(stg, exist_ok=True)
    shutil.copytree(os.path.join(multi_staging, 'META-INF'), os.path.join(stg, 'META-INF'))
    with open(os.path.join(stg, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_post_fs_data)
    with open(os.path.join(stg, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write("#!/system/bin/sh\n")
    with open(os.path.join(stg, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_system_prop)
    # Copy dada assets
    shutil.copytree(os.path.join(multi_staging, 'devices', 'dada', 'odm'), os.path.join(stg, 'system', 'odm'))

shutil.copytree(os.path.join(payload_staging, 'system', 'priv-app'), os.path.join(mi15_full_stg, 'system', 'priv-app'))
shutil.copytree(os.path.join(payload_staging, 'system', 'etc', 'permissions'), os.path.join(mi15_full_stg, 'system', 'etc', 'permissions'))

with open(os.path.join(mi15_full_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi15_master_camera_combo_full
name=Xiaomi 15 / 15 Pro Master Camera Combo (FULL Edition)
version=v5.2-Full-Dada
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Dedicated FULL Leica Camera Suite for Xiaomi 15 & 15 Pro (dada/haotian) on HyperOS 2/3. Full Leica Camera APK + oat/.replace protection + Light Hunter 900 tuning + 50MP FullRes + DCG Hardware HDR + George 8K Video + 4K120fps.
""")

with open(os.path.join(mi15_slim_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi15_master_imaging_mod_slim
name=Xiaomi 15 / 15 Pro Master Camera Combo (SLIM Edition)
version=v1.1-Slim-Dada
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Dedicated Pure Systemless Overlay for Xiaomi 15 & 15 Pro (dada/haotian) on HyperOS 2/3. Zero Camera APK replacement (100% immune to signature mismatch bootloops!). Light Hunter 900 tuning + 50MP FullRes + DCG Hardware HDR + George 8K Video + 4K120fps.
""")

mi15_full_cust = uni_full_cust.replace("Xiaomi Master Camera Combo (FULL Edition)", "Xiaomi 15 / 15 Pro Master Camera Combo (FULL Edition)")
with open(os.path.join(mi15_full_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(mi15_full_cust)

mi15_slim_cust = uni_slim_cust.replace("Xiaomi Master Camera Combo (SLIM Edition)", "Xiaomi 15 / 15 Pro Master Camera Combo (SLIM Edition)")
with open(os.path.join(mi15_slim_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(mi15_slim_cust)

mi15_full_zip = os.path.join(root_antigravity, 'Mi15_Master_Camera_Combo_Full_by_borndead.zip')
create_zip(mi15_full_stg, mi15_full_zip)
# Mirror to legacy v5.0
legacy_mi15 = os.path.join(root_antigravity, 'Mi15_Master_Camera_Combo_v5.0_by_borndead.zip')
shutil.copy2(mi15_full_zip, legacy_mi15)
shutil.copy2(mi15_full_zip, os.path.join(repo_releases, os.path.basename(legacy_mi15)))

mi15_slim_zip = os.path.join(root_antigravity, 'Mi15_Master_Imaging_MOD_Slim_by_borndead.zip')
create_zip(mi15_slim_stg, mi15_slim_zip)

# -------------------------------------------------------------
# 7. BUILD DEDICATED FULL & SLIM FOR XIAOMI 14 ULTRA (aurora)
# -------------------------------------------------------------
mi14u_full_stg = os.path.join(root_antigravity, 'Mi14U_Full_Staging')
mi14u_slim_stg = os.path.join(root_antigravity, 'Mi14U_Slim_Staging')

for stg in [mi14u_full_stg, mi14u_slim_stg]:
    if os.path.exists(stg):
        shutil.rmtree(stg)
    os.makedirs(stg, exist_ok=True)
    shutil.copytree(os.path.join(multi_staging, 'META-INF'), os.path.join(stg, 'META-INF'))
    with open(os.path.join(stg, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_post_fs_data)
    with open(os.path.join(stg, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
        f.write("#!/system/bin/sh\n")
    with open(os.path.join(stg, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(common_system_prop)
    # Copy aurora assets (aisp.json)
    if os.path.exists(os.path.join(multi_staging, 'devices', 'aurora', 'odm')):
        shutil.copytree(os.path.join(multi_staging, 'devices', 'aurora', 'odm'), os.path.join(stg, 'system', 'odm'))

# Add clean camera payload to 14U FULL
shutil.copytree(os.path.join(payload_staging, 'system', 'priv-app'), os.path.join(mi14u_full_stg, 'system', 'priv-app'))
shutil.copytree(os.path.join(payload_staging, 'system', 'etc', 'permissions'), os.path.join(mi14u_full_stg, 'system', 'etc', 'permissions'))

# Module prop for 14U FULL
with open(os.path.join(mi14u_full_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi14u_master_camera_combo_full
name=Xiaomi 14 Ultra Master Camera Combo (FULL Edition)
version=v5.2-Full-Aurora
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Dedicated FULL Leica Camera Suite for Xiaomi 14 Ultra (aurora) on HyperOS 1/2/3. Full Leica Camera APK + oat/.replace protection + Quad-50MP FullRes (0.5x, 1x, 3.2x, 5x) + Stepless Variable Aperture (F1.63-F4.0) + DCG Hardware HDR + George 8K Video all lenses + 4K120fps + Offline Processing Bypass.
""")

# Module prop for 14U SLIM
with open(os.path.join(mi14u_slim_stg, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write("""id=mi14u_master_imaging_mod_slim
name=Xiaomi 14 Ultra Master Camera Combo (SLIM Edition)
version=v1.1-Slim-Aurora
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Dedicated Pure Systemless Overlay for Xiaomi 14 Ultra (aurora) on HyperOS 1/2/3. Zero Camera APK replacement (100% immune to signature mismatch bootloops!). Quad-50MP FullRes (0.5x, 1x, 3.2x, 5x) + Stepless Variable Aperture (F1.63-F4.0) + DCG Hardware HDR + George 8K Video all lenses + 4K120fps + AISP Noise Reduction Bypass.
""")

mi14u_full_cust = uni_full_cust.replace("Xiaomi Master Camera Combo (FULL Edition)", "Xiaomi 14 Ultra Master Camera Combo (FULL Edition)")
with open(os.path.join(mi14u_full_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(mi14u_full_cust)

mi14u_slim_cust = uni_slim_cust.replace("Xiaomi Master Camera Combo (SLIM Edition)", "Xiaomi 14 Ultra Master Camera Combo (SLIM Edition)")
with open(os.path.join(mi14u_slim_stg, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(mi14u_slim_cust)

mi14u_full_zip = os.path.join(root_antigravity, 'Mi14U_Master_Camera_Combo_Full_by_borndead.zip')
create_zip(mi14u_full_stg, mi14u_full_zip)

mi14u_slim_zip = os.path.join(root_antigravity, 'Mi14U_Master_Imaging_MOD_Slim_by_borndead.zip')
create_zip(mi14u_slim_stg, mi14u_slim_zip)

print("\n=== ALL FULL & SLIM MODULES SUCCESSFULLY BUILT AND PACKAGED! ===")
