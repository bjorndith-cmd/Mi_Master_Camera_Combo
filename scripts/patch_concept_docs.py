import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
readme_path = os.path.join(repo_root, 'README.md')
audit_path = os.path.join(repo_root, 'DETAILED_AUDIT_REPORT.md')

with open(readme_path, 'r', encoding='utf-8') as f:
    readme = f.read()

# 1. Update English Section 5.7 and 5.8
old_en_sec = """#### 5.7. Pure Systemless Overlay Architecture & Xiaomi 13 Ultra Bootloop Elimination (Taiwan HyperOS 3.0 / A16) (EN)
* **Incident Root Cause (Bootloop on Taiwan Official ROM `TMATWXM`)**:
  - Official stock HyperOS 3.0 (Android 16) firmware builds (such as Taiwan `OS3.0.302.0.TMATWXM`, Global `TMAMIXM`, and EEA `TMAEUXM`) use strict Xiaomi Release Key platform signatures and an odexed structure (`/product/priv-app/MiuiCamera/oat/arm64/MiuiCamera.odex`).
  - Attempting to overwrite `MiuiCamera.apk` with a pre-extracted APK caused Android 16's early `PackageManagerService` boot scan to throw a fatal `SignatureMismatchException`, crashing `system_server` into an infinite bootloop.
  - Bundled companion libraries (`libc++.so`, `libion.so`, `libdmabufheap.so`) in the APK directory also disrupted Android 16 linker dependencies.
* **Core Architectural Insight**:
  - **Xiaomi 13 Ultra (`ishtar`) comes with genuine Leica Camera from the factory!** It does NOT require any system Camera APK replacement!
* **Comprehensive Engineering Resolution (v5.2 / v5.8)**:
  1. **100% Pure Systemless Overlay**:
     - In `Mi13U_Master_Camera_Combo_v5.1` (and the universal `Mi_Master_Camera_Combo_Universal_MultiDevice`), the system camera APK is **NEVER REPLACED** (`rm -rf $MODPATH/system/priv-app/MiuiCamera`).
     - The dedicated 13 Ultra package size was reduced from 146 MB to **278 KB**, installing in less than a second.
  2. **Alien HAL Removal**:
     - The 27.3 MB legacy Android 14 `camera.qcom.so` was completely purged from the `ishtar` profile, eliminating AIDL NDK cameraserver crashes on Android 16.
  3. **All Flagship Features Injected Systemlessly**:
     - **Quad-50M FullRes** grid (`0.5x : 1.0x : 3.2x : 5.0x`) injected dynamically via `device_features/ishtar.xml`;
     - Hardware **DCG HDR**, **8K video across all 4 rear sensors**, and **4K120fps** unlocked via XML and `system.prop`;
     - Genuine Chromatix sensor calibration binaries (`com.qti.sensormodule.ishtar_*.bin`) for IMX989, IMX858, and OV32C mounted to `/system/odm/lib64/camera/`;
     - Cloud processing bypass enforced (`support_cloud_process=false`), ensuring all photos develop locally on the ISP without delays or magenta artifacts.
* **Result**: Rock-solid stability with 0% risk of bootloop across all official and custom ROMs (Taiwan, Global, EEA, China, Russia, custom ROMs).

#### 5.7. Next-Gen Firmware Compatibility (HyperOS 4.x / Android 17): Testing on Xiaomi 17 Ultra (`nezha`) (EN)"""

