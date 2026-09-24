# Changelog

All notable changes to the **Xiaomi Master Camera Combo** project will be documented in this file.

## [v6.8-Production-Cleanup] - 2026-09-24
### Optimized
- **Repository Bloat & Obsolete Release Purge (~1.44 GB Freed)**:
  - Removed 13 obsolete duplicate aliases, intermediate beta packages, and fragmented legacy archives from `releases/` (`Mi13U_Master_Camera_Combo_v5.0/v5.1`, `Mi15U_X17U_v5.0/v5.1`, `Mi15_v5.0`, `Universal_MultiDevice`, separate AI sub-tiers, and legacy beta overlays).
  - Consolidated release distribution to strictly 16 canonical, production-grade assets: FULL & SLIM per flagship (`ishtar`, `aurora`, `dada`/`haotian`, `xuanyuan`, `nezha`), Universal Multi-Device (FULL & SLIM), Leica 13U Port v6.8, Leica Configs Master Pack, and the unified AI Suite All-In-One.
  - Purged 19 obsolete scratch and one-off generator scripts from `scripts/`, retaining 10 modular, active build and verification utilities.
  - Optimized packaging scripts (`build_full_and_slim_lineup.py`, `fix_ishtar_bootloop_modules.py`) to prevent duplicate archive generation.
  - Performed Git LFS garbage collection (`git lfs prune`), removing 145 dangling LFS objects.
- **Documentation & History Synchronization**:
  - Restored and integrated complete version history and changelog directly into `README.md` (RU and EN) and `CHANGELOG.md`.

## [v6.8-Ishtar-Port-MasterPack] - 2026-09-24
### Added
- **Exclusive Leica Camera v6.8 (6.8.001960.0) Port for Xiaomi 13 Ultra (`ishtar`)**:
  - `Mi13U_Camera_v6.8_Port_by_borndead.zip` (141.6 MB).
  - Ported and adapted latest Leica Camera app specifically optimized for Snapdragon 8 Gen 2.
- **Leica 13U Configs Master Pack**:
  - `Leica_13U_Configs_Master_Pack.zip` (4.7 KB).
  - Handcrafted tuning profiles for Leica Camera & GCam (AGC 8.x/9.x, LMC) with authentic Leica color science, Black Level 64, and Quad-50M RAW16 support.
### Fixed
- **1.6MP Chi-CDK Fallback Bug**: Resolved offline graph timeout in Qualcomm Chi-CDK pipeline; native 12.5MP and 50MP capture restored without preview buffer fallback (1440x1080).
- **200MP Mode & Thermal Throttle**: Stripped non-functional 200MP UI mode (13U has 50MP sensors) and eliminated continuous zoom sensor polling loop, resolving CPU overheating and battery drain.
- **Front Camera Dual Video Distortion**: Fixed aspect ratio calculation for OmniVision OV32C sensor in Dual Video mode, restoring 4:3 geometry instead of forced 16:9 stretch.
- **AI Scene Recognition**: Bypassed AISP 2.0 hard dependency (`o2() -> 0`), restoring full AI scene classification on Snapdragon 8 Gen 2 ISP.
- **AI Capture Assist Authentication**: Restored network auth pipe enabling direct Xiaomi Account sign-in.
- **SAT Multi-Camera Session Stability**: Sanitized `vendor.camera.aux.packagelist` for smooth lens transitions without driver arbitration hangs.

## [v6.0-AI-Suite-Ecosystem] - 2026-09-23
### Added
- **3-Tier AI Photography Suite (AI Suite)**:
  - **Tier 1 (AISP Hardware)**: Qualcomm Hexagon NPU computational photography acceleration for ultra-fast noise reduction and dynamic range expansion.
  - **Tier 2 (HyperAI Studio)**: On-device generative AI tools in Gallery and ExtraPhoto editor (generative eraser, smart image expansion).
  - **Tier 3 (AI Director & Vision HUD)**: Real-time viewfinder assistant providing composition rules, framing guidance, and horizon leveling HUD.
  - **Unified All-In-One Package**: `Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip` containing all three tiers with zero system APK modification.
- **Smart Multi-Module Synchronization**:
  - Installer-level configuration merge logic in `customize.sh` allowing simultaneous installation of FULL/SLIM modules alongside AI Suite without OverlayFS masking conflicts.

## [v5.12-HyperOS4-Compatibility] - 2026-09-24
### Fixed
- **Next-Gen Android 17 / HyperOS 4.x Compatibility (Xiaomi 17 Ultra `nezha`)**:
  - Fixed `vold` mount conflicts during late-stage boot.
  - Resolved `system.prop` string length overflow on newer Android property services.
  - Implemented surgical bind-mount for `device_features` XML to prevent partition remount failures.

## [v5.11-Full-Slim-Architecture] - 2026-09-23
### Added
- **Dedicated Dual-Tier (FULL & SLIM) Architecture Across Entire Lineup**:
  - Established explicit two-tier lineup for every supported device:
    - **FULL Edition**: modified Leica Camera APK with `oat/.replace` ART crash protection, 49 native ARM64 companion libraries, safe privapp permissions (`REBOOT`/`DEVICE_POWER` stripped).
    - **SLIM Edition**: 100% Pure Systemless Overlay, 0% risk of bootloop, 0 bytes touched in `priv-app/MiuiCamera`.
  - Built dedicated packages for `ishtar`, `aurora`, `dada`/`haotian`, `xuanyuan`, `nezha`, and Universal Multi-Device.

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
