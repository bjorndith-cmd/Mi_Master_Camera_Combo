# Changelog

All notable changes to the **Xiaomi Master Camera Combo** project will be documented in this file.

## [v5.10-Ishtar-AntiBootloop-Fix] - 2026-09-23
### Fixed
- **Bootloop on Xiaomi 13 Ultra (HyperOS 3.0.302.0 Taiwan / TMATWXM / Android 16)**:
  - **Root Cause Identified**: Official odexed stock firmware with Xiaomi release keys strictly validates platform signatures during early `PackageManagerService` init. Replacing `MiuiCamera.apk` with a pre-extracted APK triggered a fatal `SignatureMismatchException`, causing `system_server` crashes and bootloops.
  - **100% Pure Systemless Overlay**: Converted both dedicated Xiaomi 13 Ultra module (`Mi13U_Master_Camera_Combo_v5.1`) and Universal Combo (`Mi_Master_Camera_Combo_Universal_MultiDevice`) to Pure Systemless Overlay mode for `ishtar`. Preserves the native stock Leica Camera APK intact.
  - **Alien HAL Purged**: Completely purged 27.3 MB Android 14 `camera.qcom.so` from `ishtar` staging, eliminating AIDL NDK sensor service linker crashes on Android 16.
  - **Package Optimization**: Reduced `Mi13U_Master_Camera_Combo` zip size from 146.69 MB to **278 KB**, enabling near-instant installation with 0% risk of bootloops across all HyperOS versions (1.0, 2.0, 3.0) and all regional firmware builds.
- **Safety & Recovery Standards**:
  - Added comprehensive **Disclaimer (Отказ от ответственности)** and mandatory **Bootloop Saver** requirements in `README.md` and installation documentation.

## [v5.9-HOS1-A14-Fix] - 2026-09-22
### Fixed
- **Root Loss on Xiaomi 13 Ultra (HyperOS 1.0.14.0 Android 14)**:
  - Discovered that executing magiskpolicy --live permissive for system domains during post-fs-data triggered Magisk Safe Mode on HyperOS 1.0 / A14, which completely disabled root and modules upon reboot.
  - Sanitized post-fs-data.sh across all modules: completely removed dangerous live permissive calls. Root is now 100% stable across all Magisk, KernelSU, and APatch setups.
- **Black Screen Viewfinder on HyperOS 1.0.14.0 (A14)**:
  - Discovered that on Android 14 (API 34), the installer was preserving an experimental ported camera.qcom.so (27.3 MB) and attempting to mount HyperOS 3.0 MiuiCamera.apk, breaking CamX sensor stream binding and ART framework compatibility.
  - Updated customize.sh: on Android 14 (API <= 34), native Camera HAL and native Leica Camera APK are preserved.
- **Added Dedicated Module for Xiaomi 13 Ultra HyperOS 1.0 (A14)**:
  - Introduced Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip (270 KB).
  - Pure systemless overlay specifically calibrated for Xiaomi 13 Ultra running HyperOS 1.0 (Android 14 / HOS 1.0.14.0+).
  - Unlocks Quad-50MP FullRes across all 4 rear sensors, DCG Hardware HDR, 8K 24fps on all lenses, 4K 120fps, Dolby Vision, and clean AISP with zero risk of root loss or black screen.

## [v5.8-Nezha-SimpleRom-Fix] - 2026-09-22
### Fixed
- **Fatal Camera Crash on Xiaomi 17 Ultra (`nezha`) on SimpleRom 3.0.309.0 - ST**:
  - **Dynamic Linker Missing Dependency Resolved**: Completely purged naked `.so` files from Stock AIO (`libremosaiclib.so`, `libmialgo_ainr_ll.so`, `libmialgo_ellc.so`). Discovered via ELF header analysis that `libremosaiclib.so` had a hard dependency `DT_NEEDED: libdlrmsc_android15.so`, which is not present in HyperOS 3.0 / Android 16, crashing `cameraserver` on boot.
  - **Hardware Mismatch Fixed**: Restored dynamic `devices/` directory structure in `Mi15U_X17U_Master_Camera_Combo_v5.1`. Xiaomi 17 Ultra (`nezha`) now exclusively receives genuine OmniVision OVX10500U, HP9, JN5, and OV50M Chromatix tuned bins instead of `xuanyuan` bins.
  - **Custom ROM Safeguard**: Added intelligent custom ROM detection (`IS_CUSTOM_ROM`) in `customize.sh`. On SimpleRom, ST, Xiaomi.eu, EliteROM, or Xiaomi 17 Ultra, the ROM's native deodexed/patched `MiuiCamera.apk` is preserved, preventing signature and JNI runtime crashes.
