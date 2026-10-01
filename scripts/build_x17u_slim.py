#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - Xiaomi 17 Ultra Slim Packager
Author: borndead

Packages Pure Systemless Overlay MOD for Xiaomi 17 Ultra (nezha).
"""

import os
import shutil
import zipfile
import stat
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Package Xiaomi 17 Ultra Slim MOD")
    parser.add_argument("--staging", type=str, default="", help="Staging directory")
    parser.add_argument("--out-zip", type=str, default="", help="Output zip path")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    releases_dir = repo_root / "releases"
    releases_dir.mkdir(parents=True, exist_ok=True)

    staging_dir = Path(args.staging) if args.staging else (repo_root / "build" / "staging" / "X17U_Slim_Staging")
    out_zip = Path(args.out_zip) if args.out_zip else (releases_dir / "X17U_Master_Imaging_MOD_Slim_by_borndead.zip")

    if not staging_dir.exists():
        print(f"[INFO] Staging directory {staging_dir} does not exist. Skipping standalone packaging.")
        return

    print(f"Packaging X17U Slim MOD: {out_zip.name}...")
    with zipfile.ZipFile(out_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
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

    print(f"Packaged: {out_zip} ({out_zip.stat().st_size:,} bytes)")

if __name__ == '__main__':
    main()
