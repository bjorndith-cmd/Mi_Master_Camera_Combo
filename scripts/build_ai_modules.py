import os
import shutil
import zipfile

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
releases_dir = os.path.join(repo_root, 'releases')
os.makedirs(releases_dir, exist_ok=True)

temp_build_root = os.path.join(repo_root, 'temp_ai_build')
if os.path.exists(temp_build_root):
    shutil.rmtree(temp_build_root)
os.makedirs(temp_build_root, exist_ok=True)

# Common update-binary template
update_binary = """#!/system/bin/sh
umask 022
OUTFD=$2
ZIPFILE=$3

ui_print() {
    echo -e "$1"
    [ -n "$OUTFD" ] && echo -e "ui_print $1\\nui_print" > "/proc/self/fd/$OUTFD"
}

MODPATH="${0%/*}"
[ -z "$MODPATH" ] && MODPATH="/data/adb/modules/$(basename "$ZIPFILE" .zip)"

# Execute customize.sh if present
if [ -f "$MODPATH/customize.sh" ]; then
    . "$MODPATH/customize.sh"
fi
exit 0
"""

updater_script = "#MAGISK\n"

post_fs_data = """#!/system/bin/sh
MODDIR=${0%/*}
"""

service_sh = """#!/system/bin/sh
MODDIR=${0%/*}
"""

# ==============================================================================
# 1. BUILD TIER 1: AISP Hardware AI Engine
# ==============================================================================
print("--- [1/4] Building Tier 1: Mi_AI_Master_Imaging_AISP_Hardware ---")
t1_dir = os.path.join(temp_build_root, 't1_aisp')
os.makedirs(os.path.join(t1_dir, 'META-INF', 'com', 'google', 'android'), exist_ok=True)
os.makedirs(os.path.join(t1_dir, 'system', 'etc', 'device_features'), exist_ok=True)

