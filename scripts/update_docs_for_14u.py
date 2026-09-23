import os
import shutil

repo_readme = r"C:\Users\ASTA\OneDrive\Документы\GitHub\Mi_Master_Camera_Combo\README.md"
antigravity_readme = r"C:\Users\ASTA\OneDrive\Antigravity\README.md"

with open(repo_readme, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Update Subtitle
sub_old = "### Universal Flagship Suite for Xiaomi 13 Ultra, 15, 15 Pro, 15 Ultra & 17 Ultra\n#### HyperOS 2.0 / HyperOS 3.0 • Android 15 / Android 16 (API 35/36)"
sub_new = "### Universal Flagship Suite for Xiaomi 13 Ultra, 14 Ultra, 15, 15 Pro, 15 Ultra & 17 Ultra\n#### HyperOS 1.0 / HyperOS 2.0 / HyperOS 3.0 • Android 14 / Android 15 / Android 16 (API 34/35/36)"
if sub_old in c:
    c = c.replace(sub_old, sub_new, 1)
    print("1. Subtitle updated")
else:
    print("Warning: Subtitle not found")

# 2. Section 1 RU customize.sh device list
sec1_ru_old = "(`ishtar`, `dada`, `haotian`, `xuanyuan` или `nezha`)"
sec1_ru_new = "(`ishtar`, `aurora`, `dada`, `haotian`, `xuanyuan` или `nezha`)"
if sec1_ru_old in c:
    c = c.replace(sec1_ru_old, sec1_ru_new, 1)
    print("2. Section 1 RU updated")

# 3. Section 2 RU Supported devices table
sec2_ru_target = """| **Xiaomi 13 Ultra** | `ishtar` | Snapdragon 8 Gen 2 | 1" Sony IMX989 + 3x IMX858 + OV32C | **0.5x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15** | `dada` | Snapdragon 8 Elite | Light Hunter 900 + JN1 + JN5 + OV32B | **0.6x : 1.0x : 3.2x** |"""

sec2_ru_replacement = """| **Xiaomi 13 Ultra** | `ishtar` | Snapdragon 8 Gen 2 | 1" Sony IMX989 + 3x IMX858 + OV32C | **0.5x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 14 Ultra** | `aurora` | Snapdragon 8 Gen 3 | 1" Sony LYT-900 (F1.63-F4.0) + 3x IMX858 + OV32B | **0.5x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15** | `dada` | Snapdragon 8 Elite | Light Hunter 900 + JN1 + JN5 + OV32B | **0.6x : 1.0x : 3.2x** |"""

if sec2_ru_target in c:
    c = c.replace(sec2_ru_target, sec2_ru_replacement, 1)
    print("3. Section 2 RU updated")

# 4. Section 3 RU Download tables
sec3_uni_ru_old = "#### 🌐 Универсальные комбайны для всей линейки (13U, 15, 15 Pro, 15U, 17U)"
sec3_uni_ru_new = "#### 🌐 Универсальные комбайны для всей линейки (13U, 14U, 15, 15 Pro, 15U, 17U)"
if sec3_uni_ru_old in c:
    c = c.replace(sec3_uni_ru_old, sec3_uni_ru_new, 1)
    print("4. Section 3 RU Universal heading updated")

sec3_dev_ru_target = """| **Xiaomi 13 Ultra** (`ishtar`) | **[`Mi13U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_Full_by_borndead.zip)** (146.15 МБ) | **[`Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip)** (270.2 КБ) | Quad-50M (`0.5x:1.0x:3.2x:5.0x`), George Video 8K/4K120, DCG HDR, калибровки IMX989/IMX858, оффлайн-обработка *(для HOS 1.0 A14 доступен архив [HOS1_A14](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip))*. |
| **Xiaomi 17 Ultra** (`nezha`) |"""

sec3_dev_ru_replacement = """| **Xiaomi 13 Ultra** (`ishtar`) | **[`Mi13U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_Full_by_borndead.zip)** (146.15 МБ) | **[`Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip)** (270.2 КБ) | Quad-50M (`0.5x:1.0x:3.2x:5.0x`), George Video 8K/4K120, DCG HDR, калибровки IMX989/IMX858, оффлайн-обработка *(для HOS 1.0 A14 доступен архив [HOS1_A14](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip))*. |
| **Xiaomi 14 Ultra** (`aurora`) | **[`Mi14U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi14U_Master_Camera_Combo_Full_by_borndead.zip)** (145.89 МБ) | **[`Mi14U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi14U_Master_Imaging_MOD_Slim_by_borndead.zip)** (5.03 КБ) | Quad-50M (`0.5x:1.0x:3.2x:5.0x`), бесступенчатая переменная диафрагма F1.63–F4.0, 1" Sony LYT-900, George Video 8K/4K120, DCG Hardware HDR, обход облачной обработки. |
| **Xiaomi 17 Ultra** (`nezha`) |"""

if sec3_dev_ru_target in c:
    c = c.replace(sec3_dev_ru_target, sec3_dev_ru_replacement, 1)
    print("5. Section 3 RU Device table updated")

# 5. Section 4 RU Presets table
sec4_ru_target = """| **Xiaomi 13 Ultra** (`ishtar`) | Sony IMX989 + 3x IMX858 | **[`Mi13U_borndead_Universal_Leica_50MP.agc`](./configs/Xiaomi_13_Ultra_ishtar/Mi13U_borndead_Universal_Leica_50MP.agc)** | 50Мп RAW16 на всех 4 линзах, Black Level 64, Leica Authentic матрица, HDR+ Enhanced |
| **Xiaomi 15 Ultra** (`xuanyuan`) |"""

sec4_ru_replacement = """| **Xiaomi 13 Ultra** (`ishtar`) | Sony IMX989 + 3x IMX858 | **[`Mi13U_borndead_Universal_Leica_50MP.agc`](./configs/Xiaomi_13_Ultra_ishtar/Mi13U_borndead_Universal_Leica_50MP.agc)** | 50Мп RAW16 на всех 4 линзах, Black Level 64, Leica Authentic матрица, HDR+ Enhanced |
| **Xiaomi 14 Ultra** (`aurora`) | 1" Sony LYT-900 + 3x IMX858 | **[`Mi14U_borndead_Universal_Leica_LYT900_Quad50M.agc`](./configs/Xiaomi_14_Ultra_aurora/Mi14U_borndead_Universal_Leica_LYT900_Quad50M.agc)** | 50Мп RAW16 на всех 4 линзах, переменная диафрагма F1.63-F4.0, Black Level 64, Leica Authentic, DCG HDR |
| **Xiaomi 15 Ultra** (`xuanyuan`) |"""

if sec4_ru_target in c:
    c = c.replace(sec4_ru_target, sec4_ru_replacement, 1)
    print("6. Section 4 RU Presets table updated")

# 6. Section 7 RU step 1
sec7_ru_target = "(`Mi13U`, `X17U`, `Mi15U`, `Mi15`)"
sec7_ru_new = "(`Mi13U`, `Mi14U`, `X17U`, `Mi15U`, `Mi15`)"
if sec7_ru_target in c:
    c = c.replace(sec7_ru_target, sec7_ru_new, 1)
    print("7. Section 7 RU step 1 updated")

# 7. Section 8.2 RU Target device verification
sec82_ru_target = """##### 📱 Xiaomi 13 Ultra (`ishtar`)"""
sec82_ru_replacement = """##### 📱 Xiaomi 14 Ultra (`aurora`)
* **Сетка Quad-50M (Mode 175)**:
  - В режиме «50M» проверьте все 4 фокусных расстояния: **`0.5x : 1.0x : 3.2x : 5.0x`**.
  - Все 4 сенсора (1" Sony LYT-900 + 3x Sony IMX858) выводят честные **`8192 x 6144`** (50 Мп).
* **Бесступенчатая физическая диафрагма (F1.63 – F4.0)**:
  - В режиме «Профи» или «Видео» переключите диафрагму между значениями F1.63, F2.0, F2.8, F4.0 — лепестки физической диафрагмы на основном модуле плавно реагируют в реальном времени.
* **1-дюймовый сенсор Sony LYT-900 и аппаратный DCG HDR**:
  - Аппаратное объединение LCG/HCG на сенсоре LYT-900 обеспечивает расширенный динамический диапазон с одного кадра, исключая размытие движущихся объектов и пересветы.
* **Видео 8K со всех линз и 4K 120fps**:
  - Запись 8K 24/30fps доступна на всех объективах (0.5x, 1x, 3.2x, 5x) без ограничения по времени; режим 4K 120fps обеспечивает идеальную плавность слоу-мо.
* **Google Камера (GCam)**:
  - Пресет `Mi14U_borndead_Universal_Leica_LYT900_Quad50M.agc` в AGC 9.6 открывает переключение всех 4 камер с поддержкой 50Мп RAW16 и ручного шага диафрагмы.

##### 📱 Xiaomi 13 Ultra (`ishtar`)"""

if sec82_ru_target in c:
    c = c.replace(sec82_ru_target, sec82_ru_replacement, 1)
    print("8. Section 8.2 RU added 14U")

# 8. Section 1 EN customize.sh device list
sec1_en_old = "(`ishtar`, `dada`, `haotian`, `xuanyuan`, or `nezha`)"
sec1_en_new = "(`ishtar`, `aurora`, `dada`, `haotian`, `xuanyuan`, or `nezha`)"
if sec1_en_old in c:
    c = c.replace(sec1_en_old, sec1_en_new, 1)
    print("9. Section 1 EN updated")

# 9. Section 2 EN Supported devices table
sec2_en_target = """| **Xiaomi 13 Ultra** | `ishtar` | Snapdragon 8 Gen 2 | 1" Sony IMX989 + 3x IMX858 + OV32C | **0.5x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15** | `dada` | Snapdragon 8 Elite | Light Hunter 900 + JN1 + JN5 + OV32B | **0.6x : 1.0x : 3.2x** |"""

sec2_en_replacement = """| **Xiaomi 13 Ultra** | `ishtar` | Snapdragon 8 Gen 2 | 1" Sony IMX989 + 3x IMX858 + OV32C | **0.5x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 14 Ultra** | `aurora` | Snapdragon 8 Gen 3 | 1" Sony LYT-900 (F1.63-F4.0) + 3x IMX858 + OV32B | **0.5x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15** | `dada` | Snapdragon 8 Elite | Light Hunter 900 + JN1 + JN5 + OV32B | **0.6x : 1.0x : 3.2x** |"""

if sec2_en_target in c:
    c = c.replace(sec2_en_target, sec2_en_replacement, 1)
    print("10. Section 2 EN updated")

# 10. Section 3 EN Download tables
sec3_uni_en_old = "#### 🌐 Universal Multi-Device Packages (13U, 15, 15 Pro, 15U, 17U)"
sec3_uni_en_new = "#### 🌐 Universal Multi-Device Packages (13U, 14U, 15, 15 Pro, 15U, 17U)"
if sec3_uni_en_old in c:
    c = c.replace(sec3_uni_en_old, sec3_uni_en_new, 1)
    print("11. Section 3 EN Universal heading updated")

sec3_dev_en_target = """| **Xiaomi 13 Ultra** (`ishtar`) | **[`Mi13U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_Full_by_borndead.zip)** (146.15 MB) | **[`Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip)** (270.2 KB) | Quad-50M (`0.5x:1.0x:3.2x:5.0x`), George Video 8K/4K120, DCG HDR, IMX989/IMX858 tunings, offline processing *(for legacy HOS 1.0 A14 see [HOS1_A14](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip))*. |
| **Xiaomi 17 Ultra** (`nezha`) |"""

sec3_dev_en_replacement = """| **Xiaomi 13 Ultra** (`ishtar`) | **[`Mi13U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_Full_by_borndead.zip)** (146.15 MB) | **[`Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_Slim_by_borndead.zip)** (270.2 KB) | Quad-50M (`0.5x:1.0x:3.2x:5.0x`), George Video 8K/4K120, DCG HDR, IMX989/IMX858 tunings, offline processing *(for legacy HOS 1.0 A14 see [HOS1_A14](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip))*. |
| **Xiaomi 14 Ultra** (`aurora`) | **[`Mi14U_Master_Camera_Combo_Full_by_borndead.zip`](./releases/Mi14U_Master_Camera_Combo_Full_by_borndead.zip)** (145.89 MB) | **[`Mi14U_Master_Imaging_MOD_Slim_by_borndead.zip`](./releases/Mi14U_Master_Imaging_MOD_Slim_by_borndead.zip)** (5.03 KB) | Quad-50M (`0.5x:1.0x:3.2x:5.0x`), stepless variable aperture F1.63-F4.0, 1" Sony LYT-900, George Video 8K/4K120, DCG Hardware HDR, offline processing bypass. |
| **Xiaomi 17 Ultra** (`nezha`) |"""

if sec3_dev_en_target in c:
    c = c.replace(sec3_dev_en_target, sec3_dev_en_replacement, 1)
    print("12. Section 3 EN Device table updated")

# 11. Section 4 EN Presets table
sec4_en_target = """| **Xiaomi 13 Ultra** (`ishtar`) | Sony IMX989 + 3x IMX858 | **[`Mi13U_borndead_Universal_Leica_50MP.agc`](./configs/Xiaomi_13_Ultra_ishtar/Mi13U_borndead_Universal_Leica_50MP.agc)** | 50MP RAW16 on all 4 lenses, Black Level 64, Leica Authentic color matrix, HDR+ Enhanced |
| **Xiaomi 15 Ultra** (`xuanyuan`) |"""

sec4_en_replacement = """| **Xiaomi 13 Ultra** (`ishtar`) | Sony IMX989 + 3x IMX858 | **[`Mi13U_borndead_Universal_Leica_50MP.agc`](./configs/Xiaomi_13_Ultra_ishtar/Mi13U_borndead_Universal_Leica_50MP.agc)** | 50MP RAW16 on all 4 lenses, Black Level 64, Leica Authentic color matrix, HDR+ Enhanced |
| **Xiaomi 14 Ultra** (`aurora`) | 1" Sony LYT-900 + 3x IMX858 | **[`Mi14U_borndead_Universal_Leica_LYT900_Quad50M.agc`](./configs/Xiaomi_14_Ultra_aurora/Mi14U_borndead_Universal_Leica_LYT900_Quad50M.agc)** | 50MP RAW16 on all 4 lenses, variable aperture F1.63-F4.0, Black Level 64, Leica Authentic, DCG HDR |
| **Xiaomi 15 Ultra** (`xuanyuan`) |"""

if sec4_en_target in c:
    c = c.replace(sec4_en_target, sec4_en_replacement, 1)
    print("13. Section 4 EN Presets table updated")

# 12. Section 7 EN step 1
sec7_en_target = "(`Mi13U`, `X17U`, `Mi15U`, `Mi15`)"
sec7_en_new = "(`Mi13U`, `Mi14U`, `X17U`, `Mi15U`, `Mi15`)"
if sec7_en_target in c:
    c = c.replace(sec7_en_target, sec7_en_new, 1)
    print("14. Section 7 EN step 1 updated")

# 13. Section 8.2 EN Target device verification
sec82_en_target = """##### 📱 Xiaomi 13 Ultra (`ishtar`)"""
sec82_en_replacement = """##### 📱 Xiaomi 14 Ultra (`aurora`)
* **Quad-50M Zoom Grid (Mode 175)**:
  - In «50M» mode, verify all 4 focal lengths: **`0.5x : 1.0x : 3.2x : 5.0x`**.
  - All 4 cameras (1" Sony LYT-900 + 3x Sony IMX858) output full **`8192 x 6144`** (50 MP).
* **Stepless Variable Physical Aperture (F1.63 – F4.0)**:
  - In Pro mode or Video mode, switch aperture between F1.63, F2.0, F2.8, F4.0 — physical aperture iris blades on the main LYT-900 module actuate smoothly in real time.
* **1-inch Sony LYT-900 Sensor & Hardware DCG HDR**:
  - Direct hardware LCG/HCG readout on the LYT-900 sensor prevents motion ghosting on fast subjects while preventing clipping in highlights.
* **8K Video All Lenses & 4K 120fps**:
  - Full 8K 24/30fps video recording is available across all 4 rear sensors without artificial limits; 4K 120fps provides butter-smooth high-framerate action recording.
* **Google Camera (GCam)**:
  - Profile `Mi14U_borndead_Universal_Leica_LYT900_Quad50M.agc` in AGC 9.6 enables seamless switching across all 4 cameras with 50MP RAW16 and manual aperture control.

##### 📱 Xiaomi 13 Ultra (`ishtar`)"""

if sec82_en_target in c:
    c = c.replace(sec82_en_target, sec82_en_replacement, 1)
    print("15. Section 8.2 EN added 14U")

with open(repo_readme, "w", encoding="utf-8", newline="\n") as f:
    f.write(c)
print(f"Successfully saved {repo_readme}")

with open(antigravity_readme, "w", encoding="utf-8", newline="\n") as f:
    f.write(c)
print(f"Successfully mirrored to {antigravity_readme}")
