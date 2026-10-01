#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - Camera APK Rebranding, Patching & Signing Pipeline
Author: borndead

Usage:
  python scripts/build_signed_camera_apk.py --source-apk path/to/MiuiCamera.apk --out-apk output/MiuiCamera.apk
"""

import os
import sys
import shutil
import subprocess
import glob
import re
import zipfile
import tempfile
import argparse
from pathlib import Path

def find_tool(tool_name: str, build_tools_dir: str = None) -> str:
    if build_tools_dir:
        cand = os.path.join(build_tools_dir, tool_name + ('.exe' if os.name == 'nt' else ''))
        if os.path.exists(cand):
            return cand
        cand_bat = os.path.join(build_tools_dir, tool_name + '.bat')
        if os.path.exists(cand_bat):
            return cand_bat
    which_path = shutil.which(tool_name)
    if which_path:
        return which_path
    return tool_name

def main():
    parser = argparse.ArgumentParser(description="Rebrand, patch and sign MiuiCamera.apk")
    parser.add_argument("--source-apk", type=str, default="", help="Path to input MiuiCamera.apk")
    parser.add_argument("--source-zip", type=str, default="", help="Path to input zip containing MiuiCamera.apk")
    parser.add_argument("--out-apk", type=str, default="", help="Output path for signed APK")
    parser.add_argument("--work-dir", type=str, default="", help="Working directory for decompile/rebuild")
    parser.add_argument("--build-tools", type=str, default="", help="Android SDK build-tools directory")
    parser.add_argument("--apktool", type=str, default="apktool", help="Path to apktool (jar or executable)")
    parser.add_argument("--keystore", type=str, default=os.environ.get("KEYSTORE_PATH", ""), help="Path to keystore")
    parser.add_argument("--key-alias", type=str, default=os.environ.get("KEYSTORE_ALIAS", "master_camera"), help="Keystore key alias")
    parser.add_argument("--ks-pass", type=str, default=os.environ.get("KEYSTORE_PASS", ""), help="Keystore password")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent

    # Determine input APK
    if not args.source_apk and not args.source_zip:
        print("Error: Either --source-apk or --source-zip must be specified.")
        sys.exit(1)

    work_dir = Path(args.work_dir) if args.work_dir else Path(tempfile.mkdtemp(prefix="camera_rebrand_"))
    work_dir.mkdir(parents=True, exist_ok=True)
    src_apk = work_dir / "pristine_MiuiCamera.apk"

    if args.source_apk:
        shutil.copy2(args.source_apk, src_apk)
    elif args.source_zip:
        with zipfile.ZipFile(args.source_zip, 'r') as z:
            with open(src_apk, 'wb') as f:
                f.write(z.read('system/priv-app/MiuiCamera/MiuiCamera.apk'))

    print(f"Pristine APK size: {src_apk.stat().st_size:,} bytes")

    # Locate build tools
    zipalign_exe = find_tool("zipalign", args.build_tools)
    apksigner_bat = find_tool("apksigner", args.build_tools)
    apktool_cmd = args.apktool

    # 1. Decompile
    print("\n[1/6] Decompiling APK with apktool...")
    decode_dir = work_dir / "decoded"
    if apktool_cmd.endswith('.jar'):
        cmd_decode = ['java', '-jar', apktool_cmd, 'd', '-f', '-o', str(decode_dir), str(src_apk)]
    else:
        cmd_decode = [apktool_cmd, 'd', '-f', '-o', str(decode_dir), str(src_apk)]
    subprocess.run(cmd_decode, check=True)

    # 2. Patch developer channel link
    print("\n[2/6] Patching developer link in ActivityLauncher (a3.smali)...")
    a3_candidates = list(decode_dir.rglob("a3.smali"))
    for a3_path in a3_candidates:
        code = a3_path.read_text(encoding='utf-8', errors='ignore')
        if "t.me" in code:
            code = re.sub(r'https://t\.me/[a-zA-Z0-9_]+', 'https://t.me/Mi_Master_Camera_Combo', code)
            a3_path.write_text(code, encoding='utf-8', newline='\n')
            print(f"  Patched link in: {a3_path.name}")

    # 3. Patch UniversalSettings.smali
    print("\n[3/6] Updating device list in UniversalSettings.smali...")
    uni_candidates = list(decode_dir.rglob("UniversalSettings.smali"))
    target_flagships = [
        "aurora", "houji", "shennong", "ishtar", "fuxi", "nuwa", "socrates", "corot", "manet",
        "dada", "haotian", "xuanyuan", "nezha", "rothko", "vermeer", "duchamp"
    ]
    for uni_path in uni_candidates:
        uni_code = uni_path.read_text(encoding='utf-8')
        existing_devs = re.findall(r'const-string v1, "([^"]+)"', uni_code)
        all_devs = sorted(list(set(existing_devs + target_flagships)))
        dev_lines = [
            ".method public static deviceList()[Ljava/lang/CharSequence;",
            "    .locals 3",
            "",
            f"    const/16 v0, 0x{len(all_devs):x}",
            "",
            "    new-array v0, v0, [Ljava/lang/CharSequence;",
            ""
        ]
        for idx, d in enumerate(all_devs):
            dev_lines.append(f"    const/16 v2, 0x{idx:x}")
            dev_lines.append("")
            dev_lines.append(f'    const-string v1, "{d}"')
            dev_lines.append("")
            dev_lines.append("    aput-object v1, v0, v2")
            dev_lines.append("")
        dev_lines.append("    return-object v0")
        dev_lines.append(".end method")
        pattern_dev = re.compile(r'\.method public static deviceList\(\)\[Ljava/lang/CharSequence;.*?\n\.end method', re.DOTALL)
        if pattern_dev.search(uni_code):
            uni_code = pattern_dev.sub("\n".join(dev_lines), uni_code)
            uni_path.write_text(uni_code, encoding='utf-8', newline='\n')
            print(f"  Updated deviceList in {uni_path.name}")

    # 4. Patch strings.xml
    print("\n[4/6] Updating branding and author strings...")
    for str_file in decode_dir.rglob("strings.xml"):
        c = str_file.read_text(encoding='utf-8', errors='ignore')
        orig = c
        if 'values-ru' in str(str_file) or 'values-uk' in str(str_file):
            c = re.sub(r'<string name="pref_mod_title">[^<]*</string>',
                       '<string name="pref_mod_title">Описание модификации [Модификация: borndead]</string>', c)
        else:
            c = re.sub(r'<string name="pref_mod_title">[^<]*</string>',
                       '<string name="pref_mod_title">Modification Description [Build Author: borndead]</string>', c)
        c = c.replace('@itzdfplayer_stash', '@Mi_Master_Camera_Combo')
        c = c.replace('@itzdfplayer', 'borndead')
        if c != orig:
            str_file.write_text(c, encoding='utf-8', newline='\n')

    # 5. Rebuild
    print("\n[5/6] Rebuilding APK with apktool...")
    unaligned_apk = work_dir / "unaligned.apk"
    if apktool_cmd.endswith('.jar'):
        cmd_build = ['java', '-jar', apktool_cmd, 'b', '-f', '-o', str(unaligned_apk), str(decode_dir)]
    else:
        cmd_build = [apktool_cmd, 'b', '-f', '-o', str(unaligned_apk), str(decode_dir)]
    subprocess.run(cmd_build, check=True)

    # 6. Align & Sign
    print("\n[6/6] Aligning (4KB) & Signing...")
    aligned_apk = work_dir / "aligned.apk"
    subprocess.run([zipalign_exe, '-p', '-f', '4', str(unaligned_apk), str(aligned_apk)], check=True)

    out_apk = Path(args.out_apk) if args.out_apk else (work_dir / "MiuiCamera_signed.apk")
    out_apk.parent.mkdir(parents=True, exist_ok=True)

    if args.keystore and Path(args.keystore).exists() and args.ks_pass:
        cmd_sign = [
            apksigner_bat, 'sign',
            '--ks', args.keystore,
            '--ks-key-alias', args.key_alias,
            '--ks-pass', f'pass:{args.ks_pass}',
            '--key-pass', f'pass:{args.ks_pass}',
            '--v1-signing-enabled', 'true',
            '--v2-signing-enabled', 'true',
            '--v3-signing-enabled', 'true',
            '--out', str(out_apk),
            str(aligned_apk)
        ]
        subprocess.run(cmd_sign, check=True)
        print(f"[PASS] Signed APK generated at: {out_apk}")
    else:
        print("[INFO] No keystore/credentials provided. Exporting 4KB-aligned uncompressed APK.")
        shutil.copy2(aligned_apk, out_apk)
        print(f"Generated aligned APK at: {out_apk}")

if __name__ == '__main__':
    main()
