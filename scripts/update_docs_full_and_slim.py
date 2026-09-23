import os, shutil

readme_path = r'C:\Users\ASTA\OneDrive\Документы\GitHub\Mi_Master_Camera_Combo\README.md'
changelog_path = r'C:\Users\ASTA\OneDrive\Документы\GitHub\Mi_Master_Camera_Combo\CHANGELOG.md'
audit_path = r'C:\Users\ASTA\OneDrive\Документы\GitHub\Mi_Master_Camera_Combo\DETAILED_AUDIT_REPORT.md'

with open(readme_path, 'r', encoding='utf-8') as f:
    readme = f.read()

# -------------------------------------------------------------
# 1. NEW DUAL-TIER TABLES FOR README.md
# -------------------------------------------------------------
# Russian Table
table_ru_new = """### 3. Таблица модулей и ссылки на загрузку (RU)

Модули разделены на две чёткие категории:
* 🌟 **FULL Edition (с приложением камеры)**: Включает полнофункциональное приложение камеры Leica из HyperOS 3.0 со всеми интерфейсными возможностями, новыми водяными знаками, новыми фильтрами и режимами Leica. Оснащен защитой `oat/.replace` (предотвращает краш ART на проверке odex), очищен от опасных платформенных разрешений (`REBOOT`, `DEVICE_POWER`) и конфликтующих системных библиотек.
* ⚡ **SLIM Edition (без приложения камеры / Pure Systemless Overlay)**: Чистый системный оверлей. Не затрагивает системный APK камеры. Идеален для максимальной безопасности (0% риска конфликтов подписей), для официальных закрытых прошивок без CorePatch, а также для кастомных прошивок (SimpleRom ST, Xiaomi.eu), где камера уже модифицирована авторами ROM. Разблокирует 50М/200М FullRes, George Video MOD 8K/4K120, DCG Hardware HDR, Chromatix калибровки и фикс розового шума.

#### 🌐 Универсальные комбайны для всей линейки (13U, 15, 15 Pro, 15U, 17U)
| Модуль | Размер | Тип | Описание |
|---|---|---|---|
| **[`Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip)** | **182.52 МБ** | **FULL** | **Универсальный полный комбайн**. Включает приложение камеры Leica HyperOS 3.0, авто-определение любого устройства линейки, калибровки Chromatix, 50M/200M FullRes, George Video 8K/4K120fps, DCG HDR и защиту `oat/.replace`. |
| **[`Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip)** | **36.63 МБ** | **SLIM** | **Универсальный чистый оверлей (без APK)**. 100% безопасность на любых прошивках. Включает калибровки под все 5 моделей, 50M/200M, 8K видео и DCG HDR. |

#### 📱 Специализированные модули по моделям

| Модель | Версия FULL (с APK камеры) | Версия SLIM (чистый оверлей без APK) | Особенности профиля |
|---|---|---|---|
| **Xiaomi 13 Ultra** (`ishtar`) | **[`Mi13U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_Full_by_borndead.zip)** (146.15 МБ) | **[`Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip)** (270.2 КБ) | Quad-50M (`0.5x:1.0x:3.2x:5.0x`), George Video 8K/4K120, DCG HDR, калибровки IMX989/IMX858, оффлайн-обработка *(для HOS 1.0 A14 доступен архив [HOS1_A14](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip))*. |
| **Xiaomi 17 Ultra** (`nezha`) | **[`X17U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/X17U_Master_Camera_Combo_Full_by_borndead.zip)** (159.74 МБ) | **[`X17U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/X17U_Master_Imaging_MOD_Slim_by_borndead.zip)** (13.85 МБ) | Кастомные калибровки OVX10500U/HP9/JN5, DCG HDR, 8K все линзы, 4K120fps, кодек `libqcodec2` *(для SimpleRom ST без Leica доступен [SimpleRom_ST](./releases/X17U_Master_Imaging_MOD_SimpleRom_ST_NonLeica_by_borndead.zip))*. |
| **Xiaomi 15 Ultra** (`xuanyuan`) | **[`Mi15U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi15U_Master_Camera_Combo_Full_by_borndead.zip)** (163.27 МБ) | **[`Mi15U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi15U_Master_Imaging_MOD_Slim_by_borndead.zip)** (17.38 МБ) | Официальные калибровки Stock AIO 104 для 1" Sony LYT-900 и 200Мп Samsung HP9, нативный A16 HAL, ночной режим SmartAE LN2. |
| **Xiaomi 15 / 15 Pro** (`dada`/`haotian`) | **[`Mi15_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi15_Master_Camera_Combo_Full_by_borndead.zip)** (151.04 МБ) | **[`Mi15_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi15_Master_Imaging_MOD_Slim_by_borndead.zip)** (5.15 МБ) | Калибровки Light Hunter 900, 50Мп FullRes на 1.0x (на 15) и на всех линзах (на 15 Pro), DCG HDR. |"""

