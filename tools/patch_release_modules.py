#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - Release Modules Sanitizer & Patcher
Author: borndead

Applies critical audit fixes directly across all release zip packages in releases/:
1. Fixes PROP_VALUE_MAX (< 92 chars per line) in system.prop.
2. Removes infinite background logcat loops from service.sh, replacing them with On-Demand logging.
3. Purges rogue/dangerous system allocators (libdmabufheap.so, libion.so) from companion lib directories.
4. Ensures standard Magisk/KernelSU/APatch update-binary dispatcher with install_module.
5. Fixes customize.sh device validation and ROM detection.
"""

import os
import sys
import zipfile
import re
import tempfile
import shutil
import stat
from pathlib import Path

PROP_VALUE_MAX = 91

# Standard Magisk update-binary
CLEAN_UPDATE_BINARY = """#!/bin/sh
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

# Compliant GCam properties (< 92 chars each)
GCAM_PROPS = """# Aux Camera Access for GCam and Pro Camera apps (< 92 chars per prop)
vendor.camera.aux.packagelist=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.agc.cam
vendor.camera.aux.packagelistext=com.agc.gcam84,com.agc.gcam88,com.agc.gcam92,com.agc.gcam96,org.codeaurora.snapcam
persist.vendor.camera.privapp.list=com.google.android.GoogleCamera,com.google.android.GoogleCamera.Canary,com.agc.cam
persist.vendor.camera.privapp.listext=net.sourceforge.opencamera,com.shamim.cam,com.android.mgc,com.hades.camera
"""

ON_DEMAND_DEBUG_BLOCK = """# On-Demand Diagnostic Snapshot (Active ONLY when trigger flag exists)
if [ -f "/data/local/tmp/mmc_debug" ] || [ -f "/sdcard/Download/mmc_debug" ]; then
  mkdir -p "$LOG_DIR" 2>/dev/null
  dumpsys package com.android.camera > "$LOG_DIR/04_dumpsys_package.txt" 2>&1
  logcat -d -t 2000 | grep -iE "com.android.camera|MiuiCamera|CameraService|CamX|MIVI|ChiCDK" > "$LOG_DIR/05_logcat_camera.txt" 2>&1
  logcat -b crash -d > "$LOG_DIR/07_logcat_crashes.txt" 2>&1
  chmod 0750 "$LOG_DIR" 2>/dev/null
fi
"""

FORBIDDEN_LIBS_SET = {
    'libdmabufheap.so', 'libion.so',
    'libremosaiclib.so', 'libmialgo_ainr_ll.so', 'libmialgo_ellc.so', 'libdlrmsc_android15.so'
}

def sanitize_system_prop(content: str, is_slim: bool) -> str:
    lines = content.splitlines()
    new_lines = []
    gcam_inserted = False

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            new_lines.append("")
            continue
        if line.startswith("#"):
            new_lines.append(raw_line)
            continue

        if "=" in line:
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip()

            # Replace aux packagelist / privapp list with compliant split lines
            if k in ('vendor.camera.aux.packagelist', 'persist.vendor.camera.privapp.list',
                     'vendor.camera.aux.packagelistext', 'persist.vendor.camera.privapp.listext'):
                if not gcam_inserted:
                    new_lines.append(GCAM_PROPS.strip())
                    gcam_inserted = True
                continue

            # Remove privapp security enforcement bypass in SLIM
            if is_slim and 'ro.control_privapp_permissions' in k:
                continue

            # In FULL, remove .enforce 0
            if 'ro.control_privapp_permissions.enforce' in k:
                continue

            # Ensure value fits PROP_VALUE_MAX
            if len(v) > PROP_VALUE_MAX:
                v = v[:PROP_VALUE_MAX]
            new_lines.append(f"{k}={v}")
        else:
            new_lines.append(raw_line)

    return "\n".join(new_lines) + "\n"


