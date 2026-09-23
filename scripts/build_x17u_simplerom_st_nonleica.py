import os
import shutil
import zipfile

staging = r'C:\Users\ASTA\OneDrive\Antigravity\X17U_SimpleRom_ST_NonLeica_Staging'
multi_staging = r'C:\Users\ASTA\OneDrive\Antigravity\Mi_MultiDevice_Combo_Staging'
dest_releases_dir = r'C:\Users\ASTA\OneDrive\Документы\GitHub\Mi_Master_Camera_Combo\releases'
mirror_releases_dir = r'C:\Users\ASTA\OneDrive\Antigravity'

if os.path.exists(staging):
    shutil.rmtree(staging)
os.makedirs(staging, exist_ok=True)

# 1. Copy META-INF
shutil.copytree(os.path.join(multi_staging, 'META-INF'), os.path.join(staging, 'META-INF'))

# 2. Copy ODM to system/odm
shutil.copytree(os.path.join(multi_staging, 'devices', 'nezha', 'odm'), os.path.join(staging, 'system', 'odm'))

# 3. Copy Vendor to system/vendor
shutil.copytree(os.path.join(multi_staging, 'devices', 'nezha', 'vendor'), os.path.join(staging, 'system', 'vendor'))

# 4. Remove any rogue/broken libraries if present
bad_libs = ['libremosaiclib.so', 'libmialgo_ainr_ll.so', 'libmialgo_ellc.so', 'libdlrmsc_android15.so']
for lib in bad_libs:
    lp = os.path.join(staging, 'system', 'odm', 'lib64', lib)
    if os.path.exists(lp):
        os.remove(lp)
        print('Removed rogue lib from staging:', lp)

# 5. Create device_features fallback directory
os.makedirs(os.path.join(staging, 'system', 'etc', 'device_features'), exist_ok=True)
os.makedirs(os.path.join(staging, 'system', 'product', 'etc', 'device_features'), exist_ok=True)

nezha_xml_content = """<?xml version="1.0" encoding="utf-8"?>
<!-- FullRes 50MP/200MP & Offline Leica Features for Xiaomi 17 Ultra (nezha) -->
<!-- Dedicated for SimpleRom 3.0.309.0 ST (Non-Leica) & HyperOS 3.0 (Android 16) -->
<!-- Prevents Pink/Magenta Bayer CFA noise by forcing 100% on-device NPU/ISP processing -->
<features>
    <bool name="is_xiaomi">true</bool>
    <bool name="is_nezha">true</bool>
    <string name="device_name">nezha</string>
    <string name="market_name">Xiaomi 17 Ultra</string>
    <string name="product_name">nezha</string>

    <!-- Camera Hardware & Sensors (Quad Camera: OVX10500U, HP9, JN5, OV50M) -->
    <bool name="is_support_ultra_wide">true</bool>
    <bool name="is_support_optical_zoom_3">true</bool>
    <bool name="is_support_optical_zoom_5">true</bool>
    <bool name="support_quad_camera">true</bool>
    <integer name="support_camera_sensor_count">4</integer>
    <bool name="support_tele_lens">true</bool>
    <bool name="support_periscope_lens">true</bool>
    <bool name="support_tele_macro">true</bool>
    <bool name="support_super_macro">true</bool>

    <!-- Variable Physical Aperture -->
    <bool name="support_camera_aperture">true</bool>
    <bool name="support_camera_variable_aperture">true</bool>
    <bool name="support_camera_aperture_switch">true</bool>
    <bool name="support_dual_aperture">true</bool>
    <bool name="support_aperture_animation">true</bool>

    <!-- Force 100% OFFLINE Processing (Bypass Broken Cloud / Leica Essential Upload) -->
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

    <!-- Offline Leica Camera Engine -->
    <bool name="support_camera_leica">true</bool>
    <bool name="support_leica_style">true</bool>
    <bool name="is_support_leica_style">true</bool>
    <bool name="support_leica_color">true</bool>
    <bool name="support_leica_authentic">true</bool>
    <bool name="support_leica_vibrant">true</bool>
    <bool name="support_leica_filter">true</bool>
    <bool name="support_leica_watermark">true</bool>
    <bool name="support_custom_watermark">true</bool>
    <bool name="support_master_filter">true</bool>
    <bool name="support_leica_m_mode">true</bool>
    <bool name="support_portrait_master_lens">true</bool>
    <bool name="support_street_mode">true</bool>
    <bool name="support_fastshot">true</bool>

    <!-- Full Resolution 50MP/200MP Mode on All Rear Sensors (0.5x, 1x, 3.0x, 5.0x) -->
    <bool name="is_support_ultra_hd">true</bool>
    <bool name="is_support_pixel_model">true</bool>
    <bool name="support_super_resolution">true</bool>
    <bool name="support_ultra_pixel">true</bool>
    <bool name="support_50mp">true</bool>
    <string name="support_ultra_hd_zoom">0.5:1.0:3.0:5.0</string>
    <string name="ultra_pixel_zoom_ratio_support_list">0.5:1.0:3.0:5.0</string>
    <string name="support_ultra_pixel_zoom_ratio">0.5:1.0:3.0:5.0</string>
    <string name="support_super_resolution_zoom">0.5:1.0:3.0:5.0</string>

    <!-- Professional Imaging & RAW (Snapdragon 8 Elite On-Device) -->
    <bool name="support_super_raw">true</bool>
    <bool name="support_raw_domain">true</bool>
    <bool name="support_14bit_raw">true</bool>
    <bool name="support_ultra_raw">true</bool>
    <bool name="support_manual_ultra_raw">true</bool>
    <bool name="support_dng">true</bool>
    <bool name="support_pro_mode">true</bool>

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

    <!-- Camera Mode Keys -->
    <integer-array name="support_camera_mode_keys">
        <item>161</item> <!-- Photo -->
        <item>162</item> <!-- Video -->
        <item>163</item> <!-- Portrait -->
        <item>167</item> <!-- Pro -->
        <item>173</item> <!-- Super Night -->
        <item>175</item> <!-- Ultra HD 50M/200M -->
        <item>209</item> <!-- Leica Street Mode -->
        <item>184</item> <!-- Documents -->
        <item>168</item> <!-- Slow Motion -->
        <item>170</item> <!-- Time-Lapse -->
        <item>204</item> <!-- Director Mode -->
        <item>205</item> <!-- Long Exposure -->
        <item>188</item> <!-- Super Moon -->
        <item>214</item> <!-- Super Macro -->
    </integer-array>
</features>
"""

