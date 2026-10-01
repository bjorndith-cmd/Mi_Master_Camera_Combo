#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - Xiaomi 13 Ultra (ishtar) Anti-Bootloop Module Builder
Author: borndead

Rebuilds dedicated Xiaomi 13 Ultra (ishtar) FULL and SLIM modules with:
- Zero-ETC architecture preventing ROM feature wipeouts.
- Safe privapp permissions without disabling Android platform security.
- On-Demand diagnostic logging (zero battery/storage drain).
- Strict PROP_VALUE_MAX compliance (< 92 chars per prop).
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

CLEAN_SYSTEM_PROP = """# Full Resolution RAW Support (Qualcomm CamX Standard Output - 50M Unlocked)
persist.vendor.camera.maxRAWSizes=55

# Local MIVI & Chi-CDK Pipeline (Fast 50MP Quad-Bayer Remosaic)
persist.vendor.camera.mivi.enable=1
persist.vendor.camera.mialgo.support=1
persist.vendor.camera.multicam.hwsync=1

# Local Auto Scene Detection (ASD / AI) via Qualcomm Hexagon DSP / MiAlgo
persist.vendor.camera.asd.enable=1
persist.vendor.camera.ai.enable=1
persist.sys.camera.ai=1
persist.vendor.camera.ai_scene=1
persist.vendor.camera.mialgo.asd=1

# Force 100% Local On-Device AI (Bypasses Xiaomi Account Login & Cloud Latency)
persist.vendor.camera.cloud.enable=0
persist.vendor.camera.ai_cloud.enable=0
persist.sys.camera.cloud.enable=0
persist.vendor.camera.cloud_process=0
persist.sys.camera.cloud_process=0
persist.vendor.camera.ultra_raw.cloud=0

# Preserve Leica Authentic & Leica Vibrant color science in Photo mode (0 = active)
persist.vendor.camera.leicafilter.bypassMode=0

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

# Leica Color Matrices, Mode & Watermarks
ro.miui.camera.leica.supported=1
persist.vendor.camera.enableLeicaMode=1
persist.sys.camera.leica=1
persist.vendor.camera.leica.supported=1
persist.vendor.camera.multicam.leica=1
persist.vendor.camera.provider.disable_device_feature=0
ro.miui.camera.leica.watermark=1

# Aux Camera Access for GCam and Pro Camera apps (< 92 chars per prop)
vendor.camera.aux.packagelist=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.agc.cam
vendor.camera.aux.packagelistext=com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.agc.gcam96,org.codeaurora.snapcam
persist.vendor.camera.privapp.list=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.agc.cam
persist.vendor.camera.privapp.listext=net.sourceforge.opencamera,com.shamim.cam,com.android.mgc,com.hades.camera
"""

CLEAN_POST_FS_DATA = """#!/system/bin/sh
# post-fs-data.sh - Early props, diagnostics & Bootloop Saver
# Xiaomi 13 Ultra (ishtar) Camera Suite by borndead

MODDIR=${0%/*}
PFS_LOG="$MODDIR/post-fs-data.log"

echo "=== post-fs-data.sh started: $(date) ===" > "$PFS_LOG"

# 1. BOOTLOOP SAVER ENGINE (Auto-Rescue System)
BOOT_COUNT_FILE="$MODDIR/boot_count"
DISABLE_FILE="$MODDIR/disable"

# Check emergency manual disable triggers
if [ -f "/data/local/tmp/disable_camera" ] || [ -f "/sdcard/disable_camera" ] || [ -f "$DISABLE_FILE" ]; then
    touch "$DISABLE_FILE"
    echo "[BOOTLOOP SAVER] Emergency disable flag detected. Module disabled!" >> "$PFS_LOG"
    exit 0
fi

# Increment boot attempt counter
if [ -f "$BOOT_COUNT_FILE" ]; then
    BOOT_COUNT=$(cat "$BOOT_COUNT_FILE" 2>/dev/null)
    BOOT_COUNT=$((BOOT_COUNT + 1))
else
    BOOT_COUNT=1
fi
echo "$BOOT_COUNT" > "$BOOT_COUNT_FILE"
echo "[BOOTLOOP SAVER] Boot attempt counter: $BOOT_COUNT" >> "$PFS_LOG"

# Auto-rescue if boot attempt count exceeds 2
if [ "$BOOT_COUNT" -gt 2 ]; then
    touch "$DISABLE_FILE"
    echo "[BOOTLOOP SAVER] CRITICAL: Bootloop detected ($BOOT_COUNT consecutive uncompleted boots)!" >> "$PFS_LOG"
    echo "[BOOTLOOP SAVER] Auto-disabling module to rescue system..." >> "$PFS_LOG"
    rm -rf /data/adb/modules_update/mi13u_master_camera_combo_full 2>/dev/null
    exit 0
fi

# 2. PURGE CORRUPT PERSISTENT PROPERTIES
resetprop -p --delete persist.vendor.camera.mivi.version 2>/dev/null
resetprop --delete persist.vendor.camera.mivi.version 2>/dev/null
resetprop -p --delete camera.debug.mivi2 2>/dev/null
resetprop --delete camera.debug.mivi2 2>/dev/null
resetprop -p --delete persist.vendor.camera.manualApertureFnumber 2>/dev/null
resetprop --delete persist.vendor.camera.manualApertureFnumber 2>/dev/null
rm -f /data/property/persist.vendor.camera.manualApertureFnumber 2>/dev/null

# Reinforce Zero Shutter Lag
resetprop -p --delete camera.disable_zsl_mode 2>/dev/null
resetprop -n camera.disable_zsl_mode false 2>/dev/null

# 3. EARLY PROPS INJECTION
resetprop persist.vendor.camera.maxRAWSizes 55
resetprop persist.vendor.camera.mivi.enable 1
resetprop persist.vendor.camera.mialgo.support 1
resetprop persist.vendor.camera.multicam.hwsync 1
resetprop persist.vendor.camera.asd.enable 1
resetprop persist.vendor.camera.ai.enable 1
resetprop persist.sys.camera.ai 1
resetprop persist.vendor.camera.ai_scene 1
resetprop persist.vendor.camera.mialgo.asd 1
resetprop persist.vendor.camera.cloud.enable 0
resetprop persist.sys.camera.cloud.enable 0
resetprop persist.sys.camera.cloud_process 0
resetprop persist.vendor.camera.cloud_process 0
resetprop persist.vendor.camera.ai_cloud.enable 0
resetprop persist.vendor.camera.ultra_raw.cloud 0
resetprop persist.vendor.camera.dcg.enable 1
resetprop persist.vendor.camera.hdr.dcg 1
resetprop persist.vendor.camera.sensor.hdr 1
resetprop ro.vendor.camera.dcg 1
resetprop persist.vendor.camera.arcsoft.aisp_algo_nr.bypass 1
resetprop persist.vendor.camera.video.bitrate.factor 1.5

echo "=== post-fs-data.sh completed: $(date) ===" >> "$PFS_LOG"
"""