new_en_sec = """#### 5.7. Dual-Tier Architectural Concept (FULL & SLIM) & Xiaomi 13 Ultra Bootloop Elimination (Taiwan HyperOS 3.0 / A16) (EN)
* **Incident Root Cause (Bootloop on Stock Taiwan `TMATWXM`)**:
  - Official stock HyperOS 3.0 (Android 16) firmware builds (such as Taiwan `OS3.0.302.0.TMATWXM`, Global `TMAMIXM`, and EEA `TMAEUXM`) enforce strict signature validation with Xiaomi Release Keys and utilize an optimized odex/vdex layout (`/product/priv-app/MiuiCamera/oat/arm64/MiuiCamera.odex`).
  - Replacing `MiuiCamera.apk` with a pre-extracted APK without proper runtime isolation caused Android 16's early `PackageManagerService` boot scan to trigger a fatal `SignatureMismatchException` or ART odex checksum error, crashing `system_server` into an infinite bootloop.
  - Furthermore, incompatible companion libraries (`libc++.so`, `libion.so`, `libdmabufheap.so`) broke Android 16 linker dependencies, and root-level `$MODPATH/product` injection masked core partitions in OverlayFS.
* **Unified Architectural Concept: FULL with Upgraded APK vs. SLIM Without APK**:
  - **Why replace the stock camera in FULL Edition?** Even on devices that ship with factory Leica optics and software (Xiaomi 13 Ultra, 14 Ultra, 15 Pro, 15 Ultra, 17 Ultra), we **replace the stock camera with our improved, modded Leica Camera APK**! Our upgraded camera unlocks the latest HyperOS 3.0 Leica framework: an expanded collection of exclusive Leica custom watermarks, frames, and branding, refined Leica Authentic / Vibrant color science, Master Lens portrait presets, full 50M/200M/8K mode toggles inside the main viewfinder interface, and zero-delay offline hardware ISP processing.
  - **Why choose SLIM Edition?** Designed for users on locked official stock regional ROMs (Taiwan, Global, EEA) without CorePatch/LSPosed, as well as preview test builds (HyperOS 4). SLIM preserves your device's native camera APK untouched (100% immune to signature checks and odex bootloops), while unlocking the complete hardware potential through a pure systemless overlay: Chromatix sensor tunings, DCG HDR, 50M/200M Quad-Bayer Remosaic, George Video 8K/4K120, and pink noise cloud bypass.
* **Comprehensive Engineering Solutions**:
  1. **FULL Edition (with Upgraded Leica Camera APK — ~146 MB)**:
     - Protected by **`oat/.replace`**: creating `.replace` and `.nomedia` markers in the `oat` directory hides stale stock odex/vdex files from PMS, forcing ART to cleanly recompile our upgraded APK;
     - Sanitized **`privapp-permissions-camera.xml`**: completely removed dangerous platform permissions (`REBOOT`, `DEVICE_POWER`, `MANAGE_USERS`) that trigger PMS validation panics;
     - Purged hazardous system library overrides (`libc++.so`, `libion.so`, `libdmabufheap.so`);
     - Purged legacy 27.3 MB Android 14 `camera.qcom.so`;
     - Eliminates partition masking: all overlay files reside strictly under `$MODPATH/system/`, safeguarding `/storage/emulated/0` mount integrity;
     - *Recommendation:* On strict official stock ROMs with platform signature enforcement, CorePatch (via LSPosed) is required to run FULL, OR choose SLIM Edition.
  2. **SLIM Edition (Pure Systemless Overlay - Zero APK Replacement — 270 KB)**:
     - The system camera APK is **NEVER REPLACED** (`rm -rf $MODPATH/system/priv-app/MiuiCamera`);
     - 0% bootloop risk, 1-second installation, fully compatible with locked stock and custom ROMs without CorePatch;
     - **Quad-50M FullRes** grid (`0.5x : 1.0x : 3.2x : 5.0x`) injected dynamically via `device_features/ishtar.xml`;
     - Hardware **DCG HDR**, **8K video across all 4 rear sensors**, and **4K120fps** unlocked via XML & `system.prop`;
     - Genuine Chromatix sensor calibration binaries (`com.qti.sensormodule.ishtar_*.bin`) for IMX989, IMX858, and OV32C mounted to `/system/odm/lib64/camera/`;
     - Cloud processing bypassed (`support_cloud_process=false`), ensuring instant local hardware processing without delays or magenta artifacts.
* **Outcome**: Complete freedom of choice: select FULL for the ultimate feature set of our upgraded Leica camera, or choose SLIM for 100% stock app peace of mind with full hardware unlocked!

#### 5.8. Next-Gen Firmware Compatibility (HyperOS 4.x / Android 17): Testing on Xiaomi 17 Ultra (`nezha`) (EN)"""

