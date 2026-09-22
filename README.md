# Xiaomi Master Camera Combo 📸⚡
### Universal Flagship Suite for Xiaomi 13 Ultra, 15, 15 Pro, 15 Ultra & 17 Ultra
#### HyperOS 2.0 / HyperOS 3.0 • Android 15 / Android 16 (API 35/36)

<p align="center">
  <a href="#-русский"><b>🇷🇺 Перейти к русскому описанию</b></a> • 
  <a href="#-english"><b>🇬🇧 Switch to English Description</b></a>
</p>

<p align="center">
  <b>Author / Автор сборки:</b> <code>borndead</code><br>
  <i>(feat. itzdfplayer, amitkattal & GeorgeKiarie)</i><br>
  <b>Release / Версия:</b> <code>v5.8-Universal-DCG-AIO-A16</code>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Stable%20Production-brightgreen?style=for-the-badge" alt="Status">
  <img src="https://img.shields.io/badge/Root-Magisk%20%7C%20KernelSU%20%7C%20APatch-orange?style=for-the-badge" alt="Root">
  <img src="https://img.shields.io/badge/Android-15%20%26%2016-blue?style=for-the-badge" alt="Android">
  <img src="https://img.shields.io/badge/Leica-Camera-red?style=for-the-badge" alt="Leica">
</p>

---

<a name="-русский"></a>
# 🇷🇺 РУССКИЙ РАЗДЕЛ