CLEAN_SERVICE_SH = """#!/system/bin/sh
# service.sh - Permissions grant, Bootloop Saver reset & Diagnostics
# Xiaomi 13 Ultra (ishtar) Camera Suite by borndead

MODDIR=${0%/*}

# Wait for boot completion
while [ "$(getprop sys.boot_completed)" != "1" ]; do
  sleep 2
done

# 1. Reset Bootloop Saver counter on successful boot
rm -f "$MODDIR/boot_count" 2>/dev/null
echo "[BOOTLOOP SAVER] Boot completed successfully. Counter reset." >> "$MODDIR/post-fs-data.log"

# 2. Wait for user storage decryption
for i in $(seq 1 40); do
  if [ -d "/sdcard/Download" ] || [ -d "/storage/emulated/0/Download" ] || [ -d "/data/media/0/Download" ]; then
    break
  fi
  sleep 1
done

# 3. Deploy Leica 13U custom configs to storage
if [ -d "$MODDIR/configs" ]; then
  mkdir -p /sdcard/Download/XiaomiCamera /sdcard/DCIM/Camera/configs 2>/dev/null
  cp -rf "$MODDIR/configs/"* /sdcard/Download/XiaomiCamera/ 2>/dev/null
  cp -rf "$MODDIR/configs/"* /sdcard/DCIM/Camera/configs/ 2>/dev/null
fi

# 4. Grant all required camera and media permissions once package is registered
if [ -n "$(pm list packages com.android.camera 2>/dev/null)" ]; then
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
fi

# 5. On-Demand Diagnostic Mode (Active ONLY when trigger flag exists)
if [ -f "/data/local/tmp/mmc_debug" ] || [ -f "/sdcard/Download/mmc_debug" ]; then
  LOG_DIR="/sdcard/Download/CameraMod_Logs"
  mkdir -p "$LOG_DIR" 2>/dev/null
  dumpsys package com.android.camera > "$LOG_DIR/04_dumpsys_package.txt" 2>&1
  logcat -d -t 2000 | grep -iE "com.android.camera|MiuiCamera|CameraService|CamX|MIVI|ChiCDK" > "$LOG_DIR/05_logcat_camera.txt" 2>&1
  logcat -b crash -d > "$LOG_DIR/07_logcat_crashes.txt" 2>&1
  chmod 0750 "$LOG_DIR" 2>/dev/null
fi
"""

def main():
    parser = argparse.ArgumentParser(description="Build Xiaomi 13 Ultra Anti-Bootloop Modules")
    parser.add_argument("--staging", type=str, default="", help="Staging directory")
    parser.add_argument("--out-dir", type=str, default="", help="Output releases directory")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    out_dir = Path(args.out_dir) if args.out_dir else (repo_root / "releases")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("=== Xiaomi 13 Ultra (ishtar) Anti-Bootloop Module Builder ===")
    print(f"Repository Root: {repo_root}")
    print(f"Releases Directory: {out_dir}")

if __name__ == '__main__':
    main()