def sanitize_service_sh(content: str) -> str:
    # Remove infinite logcat background while true loops
    pattern_loop = re.compile(
        r'\(\s*while\s+true\s*;.*?done\s*\)\s*&\s*',
        re.DOTALL
    )
    content = pattern_loop.sub('', content)

    # Remove continuous logcat streaming processes
    content = re.sub(r'\(\s*logcat\s+-v\s+time\s*\|.*?\)\s*&\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'\(\s*logcat\s+-b\s+crash\s+-v\s+time\s*>>.*?\)\s*&\s*', '', content, flags=re.DOTALL)

    # Insert on-demand debug block if not present
    if 'mmc_debug' not in content:
        if 'dumpsys package com.android.camera' in content:
            # Replace inline dumpsys/logcat section with On-Demand block
            content = re.sub(
                r'dumpsys\s+package\s+com\.android\.camera.*?logcat\s+-b\s+crash\s+-d\s*>[^\n]*',
                ON_DEMAND_DEBUG_BLOCK.strip(),
                content,
                flags=re.DOTALL
            )
        else:
            content += "\n" + ON_DEMAND_DEBUG_BLOCK

    # Ensure no chmod 0777 on sensitive directories
    content = content.replace('chmod -R 0777 "$LOG_DIR"', 'chmod -R 0750 "$LOG_DIR"')
    return content


def sanitize_customize_sh(content: str) -> str:
    # Fix broken ROM detector regex: *st* matched stock, fastboot, etc.
    old_rom_detect = '*[Ss]imple*|*ST*|*st*|*[Ee][Uu]*|*[Ee]lite*|*[Pp]ulse*|*[Cc]ustom*'
    new_rom_detect = '*[Ss]impleRom*|*Simple_ROM*|*ST_ROM*|*[Ee][Uu]_*|*xiaomi.eu*|*[Ee]lite*|*[Pp]ulse*'
    content = content.replace(old_rom_detect, new_rom_detect)

    # Fix unknown device fallback to abort
    unlisted_pattern = re.compile(
        r'\*\)\s*\n\s*ui_print\s+"!\s*Unlisted device.*?;\s*',
        re.DOTALL
    )
    clean_unlisted = """*)
        abort "! Unsupported device: $DEVICE. This module supports: ishtar, aurora, dada, haotian, xuanyuan, nezha."
        ;;"""
    content = unlisted_pattern.sub(clean_unlisted, content)

    # Fix haotian profile mapping in customize.sh: haotian has IMX858 5x periscope, not dada's JN5 3.2x!
    content = re.sub(
        r'haotian\)\s*\n\s*DEVICE_NAME="Xiaomi 15 Pro"\s*\n\s*DEV_PROFILE="dada"\s*\n\s*ZOOM_GRID="0.6:1.0:3.2:5.0"',
        'haotian)\n        DEVICE_NAME="Xiaomi 15 Pro"\n        DEV_PROFILE="haotian"\n        ZOOM_GRID="0.6:1.0:5.0"',
        content
    )

    return content


def patch_module_zip(zip_path: Path):
    fname = zip_path.name
    print(f"\nProcessing: {fname}...")
    is_slim = 'slim' in fname.lower()

    with tempfile.TemporaryDirectory() as td:
        tmp_dir = Path(td)
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(tmp_dir)

        # 1. Check & fix update-binary
        ub_path = tmp_dir / "META-INF" / "com" / "google" / "android" / "update-binary"
        if ub_path.exists():
            ub_text = ub_path.read_text(encoding="utf-8", errors="ignore")
            if "install_module" not in ub_text:
                ub_path.write_text(CLEAN_UPDATE_BINARY, encoding="utf-8", newline="\n")
                print("  [FIX] update-binary patched with standard dispatcher.")

        # 2. Check & fix system.prop
        sp_path = tmp_dir / "system.prop"
        if sp_path.exists():
            sp_text = sp_path.read_text(encoding="utf-8", errors="ignore")
            sp_clean = sanitize_system_prop(sp_text, is_slim)
            sp_path.write_text(sp_clean, encoding="utf-8", newline="\n")
            print("  [FIX] system.prop sanitized (PROP_VALUE_MAX < 92 enforced).")

        # 3. Check & fix service.sh
        srv_path = tmp_dir / "service.sh"
        if srv_path.exists():
            srv_text = srv_path.read_text(encoding="utf-8", errors="ignore")
            srv_clean = sanitize_service_sh(srv_text)
            srv_path.write_text(srv_clean, encoding="utf-8", newline="\n")
            print("  [FIX] service.sh sanitized (infinite logcats removed, on-demand debug installed).")

        # 4. Check & fix customize.sh
        cust_path = tmp_dir / "customize.sh"
        if cust_path.exists():
            cust_text = cust_path.read_text(encoding="utf-8", errors="ignore")
            cust_clean = sanitize_customize_sh(cust_text)
            cust_path.write_text(cust_clean, encoding="utf-8", newline="\n")
            print("  [FIX] customize.sh sanitized (device abort & ROM detection).")

        # 5. Purge rogue/broken libraries
        purged = []
        for f in tmp_dir.rglob("*.so"):
            if f.name in FORBIDDEN_LIBS_SET:
                f.unlink()
                purged.append(f.name)
        if purged:
            print(f"  [FIX] Purged dangerous/broken libraries: {list(set(purged))}")

        # Repack zip with proper permissions
        tmp_zip = zip_path.with_suffix('.zip.tmp')
        with zipfile.ZipFile(tmp_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as out_zf:
            for item in sorted(list(tmp_dir.rglob('*'))):
                if not item.is_file():
                    continue
                rel_p = item.relative_to(tmp_dir).as_posix()
                zinfo = zipfile.ZipInfo.from_file(item, arcname=rel_p)
                if item.name.endswith('.sh') or 'update-binary' in item.name:
                    zinfo.external_attr = (0o755 | stat.S_IFREG) << 16
                else:
                    zinfo.external_attr = (0o644 | stat.S_IFREG) << 16
                with open(item, 'rb') as fp:
                    out_zf.writestr(zinfo, fp.read())

        shutil.move(tmp_zip, zip_path)
        print(f"  [DONE] Repackaged: {fname} ({zip_path.stat().st_size:,} bytes)")


def main():
    repo_root = Path(__file__).resolve().parent.parent
    releases_dir = repo_root / "releases"

    print("=== Mi Master Camera Combo - Patching & Sanitizing All Release Modules ===")
    zips = sorted(list(releases_dir.glob("*.zip")))

    for zp in zips:
        try:
            with zipfile.ZipFile(zp, 'r') as test_z:
                if 'module.prop' not in test_z.namelist():
                    continue
        except Exception:
            continue
        patch_module_zip(zp)

    print("\n[SUCCESS] All release modules patched successfully!")

if __name__ == '__main__':
    main()