# English Table
table_en_new = """### 3. Module Releases & Download Links (EN)

Modules are organized into two distinct, production-ready tiers:
* 🌟 **FULL Edition (with Leica Camera App)**: Includes the complete, updated Leica Camera app from HyperOS 3.0 with all UI features, new Leica watermarks, Leica Authentic/Vibrant styles, and shooting modes. Features `oat/.replace` protection (prevents ART OdexFile checksum mismatch), purged dangerous platform permissions (`REBOOT`, `DEVICE_POWER`), and clean companion libraries.
* ⚡ **SLIM Edition (Pure Systemless Overlay - No Camera APK)**: Systemless overlay that preserves your existing Camera APK untouched. Designed for maximum safety (0% risk of signature conflicts), ideal for locked stock ROMs without CorePatch, as well as custom ROMs (SimpleRom ST, Xiaomi.eu) where the camera is pre-patched by ROM developers. Unlocks 50M/200M FullRes, George Video MOD 8K/4K120, DCG Hardware HDR, Chromatix hardware tunings, and offline processing.

#### 🌐 Universal Multi-Device Packages (13U, 15, 15 Pro, 15U, 17U)
| Module Package | Size | Tier | Description |
|---|---|---|---|
| **[`Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip)** | **182.52 MB** | **FULL** | **Universal Full Flagship Suite**. Includes HyperOS 3.0 Leica Camera APK, dynamic multi-device hardware detection, Chromatix tunings for all 5 phones, 50M/200M FullRes, George 8K/4K120, DCG HDR, and `oat/.replace` protection. |
| **[`Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip)** | **36.63 MB** | **SLIM** | **Universal Pure Systemless Overlay (No APK)**. 100% safe on any ROM. Injects Chromatix sensor profiles for all 5 devices, 50M/200M, 8K video, and DCG HDR without touching the Camera APK. |

#### 📱 Dedicated Per-Device Packages

| Target Hardware | FULL Edition (with Leica Camera App) | SLIM Edition (Pure Overlay - No APK) | Highlights |
|---|---|---|---|
| **Xiaomi 13 Ultra** (`ishtar`) | **[`Mi13U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_Full_by_borndead.zip)** (146.15 MB) | **[`Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip)** (270.2 KB) | Quad-50M (`0.5x:1.0x:3.2x:5.0x`), George Video 8K/4K120, DCG HDR, IMX989/IMX858 tunings, offline processing *(for HOS 1.0 A14 see [HOS1_A14](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip))*. |
| **Xiaomi 17 Ultra** (`nezha`) | **[`X17U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/X17U_Master_Camera_Combo_Full_by_borndead.zip)** (159.74 MB) | **[`X17U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/X17U_Master_Imaging_MOD_Slim_by_borndead.zip)** (13.85 MB) | Dedicated OVX10500U/HP9/JN5 Chromatix tunings, DCG HDR, 8K all lenses, 4K120fps, `libqcodec2` *(for SimpleRom ST without Leica see [SimpleRom_ST](./releases/X17U_Master_Imaging_MOD_SimpleRom_ST_NonLeica_by_borndead.zip))*. |
| **Xiaomi 15 Ultra** (`xuanyuan`) | **[`Mi15U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi15U_Master_Camera_Combo_Full_by_borndead.zip)** (163.27 MB) | **[`Mi15U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi15U_Master_Imaging_MOD_Slim_by_borndead.zip)** (17.38 MB) | Official Stock AIO 104 Chromatix tunings for 1" Sony LYT-900 & 200MP Samsung HP9, native A16 HAL, SmartAE LN2 night mode. |
| **Xiaomi 15 / 15 Pro** (`dada`/`haotian`) | **[`Mi15_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi15_Master_Camera_Combo_Full_by_borndead.zip)** (151.04 MB) | **[`Mi15_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi15_Master_Imaging_MOD_Slim_by_borndead.zip)** (5.15 MB) | Light Hunter 900 tunings, 50MP FullRes on 1.0x (for 15) and all rear lenses (for 15 Pro), DCG HDR. |"""

# Locate old table RU
start_ru_tbl = readme.find('### 3. Таблица модулей и ссылки на загрузку (RU)')
end_ru_tbl = readme.find('### 4. Готовые пресеты конфигураций GCam (.agc) (RU)')
if start_ru_tbl != -1 and end_ru_tbl != -1:
    readme = readme[:start_ru_tbl] + table_ru_new + '\n\n---\n\n' + readme[end_ru_tbl:]
    print("[OK] Replaced Russian Table of Modules")

# Locate old table EN
start_en_tbl = readme.find('### 3. Module Releases & Download Links (EN)')
end_en_tbl = readme.find('### 4. Ready-to-Use GCam Config Presets (.agc) (EN)')
if start_en_tbl != -1 and end_en_tbl != -1:
    readme = readme[:start_en_tbl] + table_en_new + '\n\n---\n\n' + readme[end_en_tbl:]
    print("[OK] Replaced English Table of Modules")

with open(readme_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(readme)
print("[OK] README.md updated with full dual-tier lineup")

shutil.copy2(readme_path, r'C:\Users\ASTA\OneDrive\Antigravity\README.md')
print("[OK] Mirrored README.md to Antigravity root")