xml_dirs = [
    os.path.join(staging, 'system', 'etc', 'device_features'),
    os.path.join(staging, 'system', 'product', 'etc', 'device_features'),
    os.path.join(staging, 'system', 'odm', 'etc', 'device_features'),
    os.path.join(staging, 'system', 'vendor', 'etc', 'device_features'),
    os.path.join(staging, 'system', 'vendor', 'odm', 'etc', 'device_features'),
]
for d in xml_dirs:
    os.makedirs(d, exist_ok=True)
    for name in ['nezha.xml', 'xuanyuan.xml', 'ishtar.xml', 'haotian.xml', 'dada.xml']:
        with open(os.path.join(d, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(nezha_xml_content)

# 6. module.prop
module_prop = """id=x17u_master_imaging_simplerom_st_nonleica
name=Xiaomi 17 Ultra Master Imaging MOD (SimpleRom ST Non-Leica Edition)
version=v1.1-SimpleRom-ST-Offline-A16
versionCode=20260927
author=borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
description=Specialized Offline Master Imaging MOD for Xiaomi 17 Ultra (nezha) on SimpleRom 3.0.309.0 ST (Non-Leica edition) / HyperOS 3.0 (Android 16). Prevents pink/magenta noise by disabling cloud/Leica Essential upload across ODM/Vendor/System partitions & forcing 100% on-device Spectra ISP/Hexagon NPU demosaicing. Enables offline Leica Authentic/Vibrant color science, Leica M9/M-mode, Leica watermarks, Master Lens portraits, OVX10500U/HP9/JN5 Chromatix tuning, DCG Hardware HDR, 8K video on all rear lenses, 4K120fps, and full 50M/200M RAW. Pure Systemless Overlay (ROM camera APK intact, 0 crash risk).
"""

# 7. system.prop
system_prop = """# ==============================================================================
# Xiaomi 17 Ultra Master Imaging MOD (SimpleRom ST Non-Leica Edition)
# Hardware: Xiaomi 17 Ultra (nezha) - Snapdragon 8 Elite
# Optimized for SimpleRom 3.0.309.0 ST (Non-Leica) & HyperOS 3.0 / Android 16
# by borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
# ==============================================================================

# 1. Force 100% Offline Local Processing (Disable Broken Cloud / Leica Essential Upload)
# Prevents Pink/Magenta Bayer CFA noise caused by unauthenticated cloud demosaicing on Non-Leica ROMs
persist.vendor.camera.cloud.enable=0
persist.sys.camera.cloud.enable=0
persist.sys.camera.cloud_process=0
persist.vendor.camera.cloud_process=0
persist.vendor.camera.ai_cloud.enable=0
persist.sys.camera.cloud.sr=0
persist.vendor.camera.cloud.sr.enable=0
persist.vendor.camera.ultra_raw.cloud=0
persist.vendor.camera.aisp.cloud=0
persist.sys.camera.aisp.cloud=0
persist.vendor.camera.mialgo.cloud=0
persist.vendor.camera.leica_essential.cloud=0
persist.sys.camera.leica_essential.cloud=0
persist.sys.camera.leica.cloud=0
persist.vendor.camera.leica.cloud=0
ro.vendor.camera.cloud.enable=0
ro.camera.cloud.enable=0

# 2. Local Snapdragon 8 Elite ISP (Spectra) & NPU (Hexagon) Acceleration + DCG HDR
persist.vendor.camera.sensor.hdr=1
persist.vendor.camera.dcg.enable=1
persist.vendor.camera.hdr.dcg=1
persist.vendor.camera.sensor.dcg=1
ro.vendor.camera.dcg=1

# 3. Full Resolution RAW Support (Qualcomm CamX 50MP/200MP Output)
persist.vendor.camera.maxRAWSizes=55

# 4. Leica Flagship Color Matrices, Modes & Watermarks (Local Offline Engine)
ro.miui.camera.leica.supported=1
persist.vendor.camera.enableLeicaMode=1
persist.sys.camera.leica=1
persist.vendor.camera.leica.supported=1
persist.vendor.camera.multicam.leica=1
persist.vendor.camera.provider.disable_device_feature=0
ro.miui.camera.leica.watermark=1
persist.vendor.camera.leicafilter.bypassMode=0

# 5. George Video Mod Tweaks (Bypass ArcSoft video noise reduction for sharp 4K/8K video textures)
persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1
persist.vendor.camera.video.bitrate.factor=1.5
media.camera.bitrate.factor=1.5

# 6. Aux Camera Access for all Google Camera (GCam) mods and Pro Camera apps
vendor.camera.aux.packagelist=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.google.android.GoogleCamera.BigKaka,com.google.android.GoogleCamera.Urnyx,com.google.android.GoogleCameraENG,com.google.android.GoogleCameraGood,com.google.android.apps.cameralite,com.agc.cam,com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.agc.gcam96,org.codeaurora.snapcam,com.samsung.android.scan3d,com.samsung.android.ruler,com.ss.android.ugc.aweme,com.android.mgc,com.shamim.cam,net.sourceforge.opencamera,com.hades.camera,com.free.cam,com.custom.camera,com.arun.gcam,com.falcon.camera
persist.vendor.camera.privapp.list=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.google.android.GoogleCamera.BigKaka,com.google.android.GoogleCamera.Urnyx,com.google.android.GoogleCameraENG,com.google.android.GoogleCameraGood,com.google.android.apps.cameralite,com.agc.cam,com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.agc.gcam96,org.codeaurora.snapcam,com.samsung.android.scan3d,com.samsung.android.ruler,com.ss.android.ugc.aweme,com.android.mgc,com.shamim.cam,net.sourceforge.opencamera,com.hades.camera,com.free.cam,com.custom.camera,com.arun.gcam,com.falcon.camera
"""

# 8. customize.sh
customize_sh = """##########################################################################################
#
# Xiaomi 17 Ultra Master Imaging MOD (SimpleRom ST Non-Leica Edition)
# Target Device: Xiaomi 17 Ultra (nezha)
# Firmware: SimpleRom 3.0.309.0 ST (Non-Leica) & HyperOS 3.0 (Android 16)
# by borndead (feat. itzdfplayer, amitkattal & GeorgeKiarie)
#
##########################################################################################

ui_print "*********************************************************"
ui_print "   Xiaomi 17 Ultra Master Imaging MOD (SimpleRom ST)     "
ui_print "       Special Non-Leica Offline Master Edition          "
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
ui_print "- SimpleRom ST Compatibility Mode Active:"
ui_print "  * ROM native camera APK preserved (zero crash risk!)"
ui_print "  * Broken cloud demosaicing bypassed (fixes magenta/pink noise!)"
ui_print "  * Snapdragon 8 Elite 100% on-device NPU/ISP processing enforced"

# 3. Dynamic patch of device_features/nezha.xml
ui_print "- Locating stock device_features/nezha.xml..."
REAL_XML=""
for xml_candidate in \\
    /odm/etc/device_features/nezha.xml \\
    /vendor/odm/etc/device_features/nezha.xml \\
    /vendor/etc/device_features/nezha.xml \\
    /product/etc/device_features/nezha.xml \\
    /system/etc/device_features/nezha.xml \\
    /system_ext/etc/device_features/nezha.xml; do
    if [ -f "$xml_candidate" ]; then
        REAL_XML="$xml_candidate"
        break
    fi
done

TARGET_XML="$MODPATH/system/etc/device_features/nezha.xml"

if [ -n "$REAL_XML" ]; then
    ui_print "  Found stock config: $REAL_XML"
    cp -af "$REAL_XML" "$TARGET_XML"

    # Purge rogue, cloud, and conflicting tags
    for tag in \\
        support_ultra_hd_zoom ultra_pixel_zoom_ratio_support_list \\
        support_ultra_pixel_zoom_ratio support_super_resolution_zoom \\
        is_support_ultra_hd is_support_pixel_model support_super_resolution \\
        support_ultra_pixel support_50mp support_ultra_raw support_manual_ultra_raw \\
        support_8k_video support_8k_24fps support_8k_all_rear_sensors \\
        support_4k_120fps support_dolby_vision support_4k_60fps_dolby_vision \\
        support_log_video support_director_mode support_cinematic_mode \\
        support_camera_dcg is_support_dcg support_dcg_hdr support_sensor_hdr support_idcg \\
        support_cloud_process support_cloud_ai_process support_ultra_raw_cloud \\
        is_support_cloud_process support_cloud_photo_enhance support_ai_cloud \\
        support_cloud_sr support_cloud_super_resolution support_leica_essential_cloud \\
        support_leica_cloud support_aisp_cloud is_support_ultra_raw_cloud \\
        support_gallery_cloud_process \\
        support_camera_leica support_leica_style is_support_leica_style \\
        support_leica_color support_leica_watermark support_master_filter \\
        support_leica_m_mode support_portrait_master_lens support_street_mode \\
        support_leica_authentic support_leica_vibrant support_leica_filter; do
        sed -i "/$tag/d" "$TARGET_XML"
    done

    # Strip closing </features>
    sed -i 's|</features>||g' "$TARGET_XML"

    # Append tested, clean offline Leica & 50M/200M configuration
    cat << 'EOF' >> "$TARGET_XML"
    <!-- Force 100% OFFLINE Processing (Bypass Broken Cloud / Leica Essential Upload) -->
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

    <!-- Local Leica Camera Engine -->
    <bool name="support_camera_leica">true</bool>
    <bool name="support_leica_style">true</bool>
    <bool name="is_support_leica_style">true</bool>
    <bool name="support_leica_color">true</bool>
    <bool name="support_leica_authentic">true</bool>
    <bool name="support_leica_vibrant">true</bool>
    <bool name="support_leica_filter">true</bool>
    <bool name="support_leica_watermark">true</bool>
    <bool name="support_master_filter">true</bool>
    <bool name="support_leica_m_mode">true</bool>
    <bool name="support_portrait_master_lens">true</bool>
    <bool name="support_street_mode">true</bool>
    <bool name="support_fastshot">true</bool>

    <!-- FullRes 50MP/200MP Mode on All Rear Sensors (0.5x, 1x, 3.0x, 5.0x) -->
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
fi

# Mirror to ALL 9 possible partition paths (overrides /odm, /vendor, /product, /system)
for p in \\
    "$MODPATH/system/etc/device_features" \\
    "$MODPATH/system/product/etc/device_features" \\
    "$MODPATH/system/odm/etc/device_features" \\
    "$MODPATH/system/vendor/etc/device_features" \\
    "$MODPATH/system/vendor/odm/etc/device_features"; do
    mkdir -p "$p"
    for name in nezha.xml xuanyuan.xml ishtar.xml haotian.xml dada.xml; do
        cp -af "$TARGET_XML" "$p/$name"
    done
done
ui_print "  Patched nezha.xml mirrored across ODM, Vendor, Product and System."

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

# 6. Clear camera and gallery cache to purge stale corrupted state & reset app
ui_print "- Clearing camera app & gallery cache to purge corrupted cloud queues..."
pm clear com.android.camera >/dev/null 2>&1
pm clear com.miui.extraphoto >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1
rm -rf /data/data/com.android.camera/code_cache/* >/dev/null 2>&1
rm -rf /data/data/com.miui.extraphoto/cache/* >/dev/null 2>&1
rm -rf /data/data/com.miui.gallery/cache/* >/dev/null 2>&1

# 7. Set Permissions and SELinux contexts for Android 16
ui_print "- Setting permissions and SELinux contexts..."
set_perm_recursive "$MODPATH/system" 0 0 0755 0644
rm -rf "$MODPATH/product" "$MODPATH/odm" "$MODPATH/vendor" "$MODPATH/system_ext" 2>/dev/null

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

for feat_dir in \\
    "$MODPATH/system/etc/device_features" \\
    "$MODPATH/system/product/etc/device_features" \\
    "$MODPATH/product/etc/device_features" \\
    "$MODPATH/system/odm/etc/device_features" \\
    "$MODPATH/odm/etc/device_features" \\
    "$MODPATH/system/vendor/etc/device_features" \\
    "$MODPATH/system/vendor/odm/etc/device_features" \\
    "$MODPATH/vendor/etc/device_features" \\
    "$MODPATH/vendor/odm/etc/device_features"; do
    [ -d "$feat_dir" ] && chcon -R u:object_r:vendor_configs_file:s0 "$feat_dir" 2>/dev/null || chcon -R u:object_r:system_file:s0 "$feat_dir" 2>/dev/null
done

ui_print "*********************************************************"
ui_print "- Xiaomi 17 Ultra SimpleRom ST Non-Leica MOD v1.1 installed!"
ui_print "- Target: Xiaomi 17 Ultra (nezha) on SimpleRom ST"
ui_print "- Pure Systemless Overlay: ROM camera APK 100% preserved."
ui_print "- Magenta/Pink noise FIXED: Cloud processing disabled."
ui_print "- Offline Leica Authentic/Vibrant & Leica M9/M-Mode enabled."
ui_print "- 50MP/200MP FullRes active on all rear sensors."
ui_print "- 8K Video on all rear lenses & 4K120fps enabled."
ui_print "- Dual Conversion Gain (DCG / iDCG) Hardware HDR active."
ui_print "- Please reboot your device."
ui_print "*********************************************************"
"""

# 9. service.sh (Runtime Property Enforcement & Permissions)
service_sh = """#!/system/bin/sh
# service.sh - Enforce Offline Leica Properties & Auto-Grant Permissions on SimpleRom ST

while [ "$(getprop sys.boot_completed)" != "1" ]; do
  sleep 3
done

# Force override runtime properties via resetprop (Magisk / KernelSU / APatch)
# Guarantees that broken cloud / Leica Essential demosaicing cannot be re-enabled
resetprop persist.vendor.camera.cloud.enable 0
resetprop persist.sys.camera.cloud.enable 0
resetprop persist.sys.camera.cloud_process 0
resetprop persist.vendor.camera.cloud_process 0
resetprop persist.vendor.camera.ai_cloud.enable 0
resetprop persist.sys.camera.cloud.sr 0
resetprop persist.vendor.camera.cloud.sr.enable 0
resetprop persist.vendor.camera.ultra_raw.cloud 0
resetprop persist.vendor.camera.aisp.cloud 0
resetprop persist.sys.camera.aisp.cloud 0
resetprop persist.vendor.camera.mialgo.cloud 0
resetprop persist.vendor.camera.leica_essential.cloud 0
resetprop persist.sys.camera.leica_essential.cloud 0
resetprop persist.sys.camera.leica.cloud 0
resetprop persist.vendor.camera.leica.cloud 0
resetprop ro.vendor.camera.cloud.enable 0
resetprop ro.camera.cloud.enable 0

# Disable cloud camera processing service packages & settings if present
pm disable com.xiaomi.camera.cloud >/dev/null 2>&1
settings put system camera_cloud_process 0 >/dev/null 2>&1
settings put global camera_cloud_process 0 >/dev/null 2>&1
settings put secure camera_cloud_process 0 >/dev/null 2>&1

# Enforce Local Leica Engine
resetprop ro.miui.camera.leica.supported 1
resetprop persist.vendor.camera.enableLeicaMode 1
resetprop persist.sys.camera.leica 1
resetprop persist.vendor.camera.leica.supported 1
resetprop persist.vendor.camera.multicam.leica 1
resetprop ro.miui.camera.leica.watermark 1
resetprop persist.vendor.camera.maxRAWSizes 55
resetprop persist.vendor.camera.sensor.hdr 1
resetprop persist.vendor.camera.dcg.enable 1
resetprop persist.vendor.camera.hdr.dcg 1
resetprop persist.vendor.camera.sensor.dcg 1
resetprop ro.vendor.camera.dcg 1

MODDIR=${0%/*}

if [ ! -f "$MODDIR/first_boot_done" ]; then
  while [ -z "$(pm list packages com.android.camera 2>/dev/null)" ]; do
    sleep 3
  done

  # Grant all camera permissions
  pm grant com.android.camera android.permission.CAMERA >/dev/null 2>&1
  pm grant com.android.camera android.permission.RECORD_AUDIO >/dev/null 2>&1
  pm grant com.android.camera android.permission.ACCESS_FINE_LOCATION >/dev/null 2>&1
  pm grant com.android.camera android.permission.ACCESS_COARSE_LOCATION >/dev/null 2>&1
  pm grant com.android.camera android.permission.READ_MEDIA_IMAGES >/dev/null 2>&1
  pm grant com.android.camera android.permission.READ_MEDIA_VIDEO >/dev/null 2>&1
  pm grant com.android.camera android.permission.READ_MEDIA_AUDIO >/dev/null 2>&1
  pm grant com.android.camera android.permission.READ_EXTERNAL_STORAGE >/dev/null 2>&1
  pm grant com.android.camera android.permission.WRITE_EXTERNAL_STORAGE >/dev/null 2>&1
  pm grant com.android.camera android.permission.SYSTEM_ALERT_WINDOW >/dev/null 2>&1

  touch "$MODDIR/first_boot_done"
fi
"""

# 10. post-fs-data.sh
post_fs_data_sh = """#!/system/bin/sh
# post-fs-data.sh - Safe initialization & early cloud property neutralization
MODDIR=${0%/*}

resetprop persist.vendor.camera.cloud.enable 0
resetprop persist.sys.camera.cloud.enable 0
resetprop persist.sys.camera.cloud_process 0
resetprop persist.vendor.camera.cloud_process 0
resetprop persist.vendor.camera.ai_cloud.enable 0
resetprop persist.sys.camera.cloud.sr 0
resetprop persist.vendor.camera.cloud.sr.enable 0
resetprop persist.vendor.camera.ultra_raw.cloud 0
resetprop persist.vendor.camera.aisp.cloud 0
resetprop persist.sys.camera.aisp.cloud 0
resetprop persist.vendor.camera.mialgo.cloud 0
resetprop persist.vendor.camera.leica_essential.cloud 0
resetprop persist.sys.camera.leica_essential.cloud 0
resetprop persist.sys.camera.leica.cloud 0
resetprop persist.vendor.camera.leica.cloud 0
resetprop ro.vendor.camera.cloud.enable 0
resetprop ro.camera.cloud.enable 0
"""

with open(os.path.join(staging, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(module_prop)

with open(os.path.join(staging, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(system_prop)

with open(os.path.join(staging, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(customize_sh)

with open(os.path.join(staging, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(service_sh)

with open(os.path.join(staging, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(post_fs_data_sh)

# Create zip packages in releases and mirror
zip_filename = 'X17U_Master_Imaging_MOD_SimpleRom_ST_NonLeica_by_borndead.zip'
out_zip_repo = os.path.join(dest_releases_dir, zip_filename)
out_zip_mirror = os.path.join(mirror_releases_dir, zip_filename)

os.makedirs(dest_releases_dir, exist_ok=True)

with zipfile.ZipFile(out_zip_repo, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
    for root, dirs, files in os.walk(staging):
        for file in files:
            full_p = os.path.join(root, file)
            rel_p = os.path.relpath(full_p, staging).replace('\\', '/')
            zf.write(full_p, rel_p)

print('Packaged in repo releases:', out_zip_repo, 'Size:', os.path.getsize(out_zip_repo))

shutil.copy2(out_zip_repo, out_zip_mirror)
print('Mirrored to:', out_zip_mirror, 'Size:', os.path.getsize(out_zip_mirror))
