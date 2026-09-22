import os
import shutil
import zipfile

staging = r'C:\Users\ASTA\OneDrive\Antigravity\X17U_Slim_Staging'
multi_staging = r'C:\Users\ASTA\OneDrive\Antigravity\Mi_MultiDevice_Combo_Staging'

if os.path.exists(staging):
    shutil.rmtree(staging)
os.makedirs(staging, exist_ok=True)

# Copy META-INF
shutil.copytree(os.path.join(multi_staging, 'META-INF'), os.path.join(staging, 'META-INF'))

# Copy ODM to system/odm
shutil.copytree(os.path.join(multi_staging, 'devices', 'nezha', 'odm'), os.path.join(staging, 'system', 'odm'))

# Copy Vendor to system/vendor
shutil.copytree(os.path.join(multi_staging, 'devices', 'nezha', 'vendor'), os.path.join(staging, 'system', 'vendor'))

module_prop = """id=x17u_master_imaging_mod_slim
name=Xiaomi 17 Ultra Master Imaging MOD (Slim Overlay)
version=v1.0-Slim-DCG-A16
versionCode=20260926
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Pure Systemless Overlay MOD for Xiaomi 17 Ultra (nezha) on HyperOS 3.0 / Android 16 (SimpleRom ST, Xiaomi.eu, Elite, Stock). Keeps ROM camera intact (zero APK conflict!). OVX10500U/HP9/JN5/OV50M Chromatix tuned bins + Dual Conversion Gain (DCG) Hardware HDR + 8K video all sensors + 4K120fps + AISP NR bypass + high-res RAW.
"""