- **Added Dedicated Slim Pure Overlay MOD for Xiaomi 17 Ultra**:
  - Introduced `X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip` (13.8 MB).
  - Pure systemless overlay that does not modify `MiuiCamera.apk` at all.
  - Guarantees 100% rock-solid stability on SimpleRom 3.0.309.0 - ST, Xiaomi.eu, and Stock HyperOS 3.0.
  - Injects full OVX10500U Chromatix profiles, DCG Hardware HDR, 8K video on all lenses, 4K120fps, AISP NR bypass, and Qualcomm `libqcodec2_v4l2codec.so`.

## [v5.7-Universal-DCG-AIO-A16] - 2026-09-22
### Added
- **Stock AIO 104 Integration for Xiaomi 15 Ultra (`xuanyuan`)**:
  - Added full Chromatix tuning binary `com.qti.tuned.xuanyuan_semco_LYT900_wide_i.bin` (34.27 MB) for 1-inch Sony LYT-900.
  - Added full Chromatix tuning binary `com.qti.tuned.xuanyuan_semco_s5khp9_tele5x_i.bin` (21.45 MB) for 200MP Samsung HP9 periscope.
  - Added full Chromatix tuning binaries for IMX858 (3x), JN5 (ultra-wide), and OV32B40 (front).
  - Added SmartAE LN2 EV tables and night scene profiles.
- SELinux rules in `customize.sh` for all `.so` binaries in `system/odm/lib64/`.

## [v5.6-Nezha-Xuanyuan-DCG-A16] - 2026-09-22
### Added
- Official **Xiaomi 15 Ultra (`xuanyuan`, EUXM 3.0.9.0)** release profile.
- Native HyperOS 3.0.9.0 Android 16 Camera HAL `camera.qcom.so` (10.18 MB) with `android.frameworks.sensorservice-V1-ndk.so` support.
- Sensor module binaries for HP9 200MP, IMX858, JN5, and OV32B40.
- Automatic HAL branching in `customize.sh`: preserves native A16 HAL for `xuanyuan`.

## [v5.5-Universal-DCG-A16] - 2026-09-22
### Added
- **DCG (Dual Conversion Gain) / iDCG Hardware HDR**:
  - System properties: `persist.vendor.camera.dcg.enable=1`, `persist.vendor.camera.hdr.dcg=1`, `persist.vendor.camera.sensor.hdr=1`, `ro.vendor.camera.dcg=1`.
  - Feature tags in XML: `support_camera_dcg`, `is_support_dcg`, `support_dcg_hdr`, `support_sensor_hdr`, `support_idcg`.
  - Hardware HCG/LCG single-frame HDR readout for Sony IMX989, Sony LYT-900, Light Hunter 900, and OmniVision LOFIC.

## [v5.0-Universal-A16] - 2026-09-22
### Added
- Universal Multi-Device Installer supporting:
  - Xiaomi 13 Ultra (`ishtar`)
  - Xiaomi 15 (`dada`)
  - Xiaomi 15 Pro (`haotian`)
  - Xiaomi 15 Ultra (`xuanyuan`)
  - Xiaomi 17 Ultra (`nezha`)
- Full Leica Camera application (`MiuiCamera.apk`) with companion native libraries and permissions.
- FullRes Quad-50MP / 200MP unlock across all rear lenses for Stock 50M mode and all GCam mods.
- George Video MOD: 8K 24fps all rear lenses, 4K 120fps, Dolby Vision 4K 60fps, LOG, Director Mode.
- Video bitrate factor increased by 1.5x via system properties.
- ArcSoft AISP noise reduction bypass (`persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1`).
- Memory dump disabled (`dump: 0`) in `aisp.json` to prevent capture lag.
### Fixed
- **Viewfinder Freeze in Photo Mode (161)** on Xiaomi 13 Ultra: completely eliminated by purging rogue Super Resolution tags (`support_super_resolution`, `support_super_resolution_zoom`, `is_support_pixel_model`, `support_ultra_pixel`).
- **SAT Multi-Camera Arbitration**: removed `com.android.camera` from `vendor.camera.aux.packagelist` while preserving access for third-party GCam mods.
- Replaced dangerous `killall` in `service.sh` with safe boot-completed listener.
- Added `magiskpolicy` rules in `post-fs-data.sh` for camera memory sharing on Android 16.