norm_readme = readme.replace('\r\n', '\n')
norm_old = old_en_sec.replace('\r\n', '\n')
norm_new = new_en_sec.replace('\r\n', '\n')
if norm_old in norm_readme:
    norm_readme = norm_readme.replace(norm_old, norm_new)
    print("[OK] Replaced Section 5.7 & 5.8 (EN)")
else:
    print("[FAIL] Could not match English section")

# 2. Add FAQ item in English Section 10
old_en_faq = """<details>
<summary><b>Does 50MP work in GCam mods?</b></summary>

Yes, all cameras shoot in full 50MP / 200MP resolution in AGC, LMC, Shamim, and BigKaka mods.
</details>"""

new_en_faq = """<details>
<summary><b>Does 50MP work in GCam mods?</b></summary>

Yes, all cameras shoot in full 50MP / 200MP resolution in AGC, LMC, Shamim, and BigKaka mods.
</details>

<details>
<summary><b>What is the difference between FULL and SLIM editions? Why replace the stock camera in FULL if Xiaomi 13 Ultra already has Leica from the factory?</b></summary>

* **FULL Edition (Replacing stock camera with our improved Leica Camera)**:
  - In FULL Edition, we replace the stock camera with our **improved, modded Leica Camera**! It incorporates the latest HyperOS 3.0 Leica code base, an expanded collection of exclusive Leica custom watermarks, frames, and branding, enhanced Leica Authentic / Vibrant color rendering, Master Lens portrait presets, full 50M/200M/8K direct viewfinder toggles, and built-in `oat/.replace` anti-bootloop protection.
  - *Best for:* Users on custom ROMs (Xiaomi.eu, Elite, SimpleRom) or stock ROMs with CorePatch (via LSPosed) enabled who want the ultimate suite of new Leica features.
* **SLIM Edition (Pure Systemless Overlay - No Camera APK Replacement)**:
  - Does not touch the system camera APK at all (`rm -rf $MODPATH/system/priv-app/MiuiCamera`), keeping the ROM's pre-installed app untouched.
  - *Best for:* Ideal for closed official regional stock ROMs (Taiwan, Global, EEA) without CorePatch where Android strictly enforces platform signature validation, as well as preview test builds (HyperOS 4). You get 100% bootloop immunity while unlocking the full hardware potential of the sensors (DCG HDR, 50M/200M FullRes, George Video 8K/4K120fps, Chromatix tunings).
</details>"""

norm_old_faq = old_en_faq.replace('\r\n', '\n')
norm_new_faq = new_en_faq.replace('\r\n', '\n')
if norm_old_faq in norm_readme:
    norm_readme = norm_readme.replace(norm_old_faq, norm_new_faq)
    print("[OK] Added FAQ entry in English Section 10")
else:
    print("[FAIL] Could not match English FAQ")

