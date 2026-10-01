#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - AI Suite Builder (Tiers 1, 2, 3 & All-In-One)
Author: borndead

Builds:
  - Tier 1: Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip
  - Tier 2: Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip
  - Tier 3: Mi_AI_Director_Vision_Companion_by_borndead.zip
  - Tier 4: Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip
"""

import os
import shutil
import zipfile
import stat
import argparse
from pathlib import Path

# Standard Magisk / KernelSU / APatch update-binary dispatcher
UPDATE_BINARY = """#!/bin/sh
#################
# Magisk / KernelSU / APatch Module Installer Script
#################

umask 022
OUTFD=$2
ZIPFILE=$3

mount /data 2>/dev/null

if [ -f /data/adb/magisk/util_functions.sh ]; then
  . /data/adb/magisk/util_functions.sh
elif [ -f /data/adb/ksu/util_functions.sh ]; then
  . /data/adb/ksu/util_functions.sh
elif [ -f /data/adb/ap/util_functions.sh ]; then
  . /data/adb/ap/util_functions.sh
else
  echo "! Please install in Magisk / KernelSU / APatch Manager" >&2
  exit 1
fi

install_module
exit 0
"""

UPDATER_SCRIPT = "#MAGISK\n"
POST_FS_DATA = "#!/system/bin/sh\nMODDIR=${0%/*}\n"
SERVICE_SH = """#!/system/bin/sh
MODDIR=${0%/*}
"""

def write_magisk_zip(staging_dir: Path, output_zip: Path):
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists():
        output_zip.unlink()
    
    with zipfile.ZipFile(output_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for file_path in staging_dir.rglob('*'):
            if not file_path.is_file():
                continue
            rel_p = file_path.relative_to(staging_dir).as_posix()
            zinfo = zipfile.ZipInfo.from_file(file_path, arcname=rel_p)
            if file_path.name.endswith('.sh') or 'update-binary' in file_path.name:
                zinfo.external_attr = (0o755 | stat.S_IFREG) << 16
            else:
                zinfo.external_attr = (0o644 | stat.S_IFREG) << 16
            with open(file_path, 'rb') as fp:
                zf.writestr(zinfo, fp.read())

    print(f"Generated module: {output_zip.name} ({output_zip.stat().st_size:,} bytes)")


def main():
    parser = argparse.ArgumentParser(description="Build Mi AI Camera Suite Modules")
    parser.add_argument("--output-dir", type=str, default="", help="Custom output directory")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    output_dir = Path(args.output_dir) if args.output_dir else (repo_root / "releases")
    output_dir.mkdir(parents=True, exist_ok=True)
    build_dir = repo_root / "temp_ai_build"

    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True, exist_ok=True)

    print("=== Building Mi AI Master Camera Suite Modules ===")

    # ==============================================================================
    # 1. TIER 1: AISP Hardware AI Engine
    # ==============================================================================
    t1_dir = build_dir / "t1_aisp"
    (t1_dir / "META-INF" / "com" / "google" / "android").mkdir(parents=True, exist_ok=True)
    (t1_dir / "system" / "etc" / "device_features").mkdir(parents=True, exist_ok=True)

    (t1_dir / "META-INF" / "com" / "google" / "android" / "update-binary").write_text(UPDATE_BINARY, encoding="utf-8", newline="\n")
    (t1_dir / "META-INF" / "com" / "google" / "android" / "updater-script").write_text(UPDATER_SCRIPT, encoding="utf-8", newline="\n")
    (t1_dir / "post-fs-data.sh").write_text(POST_FS_DATA, encoding="utf-8", newline="\n")
    (t1_dir / "service.sh").write_text(SERVICE_SH, encoding="utf-8", newline="\n")

    t1_prop = """id=mi_ai_master_imaging_aisp_hardware
name=Xiaomi Master Camera AI - AISP Neural Engine (Hardware On-Device)
version=v1.1-AISP-Offline
versionCode=110
author=borndead
description=Unlocks Xiaomi AISP 4-LM hardware computational photography (FusionLM, ToneLM, ColorLM, PortraitLM), CyberFocus 2.0 AI tracking, AINR hardware noise reduction, and AI Super Resolution running strictly offline on Snapdragon Hexagon NPU.
"""
    (t1_dir / "module.prop").write_text(t1_prop, encoding="utf-8", newline="\n")

    t1_system_prop = """# Xiaomi AISP On-Device NPU Computational Photography
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
"""
    (t1_dir / "system.prop").write_text(t1_system_prop, encoding="utf-8", newline="\n")

    t1_customize = """##########################################################################################
# Xiaomi Master Camera AI - AISP Neural Engine (Hardware On-Device)
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
    *)
        abort "! Unsupported device: $DEVICE. This module supports: ishtar, aurora, dada, haotian, xuanyuan, nezha."
        ;;
esac

ui_print "- Detected: $DEV_NAME ($DEVICE)"
ui_print "- Injecting Xiaomi AISP Neural Photography Engine..."

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
fi

pm clear com.android.camera >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1
set_perm_recursive "$MODPATH/system" 0 0 0755 0644

ui_print "- AISP Neural Engine active!"
"""
    (t1_dir / "customize.sh").write_text(t1_customize, encoding="utf-8", newline="\n")
    write_magisk_zip(t1_dir, output_dir / "Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip")

    # ==============================================================================
    # 2. TIER 2: HyperAI Studio & ExtraPhoto GenAI Suite
    # ==============================================================================
    t2_dir = build_dir / "t2_genai"
    (t2_dir / "META-INF" / "com" / "google" / "android").mkdir(parents=True, exist_ok=True)
    (t2_dir / "system" / "etc" / "device_features").mkdir(parents=True, exist_ok=True)
    (t2_dir / "system" / "etc" / "permissions").mkdir(parents=True, exist_ok=True)

    (t2_dir / "META-INF" / "com" / "google" / "android" / "update-binary").write_text(UPDATE_BINARY, encoding="utf-8", newline="\n")
    (t2_dir / "META-INF" / "com" / "google" / "android" / "updater-script").write_text(UPDATER_SCRIPT, encoding="utf-8", newline="\n")
    (t2_dir / "post-fs-data.sh").write_text(POST_FS_DATA, encoding="utf-8", newline="\n")
    (t2_dir / "service.sh").write_text(SERVICE_SH, encoding="utf-8", newline="\n")

    t2_prop = """id=mi_ai_studio_genai_extraphoto
name=Xiaomi Master Camera AI - HyperAI Studio & ExtraPhoto (Generative Suite)
version=v1.1-HyperAI-Studio
versionCode=110
author=borndead
description=Enables on-device Generative AI photo editing suite directly from camera preview & gallery: AI Eraser Pro (Magic Elimination 2.0), AI Image Expansion (Outpainting), AI Sky 3.0, AI Portrait Lighting, and Reflection Removal.
"""
    (t2_dir / "module.prop").write_text(t2_prop, encoding="utf-8", newline="\n")

    t2_system_prop = """# HyperAI On-Device Generative Studio & ExtraPhoto Engine
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
    (t2_dir / "system.prop").write_text(t2_system_prop, encoding="utf-8", newline="\n")

    t2_perm_xml = """<?xml version="1.0" encoding="utf-8"?>
<permissions>
    <privapp-permissions package="com.miui.extraphoto">
        <permission name="android.permission.INTERACT_ACROSS_USERS" />
        <permission name="android.permission.START_ACTIVITIES_FROM_BACKGROUND" />
        <permission name="android.permission.WRITE_SECURE_SETTINGS" />
    </privapp-permissions>
</permissions>
"""
    (t2_dir / "system" / "etc" / "permissions" / "privapp-permissions-extraphoto.xml").write_text(t2_perm_xml, encoding="utf-8", newline="\n")

    t2_customize = """##########################################################################################
# Xiaomi Master Camera AI - HyperAI Studio & ExtraPhoto
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
    *)
        abort "! Unsupported device: $DEVICE. This module supports: ishtar, aurora, dada, haotian, xuanyuan, nezha."
        ;;
esac

ui_print "- Detected: $DEV_NAME ($DEVICE)"
ui_print "- Unlocking HyperAI Generative Studio features..."

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
fi

pm clear com.miui.extraphoto >/dev/null 2>&1
rm -rf /data/data/com.miui.gallery/cache/* >/dev/null 2>&1
set_perm_recursive "$MODPATH/system" 0 0 0755 0644

ui_print "- HyperAI Studio Suite ready!"
"""
    (t2_dir / "customize.sh").write_text(t2_customize, encoding="utf-8", newline="\n")
    write_magisk_zip(t2_dir, output_dir / "Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip")

    # ==============================================================================
    # 3. TIER 3: AI Director & Vision Companion
    # ==============================================================================
    t3_dir = build_dir / "t3_director"
    (t3_dir / "META-INF" / "com" / "google" / "android").mkdir(parents=True, exist_ok=True)
    (t3_dir / "system" / "etc" / "device_features").mkdir(parents=True, exist_ok=True)

    (t3_dir / "META-INF" / "com" / "google" / "android" / "update-binary").write_text(UPDATE_BINARY, encoding="utf-8", newline="\n")
    (t3_dir / "META-INF" / "com" / "google" / "android" / "updater-script").write_text(UPDATER_SCRIPT, encoding="utf-8", newline="\n")
    (t3_dir / "post-fs-data.sh").write_text(POST_FS_DATA, encoding="utf-8", newline="\n")
    (t3_dir / "service.sh").write_text(SERVICE_SH, encoding="utf-8", newline="\n")

    t3_prop = """id=mi_ai_director_vision_companion
name=Xiaomi Master Camera AI - AI Director & Vision Companion (Viewfinder HUD)
version=v1.1-AI-Director-Vision
versionCode=110
author=borndead
description=Real-time intelligent camera assistant overlaying the Leica Camera viewfinder. Features AI Golden Ratio / Rule of Thirds composition coach, horizon level stabilizer, AI Lens Advisor, and Smart Pro Mode recommender.
"""
    (t3_dir / "module.prop").write_text(t3_prop, encoding="utf-8", newline="\n")

    t3_system_prop = """# AI Director & Vision Companion Viewfinder HUD
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
    (t3_dir / "system.prop").write_text(t3_system_prop, encoding="utf-8", newline="\n")

    t3_customize = """##########################################################################################
# Xiaomi Master Camera AI - AI Director & Vision Companion
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
    *)
        abort "! Unsupported device: $DEVICE. This module supports: ishtar, aurora, dada, haotian, xuanyuan, nezha."
        ;;
esac

ui_print "- Detected: $DEV_NAME ($DEVICE)"
ui_print "- Activating AI Director viewfinder coaching..."

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
fi

pm clear com.android.camera >/dev/null 2>&1
rm -rf /data/data/com.android.camera/cache/* >/dev/null 2>&1
set_perm_recursive "$MODPATH/system" 0 0 0755 0644

ui_print "- AI Director & Vision Companion ready!"
"""
    (t3_dir / "customize.sh").write_text(t3_customize, encoding="utf-8", newline="\n")
    write_magisk_zip(t3_dir, output_dir / "Mi_AI_Director_Vision_Companion_by_borndead.zip")

    # ==============================================================================
    # 4. TIER 4: Complete All-In-One AI Master Suite
    # ==============================================================================
    t4_dir = build_dir / "t4_allinone"
    (t4_dir / "META-INF" / "com" / "google" / "android").mkdir(parents=True, exist_ok=True)
    (t4_dir / "system" / "etc" / "device_features").mkdir(parents=True, exist_ok=True)
    (t4_dir / "system" / "etc" / "permissions").mkdir(parents=True, exist_ok=True)

    (t4_dir / "META-INF" / "com" / "google" / "android" / "update-binary").write_text(UPDATE_BINARY, encoding="utf-8", newline="\n")
    (t4_dir / "META-INF" / "com" / "google" / "android" / "updater-script").write_text(UPDATER_SCRIPT, encoding="utf-8", newline="\n")
    (t4_dir / "post-fs-data.sh").write_text(POST_FS_DATA, encoding="utf-8", newline="\n")
    (t4_dir / "service.sh").write_text(SERVICE_SH, encoding="utf-8", newline="\n")

    t4_prop = """id=mi_ai_master_camera_suite_allinone
name=Xiaomi Master Camera AI - Complete Suite (All-In-One: AISP + GenAI + Director)
version=v1.1-AI-AllInOne
versionCode=110
author=borndead
description=Complete Tri-Tier AI Suite in a single package: Tier 1 (AISP 4-LM Hardware NPU Engine), Tier 2 (HyperAI GenAI Studio & ExtraPhoto), and Tier 3 (AI Director Vision Companion Viewfinder HUD). 100% offline, zero conflicts.
"""
    (t4_dir / "module.prop").write_text(t4_prop, encoding="utf-8", newline="\n")

    t4_system_prop = f"{t1_system_prop}\n{t2_system_prop}\n{t3_system_prop}"
    (t4_dir / "system.prop").write_text(t4_system_prop, encoding="utf-8", newline="\n")
    (t4_dir / "system" / "etc" / "permissions" / "privapp-permissions-extraphoto.xml").write_text(t2_perm_xml, encoding="utf-8", newline="\n")

    t4_customize = """##########################################################################################
# Xiaomi Master Camera AI - Complete Suite (All-In-One: AISP + GenAI + Director)
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
    *)
        abort "! Unsupported device: $DEVICE. This module supports: ishtar, aurora, dada, haotian, xuanyuan, nezha."
        ;;
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
    <!-- Tier 1: AISP Hardware Computational Photography -->
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

    <!-- Tier 3: AI Director Viewfinder HUD -->
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
fi

pm clear com.android.camera >/dev/null 2>&1
pm clear com.miui.extraphoto >/dev/null 2>&1
set_perm_recursive "$MODPATH/system" 0 0 0755 0644

ui_print "*********************************************************"
ui_print "- Complete Tri-Tier AI Suite armed & ready!"
ui_print "*********************************************************"
"""
    (t4_dir / "customize.sh").write_text(t4_customize, encoding="utf-8", newline="\n")
    write_magisk_zip(t4_dir, output_dir / "Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip")

    # Cleanup temp build
    shutil.rmtree(build_dir, ignore_errors=True)
    print("\n[OK] All AI Suite modules built successfully with standard update-binary!")

if __name__ == "__main__":
    main()
