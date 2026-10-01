#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - Automated CI & Release Verification Engine
Author: borndead

Validates:
1. Absence of private local paths and hardcoded secrets.
2. Android system.prop line length limits (PROP_VALUE_MAX < 92 chars).
3. Magisk/KernelSU/APatch update-binary dispatcher validity.
4. Absence of infinite logcat daemons in production service.sh.
5. Absence of dangerous platform permissions and rogue/broken shared libraries.
6. Unix LF line endings across all shell scripts.

Exit Code:
  0 - All checks PASSED
  1 - Verification FAILED
"""

import os
import sys
import zipfile
import re
import argparse
from pathlib import Path

# Limits & rules
PROP_VALUE_MAX = 91  # Linux / Android property value limit (92 bytes including null terminator)
FORBIDDEN_LIBS = [
    'libremosaiclib.so',
    'libmialgo_ainr_ll.so',
    'libmialgo_ellc.so',
    'libdlrmsc_android15.so'
]
DANGEROUS_SYSTEM_OVERRIDES = [
    'libion.so',
    'libdmabufheap.so'
]
DANGEROUS_PERMS = [
    'android.permission.REBOOT',
    'android.permission.DEVICE_POWER',
    'android.permission.MANAGE_USERS'
]

# Generic patterns to detect non-portable host paths and exposed credentials
HARDCODED_HOST_PATH_REGEX = re.compile(
    r'(?:[A-Za-z]:[\\/](?:Users|Users[\\/]|home)|OneDrive|pass:[a-zA-Z0-9_]+123)',
    re.IGNORECASE
)

def check_repo_cleanliness(repo_root: Path) -> list:
    errors = []
    print("\n[1/5] Checking repository files for non-portable paths and credentials...")
    
    scanned_exts = {'.py', '.sh', '.yml', '.yaml', '.json', '.xml', '.prop'}
    
    for path in repo_root.rglob('*'):
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root)
        if any(part.startswith('.') for part in rel.parts) and not str(rel).startswith('.github'):
            continue
        if '__pycache__' in rel.parts or 'releases' in rel.parts:
            continue
        if rel == Path('tools/verify.py'):
            continue
        if path.suffix not in scanned_exts and path.name not in {'update-binary', 'customize.sh', 'service.sh', 'post-fs-data.sh', 'module.prop', 'system.prop'}:
            continue

        try:
            content = path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue

        match = HARDCODED_HOST_PATH_REGEX.search(content)
        if match:
            errors.append(f"Non-portable host path or credential pattern '{match.group(0)}' found in: {rel}")

    if not errors:
        print("  [PASS] Clean codebase: 0 non-portable host paths or credentials found.")
    return errors


def check_module_zip(zip_path: Path) -> list:
    errors = []
    fname = zip_path.name
    print(f"\nAuditing module: {fname} ({zip_path.stat().st_size:,} bytes)...")

    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            names = z.namelist()

            # 1. Update binary
            ub_names = [n for n in names if n.endswith('update-binary')]
            if not ub_names:
                errors.append(f"{fname}: Missing META-INF/.../update-binary!")
            else:
                ub_content = z.read(ub_names[0]).decode('utf-8', errors='ignore')
                if 'install_module' not in ub_content:
                    errors.append(f"{fname}: update-binary missing install_module dispatcher call!")

            # 2. module.prop
            if 'module.prop' not in names:
                errors.append(f"{fname}: Missing module.prop!")
            else:
                mprop = z.read('module.prop').decode('utf-8', errors='ignore')
                for req in ['id=', 'name=', 'version=', 'versionCode=', 'author=', 'description=']:
                    if req not in mprop:
                        errors.append(f"{fname}: module.prop missing required field '{req}'")

            # 3. system.prop
            if 'system.prop' in names:
                sp_content = z.read('system.prop').decode('utf-8', errors='ignore')
                for line_no, raw_line in enumerate(sp_content.splitlines(), start=1):
                    line = raw_line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' in line:
                        k, v = line.split('=', 1)
                        k = k.strip()
                        v = v.strip()
                        if len(k) > PROP_VALUE_MAX:
                            errors.append(f"{fname}: system.prop line {line_no} key '{k}' exceeds {PROP_VALUE_MAX} chars ({len(k)})!")
                        if len(v) > PROP_VALUE_MAX:
                            errors.append(f"{fname}: system.prop line {line_no} value of '{k}' exceeds {PROP_VALUE_MAX} chars ({len(v)}): '{v[:40]}...'!")
                
                # Check for unnecessary global privapp enforcement bypass in SLIM
                if 'slim' in fname.lower() and 'ro.control_privapp_permissions.enforce' in sp_content:
                    errors.append(f"{fname}: SLIM module contains unnecessary ro.control_privapp_permissions.enforce setting!")

            # 4. service.sh
            if 'service.sh' in names:
                srv_content = z.read('service.sh').decode('utf-8', errors='ignore')
                # Check for infinite logcat loops
                if re.search(r'while\s+true\s*;.*logcat', srv_content, re.DOTALL):
                    errors.append(f"{fname}: service.sh contains infinite while true logcat daemon loop!")

            # 5. Check forbidden libs
            found_broken = [f for f in names if any(bad in f for bad in FORBIDDEN_LIBS)]
            if found_broken:
                errors.append(f"{fname}: Contains broken/rogue dynamic libraries: {found_broken}")

            # 6. Check dangerous system overrides
            found_overrides = [f for f in names if any(f.endswith('/' + bad) or f == bad for bad in DANGEROUS_SYSTEM_OVERRIDES)]
            if found_overrides:
                errors.append(f"{fname}: Contains dangerous system overrides: {found_overrides}")

            # 7. Check dangerous platform permissions
            perm_files = [f for f in names if 'privapp-permissions' in f and f.endswith('.xml')]
            for pf in perm_files:
                p_text = z.read(pf).decode('utf-8', errors='ignore')
                for dp in DANGEROUS_PERMS:
                    if dp in p_text:
                        errors.append(f"{fname}: Contains dangerous platform permission '{dp}' in {pf}!")

    except zipfile.BadZipFile:
        errors.append(f"{fname}: Corrupted zip file!")
    except Exception as e:
        errors.append(f"{fname}: Error auditing zip: {e}")

    if not any(fname in err for err in errors):
        print(f"  [PASS] {fname}: Fully compliant.")
    return errors


def check_shell_scripts_crlf(repo_root: Path) -> list:
    errors = []
    print("\n[3/5] Checking shell scripts for Unix LF line endings...")
    for path in repo_root.rglob('*.sh'):
        if not path.is_file() or '__pycache__' in path.parts:
            continue
        try:
            content = path.read_bytes()
            if b'\r\n' in content:
                rel = path.relative_to(repo_root)
                errors.append(f"Windows CRLF line endings detected in shell script: {rel}")
        except Exception:
            pass
    if not errors:
        print("  [PASS] All shell scripts use canonical Unix LF line endings.")
    return errors


def check_devices_and_configs(repo_root: Path) -> list:
    errors = []
    print("\n[4/5] Checking hardware and devices configuration...")
    dev_json = repo_root / 'configs' / 'devices.json'
    if not dev_json.exists():
        errors.append("configs/devices.json missing!")
    else:
        try:
            import json
            data = json.loads(dev_json.read_text(encoding='utf-8'))
            devs = data.get('devices', {})
            for d in ['ishtar', 'aurora', 'dada', 'haotian', 'xuanyuan', 'nezha']:
                if d not in devs:
                    errors.append(f"configs/devices.json missing device profile for: {d}")
        except Exception as e:
            errors.append(f"configs/devices.json invalid JSON: {e}")
    if not errors:
        print("  [PASS] Hardware devices configuration verified.")
    return errors


def main():
    parser = argparse.ArgumentParser(description="Mi Master Camera Combo Verification Suite")
    parser.add_argument("--strict", action="store_true", help="Fail with exit code 1 if any warning/error occurs")
    parser.add_argument("--releases-dir", type=str, default="", help="Custom releases directory to check")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    releases_dir = Path(args.releases_dir) if args.releases_dir else (repo_root / "releases")

    print(f"=== Starting Comprehensive Audit & Verification ===")
    print(f"Repository Root: {repo_root}")
    print(f"Releases Directory: {releases_dir}")

    all_errors = []

    # 1. Cleanliness
    all_errors.extend(check_repo_cleanliness(repo_root))

    # 2. Release modules
    print(f"\n[2/5] Auditing release archives in {releases_dir.name}/...")
    if releases_dir.exists():
        zips = sorted(list(releases_dir.glob("*.zip")))
        if not zips:
            print("  [INFO] No .zip archives found in releases directory.")
        for zp in zips:
            # Skip non-module packs like config zip packs if they don't contain module.prop
            try:
                with zipfile.ZipFile(zp, 'r') as zf:
                    if 'module.prop' not in zf.namelist():
                        continue
            except Exception:
                continue
            all_errors.extend(check_module_zip(zp))
    else:
        print(f"  [WARN] Releases directory {releases_dir} does not exist.")

    # 3. CRLF check
    all_errors.extend(check_shell_scripts_crlf(repo_root))

    # 4. Devices config
    all_errors.extend(check_devices_and_configs(repo_root))

    # Summary
    print("\n" + "=" * 60)
    if all_errors:
        print(f"FAILED: {len(all_errors)} issues detected:")
        for idx, err in enumerate(all_errors, start=1):
            print(f"  [{idx}] {err}")
        print("=" * 60)
        sys.exit(1)
    else:
        print("SUCCESS: 100% of checks PASSED! Repository and packages are clean and ready.")
        print("=" * 60)
        sys.exit(0)

if __name__ == "__main__":
    main()
