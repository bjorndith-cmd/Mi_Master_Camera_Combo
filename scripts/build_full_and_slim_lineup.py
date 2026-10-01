#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - Full and Slim Lineup Builder
Author: borndead

Builds the entire Dual-Tier (FULL & SLIM) flagship module lineup across:
- Universal FULL & SLIM
- Xiaomi 13 Ultra (ishtar) FULL & SLIM
- Xiaomi 14 Ultra (aurora) FULL & SLIM
- Xiaomi 15 (dada) FULL & SLIM
- Xiaomi 15 Pro (haotian) FULL & SLIM
- Xiaomi 15 Ultra (xuanyuan) FULL & SLIM
- Xiaomi 17 Ultra (nezha) FULL & SLIM
"""

import os
import shutil
import zipfile
import stat
import argparse
from pathlib import Path

# Limits & rules
PROP_VALUE_MAX = 91

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
POST_FS_DATA = "#!/system/bin/sh\n# Safe initialization without policy tampering\nMODDIR=${0%/*}\n"

COMMON_SYSTEM_PROP = """# Full Resolution RAW Support (Qualcomm CamX 50MP/200MP Output)
persist.vendor.camera.maxRAWSizes=55

# Aux Camera Access for GCam and Pro Camera apps (< 92 chars per prop)
vendor.camera.aux.packagelist=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.agc.cam
vendor.camera.aux.packagelistext=com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.agc.gcam96,org.codeaurora.snapcam
persist.vendor.camera.privapp.list=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.agc.cam
persist.vendor.camera.privapp.listext=net.sourceforge.opencamera,com.shamim.cam,com.android.mgc,com.hades.camera

# Bypass ArcSoft video noise reduction for sharp 4K/8K textures
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

COMMON_SERVICE_SH = """#!/system/bin/sh
# service.sh - Xiaomi Master Camera Combo Late-boot Service
# Author: borndead
MODDIR=${0%/*}

# Auto-deploy pre-tuned camera configs to /sdcard/Download/XiaomiCamera/
for i in $(seq 1 30); do
    [ -d "/sdcard/Download" ] && break
    sleep 1
done

if [ -d "/sdcard/Download" ]; then
    mkdir -p "/sdcard/Download/XiaomiCamera"
    if [ -d "$MODDIR/configs" ]; then
        cp -n "$MODDIR/configs/"*.json "/sdcard/Download/XiaomiCamera/" 2>/dev/null
    fi
fi

# On-Demand Diagnostic Mode (Active ONLY when trigger flag exists)
if [ -f "/data/local/tmp/mmc_debug" ] || [ -f "/sdcard/Download/mmc_debug" ]; then
    LOG_DIR="/sdcard/Download/CameraMod_Logs"
    mkdir -p "$LOG_DIR" 2>/dev/null
    dumpsys package com.android.camera > "$LOG_DIR/04_dumpsys_package.txt" 2>&1
    logcat -d -t 2000 | grep -iE "com.android.camera|MiuiCamera|CameraService|CamX|MIVI|ChiCDK" > "$LOG_DIR/05_logcat_camera.txt" 2>&1
    logcat -b crash -d > "$LOG_DIR/07_logcat_crashes.txt" 2>&1
    chmod 0750 "$LOG_DIR" 2>/dev/null
fi
"""

SAFE_PERM_XML = """<?xml version="1.0" encoding="utf-8"?>
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

def create_module_zip(staging_dir: Path, output_zip: Path):
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
    parser = argparse.ArgumentParser(description="Build Full and Slim Module Lineup")
    parser.add_argument("--staging-dir", type=str, default="", help="Base staging directory")
    parser.add_argument("--output-dir", type=str, default="", help="Output releases directory")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    output_dir = Path(args.output_dir) if args.output_dir else (repo_root / "releases")
    output_dir.mkdir(parents=True, exist_ok=True)
    base_staging = Path(args.staging_dir) if args.staging_dir else (repo_root / "build" / "staging")
    base_staging.mkdir(parents=True, exist_ok=True)

    print("=== Building Dual-Tier (FULL & SLIM) Module Lineup ===")
    print(f"Repository Root: {repo_root}")
    print(f"Output Directory: {output_dir}")
    print(f"Base Staging: {base_staging}")

if __name__ == "__main__":
    main()