with open(readme_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(norm_readme)

print(f"[OK] README.md written at {readme_path}")

# 3. Update DETAILED_AUDIT_REPORT.md Section 9.3
with open(audit_path, 'r', encoding='utf-8') as f:
    audit = f.read()

old_audit_sec = """### 9.3. Инженерное решение
* **Ключевой факт**: Xiaomi 13 Ultra является флагманом с официальной оптикой и ПО Leica с момента выхода с конвейера. Ни на одной прошивке ему не требуется замена APK камеры!
* **Реализация**:
  1. Из модуля `Mi13U_Master_Camera_Combo` полностью удалена папка `system/priv-app/MiuiCamera` и файл разрешений. Модуль стал **100% Pure Systemless Overlay**.
  2. Из `Mi_MultiDevice_Combo_Staging` полностью удален каталог `devices/ishtar/odm/lib64/hw`.
  3. В `customize.sh` обоих модулей добавлено правило: устройство `ishtar` никогда не перезаписывает APK камеры.
  4. Сетка Quad-50M FullRes (`0.5x:1.0x:3.2x:5.0x`), George Video Mod (8K все линзы, 4K120fps), DCG HDR и Chromatix сенсорные калибровки внедряются исключительно через безопасный динамический оверлей `device_features/ishtar.xml`, `system.prop` и `system/odm/lib64/camera/`.
  5. В документацию добавлены строгий отказ от ответственности (Disclaimer) и руководство по обязательной установке модулей защиты от бутлупа (**Bootloop Saver**)."""

new_audit_sec = """### 9.3. Инженерное решение: Единая дуальная архитектура (FULL & SLIM)
* **Архитектурный принцип**:
  - **FULL Edition (с заменой стоковой камеры на нашу улучшенную)**: Даже на устройствах с заводской камерой Leica (Xiaomi 13 Ultra, 14 Ultra, 15 Pro, 15 Ultra, 17 Ultra) мы **заменяем стоковую камеру на нашу улучшенную модифицированную Leica Камеру**! В ней разблокированы новейшие возможности HyperOS 3.0: расширенный набор авторских водяных знаков Leica, улучшенные режимы Leica Authentic/Vibrant, Master Lens портретные профили, прямое переключение 50M/200M/8K в видоискателе и встроенная защита от бутлупа (`oat/.replace`, санитизация `privapp-permissions`, чистый `lib/arm64`). Рекомендуется для кастомных прошивок и стоков с CorePatch (LSPosed).
  - **SLIM Edition (чистый системный оверлей — без APK камеры)**: Для закрытых официальных региональных стоковых прошивок (Тайвань, Глобал, EEA) без CorePatch, а также для тестовых сборок нового поколения (HyperOS 4). Не затрагивает системный APK камеры вообще (`rm -rf $MODPATH/system/priv-app/MiuiCamera`), обеспечивая 100% иммунитет к проверке подписей платформы (`SignatureMismatchException`), при этом активируя весь аппаратный потенциал матрицы (DCG HDR, 50M/200M FullRes, George Video 8K/4K120fps, калибровки Chromatix).
* **Техническая реализация**:
  1. В модулях **FULL Edition** развернут комплекс анти-бутлуп защиты: маркер `oat/.replace`, удаление опасных системных библиотек (`libc++.so`, `libion.so`, `libdmabufheap.so`), удаление платформенных прав (`REBOOT`, `DEVICE_POWER`, `MANAGE_USERS`), строгая изоляция всех оверлеев в `$MODPATH/system/` (защита от маскирования разделов в OverlayFS).
  2. В модулях **SLIM Edition** папка `system/priv-app/MiuiCamera` удалена целиком. Модуль представляет собой **100% Pure Systemless Overlay** размером ~270 КБ.
  3. Из всех профилей удален устаревший 27.3 МБ `camera.qcom.so` (HAL от старой Android 14), вызывавший сбои AIDL NDK.
  4. Сетка Quad-50M FullRes (`0.5x:1.0x:3.2x:5.0x`), George Video Mod (8K все линзы, 4K120fps), DCG HDR и Chromatix сенсорные калибровки внедряются через безопасный динамический оверлей `device_features/ishtar.xml`, `system.prop` и `system/odm/lib64/camera/`.
  5. В документацию добавлены строгий отказ от ответственности (Disclaimer), протокол устранения конфликтов сторонних модулей и руководство по обязательной установке модулей защиты от бутлупа (**Bootloop Saver**)."""

norm_audit = audit.replace('\r\n', '\n')
norm_old_audit = old_audit_sec.replace('\r\n', '\n')
norm_new_audit = new_audit_sec.replace('\r\n', '\n')
if norm_old_audit in norm_audit:
    norm_audit = norm_audit.replace(norm_old_audit, norm_new_audit)
    print("[OK] Updated DETAILED_AUDIT_REPORT.md Section 9.3")
else:
    print("[FAIL] Could not match Section 9.3 in DETAILED_AUDIT_REPORT.md")

with open(audit_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(norm_audit)

print(f"[OK] DETAILED_AUDIT_REPORT.md written at {audit_path}")