with open(os.path.join(t1_dir, 'META-INF', 'com', 'google', 'android', 'update-binary'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(update_binary)
with open(os.path.join(t1_dir, 'META-INF', 'com', 'google', 'android', 'updater-script'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(updater_script)
with open(os.path.join(t1_dir, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(post_fs_data)
with open(os.path.join(t1_dir, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(service_sh)

t1_prop = """id=mi_ai_master_imaging_aisp_hardware
name=Xiaomi Master Camera AI - AISP Neural Engine (Hardware On-Device)
version=v1.0-AISP-Offline
versionCode=100
author=borndead
description=Unlocks Xiaomi AISP 4-LM hardware computational photography (FusionLM, ToneLM, ColorLM, PortraitLM), CyberFocus 2.0 AI tracking, AINR hardware noise reduction, and AI Super Resolution (30x-100x) running strictly offline on Snapdragon Hexagon NPU.
"""
with open(os.path.join(t1_dir, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t1_prop)

t1_system_prop = """# ==============================================================================
# Xiaomi AISP On-Device NPU Computational Photography
# ==============================================================================
persist.vendor.camera.aisp=1
persist.vendor.camera.sensor.ainr=1
persist.vendor.camera.cyberfocus.enable=1
persist.vendor.camera.ai.scene=1
persist.vendor.camera.sr.fusion=1
persist.vendor.camera.super_resolution=1
persist.vendor.camera.motion.tracking=1
ro.vendor.camera.ai.engine=qualcomm_qnn
ro.hardware.camera.aisp=1

# Hardware HDR & Offline Neural Pipeline
persist.vendor.camera.dcg.enable=1
persist.vendor.camera.hdr.dcg=1
persist.vendor.camera.sensor.hdr=1
persist.vendor.camera.sensor.idcg=1

# Bypass ArcSoft video noise reduction for sharp neural textures
persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1

# Mandatory 100% Offline Processing (Eliminates China Cloud Latency & Pink Noise)
persist.vendor.camera.cloud.enable=0
persist.sys.camera.leica_essential.cloud=0
ro.camera.cloud.ai.enable=0
"""
with open(os.path.join(t1_dir, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t1_system_prop)

t1_customize = """##########################################################################################
# Xiaomi Master Camera AI - AISP Neural Engine (Hardware On-Device)
# Activates FusionLM, ToneLM, ColorLM, PortraitLM, CyberFocus 2.0 & AINR
##########################################################################################

ui_print "*********************************************************"
ui_print "  Xiaomi Master Camera AI - AISP Neural Engine           "
ui_print "  Hexagon NPU 4-LM Pipeline (Offline Hardware AI)        "
ui_print "  FusionLM + ToneLM + ColorLM + PortraitLM + CyberFocus  "
ui_print "                     by borndead                         "
ui_print "*********************************************************"

DEVICE=$(getprop ro.product.device)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.build.product)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.product.vendor.device)

case "$DEVICE" in
    ishtar)   DEV_NAME="Xiaomi 13 Ultra"; XML_NAMES="ishtar.xml" ;;
    aurora)   DEV_NAME="Xiaomi 14 Ultra"; XML_NAMES="aurora.xml ishtar.xml" ;;
    dada)     DEV_NAME="Xiaomi 15"; XML_NAMES="dada.xml ishtar.xml" ;;
    haotian)  DEV_NAME="Xiaomi 15 Pro"; XML_NAMES="haotian.xml dada.xml ishtar.xml" ;;
    xuanyuan) DEV_NAME="Xiaomi 15 Ultra"; XML_NAMES="xuanyuan.xml ishtar.xml" ;;
    nezha)    DEV_NAME="Xiaomi 17 Ultra"; XML_NAMES="nezha.xml xuanyuan.xml ishtar.xml" ;;
    *)        DEV_NAME="Flagship Device ($DEVICE)"; XML_NAMES="${DEVICE}.xml ishtar.xml" ;;
esac

ui_print "- Detected: $DEV_NAME ($DEVICE)"
ui_print "- Injecting Xiaomi AISP Neural Photography Engine..."

# Smart source XML lookup: check other active modules in /data/adb/modules first
SRC_XML=""
for mod_dir in /data/adb/modules/*; do
    [ ! -d "$mod_dir" ] && continue
    [ "$mod_dir" = "$MODPATH" ] && continue
    for cand in "$mod_dir/system/etc/device_features/$DEVICE.xml" "$mod_dir/system/product/etc/device_features/$DEVICE.xml"; do
        if [ -f "$cand" ]; then
            SRC_XML="$cand"
            break 2
        fi
    done
done

if [ -z "$SRC_XML" ]; then
    for dir in /odm/etc/device_features /vendor/etc/device_features /product/etc/device_features /system/etc/device_features; do
        if [ -f "$dir/$DEVICE.xml" ]; then
            SRC_XML="$dir/$DEVICE.xml"
            break
        fi
    done
fi

if [ -n "$SRC_XML" ]; then
    TARGET_XML="$MODPATH/system/etc/device_features/$DEVICE.xml"
    mkdir -p "$MODPATH/system/etc/device_features"
    cp -af "$SRC_XML" "$TARGET_XML"

    for tag in \
        support_aisp support_aisp_portrait support_aisp_ultra_raw \
        support_aisp_sr support_cyber_focus support_eye_tracking \
        support_ai_scene_detection support_ai_composition_guide \
        support_ai_shutter support_night_video_ai support_motion_capture \
        support_cloud_process support_cloud_ai_process support_ultra_raw_cloud \
        support_leica_essential_cloud support_leica_cloud support_aisp_cloud; do
        sed -i "/$tag/d" "$TARGET_XML"
    done

    sed -i 's|</features>||g' "$TARGET_XML"

    cat << EOF >> "$TARGET_XML"
    <!-- Xiaomi AISP 4-LM Hardware Computational Photography -->
    <bool name="support_aisp">true</bool>
    <bool name="support_aisp_portrait">true</bool>
    <bool name="support_aisp_ultra_raw">true</bool>
    <bool name="support_aisp_sr">true</bool>
    <bool name="support_cyber_focus">true</bool>
    <bool name="support_eye_tracking">true</bool>
    <bool name="support_ai_scene_detection">true</bool>
    <bool name="support_ai_composition_guide">true</bool>
    <bool name="support_ai_shutter">true</bool>
    <bool name="support_night_video_ai">true</bool>
    <bool name="support_motion_capture">true</bool>

    <!-- Enforce 100% Offline Hardware Execution (Zero Magenta Cloud Glitch) -->
    <bool name="support_cloud_process">false</bool>
    <bool name="support_cloud_ai_process">false</bool>
    <bool name="support_ultra_raw_cloud">false</bool>
    <bool name="support_leica_essential_cloud">false</bool>
    <bool name="support_leica_cloud">false</bool>
    <bool name="support_aisp_cloud">false</bool>
</features>
EOF

    for xname in $XML_NAMES; do
        cp -af "$TARGET_XML" "$MODPATH/system/etc/device_features/$xname"
        mkdir -p "$MODPATH/system/product/etc/device_features"
        cp -af "$TARGET_XML" "$MODPATH/system/product/etc/device_features/$xname"
    done

    # Smart synchronization to other installed camera modules for 100% overlay compatibility
    for other_mod in /data/adb/modules/*; do
        [ ! -d "$other_mod" ] && continue
        [ "$other_mod" = "$MODPATH" ] && continue
        for other_dir in "$other_mod/system/etc/device_features" "$other_mod/system/product/etc/device_features"; do
            if [ -d "$other_dir" ] && [ -f "$other_dir/$DEVICE.xml" ]; then
                for xname in $XML_NAMES; do
                    cp -af "$TARGET_XML" "$other_dir/$xname" 2>/dev/null
                done
            fi
        done
    done
fi

# Reset camera cache for clean NPU graph initialization
ui_print "- Resetting camera cache..."
pm clear com.android.camera >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1

set_perm_recursive "$MODPATH/system" 0 0 0755 0644
rm -rf "$MODPATH/product" "$MODPATH/odm" "$MODPATH/vendor" "$MODPATH/system_ext" 2>/dev/null

ui_print "*********************************************************"
ui_print "- AISP Neural Engine active!"
ui_print "- Snapdragon Hexagon NPU computational photography ready!"
"""
with open(os.path.join(t1_dir, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t1_customize)

t1_zip = os.path.join(releases_dir, 'Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip')
with zipfile.ZipFile(t1_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(t1_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, t1_dir).replace('\\', '/')
            z.write(full_path, rel_path)
print(f"[OK] Tier 1 built: {t1_zip} ({os.path.getsize(t1_zip):,} bytes)")

# ==============================================================================
# 2. BUILD TIER 2: HyperAI Studio & ExtraPhoto GenAI Suite
# ==============================================================================
print("\n--- [2/4] Building Tier 2: Mi_AI_Studio_GenAI_ExtraPhoto ---")
t2_dir = os.path.join(temp_build_root, 't2_genai')
os.makedirs(os.path.join(t2_dir, 'META-INF', 'com', 'google', 'android'), exist_ok=True)
os.makedirs(os.path.join(t2_dir, 'system', 'etc', 'device_features'), exist_ok=True)
os.makedirs(os.path.join(t2_dir, 'system', 'etc', 'permissions'), exist_ok=True)

with open(os.path.join(t2_dir, 'META-INF', 'com', 'google', 'android', 'update-binary'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(update_binary)
with open(os.path.join(t2_dir, 'META-INF', 'com', 'google', 'android', 'updater-script'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(updater_script)
with open(os.path.join(t2_dir, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(post_fs_data)
with open(os.path.join(t2_dir, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(service_sh)

t2_prop = """id=mi_ai_studio_genai_extraphoto
name=Xiaomi Master Camera AI - HyperAI Studio & ExtraPhoto (Generative Suite)
version=v1.0-HyperAI-Studio
versionCode=100
author=borndead
description=Enables on-device Generative AI photo editing suite directly from camera preview & gallery: AI Eraser Pro (Magic Elimination 2.0), AI Image Expansion (Outpainting), AI Sky 3.0 (Dynamic Relighting), AI Portrait Lighting, and Reflection Removal.
"""
with open(os.path.join(t2_dir, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t2_prop)

t2_system_prop = """# ==============================================================================
# HyperAI On-Device Generative Studio & ExtraPhoto Engine
# ==============================================================================
ro.miui.has_gm_genai=1
persist.sys.miui.gallery.ai_editor=1
ro.miui.support_ai_elimination=true
ro.miui.support_ai_expand=true
ro.miui.support_ai_sky=true
ro.miui.support_ai_light=true
ro.miui.support_ai_reflection=true
persist.sys.extraphoto.npu_mode=1
persist.sys.gallery.ai_eraser_pro=1
ro.hardware.npu.genai=1
ro.miui.ai_cutout=1
persist.sys.miui.gallery.dynamic_sky=1
"""
with open(os.path.join(t2_dir, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t2_system_prop)

t2_perm_xml = """<?xml version="1.0" encoding="utf-8"?>
<permissions>
    <privapp-permissions package="com.miui.extraphoto">
        <permission name="android.permission.INTERACT_ACROSS_USERS" />
        <permission name="android.permission.START_ACTIVITIES_FROM_BACKGROUND" />
        <permission name="android.permission.WRITE_SECURE_SETTINGS" />
    </privapp-permissions>
</permissions>
"""
with open(os.path.join(t2_dir, 'system', 'etc', 'permissions', 'privapp-permissions-extraphoto.xml'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t2_perm_xml)

t2_customize = """##########################################################################################
# Xiaomi Master Camera AI - HyperAI Studio & ExtraPhoto (Generative Suite)
# Activates AI Eraser Pro, AI Image Expansion, AI Sky 3.0 & Studio Portrait Light
##########################################################################################

ui_print "*********************************************************"
ui_print "  Xiaomi Master Camera AI - HyperAI Studio & ExtraPhoto  "
ui_print "  Generative AI Post-Processing Suite                    "
ui_print "  AI Eraser Pro + AI Expansion + AI Sky 3.0 + AI Light   "
ui_print "                     by borndead                         "
ui_print "*********************************************************"

DEVICE=$(getprop ro.product.device)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.build.product)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.product.vendor.device)

case "$DEVICE" in
    ishtar)   DEV_NAME="Xiaomi 13 Ultra"; XML_NAMES="ishtar.xml" ;;
    aurora)   DEV_NAME="Xiaomi 14 Ultra"; XML_NAMES="aurora.xml ishtar.xml" ;;
    dada)     DEV_NAME="Xiaomi 15"; XML_NAMES="dada.xml ishtar.xml" ;;
    haotian)  DEV_NAME="Xiaomi 15 Pro"; XML_NAMES="haotian.xml dada.xml ishtar.xml" ;;
    xuanyuan) DEV_NAME="Xiaomi 15 Ultra"; XML_NAMES="xuanyuan.xml ishtar.xml" ;;
    nezha)    DEV_NAME="Xiaomi 17 Ultra"; XML_NAMES="nezha.xml xuanyuan.xml ishtar.xml" ;;
    *)        DEV_NAME="Flagship Device ($DEVICE)"; XML_NAMES="${DEVICE}.xml ishtar.xml" ;;
esac

ui_print "- Detected: $DEV_NAME ($DEVICE)"
ui_print "- Unlocking HyperAI Generative Studio features..."

# Smart source XML lookup: check other active modules in /data/adb/modules first
SRC_XML=""
for mod_dir in /data/adb/modules/*; do
    [ ! -d "$mod_dir" ] && continue
    [ "$mod_dir" = "$MODPATH" ] && continue
    for cand in "$mod_dir/system/etc/device_features/$DEVICE.xml" "$mod_dir/system/product/etc/device_features/$DEVICE.xml"; do
        if [ -f "$cand" ]; then
            SRC_XML="$cand"
            break 2
        fi
    done
done

if [ -z "$SRC_XML" ]; then
    for dir in /odm/etc/device_features /vendor/etc/device_features /product/etc/device_features /system/etc/device_features; do
        if [ -f "$dir/$DEVICE.xml" ]; then
            SRC_XML="$dir/$DEVICE.xml"
            break
        fi
    done
fi

if [ -n "$SRC_XML" ]; then
    TARGET_XML="$MODPATH/system/etc/device_features/$DEVICE.xml"
    mkdir -p "$MODPATH/system/etc/device_features"
    cp -af "$SRC_XML" "$TARGET_XML"

    for tag in \
        support_ai_editor support_magic_elimination support_magic_elimination_pro \
        support_image_expand support_ai_sky support_portrait_lighting \
        support_reflection_removal support_ai_cutout; do
        sed -i "/$tag/d" "$TARGET_XML"
    done

    sed -i 's|</features>||g' "$TARGET_XML"

    cat << EOF >> "$TARGET_XML"
    <!-- HyperAI Generative Studio Capabilities -->
    <bool name="support_ai_editor">true</bool>
    <bool name="support_magic_elimination">true</bool>
    <bool name="support_magic_elimination_pro">true</bool>
    <bool name="support_image_expand">true</bool>
    <bool name="support_ai_sky">true</bool>
    <bool name="support_portrait_lighting">true</bool>
    <bool name="support_reflection_removal">true</bool>
    <bool name="support_ai_cutout">true</bool>
</features>
EOF

    for xname in $XML_NAMES; do
        cp -af "$TARGET_XML" "$MODPATH/system/etc/device_features/$xname"
        mkdir -p "$MODPATH/system/product/etc/device_features"
        cp -af "$TARGET_XML" "$MODPATH/system/product/etc/device_features/$xname"
    done

    # Smart synchronization to other installed camera modules for 100% overlay compatibility
    for other_mod in /data/adb/modules/*; do
        [ ! -d "$other_mod" ] && continue
        [ "$other_mod" = "$MODPATH" ] && continue
        for other_dir in "$other_mod/system/etc/device_features" "$other_mod/system/product/etc/device_features"; do
            if [ -d "$other_dir" ] && [ -f "$other_dir/$DEVICE.xml" ]; then
                for xname in $XML_NAMES; do
                    cp -af "$TARGET_XML" "$other_dir/$xname" 2>/dev/null
                done
            fi
        done
    done
fi

ui_print "- Refreshing Gallery & ExtraPhoto caches..."
pm clear com.miui.extraphoto >/dev/null 2>&1
rm -rf /data/data/com.miui.gallery/cache/* >/dev/null 2>&1
rm -rf /data/data/com.miui.extraphoto/cache/* >/dev/null 2>&1

set_perm_recursive "$MODPATH/system" 0 0 0755 0644
rm -rf "$MODPATH/product" "$MODPATH/odm" "$MODPATH/vendor" "$MODPATH/system_ext" 2>/dev/null

ui_print "*********************************************************"
ui_print "- HyperAI Studio Suite ready!"
ui_print "- Generative tools available in Camera Photo Preview & Gallery!"
"""
with open(os.path.join(t2_dir, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t2_customize)

t2_zip = os.path.join(releases_dir, 'Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip')
with zipfile.ZipFile(t2_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(t2_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, t2_dir).replace('\\', '/')
            z.write(full_path, rel_path)
print(f"[OK] Tier 2 built: {t2_zip} ({os.path.getsize(t2_zip):,} bytes)")

# ==============================================================================
# 3. BUILD TIER 3: AI Director & Vision Companion
# ==============================================================================
print("\n--- [3/4] Building Tier 3: Mi_AI_Director_Vision_Companion ---")
t3_dir = os.path.join(temp_build_root, 't3_director')
os.makedirs(os.path.join(t3_dir, 'META-INF', 'com', 'google', 'android'), exist_ok=True)
os.makedirs(os.path.join(t3_dir, 'system', 'etc', 'device_features'), exist_ok=True)

with open(os.path.join(t3_dir, 'META-INF', 'com', 'google', 'android', 'update-binary'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(update_binary)
with open(os.path.join(t3_dir, 'META-INF', 'com', 'google', 'android', 'updater-script'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(updater_script)
with open(os.path.join(t3_dir, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(post_fs_data)
with open(os.path.join(t3_dir, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(service_sh)

t3_prop = """id=mi_ai_director_vision_companion
name=Xiaomi Master Camera AI - AI Director & Vision Companion (Viewfinder HUD)
version=v1.0-AI-Director-Vision
versionCode=100
author=borndead
description=Real-time intelligent camera assistant overlaying the Leica Camera viewfinder. Features AI Golden Ratio / Rule of Thirds composition coach, horizon level stabilizer, AI Lens Advisor, and Smart Pro Mode parameter recommender.
"""
with open(os.path.join(t3_dir, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t3_prop)

t3_system_prop = """# ==============================================================================
# AI Director & Vision Companion Viewfinder HUD
# ==============================================================================
persist.vendor.camera.ai.director=1
persist.vendor.camera.composition.guide=1
ro.vendor.camera.ai.advisor=1
persist.vendor.camera.horizon.level=1
persist.vendor.camera.golden.ratio=1
persist.vendor.camera.smart.pro=1
ro.miui.camera.leica.composition_lines=1
ro.miui.camera.ai_advisor.toast=1
persist.sys.camera.ai_coach.enable=1
"""
with open(os.path.join(t3_dir, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t3_system_prop)

t3_customize = """##########################################################################################
# Xiaomi Master Camera AI - AI Director & Vision Companion (Viewfinder HUD)
# Real-Time Composition Lines + Horizon Stabilizer + Lens Advisor + Pro Suggester
##########################################################################################

ui_print "*********************************************************"
ui_print "  Xiaomi Master Camera AI - AI Director & Vision         "
ui_print "  Real-Time Viewfinder HUD Assistant                     "
ui_print "  Golden Ratio + Horizon Level + Smart Lens Advisor      "
ui_print "                     by borndead                         "
ui_print "*********************************************************"

DEVICE=$(getprop ro.product.device)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.build.product)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.product.vendor.device)

case "$DEVICE" in
    ishtar)   DEV_NAME="Xiaomi 13 Ultra"; XML_NAMES="ishtar.xml" ;;
    aurora)   DEV_NAME="Xiaomi 14 Ultra"; XML_NAMES="aurora.xml ishtar.xml" ;;
    dada)     DEV_NAME="Xiaomi 15"; XML_NAMES="dada.xml ishtar.xml" ;;
    haotian)  DEV_NAME="Xiaomi 15 Pro"; XML_NAMES="haotian.xml dada.xml ishtar.xml" ;;
    xuanyuan) DEV_NAME="Xiaomi 15 Ultra"; XML_NAMES="xuanyuan.xml ishtar.xml" ;;
    nezha)    DEV_NAME="Xiaomi 17 Ultra"; XML_NAMES="nezha.xml xuanyuan.xml ishtar.xml" ;;
    *)        DEV_NAME="Flagship Device ($DEVICE)"; XML_NAMES="${DEVICE}.xml ishtar.xml" ;;
esac

ui_print "- Detected: $DEV_NAME ($DEVICE)"
ui_print "- Activating AI Director viewfinder coaching..."

# Smart source XML lookup: check other active modules in /data/adb/modules first
SRC_XML=""
for mod_dir in /data/adb/modules/*; do
    [ ! -d "$mod_dir" ] && continue
    [ "$mod_dir" = "$MODPATH" ] && continue
    for cand in "$mod_dir/system/etc/device_features/$DEVICE.xml" "$mod_dir/system/product/etc/device_features/$DEVICE.xml"; do
        if [ -f "$cand" ]; then
            SRC_XML="$cand"
            break 2
        fi
    done
done

if [ -z "$SRC_XML" ]; then
    for dir in /odm/etc/device_features /vendor/etc/device_features /product/etc/device_features /system/etc/device_features; do
        if [ -f "$dir/$DEVICE.xml" ]; then
            SRC_XML="$dir/$DEVICE.xml"
            break
        fi
    done
fi

if [ -n "$SRC_XML" ]; then
    TARGET_XML="$MODPATH/system/etc/device_features/$DEVICE.xml"
    mkdir -p "$MODPATH/system/etc/device_features"
    cp -af "$SRC_XML" "$TARGET_XML"

    for tag in \
        support_ai_composition_guide support_composition_lines \
        support_horizon_level support_golden_ratio support_smart_pro_tips \
        support_ai_lens_advisor support_ai_assistant; do
        sed -i "/$tag/d" "$TARGET_XML"
    done

    sed -i 's|</features>||g' "$TARGET_XML"

    cat << EOF >> "$TARGET_XML"
    <!-- AI Director & Vision Companion Capabilities -->
    <bool name="support_ai_composition_guide">true</bool>
    <bool name="support_composition_lines">true</bool>
    <bool name="support_horizon_level">true</bool>
    <bool name="support_golden_ratio">true</bool>
    <bool name="support_smart_pro_tips">true</bool>
    <bool name="support_ai_lens_advisor">true</bool>
    <bool name="support_ai_assistant">true</bool>
</features>
EOF

    for xname in $XML_NAMES; do
        cp -af "$TARGET_XML" "$MODPATH/system/etc/device_features/$xname"
        mkdir -p "$MODPATH/system/product/etc/device_features"
        cp -af "$TARGET_XML" "$MODPATH/system/product/etc/device_features/$xname"
    done

    # Smart synchronization to other installed camera modules for 100% overlay compatibility
    for other_mod in /data/adb/modules/*; do
        [ ! -d "$other_mod" ] && continue
        [ "$other_mod" = "$MODPATH" ] && continue
        for other_dir in "$other_mod/system/etc/device_features" "$other_mod/system/product/etc/device_features"; do
            if [ -d "$other_dir" ] && [ -f "$other_dir/$DEVICE.xml" ]; then
                for xname in $XML_NAMES; do
                    cp -af "$TARGET_XML" "$other_dir/$xname" 2>/dev/null
                done
            fi
        done
    done
fi

ui_print "- Clearing camera caches for HUD overlay binding..."
pm clear com.android.camera >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1

set_perm_recursive "$MODPATH/system" 0 0 0755 0644
rm -rf "$MODPATH/product" "$MODPATH/odm" "$MODPATH/vendor" "$MODPATH/system_ext" 2>/dev/null

ui_print "*********************************************************"
ui_print "- AI Director & Vision Companion ready!"
ui_print "- Minimalist Leica composition guide & horizon HUD active in Viewfinder!"
"""
with open(os.path.join(t3_dir, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t3_customize)

t3_zip = os.path.join(releases_dir, 'Mi_AI_Director_Vision_Companion_by_borndead.zip')
with zipfile.ZipFile(t3_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(t3_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, t3_dir).replace('\\', '/')
            z.write(full_path, rel_path)
print(f"[OK] Tier 3 built: {t3_zip} ({os.path.getsize(t3_zip):,} bytes)")

# ==============================================================================
# 4. BUILD TIER 4: Complete All-In-One AI Master Suite (Tiers 1 + 2 + 3 Combined)
# ==============================================================================
print("\n--- [4/4] Building Tier 4: Mi_AI_Master_Camera_Suite_AllInOne ---")
t4_dir = os.path.join(temp_build_root, 't4_allinone')
os.makedirs(os.path.join(t4_dir, 'META-INF', 'com', 'google', 'android'), exist_ok=True)
os.makedirs(os.path.join(t4_dir, 'system', 'etc', 'device_features'), exist_ok=True)
os.makedirs(os.path.join(t4_dir, 'system', 'etc', 'permissions'), exist_ok=True)

with open(os.path.join(t4_dir, 'META-INF', 'com', 'google', 'android', 'update-binary'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(update_binary)
with open(os.path.join(t4_dir, 'META-INF', 'com', 'google', 'android', 'updater-script'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(updater_script)
with open(os.path.join(t4_dir, 'post-fs-data.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(post_fs_data)
with open(os.path.join(t4_dir, 'service.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(service_sh)

t4_prop = """id=mi_ai_master_camera_suite_allinone
name=Xiaomi Master Camera AI - Complete Suite (All-In-One: AISP + GenAI + Director)
version=v1.0-AI-AllInOne
versionCode=100
author=borndead
description=Complete Tri-Tier AI Suite in a single package: Tier 1 (AISP 4-LM Hardware NPU Engine), Tier 2 (HyperAI GenAI Studio & ExtraPhoto), and Tier 3 (AI Director Vision Companion Viewfinder HUD). 100% offline, zero conflicts.
"""
with open(os.path.join(t4_dir, 'module.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t4_prop)

t4_system_prop = """# ==============================================================================
# Complete Tri-Tier AI Camera Suite (All-In-One)
# ==============================================================================

# [Tier 1: AISP Hardware Engine - NPU / ISP / CamX]
persist.vendor.camera.aisp=1
persist.vendor.camera.sensor.ainr=1
persist.vendor.camera.cyberfocus.enable=1
persist.vendor.camera.ai.scene=1
persist.vendor.camera.sr.fusion=1
persist.vendor.camera.super_resolution=1
persist.vendor.camera.motion.tracking=1
ro.vendor.camera.ai.engine=qualcomm_qnn
ro.hardware.camera.aisp=1
persist.vendor.camera.dcg.enable=1
persist.vendor.camera.hdr.dcg=1
persist.vendor.camera.sensor.hdr=1
persist.vendor.camera.sensor.idcg=1
persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1
persist.vendor.camera.cloud.enable=0
persist.sys.camera.leica_essential.cloud=0
ro.camera.cloud.ai.enable=0

# [Tier 2: HyperAI Studio & ExtraPhoto Generative Engine]
ro.miui.has_gm_genai=1
persist.sys.miui.gallery.ai_editor=1
ro.miui.support_ai_elimination=true
ro.miui.support_ai_expand=true
ro.miui.support_ai_sky=true
ro.miui.support_ai_light=true
ro.miui.support_ai_reflection=true
persist.sys.extraphoto.npu_mode=1
persist.sys.gallery.ai_eraser_pro=1
ro.hardware.npu.genai=1
ro.miui.ai_cutout=1
persist.sys.miui.gallery.dynamic_sky=1

# [Tier 3: AI Director & Vision Companion Viewfinder HUD]
persist.vendor.camera.ai.director=1
persist.vendor.camera.composition.guide=1
ro.vendor.camera.ai.advisor=1
persist.vendor.camera.horizon.level=1
persist.vendor.camera.golden.ratio=1
persist.vendor.camera.smart.pro=1
ro.miui.camera.leica.composition_lines=1
ro.miui.camera.ai_advisor.toast=1
persist.sys.camera.ai_coach.enable=1
"""
with open(os.path.join(t4_dir, 'system.prop'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t4_system_prop)

with open(os.path.join(t4_dir, 'system', 'etc', 'permissions', 'privapp-permissions-extraphoto.xml'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t2_perm_xml)

t4_customize = """##########################################################################################
# Xiaomi Master Camera AI - Complete Suite (All-In-One: AISP + GenAI + Director)
# Full Tri-Tier AI Integration: NPU Hardware + Generative Studio + Viewfinder HUD
##########################################################################################

ui_print "*********************************************************"
ui_print "  Xiaomi Master Camera AI - Complete Suite (All-In-One)  "
ui_print "  Tier 1: AISP 4-LM Hardware NPU Engine                  "
ui_print "  Tier 2: HyperAI GenAI Studio & ExtraPhoto              "
ui_print "  Tier 3: AI Director & Vision Companion Viewfinder HUD  "
ui_print "                     by borndead                         "
ui_print "*********************************************************"

DEVICE=$(getprop ro.product.device)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.build.product)
[ -z "$DEVICE" ] && DEVICE=$(getprop ro.product.vendor.device)

case "$DEVICE" in
    ishtar)   DEV_NAME="Xiaomi 13 Ultra"; XML_NAMES="ishtar.xml" ;;
    aurora)   DEV_NAME="Xiaomi 14 Ultra"; XML_NAMES="aurora.xml ishtar.xml" ;;
    dada)     DEV_NAME="Xiaomi 15"; XML_NAMES="dada.xml ishtar.xml" ;;
    haotian)  DEV_NAME="Xiaomi 15 Pro"; XML_NAMES="haotian.xml dada.xml ishtar.xml" ;;
    xuanyuan) DEV_NAME="Xiaomi 15 Ultra"; XML_NAMES="xuanyuan.xml ishtar.xml" ;;
    nezha)    DEV_NAME="Xiaomi 17 Ultra"; XML_NAMES="nezha.xml xuanyuan.xml ishtar.xml" ;;
    *)        DEV_NAME="Flagship Device ($DEVICE)"; XML_NAMES="${DEVICE}.xml ishtar.xml" ;;
esac

ui_print "- Detected: $DEV_NAME ($DEVICE)"
ui_print "- Injecting Complete Tri-Tier AI Suite..."

SRC_XML=""
for mod_dir in /data/adb/modules/*; do
    [ ! -d "$mod_dir" ] && continue
    [ "$mod_dir" = "$MODPATH" ] && continue
    for cand in "$mod_dir/system/etc/device_features/$DEVICE.xml" "$mod_dir/system/product/etc/device_features/$DEVICE.xml"; do
        if [ -f "$cand" ]; then
            SRC_XML="$cand"
            break 2
        fi
    done
done

if [ -z "$SRC_XML" ]; then
    for dir in /odm/etc/device_features /vendor/etc/device_features /product/etc/device_features /system/etc/device_features; do
        if [ -f "$dir/$DEVICE.xml" ]; then
            SRC_XML="$dir/$DEVICE.xml"
            break
        fi
    done
fi

if [ -n "$SRC_XML" ]; then
    TARGET_XML="$MODPATH/system/etc/device_features/$DEVICE.xml"
    mkdir -p "$MODPATH/system/etc/device_features"
    cp -af "$SRC_XML" "$TARGET_XML"

    for tag in \
        support_aisp support_aisp_portrait support_aisp_ultra_raw \
        support_aisp_sr support_cyber_focus support_eye_tracking \
        support_ai_scene_detection support_ai_composition_guide \
        support_ai_shutter support_night_video_ai support_motion_capture \
        support_cloud_process support_cloud_ai_process support_ultra_raw_cloud \
        support_leica_essential_cloud support_leica_cloud support_aisp_cloud \
        support_ai_editor support_magic_elimination support_magic_elimination_pro \
        support_image_expand support_ai_sky support_portrait_lighting \
        support_reflection_removal support_ai_cutout \
        support_composition_lines support_horizon_level support_golden_ratio \
        support_smart_pro_tips support_ai_lens_advisor support_ai_assistant; do
        sed -i "/$tag/d" "$TARGET_XML"
    done

    sed -i 's|</features>||g' "$TARGET_XML"

    cat << EOF >> "$TARGET_XML"
    <!-- Tier 1: Xiaomi AISP 4-LM Hardware Computational Photography -->
    <bool name="support_aisp">true</bool>
    <bool name="support_aisp_portrait">true</bool>
    <bool name="support_aisp_ultra_raw">true</bool>
    <bool name="support_aisp_sr">true</bool>
    <bool name="support_cyber_focus">true</bool>
    <bool name="support_eye_tracking">true</bool>
    <bool name="support_ai_scene_detection">true</bool>
    <bool name="support_ai_composition_guide">true</bool>
    <bool name="support_ai_shutter">true</bool>
    <bool name="support_night_video_ai">true</bool>
    <bool name="support_motion_capture">true</bool>

    <!-- Enforce 100% Offline Hardware Execution (Zero Magenta Cloud Glitch) -->
    <bool name="support_cloud_process">false</bool>
    <bool name="support_cloud_ai_process">false</bool>
    <bool name="support_ultra_raw_cloud">false</bool>
    <bool name="support_leica_essential_cloud">false</bool>
    <bool name="support_leica_cloud">false</bool>
    <bool name="support_aisp_cloud">false</bool>

    <!-- Tier 2: HyperAI Generative Studio Capabilities -->
    <bool name="support_ai_editor">true</bool>
    <bool name="support_magic_elimination">true</bool>
    <bool name="support_magic_elimination_pro">true</bool>
    <bool name="support_image_expand">true</bool>
    <bool name="support_ai_sky">true</bool>
    <bool name="support_portrait_lighting">true</bool>
    <bool name="support_reflection_removal">true</bool>
    <bool name="support_ai_cutout">true</bool>

    <!-- Tier 3: AI Director & Vision Companion Capabilities -->
    <bool name="support_composition_lines">true</bool>
    <bool name="support_horizon_level">true</bool>
    <bool name="support_golden_ratio">true</bool>
    <bool name="support_smart_pro_tips">true</bool>
    <bool name="support_ai_lens_advisor">true</bool>
    <bool name="support_ai_assistant">true</bool>
</features>
EOF

    for xname in $XML_NAMES; do
        cp -af "$TARGET_XML" "$MODPATH/system/etc/device_features/$xname"
        mkdir -p "$MODPATH/system/product/etc/device_features"
        cp -af "$TARGET_XML" "$MODPATH/system/product/etc/device_features/$xname"
    done

    for other_mod in /data/adb/modules/*; do
        [ ! -d "$other_mod" ] && continue
        [ "$other_mod" = "$MODPATH" ] && continue
        for other_dir in "$other_mod/system/etc/device_features" "$other_mod/system/product/etc/device_features"; do
            if [ -d "$other_dir" ] && [ -f "$other_dir/$DEVICE.xml" ]; then
                for xname in $XML_NAMES; do
                    cp -af "$TARGET_XML" "$other_dir/$xname" 2>/dev/null
                done
            fi
        done
    done
fi

ui_print "- Resetting camera and gallery caches..."
pm clear com.android.camera >/dev/null 2>&1
pm clear com.miui.extraphoto >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1
rm -rf /data/data/com.miui.gallery/cache/* >/dev/null 2>&1
rm -rf /data/data/com.miui.extraphoto/cache/* >/dev/null 2>&1

set_perm_recursive "$MODPATH/system" 0 0 0755 0644
rm -rf "$MODPATH/product" "$MODPATH/odm" "$MODPATH/vendor" "$MODPATH/system_ext" 2>/dev/null

ui_print "*********************************************************"
ui_print "- Complete Tri-Tier AI Suite active!"
ui_print "- AISP + GenAI ExtraPhoto + AI Director fully armed!"
"""
with open(os.path.join(t4_dir, 'customize.sh'), 'w', encoding='utf-8', newline='\n') as f:
    f.write(t4_customize)

t4_zip = os.path.join(releases_dir, 'Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip')
with zipfile.ZipFile(t4_zip, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(t4_dir):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, t4_dir).replace('\\', '/')
            z.write(full_path, rel_path)
print(f"[OK] Tier 4 (All-In-One) built: {t4_zip} ({os.path.getsize(t4_zip):,} bytes)")

# Cleanup temp build directory
shutil.rmtree(temp_build_root, ignore_errors=True)
print("\n=== ALL 4 AI PACKAGES (3 TIERS + ALL-IN-ONE) PACKAGED SUCCESSFULLY IN releases/ ===")