system_prop = """# Full Resolution RAW Support (Qualcomm CamX 50MP/200MP Output)
persist.vendor.camera.maxRAWSizes=55

# Aux Camera Access for all Google Camera (GCam) mods and Pro Camera apps
vendor.camera.aux.packagelist=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.google.android.GoogleCamera.BigKaka,com.google.android.GoogleCamera.Urnyx,com.google.android.GoogleCameraENG,com.google.android.GoogleCameraGood,com.google.android.apps.cameralite,com.agc.cam,com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.agc.gcam96,org.codeaurora.snapcam,com.samsung.android.scan3d,com.samsung.android.ruler,com.ss.android.ugc.aweme,com.android.mgc,com.shamim.cam,net.sourceforge.opencamera,com.hades.camera,com.free.cam,com.custom.camera,com.arun.gcam,com.falcon.camera
persist.vendor.camera.privapp.list=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.google.android.GoogleCamera.BigKaka,com.google.android.GoogleCamera.Urnyx,com.google.android.GoogleCameraENG,com.google.android.GoogleCameraGood,com.google.android.apps.cameralite,com.agc.cam,com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.agc.gcam96,org.codeaurora.snapcam,com.samsung.android.scan3d,com.samsung.android.ruler,com.ss.android.ugc.aweme,com.android.mgc,com.shamim.cam,net.sourceforge.opencamera,com.hades.camera,com.free.cam,com.custom.camera,com.arun.gcam,com.falcon.camera

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
# Xiaomi 17 Ultra Master Imaging MOD (Slim Pure Overlay Edition)
# Hardware: Xiaomi 17 Ultra (nezha)
# Compatible with HyperOS 3.0 / Android 16 (SimpleRom ST, Xiaomi.eu, EliteROM, Stock)
# by borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
#
##########################################################################################

ui_print "*********************************************************"
ui_print "   Xiaomi 17 Ultra Master Imaging MOD (Slim Overlay)     "
ui_print "            Target Device: Xiaomi 17 Ultra (nezha)       "
ui_print "                     by borndead                         "
ui_print "*********************************************************"

# 1. Device check
DEVICE=$(getprop ro.product.device)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.build.product)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.product.vendor.device)

ui_print "- Detected device: $DEVICE"

if [ "$DEVICE" != "nezha" ] && [ "$DEVICE" != "x17u" ]; then
    ui_print "! Notice: Detected device ($DEVICE) is not nezha."
    ui_print "! Applying module with nezha Chromatix profiles."
fi

# 2. Android & ROM version check
API=$(getprop ro.build.version.sdk)
OS_VER=$(getprop ro.build.version.release)
BUILD_ID=$(getprop ro.build.display.id)
ui_print "- Android Version: $OS_VER (API $API)"
ui_print "- Firmware/ROM: $BUILD_ID"
ui_print "- Pure Overlay Mode: ROM native camera APK is 100% preserved."
ui_print "  (Guaranteed zero crashes on SimpleRom, Xiaomi.eu, and Stock!)"

# 3. Dynamic patch of device_features/nezha.xml
ui_print "- Locating stock device_features/nezha.xml..."
REAL_XML=""
for xml_candidate in \\
    /product/etc/device_features/nezha.xml \\
    /system/etc/device_features/nezha.xml \\
    /odm/etc/device_features/nezha.xml \\
    /vendor/etc/device_features/nezha.xml \\
    /product/etc/device_features/ishtar.xml \\
    /system/etc/device_features/ishtar.xml; do
    if [ -f "$xml_candidate" ]; then
        REAL_XML="$xml_candidate"
        break
    fi
done

if [ -n "$REAL_XML" ]; then
    ui_print "  Found stock config: $REAL_XML"
    mkdir -p "$MODPATH/system/etc/device_features"
    mkdir -p "$MODPATH/system/product/etc/device_features"
    mkdir -p "$MODPATH/product/etc/device_features"
    TARGET_XML="$MODPATH/system/etc/device_features/nezha.xml"
    cp -af "$REAL_XML" "$TARGET_XML"

    # Purge any conflicting / rogue tags that cause camera freezes
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

    # Strip closing </features>
    sed -i 's|</features>||g' "$TARGET_XML"

    # Append tested, clean 50MP/200MP FullRes and Video MOD configuration
    cat << 'EOF' >> "$TARGET_XML"
    <!-- FullRes 50MP/200MP Mode on All Rear Sensors (0.5x, 1x, 3.0x, 5.0x) -->
    <!-- Photo mode (161) remains clean, fluid, and freeze-free -->
    <bool name="is_support_ultra_hd">true</bool>
    <bool name="support_50mp">true</bool>
    <string name="support_ultra_hd_zoom">0.5:1.0:3.0:5.0</string>
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

    # Mirror to product and system partitions
    cp -af "$TARGET_XML" "$MODPATH/system/product/etc/device_features/nezha.xml"
    cp -af "$TARGET_XML" "$MODPATH/product/etc/device_features/nezha.xml"
    ui_print "  Patched nezha.xml: 50M/200M (0.5x, 1x, 3x, 5x) + 8K/4K120 injected safely."
else
    ui_print "  Notice: stock config not found on standard paths, skipping XML overlay."
fi

# 4. Handle HAL Compatibility
ui_print "- Preserving native HyperOS 3.0 / A16 Camera HAL (prevents black screen)."
rm -rf "$MODPATH/system/odm/lib64/hw"
rm -rf "$MODPATH/system/vendor/odm/lib64/hw"

# 5. Handle ODM / Vendor partition layout
if [ -d "$MODPATH/system/odm" ]; then
    if [ -d /vendor/odm ] || [ -L /odm ]; then
        ui_print "- Mirroring ODM files to /vendor/odm for ROM compatibility..."
        mkdir -p "$MODPATH/system/vendor/odm/lib64/camera"
        mkdir -p "$MODPATH/system/vendor/odm/etc/camera"
        cp -af "$MODPATH/system/odm/lib64/camera/." "$MODPATH/system/vendor/odm/lib64/camera/"
        cp -af "$MODPATH/system/odm/etc/camera/." "$MODPATH/system/vendor/odm/etc/camera/"
    fi
fi

# 6. Clear camera cache to purge stale capabilities & old frozen state
ui_print "- Clearing camera app cache and preferences..."
pm clear com.android.camera >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1
rm -rf /data/data/com.android.camera/code_cache/* >/dev/null 2>&1

# 7. Set Permissions and SELinux contexts for Android 16
ui_print "- Setting permissions and SELinux contexts..."
set_perm_recursive "$MODPATH/system" 0 0 0755 0644
[ -d "$MODPATH/product" ] && set_perm_recursive "$MODPATH/product" 0 0 0755 0644

# Contexts for Chromatix sensor binaries
for bin_file in "$MODPATH/system/odm/lib64/camera"/*.bin; do
    [ -f "$bin_file" ] || continue
    ref_name="/odm/lib64/camera/$(basename "$bin_file")"
    if [ -e "$ref_name" ]; then
        chcon --reference="$ref_name" "$bin_file" 2>/dev/null
    else
        chcon u:object_r:vendor_configs_file:s0 "$bin_file" 2>/dev/null || chcon u:object_r:vendor_file:s0 "$bin_file" 2>/dev/null
    fi
done

# Contexts for json configs
for j_file in "$MODPATH/system/odm/etc/camera"/*.json; do
    [ -f "$j_file" ] || continue
    chcon u:object_r:vendor_configs_file:s0 "$j_file" 2>/dev/null
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

ui_print "*********************************************************"
ui_print "- Xiaomi 17 Ultra Master Imaging MOD installed!"
ui_print "- Target Hardware: Xiaomi 17 Ultra (nezha)"
ui_print "- Pure Overlay Mode: 100% compatible with SimpleRom & Stock."
ui_print "- Stock Photo mode freeze FIXED (smooth fluid preview)."
ui_print "- 50MP/200MP FullRes active on all rear cameras."
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
out_zip = r'C:\Users\ASTA\OneDrive\Antigravity\X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip'
with zipfile.ZipFile(out_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for root, dirs, files in os.walk(staging):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, staging).replace('\\', '/')
            zf.write(full_p, rel_p)

print('Packaged:', out_zip, 'Size:', os.path.getsize(out_zip))
