#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - Xiaomi 13 Ultra APK Verification Tool
Author: borndead
"""

import os
import sys
import zipfile
import subprocess
import tempfile
import shutil
import argparse
from pathlib import Path

def find_tool(tool_name: str, build_tools_dir: str = None) -> str:
    if build_tools_dir:
        cand = os.path.join(build_tools_dir, tool_name)
        if os.path.exists(cand):
            return cand
    which_path = shutil.which(tool_name)
    if which_path:
        return which_path
    return tool_name

def main():
    parser = argparse.ArgumentParser(description="Verify MiuiCamera.apk inside release zip")
    parser.add_argument("--zip", type=str, default="", help="Path to zip module")
    parser.add_argument("--build-tools", type=str, default="", help="Android SDK build-tools directory")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    zip_path = Path(args.zip) if args.zip else (repo_root / "releases" / "Mi13U_Master_Camera_Combo_5_v6.2_Full_by_borndead.zip")

    if not zip_path.exists():
        print(f"Error: Zip not found: {zip_path}")
        sys.exit(1)

    zipalign_exe = find_tool("zipalign", args.build_tools)
    apksigner_bat = find_tool("apksigner", args.build_tools)
    dexdump_exe = find_tool("dexdump", args.build_tools)

    print(f"Auditing APK in: {zip_path.name}")
    with tempfile.TemporaryDirectory() as td:
        apk_out = os.path.join(td, 'MiuiCamera.apk')
        with zipfile.ZipFile(zip_path, 'r') as z:
            libs = [f for f in z.namelist() if 'system/priv-app/MiuiCamera/lib/arm64/' in f or 'product/priv-app/MiuiCamera/lib/arm64/' in f]
            print(f"Companion libraries count: {len(libs)}")
            for l in sorted(libs):
                print("  ", os.path.basename(l))
            
            apk_entry = next((e for e in z.namelist() if e.endswith('MiuiCamera.apk')), None)
            if not apk_entry:
                print("Error: MiuiCamera.apk not found in zip!")
                sys.exit(1)
            with open(apk_out, 'wb') as f:
                f.write(z.read(apk_entry))
        
        # 1. zipalign check
        try:
            za = subprocess.run([zipalign_exe, '-c', '4', apk_out], capture_output=True, text=True)
            status_za = "PASS (OK)" if za.returncode == 0 else f"FAIL ({za.stderr.strip()})"
            print(f"Zipalign 4KB page alignment: {status_za}")
        except FileNotFoundError:
            print("zipalign not installed or not in PATH, skipping alignment check.")

        # 2. apksigner verify
        try:
            sig = subprocess.run([apksigner_bat, 'verify', '-v', apk_out], capture_output=True, text=True)
            print("Signature verification:")
            for line in sig.stdout.splitlines():
                if 'Verified' in line or 'Signer' in line:
                    print("  ", line)
        except FileNotFoundError:
            print("apksigner not installed or not in PATH, skipping signature verify.")

        # 3. DEX verify
        try:
            with zipfile.ZipFile(apk_out, 'r') as apk_z:
                for name in apk_z.namelist():
                    if name.endswith('.dex'):
                        dex_path = os.path.join(td, name)
                        with open(dex_path, 'wb') as df:
                            df.write(apk_z.read(name))
                        dd = subprocess.run([dexdump_exe, '-c', dex_path], capture_output=True, text=True)
                        has_err = 'Out-of-order' in dd.stderr
                        status_dex = "FAIL" if has_err else "PASS (Clean bytecode)"
                        print(f"DEX {name}: {status_dex}")
        except FileNotFoundError:
            print("dexdump not found in PATH, skipping DEX verification.")

if __name__ == '__main__':
    main()