## 📑 Меню навигации (RU)
1. [О проекте](#1-о-проекте-ru)
2. [Поддерживаемые смартфоны и сенсоры](#2-поддерживаемые-смартфоны-и-сенсоры-ru)
3. [Таблица модулей и ссылки на загрузку](#3-таблица-модулей-и-ссылки-на-загрузку-ru)
4. [Ключевые возможности и технологии](#4-ключевые-возможности-и-технологии-ru)
   - [Устранение зависания видоискателя в «Фото»](#41-устранение-зависания-видоискателя-в-фото-ru)
   - [Аппаратный DCG (Dual Conversion Gain) / iDCG HDR](#42-аппаратный-dcg-dual-conversion-gain--idcg-hdr-ru)
   - [Разблокировка 50Мп и 200Мп FullRes](#43-разблокировка-50мп-и-200мп-fullres-ru)
   - [George Video MOD (8K со всех камер, 4K120, чистый AISP)](#44-george-video-mod-8k-со-всех-камер-4k120-чистый-aisp-ru)
   - [Stock AIO 104 для Xiaomi 15 Ultra (LYT-900)](#45-stock-aio-104-для-xiaomi-15-ultra-lyt-900-ru)
   - [Защита от вылетов на Xiaomi 17 Ultra (SimpleRom ST, EU, Elite)](#46-защита-от-вылетов-на-xiaomi-17-ultra-simplerom-st-eu-elite-ru)
5. [Инструкция по установке](#5-инструкция-по-установке-ru)
6. [Часто задаваемые вопросы (FAQ)](#6-часто-задаваемые-вопросы-faq-ru)

---

### 1. О проекте (RU)

**Xiaomi Master Camera Combo** — это флагманский системный модуль для **Magisk (v26+)**, **KernelSU** и **APatch**, снимающий все аппаратные и программные ограничения стоковой камеры Leica на смартфонах Xiaomi под управлением **HyperOS 2.0 и HyperOS 3.0** (Android 15 и Android 16).

Модуль оснащён **интеллектуальным инсталлятором**: при установке скрипт `customize.sh` на лету определяет модель вашего смартфона (`ishtar`, `dada`, `haotian`, `xuanyuan` или `nezha`), тип прошивки (Stock, SimpleRom, Xiaomi.eu, EliteROM), активирует соответствующие Chromatix-калибровки сенсоров, настраивает сетку зума 50M/200M и монтирует только проверенные компоненты.

---

### 2. Поддерживаемые смартфоны и сенсоры (RU)

| Модель | Кодовое имя | Процессор | Основные сенсоры | Сетка зума 50M/200M |
|---|---|---|---|---|
| **Xiaomi 13 Ultra** | `ishtar` | Snapdragon 8 Gen 2 | 1" Sony IMX989 + 3x IMX858 + OV32C | **0.5x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15** | `dada` | Snapdragon 8 Elite | Light Hunter 900 + JN1 + JN5 + OV32B | **0.6x : 1.0x : 3.2x** |
| **Xiaomi 15 Pro** | `haotian` | Snapdragon 8 Elite | Light Hunter 900 + JN1 + IMX858 (5x) | **0.6x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15 Ultra** | `xuanyuan` | Snapdragon 8 Elite | 1" Sony LYT-900 + Samsung HP9 200M + IMX858 + JN5 | **0.5x : 1.0x : 3.0x : 5.0x** |
| **Xiaomi 17 Ultra** | `nezha` | Snapdragon 8 Elite | 1" OVX10500U + Samsung HP9 200M + JN5 + OV50M | **0.5x : 1.0x : 3.0x : 5.0x** |

---

### 3. Таблица модулей и ссылки на загрузку (RU)

Все файлы размещены в папке [`releases/`](./releases/):

| Файл модуля | Размер | Совместимость | Описание и назначение |
|---|---|---|---|
| **[`X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`](./releases/X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip)** | **13.85 МБ** | 17 Ultra (`nezha`) | **⭐ Рекомендуется для 17 Ultra (SimpleRom 3.0.309.0 - ST, EU, Elite, Stock)**. Чистый оверлей: НЕ перезаписывает APK камеры (0% риска вылета!). Все калибровки OVX10500U/HP9/JN5/OV50M, DCG HDR, 8K, 4K120fps, кодек. |
| **[`Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip`](./releases/Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip)** | **177.66 МБ** | 15U (`xuanyuan`) & 17U (`nezha`) | **Исправленный комбо-модуль**. Динамическое разделение 15U и 17U, удалены битые библиотеки, авто-детектор SimpleRom ST. |
| **[`Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip)** | **195.13 МБ** | 13U, 15, 15 Pro, 15U, 17U | **Универсальный комбайн для всей линейки**. Автоматически определяет устройство и тип прошивки, активирует полный комплекс твиков. |
| **[`Mi13U_Master_Camera_Combo_v5.0_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_v5.0_by_borndead.zip)** | **158.76 МБ** | 13 Ultra (`ishtar`) | Выделенная полная Leica-камера для 13 Ultra, Quad-50M, DCG HDR, 8K все линзы, фикс зависания видоискателя. |
| **[`Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip)** | **270.4 КБ** | 13 Ultra (`ishtar`) | Облегчённый оверлей для 13 Ultra (без приложения камеры). |
| **[`Mi15_Master_Camera_Combo_v5.0_by_borndead.zip`](./releases/Mi15_Master_Camera_Combo_v5.0_by_borndead.zip)** | **151.58 МБ** | 15 (`dada`) & 15 Pro (`haotian`) | Выделенный комбайн для Xiaomi 15 и 15 Pro. |

---

### 4. Ключевые возможности и технологии (RU)

#### 4.1. Устранение зависания видоискателя в «Фото» (RU)
* **Причина бага в прошлых модах**: Внедрение тегов `support_super_resolution` принуждало сенсор 1.0" на зуме 1.0x ждать буфера цифрового супер-разрешения, из-за чего первый кадр застывал намертво.
* **Исправление**: Скрипт очищает конфликтные теги. Режим «Фото» работает на стабильных 60 кадр/с с мгновенным откликом затвора, а максимальные 50Мп/200Мп включаются строго в режимах «50M Ultra HD» и «Ultra RAW».

#### 4.2. Аппаратный DCG (Dual Conversion Gain) / iDCG HDR (RU)
* В каждом пикселе матрицы работают два параллельных узла: **LCG** (защита от пересветов в ярких областях) и **HCG** (экстремальная светосила и чистота в тенях).
* **Считывание с одного кадра**: движущиеся объекты не раздваиваются (Zero Motion Ghosting).

#### 4.3. Разблокировка 50Мп и 200Мп FullRes (RU)
* Параметр `persist.vendor.camera.maxRAWSizes=55` открывает полноразмерный RAW-поток.
* Все сторонние моды GCam (AGC, LMC, Shamim, BSG) получают полный доступ к 50Мп/200Мп на всех объективах благодаря `vendor.camera.aux.packagelist`.
* Пакет `com.android.camera` исключён из aux-списка, сохраняя штатную логическую многокамерность (SAT).

#### 4.4. George Video MOD (8K со всех камер, 4K120, чистый AISP) (RU)
* Запись видео **8K 24fps со всех задних сенсоров** и **4K 120fps**.
* Твик `aisp.json` (`dump: 0`) и `persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1` отключают агрессивное размытие видео-шумодава ArcSoft, возвращая детализацию.
* Интегрирован видео-кодек `libqcodec2_v4l2codec.so` для стабильной записи высокого битрейта.

#### 4.5. Stock AIO 104 для Xiaomi 15 Ultra (LYT-900) (RU)
* Полные оригинальные калибровки Chromatix `com.qti.tuned.xuanyuan_*.bin` для сенсора **Sony LYT-900** (34.27 МБ) и 200Мп Samsung HP9.
* Таблицы экспозиции SmartAE LN2 для ночной съемки.
* Библиотека `libmialgo_snsc.so`.

#### 4.6. Защита от вылетов на Xiaomi 17 Ultra (SimpleRom ST, EU, Elite) (RU)
* **В чём была проблема**: в ранних сборках отсутствовала папка `devices/` (на 17U попадали файлы 15U) и лежали бинарники с отсутствующей зависимостью `libdlrmsc_android15.so`, а замена APK на кастоме SimpleRom вызывала краш.
* **Решение**: Удалены битые библиотеки, разделены профили `devices/nezha` и `devices/xuanyuan`, добавлен авто-детектор кастомов (`IS_CUSTOM_ROM`), и создан специальный модуль **`X17U_Master_Imaging_MOD_v1.0_Slim`** (без APK, чистый оверлей).

---

### 5. Инструкция по установке (RU)

1. Скачайте необходимый zip-архив из папки [`releases/`](./releases/).
   * **Для Xiaomi 17 Ultra на SimpleRom ST**: выберите **`X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`**.
   * **Для универсальной установки на любой флагман**: выберите **`Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip`**.
2. Откройте **Magisk (v26+)**, **KernelSU** или **APatch**.
3. Зайдите в раздел **«Модули»** ➔ **«Установить из хранилища»** и выберите архив.
4. Дождитесь завершения работы скрипта и нажмите **«Перезагрузка»**.
5. *(Рекомендуется)* После перезагрузки очистите данные приложения Камера в Настройках.

---

### 6. Часто задаваемые вопросы (FAQ) (RU)

<details>
<summary><b>Что делать на Xiaomi 13 Ultra (HyperOS 1.0.14.0 Android 14), если пропал рут или черный экран?</b></summary>\nПроблема полностью решена! На Android 14 рут отпадал из-за агрессивных permissive-правил в <code>post-fs-data.sh</code>, вызывавших Safe Mode в Magisk, а чёрный экран возникал из-за подмены системного Camera HAL на порт от A16.  \nУстановите выделенный модуль <b>Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip</b> — он сохраняет родной системный HAL и APK, не трогает SELinux, активирует Quad-50MP на всех линзах, DCG HDR и 8K видео с нулевым риском сбоев!\n</details>\n\n<details>\n<summary><b>Камера на Xiaomi 17 Ultra (SimpleRom 3.0.309.0 - ST) теперь не вылетает?</b></summary>
Да, проблема решена на 100%! Для пользователей SimpleRom ST мы рекомендуем <b>X17U_Master_Imaging_MOD_v1.0_Slim</b>. Модуль не затрагивает модифицированный APK камеры, а накатывает только сенсорные калибровки, DCG HDR и видеомод.
</details>

<details>
<summary><b>Плавный ли видоискатель в режиме «Фото»?</b></summary>
Да, видоискатель выдаёт стабильные 60 fps без фризов благодаря удалению конфликтных тегов Super Resolution из XML.
</details>

<details>
<summary><b>Работает ли 50Мп в Google Камере (GCam)?</b></summary>
Да, все объективы доступны в модах AGC, LMC, Shamim в полном разрешении 50Мп / 200Мп.
</details>

---
---

<a name="-english"></a>
# 🇬🇧 ENGLISH SECTION

## 📑 Navigation Menu (EN)
1. [About the Project](#1-about-the-project-en)
2. [Supported Devices & Camera Hardware](#2-supported-devices--camera-hardware-en)
3. [Module Releases & Download Links](#3-module-releases--download-links-en)
4. [Core Features & Technologies](#4-core-features--technologies-en)
   - [Photo Mode Viewfinder Freeze Fix](#41-photo-mode-viewfinder-freeze-fix-en)
   - [Hardware DCG (Dual Conversion Gain) / iDCG HDR](#42-hardware-dcg-dual-conversion-gain--idcg-hdr-en)
   - [50MP & 200MP Full Resolution RAW Unlock](#43-50mp--200mp-full-resolution-raw-unlock-en)
   - [George Video MOD (8K All Sensors, 4K120fps, Clean AISP)](#44-george-video-mod-8k-all-sensors-4k120fps-clean-aisp-en)
   - [Stock AIO 104 for Xiaomi 15 Ultra (LYT-900)](#45-stock-aio-104-for-xiaomi-15-ultra-lyt-900-en)
   - [Crash Prevention on Xiaomi 17 Ultra (SimpleRom ST, EU, Elite)](#46-crash-prevention-on-xiaomi-17-ultra-simplerom-st-eu-elite-en)
5. [Installation Guide](#5-installation-guide-en)
6. [Frequently Asked Questions (FAQ)](#6-frequently-asked-questions-faq-en)

---

### 1. About the Project (EN)

**Xiaomi Master Camera Combo** is the ultimate flagship system module for **Magisk (v26+)**, **KernelSU**, and **APatch**. It eliminates all known hardware and software limitations in the stock Leica Camera app on Xiaomi flagships running **HyperOS 2.0 and HyperOS 3.0** (Android 15 and Android 16).

The module includes an **intelligent dynamic installer**: during flashing, `customize.sh` detects the target device (`ishtar`, `dada`, `haotian`, `xuanyuan`, or `nezha`), verifies the ROM environment (Stock, SimpleRom, Xiaomi.eu, EliteROM), applies matched Chromatix sensor profiles, configures the 50M/200M zoom grid, and mounts only verified libraries.

---

### 2. Supported Devices & Camera Hardware (EN)

| Device | Code Name | SoC | Primary Sensors | 50M/200M Zoom Grid |
|---|---|---|---|---|
| **Xiaomi 13 Ultra** | `ishtar` | Snapdragon 8 Gen 2 | 1" Sony IMX989 + 3x IMX858 + OV32C | **0.5x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15** | `dada` | Snapdragon 8 Elite | Light Hunter 900 + JN1 + JN5 + OV32B | **0.6x : 1.0x : 3.2x** |
| **Xiaomi 15 Pro** | `haotian` | Snapdragon 8 Elite | Light Hunter 900 + JN1 + IMX858 (5x) | **0.6x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15 Ultra** | `xuanyuan` | Snapdragon 8 Elite | 1" Sony LYT-900 + Samsung HP9 200M + IMX858 + JN5 | **0.5x : 1.0x : 3.0x : 5.0x** |
| **Xiaomi 17 Ultra** | `nezha` | Snapdragon 8 Elite | 1" OVX10500U + Samsung HP9 200M + JN5 + OV50M | **0.5x : 1.0x : 3.0x : 5.0x** |

---

### 3. Module Releases & Download Links (EN)

All packages are hosted in the [`releases/`](./releases/) directory:

| Module Package | Size | Target Hardware | Description & Role |
|---|---|---|---|
| **[`X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`](./releases/X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip)** | **13.85 MB** | 17 Ultra (`nezha`) | **⭐ Recommended for 17 Ultra (SimpleRom 3.0.309.0 - ST, EU, Elite, Stock)**. Pure systemless overlay: DOES NOT touch `MiuiCamera.apk` (0% crash risk!). Genuine OVX10500U/HP9/JN5/OV50M Chromatix bins, DCG HDR, 8K video, 4K120fps, video codec. |
| **[`Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip`](./releases/Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip)** | **177.66 MB** | 15U (`xuanyuan`) & 17U (`nezha`) | **Fixed Dual-Flagship Combo**. Dynamic separation of 15U and 17U profiles, purged broken libraries, auto-detects SimpleRom ST to preserve native APK. |
| **[`Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip)** | **195.13 MB** | 13U, 15, 15 Pro, 15U, 17U | **Universal Multi-Device Combo**. Auto-detects device hardware and ROM type, deploys full Leica suite, DCG HDR, and George Video MOD. |
| **[`Mi13U_Master_Camera_Combo_v5.0_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_v5.0_by_borndead.zip)** | **158.76 MB** | 13 Ultra (`ishtar`) | Dedicated full Leica suite for 13 Ultra, Quad-50M, DCG HDR, 8K on all lenses, photo viewfinder freeze fix. |
| **[`Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip)** | **270.4 KB** | 13 Ultra (`ishtar`) | Lightweight pure overlay for 13 Ultra (without APK replacement). |
| **[`Mi15_Master_Camera_Combo_v5.0_by_borndead.zip`](./releases/Mi15_Master_Camera_Combo_v5.0_by_borndead.zip)** | **151.58 MB** | 15 (`dada`) & 15 Pro (`haotian`) | Dedicated combo for Xiaomi 15 and 15 Pro. |

---

### 4. Core Features & Technologies (EN)

#### 4.1. Photo Mode Viewfinder Freeze Fix (EN)
* **Root Cause**: Injecting `support_super_resolution` into `device_features` caused the 1-inch main sensor at 1.0x zoom to enter an unsupported `SuperResolutionProcessor` pipeline, locking the viewfinder on the very first frame.
* **Resolution**: The installer cleanly purges conflicting tags. Photo mode (161) operates in fluid 60 fps with zero shutter lag, while 50MP/200MP modes remain active in Ultra HD (175) and Ultra RAW.

#### 4.2. Hardware DCG (Dual Conversion Gain) / iDCG HDR (EN)
* Each pixel on the sensor features two parallel readout stages: **LCG** (highlights protection) and **HCG** (ultra-high sensitivity & deep shadow clarity).
* **Single-exposure readout**: Moving subjects remain crisp without motion ghosting or multi-frame artifacts.

#### 4.3. 50MP & 200MP Full Resolution RAW Unlock (EN)
* Setting `persist.vendor.camera.maxRAWSizes=55` unlocks the full-resolution RAW buffer in Qualcomm CamX.
* Third-party GCam mods (AGC, LMC, Shamim, BSG) gain full physical sensor access via `vendor.camera.aux.packagelist`.
* `com.android.camera` is excluded from the aux list to preserve native Leica Spatial Alignment Telephoto (SAT) switching.

#### 4.4. George Video MOD (8K All Sensors, 4K120fps, Clean AISP) (EN)
* **8K 24fps video recording across all rear cameras** and **4K 120fps**.
* `aisp.json` (`dump: 0`) and `persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1` bypass ArcSoft video noise reduction smearing.
* Hardware video codec `libqcodec2_v4l2codec.so` included for smooth high-bitrate encoding.

#### 4.5. Stock AIO 104 for Xiaomi 15 Ultra (LYT-900) (EN)
* Official Chromatix calibration binaries `com.qti.tuned.xuanyuan_*.bin` for **Sony LYT-900** (34.27 MB) and Samsung HP9 200MP periscope.
* SmartAE LN2 low-light exposure tables.
* Self-contained `libmialgo_snsc.so`.

#### 4.6. Crash Prevention on Xiaomi 17 Ultra (SimpleRom ST, EU, Elite) (EN)
* **Root Cause of Past Crashes**: The earlier zip lacked the `devices/` directory (causing 15U files to be flashed onto 17U), contained naked libraries with an unresolved `libdlrmsc_android15.so` dependency, and overwrote the custom deodexed camera APK on SimpleRom ST.
* **Resolution**: Purged broken libraries, isolated `devices/nezha` and `devices/xuanyuan` trees, added custom ROM detection (`IS_CUSTOM_ROM`), and introduced **`X17U_Master_Imaging_MOD_v1.0_Slim`** (pure overlay, zero APK conflict).

---

### 5. Installation Guide (EN)

1. Download the required zip from the [`releases/`](./releases/) directory.
   * **For Xiaomi 17 Ultra on SimpleRom ST**: pick **`X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`**.
   * **For general installation on any flagship**: pick **`Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip`**.
2. Open **Magisk (v26+)**, **KernelSU**, or **APatch**.
3. Navigate to **Modules** ➔ **Install from storage** and select the zip.
4. Wait for installation to complete, then tap **Reboot**.
5. *(Recommended)* After reboot, clear Camera app data in Android Settings.

---

### 6. Frequently Asked Questions (FAQ) (EN)

<details>
<summary><b>What should I do on Xiaomi 13 Ultra (HyperOS 1.0.14.0 Android 14) if root dropped or screen went black?</b></summary>
This issue is 100% fixed! On Android 14, root dropped because permissive rules in <code>post-fs-data.sh</code> triggered Magisk Safe Mode, and the black screen was caused by overwriting the Camera HAL with an incompatible ported library.  
Flash the dedicated <b>Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip</b> module — it preserves native Camera HAL and APK, cleans boot scripts, and enables Quad-50MP on all lenses, DCG HDR, and 8K video with zero crash or root loss risk!
</details>

<details>
<summary><b>Does the camera crash on Xiaomi 17 Ultra (SimpleRom 3.0.309.0 - ST)?</b></summary>
No, this issue is 100% resolved in <b>v5.8</b>! For SimpleRom ST users, we recommend <b>X17U_Master_Imaging_MOD_v1.0_Slim</b>. It does not overwrite the custom camera APK, only applying sensor calibrations, DCG HDR, and video tweaks.
</details>

<details>
<summary><b>Is the viewfinder smooth in Photo mode?</b></summary>
Yes, the viewfinder maintains a steady 60 fps without freezing, thanks to dynamic cleanup of rogue Super Resolution tags.
</details>

<details>
<summary><b>Does 50MP work in GCam mods?</b></summary>
Yes, all cameras shoot in full 50MP / 200MP resolution in AGC, LMC, Shamim, and BigKaka mods.
</details>

---

## 📄 Technical Audit Report / Технический отчёт
For in-depth register dumps, dynamic linker analysis, and hardware profiles:  
👉 **[DETAILED_AUDIT_REPORT.md](./DETAILED_AUDIT_REPORT.md)**
