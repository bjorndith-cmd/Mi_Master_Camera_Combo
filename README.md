<p align="center">
  <img src="./assets/LOGO_G.jpg" alt="Mi Master Camera Combo Banner" width="100%">
</p>

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
4. [Готовые пресеты конфигураций GCam (.agc)](#4-готовые-пресеты-конфигураций-gcam-agc-ru)
5. [Ключевые возможности и технологии](#5-ключевые-возможности-и-технологии-ru)
   - [Устранение зависания видоискателя в «Фото»](#51-устранение-зависания-видоискателя-в-фото-ru)
   - [Аппаратный DCG (Dual Conversion Gain) / iDCG HDR](#52-аппаратный-dcg-dual-conversion-gain--idcg-hdr-ru)
   - [Разблокировка 50Мп и 200Мп FullRes](#53-разблокировка-50мп-и-200мп-fullres-ru)
   - [George Video MOD (8K со всех камер, 4K120, чистый AISP)](#54-george-video-mod-8k-со-всех-камер-4k120-чистый-aisp-ru)
   - [Stock AIO 104 для Xiaomi 15 Ultra (LYT-900)](#55-stock-aio-104-для-xiaomi-15-ultra-lyt-900-ru)
   - [Защита от вылетов на Xiaomi 17 Ultra (SimpleRom ST, EU, Elite)](#56-защита-от-вылетов-на-xiaomi-17-ultra-simplerom-st-eu-elite-ru)
6. [Визуальные сравнения «До / После» (Visual Proof)](#6-визуальные-сравнения-до--после-visual-proof-ru)
7. [Инструкция по установке](#7-инструкция-по-установке-ru)
8. [Инструкция по тестированию и проверке работы модуля](#8-инструкция-по-тестированию-и-проверке-работы-модуля-для-всех-версий-ru)
   - [Настройка и проверка 50Мп/200Мп в Google Камере (AGC 8.x/9.x, LMC, Shamim)](#86-настройка-и-проверка-50мп--200мп-в-google-камере-agc-8x--9x-lmc-shamim-ru)
9. [Скрипт автоматической диагностики (check_support.sh)](#9-скрипт-автоматической-диагностики-check_supportsh-ru)
10. [Часто задаваемые вопросы (FAQ)](#10-часто-задаваемые-вопросы-faq-ru)
11. [Обратная связь и шаблоны сообщений об ошибках (Issues)](#11-обратная-связь-и-шаблоны-сообщений-об-ошибках-issues-ru)

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
| **[`Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip)** | **270.3 КБ** | 13 Ultra (`ishtar`) | **⭐ Рекомендуется для HyperOS 1.0 (Android 14)**. Чистый оверлей, сохраняет нативный HAL и APK, 100% безопасен для рута (SELinux не трогает), Quad-50M, DCG HDR, 8K. |
| **[`Mi13U_Master_Camera_Combo_v5.1_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_v5.1_by_borndead.zip)** | **146.69 МБ** | 13 Ultra (`ishtar`) | Выделенная полная Leica-камера для 13 Ultra на HyperOS 2/3 (A15/A16), Quad-50M, DCG HDR, 8K все линзы, фикс зависания видоискателя. |
| **[`Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip)** | **270.4 КБ** | 13 Ultra (`ishtar`) | Облегчённый оверлей для 13 Ultra на HyperOS 2/3 (без приложения камеры). |
| **[`Mi15_Master_Camera_Combo_v5.0_by_borndead.zip`](./releases/Mi15_Master_Camera_Combo_v5.0_by_borndead.zip)** | **151.58 МБ** | 15 (`dada`) & 15 Pro (`haotian`) | Выделенный комбайн для Xiaomi 15 и 15 Pro. |

---

### 4. Готовые пресеты конфигураций GCam (.agc) (RU)

Для мгновенного раскрытия возможностей сенсоров и калибровок Chromatix в Google Камере (AGC 8.x / 9.x) подготовлены авторские профили конфигурации:

| Смартфон | Целевые сенсоры | Файл пресета | Возможности пресета |
|---|---|---|---|
| **Xiaomi 13 Ultra** (`ishtar`) | Sony IMX989 + 3x IMX858 | **[`Mi13U_borndead_Universal_Leica_50MP.agc`](./configs/Xiaomi_13_Ultra_ishtar/Mi13U_borndead_Universal_Leica_50MP.agc)** | 50Мп RAW16 на всех 4 линзах, Black Level 64, Leica Authentic матрица, HDR+ Enhanced |
| **Xiaomi 15 Ultra** (`xuanyuan`) | Sony LYT-900 + Samsung HP9 | **[`Mi15U_borndead_StockAIO_LYT900_HP9_50M_200M.agc`](./configs/Xiaomi_15_Ultra_xuanyuan/Mi15U_borndead_StockAIO_LYT900_HP9_50M_200M.agc)** | 50Мп на 1" LYT-900, **200Мп** на перископе HP9 (`16384x12288`), SmartAE ночная экспозиция |
| **Xiaomi 17 Ultra** (`nezha`) | OVX10500U + Samsung HP9 | **[`X17U_borndead_Master_OVX10500U_HP9_50M_200M.agc`](./configs/Xiaomi_17_Ultra_nezha/X17U_borndead_Master_OVX10500U_HP9_50M_200M.agc)** | 50Мп на 1" OVX10500U, **200Мп** на перископе HP9, DCG HDR шумовая модель |
| **Xiaomi 15 / 15 Pro** (`dada`/`haotian`) | Light Hunter 900 + JN1/JN5 | **[`Mi15_borndead_LightHunter_50M.agc`](./configs/Xiaomi_15_15Pro_dada_haotian/Mi15_borndead_LightHunter_50M.agc)** | 50Мп на Light Hunter 900, кастомные цвета Leica, быстрый захват |

📖 **Подробное руководство по импорту пресетов в AGC:** 👉 **[`configs/README.md`](./configs/README.md)**

---

### 5. Ключевые возможности и технологии (RU)

#### 5.1. Устранение зависания видоискателя в «Фото» (RU)
* **Причина бага в прошлых модах**: Внедрение тегов `support_super_resolution` принуждало сенсор 1.0" на зуме 1.0x ждать буфера цифрового супер-разрешения, из-за чего первый кадр застывал намертво.
* **Исправление**: Скрипт очищает конфликтные теги. Режим «Фото» работает на стабильных 60 кадр/с с мгновенным откликом затвора, а максимальные 50Мп/200Мп включаются строго в режимах «50M Ultra HD» и «Ultra RAW».

#### 5.2. Аппаратный DCG (Dual Conversion Gain) / iDCG HDR (RU)
* В каждом пикселе матрицы работают два параллельных узла: **LCG** (защита от пересветов в ярких областях) и **HCG** (экстремальная светосила и чистота в тенях).
* **Считывание с одного кадра**: движущиеся объекты не раздваиваются (Zero Motion Ghosting).

#### 5.3. Разблокировка 50Мп и 200Мп FullRes (RU)
* Параметр `persist.vendor.camera.maxRAWSizes=55` открывает полноразмерный RAW-поток.
* Все сторонние моды GCam (AGC, LMC, Shamim, BSG) получают полный доступ к 50Мп/200Мп на всех объективах благодаря `vendor.camera.aux.packagelist`.
* Пакет `com.android.camera` исключён из aux-списка, сохраняя штатную логическую многокамерность (SAT).

#### 5.4. George Video MOD (8K со всех камер, 4K120, чистый AISP) (RU)
* Запись видео **8K 24fps со всех задних сенсоров** и **4K 120fps**.
* Твик `aisp.json` (`dump: 0`) и `persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1` отключают агрессивное размытие видео-шумодава ArcSoft, возвращая детализацию.
* Интегрирован видео-кодек `libqcodec2_v4l2codec.so` для стабильной записи высокого битрейта.

#### 5.5. Stock AIO 104 для Xiaomi 15 Ultra (LYT-900) (RU)
* Полные оригинальные калибровки Chromatix `com.qti.tuned.xuanyuan_*.bin` для сенсора **Sony LYT-900** (34.27 МБ) и 200Мп Samsung HP9.
* Таблицы экспозиции SmartAE LN2 для ночной съемки.
* Библиотека `libmialgo_snsc.so`.

#### 5.6. Защита от вылетов на Xiaomi 17 Ultra (SimpleRom ST, EU, Elite) (RU)
* **В чём была проблема**: в ранних сборках отсутствовала папка `devices/` (на 17U попадали файлы 15U) и лежали бинарники с отсутствующей зависимостью `libdlrmsc_android15.so`, а замена APK на кастоме SimpleRom вызывала краш.
* **Решение**: Удалены битые библиотеки, разделены профили `devices/nezha` и `devices/xuanyuan`, добавлен авто-детектор кастомов (`IS_CUSTOM_ROM`), и создан специальный модуль **`X17U_Master_Imaging_MOD_v1.0_Slim`** (без APK, чистый оверлей).

---

### 6. Визуальные сравнения «До / После» (Visual Proof) (RU)

#### 6.1. Аппаратный DCG против программного мульти-кадрового HDR (Движение в кадре)
<p align="center">
  <img src="./assets/dcg_vs_hdr_comparison.svg" alt="DCG vs Staggered HDR Comparison" width="100%">
</p>

* **Обычный программный HDR**: Из-за склейки 3 кадров с разной выдержкой движущиеся объекты неизбежно двоятся (*Motion Ghosting*).
* **Аппаратный DCG (наш мод)**: Одновременное считывание LCG (света) и HCG (тени) с **одного физического кадра экспозиции**. Движущийся объект абсолютно резок, контуры не двоятся.

#### 6.2. Шумоподавление в видео: Сток ArcSoft AISP против George MOD Bypass
<p align="center">
  <img src="./assets/aisp_texture_comparison.svg" alt="AISP Noise Reduction Bypass Comparison" width="100%">
</p>

* **Сток**: Алгоритм ArcSoft AISP агрессивно размывает мелкие текстуры, превращая траву, волосы и асфальт в «пластилин» и «масляную живопись».
* **George MOD Bypass**: Параметр `aisp_algo_nr.bypass=1` отключает смазывание. Видео в 4K120fps и 8K сохраняет честный кинематографический микро-контраст и естественную резкость оптики Leica.

#### 6.3. Разрешающая способность: 12.5Мп Биннинг против 50Мп и 200Мп FullRes (100% Crop)
<p align="center">
  <img src="./assets/resolution_comparison.svg" alt="Resolution Scale Comparison" width="100%">
</p>

* **12.5 Мп (Биннинг)**: Мелкие дорожные знаки, надписи на вывесках и лица людей на общем плане размыты.
* **50 Мп / 200 Мп FullRes**: Честные `8192 x 6144` и `16384 x 12288` пикселей. 4-кратная оптико-цифровая детализация, позволяющая кадрировать снимок без потери резкости.

---

### 7. Инструкция по установке (RU)

1. Скачайте необходимый zip-архив из папки [`releases/`](./releases/).
   * **Для Xiaomi 17 Ultra на SimpleRom ST**: выберите **`X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`**.
   * **Для универсальной установки на любой флагман**: выберите **`Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip`**.
2. Откройте **Magisk (v26+)**, **KernelSU** или **APatch**.
3. Зайдите в раздел **«Модули»** ➔ **«Установить из хранилища»** и выберите архив.
4. Дождитесь завершения работы скрипта и нажмите **«Перезагрузка»**.
5. *(Рекомендуется)* После перезагрузки очистите данные приложения Камера в Настройках.

---

### 8. Инструкция по тестированию и проверке работы модуля (для всех версий) (RU)

После установки любого модуля из линейки рекомендуется провести пошаговую диагностику, чтобы убедиться в корректной активации всех аппаратных алгоритмов и системных оверлеев.

#### 8.1. Базовый чек-лист сразу после перезагрузки
1. **Проверка Root-прав**: Откройте **Magisk**, **KernelSU** или **APatch**.
   - Убедитесь, что модуль активен (включён переключатель).
   - Убедитесь, что статус суперпользователя сохранён (на Android 14 исключён переход в Magisk Safe Mode благодаря чистым скриптам загрузки).
2. **Сброс кэша камеры** *(обязательно для применения XML-конфигов)*:
   - Перейдите в *Настройки ➔ Приложения ➔ Все приложения ➔ Камера*.
   - Нажмите **«Очистить всё»** (это сбросит внутренний кэш разрешений и применит новые сетки зума `device_features`).
3. **Первичный запуск**:
   - Откройте стоковую камеру Leica. Приложение должно открыться мгновенно, без задержек, без падений и без чёрного экрана.

---

#### 8.2. Проверка ключевых режимов по моделям смартфонов

##### 📱 Xiaomi 17 Ultra (`nezha`)
* **Проверка стабильности на SimpleRom ST / Custom ROM**:
  - При установке `X17U_Master_Imaging_MOD_v1.0_Slim` или исправленного комбо v5.1 стоковый модифицированный APK камеры сохраняется. Камера не крашится при запуске, динамический компоновщик не падает из-за отсутствующей библиотеки `libdlrmsc`.
* **Режим «50M / 200M Ultra HD» (Mode 175)**:
  - Переключитесь в режим «50M» (или «Ultra HD»).
  - Выберите зум **5.0x** (перископический телеобъектив Samsung HP9 200Мп). Сделайте снимок. Откройте снимок в Галерее ➔ *«Сведения»*: разрешение файла должно составлять **`16384 x 12288`** (~200 Мп, размер файла от 40 до 80 МБ).
  - Проверьте переключение на **0.5x** (ультраширокоугольный JN5), **1.0x** (основной 1" OVX10500U) и **3.0x**: разрешение снимков должно быть ровно **`8192 x 6144`** (50 Мп).
* **Режим «Видео» (8K и 4K120fps)**:
  - Перейдите в режим «Видео» ➔ выберите **8K 24fps**. Переключайтесь между всеми объективами (0.5x, 1x, 3x, 5x) — запись ведётся со всех 4 сенсоров.
  - Переключитесь в **4K 120fps** — проверьте плавность записи. Интегрированный видеокодек `libqcodec2_v4l2codec.so` гарантирует отсутствие дропов кадров на высоком битрейте.

##### 📱 Xiaomi 15 Ultra (`xuanyuan`)
* **Официальные калибровки Sony LYT-900 (Stock AIO 104)**:
  - Основной 1-дюймовый сенсор LYT-900 считывает оригинальные Chromatix-профили `xuanyuan_semco_LYT900_wide_i.bin`. Цвета естественные, без синевы или пересветов.
* **200Мп перископ Samsung HP9**:
  - В режиме «50M Ultra HD» на зуме **5.0x** проверьте разрешение снимка: честные **`16384 x 12288`**. На 1.0x — **`8192 x 6144`**.
* **Ночной режим SmartAE LN2**:
  - Сделайте ночной кадр в слабом освещении: экспозиция сбалансирована, фонари не превращаются в белые пятна, тени не зашумлены.
* **Видео 8K со всех линз**: Запись 8K 24fps доступна на 0.5x, 1x, 3x, 5x.

##### 📱 Xiaomi 13 Ultra (`ishtar`)
* **Проверка на HyperOS 1.0 (Android 14)**:
  - С модулем `Mi13U_Master_Imaging_MOD_HOS1_A14` видоискатель работает сразу (нет черного экрана, нативный HAL сохранён). Рут в Magisk не пропадает.
* **Плавность режима «Фото» (Mode 161)**:
  - Запустите камеру в обычном режиме «Фото» на 1.0x (Sony IMX989). Видоискатель должен работать на стабильных 60 fps без малейшего зависания первого кадра (устранён баг Super Resolution).
* **Сетка Quad-50M (Mode 175)**:
  - В режиме «50M» проверьте все 4 фокусных расстояния: **`0.5x : 1.0x : 3.2x : 5.0x`**.
  - Все 4 камеры (Sony IMX989 + 3x IMX858) выводят честные **`8192 x 6144`** (50 Мп).
* **Pro-режим и 14-битный Ultra RAW**:
  - В режиме «Профи» включите RAW — снимается полноценный 50Мп поток без сжатия благодаря `persist.vendor.camera.maxRAWSizes=55`.
* **Google Камера (GCam)**:
  - В модах AGC, LMC, Shamim все 4 тыловые камеры доступны для переключения и снимают в полном разрешении 50Мп RAW.

##### 📱 Xiaomi 15 / 15 Pro (`dada` / `haotian`)
* **Сетка зума 50M Ultra HD**:
  - На Xiaomi 15 доступны переключатели: **`0.6x : 1.0x : 3.2x`**.
  - На Xiaomi 15 Pro доступны переключатели: **`0.6x : 1.0x : 3.2x : 5.0x`**.
* **Сенсор Light Hunter 900**: Проверьте контрастные дневные сцены — тени мягко подтягиваются без пересветов благодаря калибровкам DCG.

---

#### 8.3. Тестирование аппаратного DCG (Dual Conversion Gain) / iDCG HDR
Главное преимущество аппаратного DCG перед обычным программным HDR — **считывание LCG (яркие участки) и HCG (тени) с одного единственного физического кадра**:
1. Найдите высококонтрастную сцену: комната с ярким солнечным окном или ночная улица с яркой неоновой вывеской/фонарём.
2. Поместите в кадр быстро движущийся объект (помашите рукой перед камерой или сфотографируйте проезжающий автомобиль).
3. Сделайте снимок в режиме «Фото» или «50M».
4. **Оценка результата**:
   - **Света (LCG)**: лампы, небо за окном или неоновые вывески не выбиты в белый клиппинг, текстура ламп и облаков сохранена.
   - **Тени (HCG)**: в тёмных углах комнаты видны детали и цвета без цветного цифрового шума.
   - **Отсутствие двоения (Zero Motion Ghosting)**: движущаяся рука или автомобиль имеют абсолютно резкий, чёткий контур. Нет «призраков» и артефактов склейки кадров, характерных для обычного программного HDR.

---

#### 8.4. Проверка системных свойств в Termux / ADB
Вы можете за 10 секунд подтвердить активность всех модульных твиков через терминал (Termux с рутом на смартфоне или командная строка ADB на ПК):

```bash
# Получение прав суперпользователя (в Termux)
su

# 1. Проверка активации аппаратного DCG HDR
getprop persist.vendor.camera.dcg.enable
# Ожидаемый вывод: 1

# 2. Проверка флага сенсорного HDR
getprop persist.vendor.camera.sensor.hdr
# Ожидаемый вывод: 1

# 3. Проверка разблокировки полноразмерных RAW буферов (50M/200M)
getprop persist.vendor.camera.maxRAWSizes
# Ожидаемый вывод: 55

# 4. Проверка обхода агрессивного видео-шумодава ArcSoft AISP
getprop persist.vendor.camera.arcsoft.aisp_algo_nr.bypass
# Ожидаемый вывод: 1

# 5. Проверка коэффициента битрейта видео (увеличение на 50%)
getprop persist.vendor.camera.video.bitrate.factor
# Ожидаемый вывод: 1.5

# 6. Проверка поддержки DCG на вендорном уровне
getprop ro.vendor.camera.dcg
# Ожидаемый вывод: 1
```

#### 8.5. Проверка логов CamX HAL через ADB Logcat (для продвинутых пользователей)
Если подключить смартфон к ПК по USB и включить отладку по ADB:
```bash
adb logcat -s CamX | grep -iE "dcg|hdr|stream"
```
При запуске видоискателя драйвер Qualcomm CamX выведет вызовы `EnableHDRDCGMode: success` и подтвердит сопряжение каналов усиления в реальном времени.

---

#### 8.6. Настройка и проверка 50Мп / 200Мп в Google Камере (AGC 8.x / 9.x, LMC, Shamim) (RU)

Модули **Xiaomi Master Camera Combo** разблокируют аппаратный вывод полного разрешения на уровне системы и драйвера Qualcomm CamX. Однако **Google Камера (AGC 9.6 / BigKaka, LMC 8.4, Shamim)** изначально создана для смартфонов Google Pixel и «из коробки» (без специального `.agc` конфига или ручной настройки) **НЕ будет снимать в 50Мп** даже при нажатии на плашку «50M / RES» в видоискателе.

Ниже приведено подробное руководство по правильной настройке и тестированию режима полного разрешения.

##### 1. Почему в GCam без настройки не работает 50Мп?
* **Роль модуля Magisk**: Параметр `persist.vendor.camera.maxRAWSizes=55` открывает для Camera2 API аппаратный буфер RAW16 высокого разрешения (`8192x6144` и `16384x12288`), а `vendor.camera.aux.packagelist` даёт приложению доступ ко всем физическим объективам.
* **Поведение GCam по умолчанию**: Приложение настроено на стандартный 12.5 Мп биннинг (4-в-1). Если включить режим «50M» без изменения конфигурации сессии и типа спуска, то:
  - Снимок сохранится в стандартном разрешении `4096 x 3072` (12.5 Мп);
  - Либо зависнет индикатор запекания HDR+ в шторке;
  - Либо приложение аварийно завершится из-за несоответствия потоков (`SessionConfiguration`).

##### 2. Главное правило съёмки в 50Мп: Режим затвора (ZSL vs HDR+ Enhanced) ⚠️
* **В режиме моментального спуска (ZSL / Zero Shutter Lag / обычный HDR+) съёмка в 50Мп НЕВОЗМОЖНА!**  
  *Причина:* В режиме ZSL камера непрерывно прокачивает через оперативную память кольцевой буфер из 15–25 несжатых RAW-кадров со скоростью 30 fps. Для 50Мп такой буфер требует более 2.5 ГБ RAM в секунду — процессор Qualcomm ISP не успевает его обрабатывать и принудительно сбрасывает поток в 12.5 Мп биннинг.
* **Решение:**  
  В видоискателе AGC откройте верхнюю шторку быстрых настроек и **переключите затвор в режим «HDR+ Enhanced» («HDR+ Расширенный»)** (значок `HDR+` в рамке/с плюсом) или одиночный RAW. Только в этом режиме камера при нажатии на спуск делает точечный захват 1–3 кадров высокого разрешения.

##### 3. Пошаговая ручная настройка AGC 9.6 / 9.x (если нет готового конфига)
1. Нажмите на значок **шестерёнки** вверху видоискателя ➔ **More Settings (Дополнительные настройки)**.
2. Перейдите в раздел **Camera Lens (Объективы)** ➔ выберите нужный объектив (например, **Main Lens**).
3. **High Resolution / 50MP:** переведите тумблер в положение **ВКЛ (ON)**.
4. **RAW Format (Формат RAW):** выберите **RAW16** *(процессоры Snapdragon 8 Gen 2 / Gen 3 / Elite отдают 50Мп поток строго в RAW16)*.
5. **Session Configuration (Конфигурация сессии / OpMode):** выберите значение `0xF000` или `0x0` (либо режим `High Resolution`).
6. **HDR+ Frames (Количество кадров):** для 50Мп установите **от 1 до 3 кадров** (если оставить 15–20 кадров, телефон зависнет из-за нехватки RAM при склейке).
7. **Уровни Black Level / White Level:**
   - **Sony IMX989, IMX858, LYT-900 (Xiaomi 13 Ultra, 15 Ultra):** Black Level = `64`, White Level = `1023`.
   - **OmniVision OVX10500U (Xiaomi 17 Ultra):** Black Level = `64`, White Level = `1023` (или `4095`).
   - **Samsung HP9 200MP, JN5 (Xiaomi 15 Ultra, 17 Ultra):** Black Level = `64`, White Level = `1023`.
8. Повторите настройку для остальных объективов (Tele 3.2x, Tele 5x, Ultra-Wide).

##### 4. Проверка на Xiaomi 13 Ultra (`ishtar`)
1. Откройте AGC. Убедитесь, что в видоискателе видны все 4 переключателя камер: **`0.5x`**, **`1.0x`**, **`3.2x`**, **`5.0x`** (все 4 модуля — честные сенсоры Sony Quad Bayer).
2. Нажмите на плашку **50M / RES** (она станет активной) и переключитесь в **HDR+ Enhanced**.
3. Сделайте снимок на 1.0x (Sony IMX989).
4. Откройте фото в стандартной Галерее Xiaomi или Google Фото ➔ нажмите «Сведения о фото»:
   - Обычный биннинг: `4096 x 3072` (12.5 Мп, размер 3–6 МБ).
   - **Полноразмерный режим 50Мп:** **`8192 x 6144`** (50.3 Мп, размер файла **от 18 до 45 МБ**)!
5. Повторите проверку на `0.5x`, `3.2x` и `5.0x` — все 4 объектива выдадут **`8192 x 6144`**!

> **💡 Подсказка для 13 Ultra:** Вы можете скачать готовые авторские `.agc` конфиги (от *John Galt*, *Vova*, *KaKaru*) из Telegram-сообществ по Xiaomi 13 Ultra, положить файл в папку `/Download/AGC.9.6/configs/` и загрузить двойным тапом по чёрному полю рядом с кнопкой затвора — 50Мп настроится автоматически!

##### 5. Проверка на Xiaomi 17 Ultra (`nezha`)
* **Основной сенсор 1" OVX10500U (1.0x):** формирует снимки с разрешением **`8192 x 6144`** (50 Мп).
* **Перископ Samsung HP9 200MP (5.0x):** в режиме High Resolution формирует снимки с разрешением до **`16384 x 12288`** (~200 Мп, размер файла от 40 до 90 МБ). Для 200Мп рекомендуется выставить ровно **1 или 2 кадра** в настройках HDR+ Frames.

##### 6. Белый список пакетов GCam в модуле
В системный белый список `vendor.camera.aux.packagelist` нашего модуля включены абсолютно все официальные сборки и клоны:
* `com.google.android.GoogleCamera` (стандартный Google Pixel)
* `com.agc.cam` (официальный AGC клон)
* `com.agc.gcam96` (AGC 9.6)
* `com.samsung.android.scan3d` (популярный вариант AGC для обхода вендорных блокировок)
* `com.samsung.android.ruler` (AGC Ruler)
* `com.ss.android.ugc.aweme` (AGC Aweme)
* `com.android.mgc` (BSG GCam)
* `com.shamim.cam` (Shamim GCam)
* `org.codeaurora.snapcam` (Snapdragon SnapCam)

---

### 9. Скрипт автоматической диагностики (check_support.sh) (RU)

Для быстрой и безошибочной проверки состояния устройства, прошивки, рут-окружения и активности всех ключевых системных параметров модуля разработан портативный скрипт диагностики **`check_support.sh`**.

#### Возможности скрипта:
* **Сведения об устройстве**: модель (`ishtar`, `dada`, `haotian`, `xuanyuan`, `nezha`), платформа SoC и версия HyperOS/Android.
* **Проверка Root-окружения**: права Superuser (UID 0), статус SELinux (Enforcing/Permissive) и поиск активного модуля в каталогах Magisk, KernelSU и APatch (`/data/adb/modules`).
* **Параметры Qualcomm CamX**:
  - Аппаратный буфер 50M/200M RAW: `persist.vendor.camera.maxRAWSizes = 55`
  - Аппаратный DCG HDR: `persist.vendor.camera.dcg.enable = 1`
  - Сенсорный HDR: `persist.vendor.camera.sensor.hdr = 1`
  - Обход видео-шумодава: `persist.vendor.camera.arcsoft.aisp_algo_nr.bypass = 1`
  - Множитель битрейта: `persist.vendor.camera.video.bitrate.factor = 1.5`
  - Вендорный флаг DCG: `ro.vendor.camera.dcg = 1`
* **Белый список AUX**: проверка `vendor.camera.aux.packagelist` на наличие пакетов GCam / AGC / LMC / Shamim.
* **Автоматическое сохранение отчёта**:  
  📁 `/sdcard/Download/Mi_Camera_Diagnostic_Report.txt` (можно легко прикрепить к баг-репорту на GitHub).

#### Способы запуска:

**Вариант 1: Запуск на смартфоне через Termux (с правами Root)**
```bash
# Быстрый запуск одной командой напрямую из репозитория:
curl -sSL https://raw.githubusercontent.com/bjorndith-cmd/Mi_Master_Camera_Combo/main/check_support.sh | su -c sh

# Либо запуск локального файла (если скачан в Download):
su
sh /sdcard/Download/check_support.sh
```

**Вариант 2: Запуск с компьютера через ADB**
```bash
adb push check_support.sh /data/local/tmp/
adb shell "su -c sh /data/local/tmp/check_support.sh"
```

---

### 10. Часто задаваемые вопросы (FAQ) (RU)

<details>
<summary><b>Что делать на Xiaomi 13 Ultra (HyperOS 1.0.14.0 Android 14), если пропал рут или черный экран?</b></summary>

Проблема полностью решена! На Android 14 рут отпадал из-за агрессивных permissive-правил в `post-fs-data.sh`, вызывавших Safe Mode в Magisk, а чёрный экран возникал из-за подмены системного Camera HAL на порт от A16.  
Установите выделенный модуль **Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip** — он сохраняет родной системный HAL и APK, не трогает SELinux, активирует Quad-50MP на всех линзах, DCG HDR и 8K видео с нулевым риском сбоев!
</details>

<details>
<summary><b>Камера на Xiaomi 17 Ultra (SimpleRom 3.0.309.0 - ST) теперь не вылетает?</b></summary>

Да, проблема решена на 100%! Для пользователей SimpleRom ST мы рекомендуем **X17U_Master_Imaging_MOD_v1.0_Slim**. Модуль не затрагивает модифицированный APK камеры, а накатывает только сенсорные калибровки, DCG HDR и видеомод.
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

### 11. Обратная связь и шаблоны сообщений об ошибках (Issues) (RU)

Если вы столкнулись с проблемой или хотите предложить новую функцию/конфиг, воспользуйтесь официальными формами в разделе [Issues](../../issues/new/choose):

* 🐛 **[Отчёт об ошибке (Bug Report)](../../issues/new?template=bug_report.yml)** — структурированная форма для репорта о вылетах, чёрном экране или сбоях. Обязательно прикрепите сгенерированный отчёт `/sdcard/Download/Mi_Camera_Diagnostic_Report.txt`.
* ⚙️ **[Отзыв о конфигурациях GCam (Config Feedback)](../../issues/new?template=config_feedback.yml)** — делитесь своими `.agc` / `.xml` пресетами, калибровками цветовых матриц Leica и профилями шума для сенсоров Sony, OmniVision и Samsung.
* 💡 **[Предложение новой функции (Feature Request)](../../issues/new?template=feature_request.yml)** — запрос поддержки новых ревизий прошивок, сенсоров или видеорежимов.

---
---

<a name="-english"></a>
# 🇬🇧 ENGLISH SECTION

## 📑 Navigation Menu (EN)
1. [About the Project](#1-about-the-project-en)
2. [Supported Devices & Camera Hardware](#2-supported-devices--camera-hardware-en)
3. [Module Releases & Download Links](#3-module-releases--download-links-en)
4. [Ready-to-Use GCam Config Presets (.agc)](#4-ready-to-use-gcam-config-presets-agc-en)
5. [Core Features & Technologies](#5-core-features--technologies-en)
   - [Photo Mode Viewfinder Freeze Fix](#51-photo-mode-viewfinder-freeze-fix-en)
   - [Hardware DCG (Dual Conversion Gain) / iDCG HDR](#52-hardware-dcg-dual-conversion-gain--idcg-hdr-en)
   - [50MP & 200MP Full Resolution RAW Unlock](#53-50mp--200mp-full-resolution-raw-unlock-en)
   - [George Video MOD (8K All Sensors, 4K120fps, Clean AISP)](#54-george-video-mod-8k-all-sensors-4k120fps-clean-aisp-en)
   - [Stock AIO 104 for Xiaomi 15 Ultra (LYT-900)](#55-stock-aio-104-for-xiaomi-15-ultra-lyt-900-en)
   - [Crash Prevention on Xiaomi 17 Ultra (SimpleRom ST, EU, Elite)](#56-crash-prevention-on-xiaomi-17-ultra-simplerom-st-eu-elite-en)
6. [Visual Proof Gallery (Before vs After)](#6-visual-proof-gallery-before-vs-after-en)
7. [Installation Guide](#7-installation-guide-en)
8. [Verification & Testing Guide (All Devices & Versions)](#8-verification--testing-guide-all-devices--versions-en)
   - [Google Camera (AGC 8.x/9.x, LMC, Shamim) 50MP Setup & Guide](#86-google-camera-agc-8x--9x-lmc-shamim-50mp--200mp-configuration--testing-guide-en)
9. [Automated Diagnostic Tool (check_support.sh)](#9-automated-diagnostic-tool-check_supportsh-en)
10. [Frequently Asked Questions (FAQ)](#10-frequently-asked-questions-faq-en)
11. [Feedback & Issue Reporting Templates](#11-feedback--issue-reporting-templates-en)

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
| **[`Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip)** | **270.3 KB** | 13 Ultra (`ishtar`) | **⭐ Recommended for HyperOS 1.0 (Android 14)**. Pure overlay, preserves native HAL and APK, 100% root safe (clean SELinux), Quad-50M, DCG HDR, 8K. |
| **[`Mi13U_Master_Camera_Combo_v5.1_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_v5.1_by_borndead.zip)** | **146.69 MB** | 13 Ultra (`ishtar`) | Dedicated full Leica suite for 13 Ultra on HyperOS 2/3 (A15/A16), Quad-50M, DCG HDR, 8K on all lenses, photo viewfinder freeze fix. |
| **[`Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip)** | **270.4 KB** | 13 Ultra (`ishtar`) | Lightweight pure overlay for 13 Ultra on HyperOS 2/3 (without APK replacement). |
| **[`Mi15_Master_Camera_Combo_v5.0_by_borndead.zip`](./releases/Mi15_Master_Camera_Combo_v5.0_by_borndead.zip)** | **151.58 MB** | 15 (`dada`) & 15 Pro (`haotian`) | Dedicated combo for Xiaomi 15 and 15 Pro. |

---

### 4. Ready-to-Use GCam Config Presets (.agc) (EN)

To immediately unlock the full potential of your device's sensors, Chromatix calibrations, and RAW16 pipelines in Google Camera (AGC 8.x / 9.x), dedicated config presets are provided:

| Device | Target Sensors | Config Preset File | Profile Highlights |
|---|---|---|---|
| **Xiaomi 13 Ultra** (`ishtar`) | Sony IMX989 + 3x IMX858 | **[`Mi13U_borndead_Universal_Leica_50MP.agc`](./configs/Xiaomi_13_Ultra_ishtar/Mi13U_borndead_Universal_Leica_50MP.agc)** | 50MP RAW16 on all 4 rear lenses, Black Level 64, Leica Authentic color matrix, HDR+ Enhanced |
| **Xiaomi 15 Ultra** (`xuanyuan`) | Sony LYT-900 + Samsung HP9 | **[`Mi15U_borndead_StockAIO_LYT900_HP9_50M_200M.agc`](./configs/Xiaomi_15_Ultra_xuanyuan/Mi15U_borndead_StockAIO_LYT900_HP9_50M_200M.agc)** | 50MP on 1" LYT-900, **200MP** on HP9 periscope (`16384x12288`), SmartAE night exposure |
| **Xiaomi 17 Ultra** (`nezha`) | OVX10500U + Samsung HP9 | **[`X17U_borndead_Master_OVX10500U_HP9_50M_200M.agc`](./configs/Xiaomi_17_Ultra_nezha/X17U_borndead_Master_OVX10500U_HP9_50M_200M.agc)** | 50MP on 1" OVX10500U, **200MP** on HP9 periscope, DCG HDR sensor noise model |
| **Xiaomi 15 / 15 Pro** (`dada`/`haotian`) | Light Hunter 900 + JN1/JN5 | **[`Mi15_borndead_LightHunter_50M.agc`](./configs/Xiaomi_15_15Pro_dada_haotian/Mi15_borndead_LightHunter_50M.agc)** | 50MP on Light Hunter 900, Leica custom tonemapping, fast shutter response |

📖 **Step-by-step AGC Config Import Guide:** 👉 **[`configs/README.md`](./configs/README.md)**

---

### 5. Core Features & Technologies (EN)

#### 5.1. Photo Mode Viewfinder Freeze Fix (EN)
* **Root Cause**: Injecting `support_super_resolution` into `device_features` caused the 1-inch main sensor at 1.0x zoom to enter an unsupported `SuperResolutionProcessor` pipeline, locking the viewfinder on the very first frame.
* **Resolution**: The installer cleanly purges conflicting tags. Photo mode (161) operates in fluid 60 fps with zero shutter lag, while 50MP/200MP modes remain active in Ultra HD (175) and Ultra RAW.

#### 5.2. Hardware DCG (Dual Conversion Gain) / iDCG HDR (EN)
* Each pixel on the sensor features two parallel readout stages: **LCG** (highlights protection) and **HCG** (ultra-high sensitivity & deep shadow clarity).
* **Single-exposure readout**: Moving subjects remain crisp without motion ghosting or multi-frame artifacts.

#### 5.3. 50MP & 200MP Full Resolution RAW Unlock (EN)
* Setting `persist.vendor.camera.maxRAWSizes=55` unlocks the full-resolution RAW buffer in Qualcomm CamX.
* Third-party GCam mods (AGC, LMC, Shamim, BSG) gain full physical sensor access via `vendor.camera.aux.packagelist`.
* `com.android.camera` is excluded from the aux list to preserve native Leica Spatial Alignment Telephoto (SAT) switching.

#### 5.4. George Video MOD (8K All Sensors, 4K120fps, Clean AISP) (EN)
* **8K 24fps video recording across all rear cameras** and **4K 120fps**.
* `aisp.json` (`dump: 0`) and `persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1` bypass ArcSoft video noise reduction smearing.
* Hardware video codec `libqcodec2_v4l2codec.so` included for smooth high-bitrate encoding.

#### 5.5. Stock AIO 104 for Xiaomi 15 Ultra (LYT-900) (EN)
* Official Chromatix calibration binaries `com.qti.tuned.xuanyuan_*.bin` for **Sony LYT-900** (34.27 MB) and Samsung HP9 200MP periscope.
* SmartAE LN2 low-light exposure tables.
* Self-contained `libmialgo_snsc.so`.

#### 5.6. Crash Prevention on Xiaomi 17 Ultra (SimpleRom ST, EU, Elite) (EN)
* **Root Cause of Past Crashes**: The earlier zip lacked the `devices/` directory (causing 15U files to be flashed onto 17U), contained naked libraries with an unresolved `libdlrmsc_android15.so` dependency, and overwrote the custom deodexed camera APK on SimpleRom ST.
* **Resolution**: Purged broken libraries, isolated `devices/nezha` and `devices/xuanyuan` trees, added custom ROM detection (`IS_CUSTOM_ROM`), and introduced **`X17U_Master_Imaging_MOD_v1.0_Slim`** (pure overlay, zero APK conflict).

---

### 6. Visual Proof Gallery (Before vs After) (EN)

#### 6.1. Hardware DCG vs Conventional Multi-Frame Staggered HDR (Motion in Frame)
<p align="center">
  <img src="./assets/dcg_vs_hdr_comparison.svg" alt="DCG vs Staggered HDR Comparison" width="100%">
</p>

* **Conventional Software HDR**: Because it aligns and blends 3 distinct bracketed frames taken at different times, moving subjects inevitably suffer from severe double edges (*Motion Ghosting*).
* **Hardware DCG (Our MOD)**: Simultaneous dual readout (LCG for highlights + HCG for deep shadows) from a **single physical sensor exposure**. Moving subjects retain needle-sharp, crisp outlines with zero ghosting.

#### 6.2. Video Noise Reduction: Stock ArcSoft AISP Smear vs George MOD Bypass
<p align="center">
  <img src="./assets/aisp_texture_comparison.svg" alt="AISP Noise Reduction Bypass Comparison" width="100%">
</p>

* **Stock**: ArcSoft's AISP video noise reduction aggressively smears fine micro-textures, rendering grass, foliage, hair, and road asphalt into an artificial "oil-paint watercolor" look.
* **George MOD Bypass**: Setting `aisp_algo_nr.bypass=1` completely neutralizes aggressive spatial smoothing. Video in 4K120fps and 8K retains authentic cinematic micro-contrast, organic grain, and the true optical clarity of Leica lenses.

#### 6.3. Spatial Resolving Power: 12.5MP Binned vs 50MP & 200MP FullRes (100% Crop)
<p align="center">
  <img src="./assets/resolution_comparison.svg" alt="Resolution Scale Comparison" width="100%">
</p>

* **12.5 MP (4-in-1 Binned)**: Fine street signage, architectural textures, and distant faces are blurred into pixel clusters.
* **50 MP / 200 MP FullRes**: True `8192 x 6144` and `16384 x 12288` pixels. Delivers up to 4x higher spatial resolution, allowing aggressive digital cropping without detail loss.

---

### 7. Installation Guide (EN)

1. Download the required zip from the [`releases/`](./releases/) directory.
   * **For Xiaomi 17 Ultra on SimpleRom ST**: pick **`X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`**.
   * **For general installation on any flagship**: pick **`Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip`**.
2. Open **Magisk (v26+)**, **KernelSU**, or **APatch**.
3. Navigate to **Modules** ➔ **Install from storage** and select the zip.
4. Wait for installation to complete, then tap **Reboot**.
5. *(Recommended)* After reboot, clear Camera app data in Android Settings.

---

### 8. Verification & Testing Guide (All Devices & Versions) (EN)

After installing any module package from the suite, follow this step-by-step diagnostic guide to verify that all hardware pipelines, Chromatix tunings, and system overrides are operational.

#### 8.1. Baseline Post-Reboot Verification
1. **Root Status Check**: Open **Magisk**, **KernelSU**, or **APatch**.
   - Verify the module is active with a green checkmark.
   - Confirm root access remains fully functional (Magisk Safe Mode is completely bypassed on Android 14 due to sanitized boot scripts).
2. **Clear Camera App Data** *(mandatory to apply modified `device_features` XML)*:
   - Navigate to *Settings ➔ Apps ➔ Manage apps ➔ Camera*.
   - Tap **«Clear all data»** (this purges cached resolution lists and enforces new 50M/200M zoom ratios).
3. **Initial Launch**:
   - Open the stock Leica Camera app. It should launch instantly with zero lag, no crash, and no black screen.

---

#### 8.2. Target Device Verification Steps

##### 📱 Xiaomi 17 Ultra (`nezha`)
* **SimpleRom ST / Custom ROM Stability**:
  - With `X17U_Master_Imaging_MOD_v1.0_Slim` or updated Combo v5.1, the ROM's native deodexed camera APK is preserved. The camera starts reliably without crashing, and dynamic linker errors (`libdlrmsc_android15.so not found`) are eliminated.
* **50M / 200M Ultra HD Mode (Mode 175)**:
  - Switch to «50M» (or «Ultra HD») mode.
  - Select **5.0x zoom** (Samsung HP9 200MP periscope telephoto). Capture a photo. Open the image in Gallery ➔ *«Details»*: file dimensions must show **`16384 x 12288`** (~200 MP, file size 40–80 MB).
  - Test switching to **0.5x** (JN5 ultrawide), **1.0x** (1" OVX10500U wide), and **3.0x**: all output native **`8192 x 6144`** (50 MP).
* **Video Mode (8K All Lenses & 4K120fps)**:
  - Switch to «Video» ➔ select **8K 24fps**. Switch between lenses (0.5x, 1x, 3x, 5x) — recording functions on all 4 rear sensors.
  - Select **4K 120fps** — verify video smoothness. The integrated `libqcodec2_v4l2codec.so` codec ensures zero frame drops under increased bitrates.

##### 📱 Xiaomi 15 Ultra (`xuanyuan`)
* **Official Stock AIO 104 Tunings for Sony LYT-900**:
  - The 1-inch LYT-900 sensor loads official Chromatix tunings `xuanyuan_semco_LYT900_wide_i.bin`. Colors and contrast remain balanced without clipping or color cast.
* **Samsung HP9 200MP Periscope**:
  - In «50M Ultra HD» mode at **5.0x**, confirm **`16384 x 12288`** resolution. At 1.0x, verify **`8192 x 6144`**.
* **SmartAE LN2 Low-Light Exposure**:
  - Capture a night scene: exposure is natural, streetlight blowout is prevented, and dark shadows retain detail without noise grain.
* **8K Video All Lenses**: 8K 24fps is enabled across 0.5x, 1x, 3x, 5x sensors alongside 4K120fps.

##### 📱 Xiaomi 13 Ultra (`ishtar`)
* **HyperOS 1.0 (Android 14) Verification**:
  - Using `Mi13U_Master_Imaging_MOD_HOS1_A14`, the viewfinder opens immediately (no black screen, native A14 HAL preserved). Magisk root stays active.
* **Photo Mode Viewfinder Smoothness (Mode 161)**:
  - Launch the camera in default «Photo» mode on 1.0x (Sony IMX989). The viewfinder maintains a steady 60 fps without freezing on the first frame (Super Resolution conflict stripped).
* **Quad-50M Grid (Mode 175)**:
  - In «50M» mode, verify all 4 focal lengths: **`0.5x : 1.0x : 3.2x : 5.0x`**.
  - All 4 cameras (Sony IMX989 + 3x IMX858) output full **`8192 x 6144`** (50 MP).
* **Pro Mode & 14-Bit Ultra RAW**:
  - In Pro mode, enable RAW — outputs uncompressed 50MP DNG files (`persist.vendor.camera.maxRAWSizes=55`).
* **GCam Port Compatibility**:
  - AGC, LMC, and Shamim mods identify all 4 rear cameras (AUX IDs 0, 1, 2, 3, 4) with full 50MP RAW capability.

##### 📱 Xiaomi 15 / 15 Pro (`dada` / `haotian`)
* **50M Ultra HD Zoom Grid**:
  - Xiaomi 15: **`0.6x : 1.0x : 3.2x`**.
  - Xiaomi 15 Pro: **`0.6x : 1.0x : 3.2x : 5.0x`**.
* **Light Hunter 900 DCG Dynamic Range**: Backlit daytime and night shots benefit from true hardware sensor HDR.

---

#### 8.3. Testing Hardware DCG (Dual Conversion Gain) / iDCG HDR
The key advantage of hardware DCG over standard multi-frame HDR is **simultaneous LCG (highlights) and HCG (shadows) readout from a single exposure**:
1. Frame a high dynamic range scene (e.g., an indoor room facing a bright sunny window, or a night street with bright neon signs/streetlights).
2. Introduce rapid motion in the frame (wave your hand in front of the lens or photograph a passing car).
3. Capture a shot in «Photo» or «50M» mode.
4. **Evaluate the Image**:
   - **Highlights (LCG)**: Bright light sources and sky textures are retained without harsh white clipping.
   - **Shadows (HCG)**: Shadowed corners show rich colors and low noise.
   - **Zero Motion Ghosting**: The moving subject has sharp, clean edges with zero double-contours or ghosting artifacts.

---

#### 8.4. Terminal / ADB Properties Verification
Quickly verify system properties using Termux (with root) or ADB on PC:

```bash
# Obtain root (in Termux)
su

# 1. Verify Hardware DCG HDR is enabled
getprop persist.vendor.camera.dcg.enable
# Expected: 1

# 2. Verify Sensor-level HDR
getprop persist.vendor.camera.sensor.hdr
# Expected: 1

# 3. Verify Full-Resolution RAW buffer unlock (50M/200M)
getprop persist.vendor.camera.maxRAWSizes
# Expected: 55

# 4. Verify ArcSoft AISP video noise reduction bypass
getprop persist.vendor.camera.arcsoft.aisp_algo_nr.bypass
# Expected: 1

# 5. Verify video bitrate factor (50% increase)
getprop persist.vendor.camera.video.bitrate.factor
# Expected: 1.5

# 6. Verify vendor-level DCG support flag
getprop ro.vendor.camera.dcg
# Expected: 1
```

#### 8.5. CamX HAL Logcat Verification (Advanced)
Via USB debugging on PC:
```bash
adb logcat -s CamX | grep -iE "dcg|hdr|stream"
```
During viewfinder startup, Qualcomm CamX will log `EnableHDRDCGMode: success`, confirming real-time dual-gain channel operation.

---

#### 8.6. Google Camera (AGC 8.x / 9.x, LMC, Shamim) 50MP / 200MP Configuration & Testing Guide (EN)

The **Xiaomi Master Camera Combo** module removes all vendor restrictions at the kernel and Qualcomm CamX HAL level. However, **Google Camera ports (such as BigKaka AGC 9.6, LMC 8.4, and Shamim)** are originally designed for Google Pixel devices. Without an appropriate `.agc` config profile or proper manual stream configuration, **GCam will NOT capture in 50MP** out of the box, even if you tap the «50M / RES» button in the viewfinder.

Below is the definitive engineering guide to configure and verify high-resolution modes in AGC.

##### 1. Why GCam Doesn't Shoot 50MP Out of the Box Without Configuration
* **Module's System Role**: The property `persist.vendor.camera.maxRAWSizes=55` exposes the physical RAW16 full-resolution buffer (`8192x6144` and `16384x12288`) to the Android Camera2 API, while `vendor.camera.aux.packagelist` grants physical sensor access.
* **GCam's Default Behavior**: GCam boots with default Google Pixel profiles tuned for 12.5MP binned output (4-in-1 Quad Bayer). If you activate the «50M» toggle without configuring the session streams and shutter mode:
  - The photo will still be saved in standard `4096 x 3072` (12.5MP);
  - Or the HDR+ processing progress bar in the notification shade will spin indefinitely;
  - Or the app will crash due to unsupported stream configurations.

##### 2. The Golden Rule of 50MP GCam Capture: Shutter Mode (ZSL vs HDR+ Enhanced) ⚠️
* **50MP capture is IMPOSSIBLE in standard Zero Shutter Lag (ZSL / Instant HDR+) mode!**  
  *Technical Reason:* ZSL maintains a continuous 30 fps circular memory ring buffer of 15–25 uncompressed RAW frames in RAM. For 50MP streams, this consumes over 2.5 GB of RAM per second — Qualcomm's ISP remosaic pipeline cannot process this throughput and drops the stream back to 12.5MP binning.
* **The Solution:**  
  In the AGC viewfinder, pull down the quick settings menu and **switch the shutter mode to «HDR+ Enhanced»** (the `HDR+` icon with a plus sign or border) or single-frame RAW. In HDR+ Enhanced mode, the camera opens the high-resolution stream only upon shutter release, capturing a controlled burst of 1–3 frames.

##### 3. Step-by-Step Manual AGC 9.6 / 9.x Configuration (No Config File Required)
1. Tap the **gear icon** at the top of the viewfinder ➔ **More Settings**.
2. Navigate to **Camera Lens** ➔ select the target lens (e.g., **Main Lens**).
3. **High Resolution / 50MP:** toggle **ON**.
4. **RAW Format:** select **RAW16** *(Snapdragon 8 Gen 2 / Gen 3 / Elite ISP delivers 50MP streams exclusively in RAW16)*.
5. **Session Configuration (OpMode):** select `0xF000` or `0x0` (or `High Resolution` mode).
6. **HDR+ Frames:** set to **1 to 3 frames** (do not leave at 15–20 frames, or the device will run out of memory during remosaicing).
7. **Black Level / White Level Calibration:**
   - **Sony IMX989, IMX858, LYT-900 (Xiaomi 13 Ultra, 15 Ultra):** Black Level = `64`, White Level = `1023`.
   - **OmniVision OVX10500U (Xiaomi 17 Ultra):** Black Level = `64`, White Level = `1023` (or `4095`).
   - **Samsung HP9 200MP, JN5 (Xiaomi 15 Ultra, 17 Ultra):** Black Level = `64`, White Level = `1023`.
8. Repeat for other focal lengths (Tele 3.2x, Tele 5x, Ultra-Wide).

##### 4. Verification on Xiaomi 13 Ultra (`ishtar`)
1. Launch AGC. Confirm that all 4 rear camera buttons are visible: **`0.5x`**, **`1.0x`**, **`3.2x`**, **`5.0x`** (all 4 lenses are genuine Sony 50MP Quad-Bayer sensors).
2. Tap the **50M / RES** button (it will highlight) and switch to **HDR+ Enhanced**.
3. Capture a shot on 1.0x (Sony IMX989).
4. Open the image in Xiaomi Gallery or Google Photos ➔ check Image Details:
   - Standard binned photo: `4096 x 3072` (12.5 MP, ~3–6 MB).
   - **Full-Resolution 50MP photo:** **`8192 x 6144`** (50.3 MP, file size **18 to 45 MB**)!
5. Switch to `0.5x`, `3.2x`, and `5.0x` — all 4 sensors output **`8192 x 6144`**!

> **💡 Pro Tip for 13 Ultra:** You can download community `.agc` configs (such as *John Galt*, *Vova*, *KaKaru*) from Telegram communities, place the file in `/Download/AGC.9.6/configs/`, and load it by double-tapping the black area next to the shutter button — 50MP will be pre-configured across all 4 cameras.

##### 5. Verification on Xiaomi 17 Ultra (`nezha`)
* **Primary 1" OVX10500U Sensor (1.0x):** captures full **`8192 x 6144`** (50 MP).
* **Periscope Samsung HP9 200MP (5.0x):** in High Resolution mode outputs up to **`16384 x 12288`** (~200 MP, file size 40–90 MB). Set HDR+ frames to **1 or 2 frames** for instantaneous processing.

##### 6. Whitelisted GCam Packages
The following package variants are explicitly included in `vendor.camera.aux.packagelist` and `persist.vendor.camera.privapp.list`:
* `com.google.android.GoogleCamera` (standard Google Pixel)
* `com.agc.cam` (official AGC clone)
* `com.agc.gcam96` (AGC 9.6)
* `com.samsung.android.scan3d` (popular AGC package bypassing vendor blocks)
* `com.samsung.android.ruler` (AGC Ruler)
* `com.ss.android.ugc.aweme` (AGC Aweme)
* `com.android.mgc` (BSG GCam)
* `com.shamim.cam` (Shamim GCam)
* `org.codeaurora.snapcam` (Snapdragon SnapCam)

---

### 9. Automated Diagnostic Tool (check_support.sh) (EN)

To quickly and reliably verify your device, ROM environment, root access, and the live status of all Qualcomm CamX overrides, a portable shell diagnostic script **`check_support.sh`** is provided.

#### Script Features:
* **Device Identification**: hardware codename (`ishtar`, `dada`, `haotian`, `xuanyuan`, `nezha`), SoC platform, and HyperOS/Android release.
* **Root Environment Check**: Superuser access (UID 0), SELinux status (Enforcing/Permissive), and detection of active module folders in Magisk, KernelSU, and APatch (`/data/adb/modules`).
* **Qualcomm CamX Hardware Properties**:
  - Full-resolution 50M/200M RAW buffer: `persist.vendor.camera.maxRAWSizes = 55`
  - Hardware DCG HDR: `persist.vendor.camera.dcg.enable = 1`
  - Sensor-level HDR: `persist.vendor.camera.sensor.hdr = 1`
  - ArcSoft AISP video noise reduction bypass: `persist.vendor.camera.arcsoft.aisp_algo_nr.bypass = 1`
  - Video bitrate multiplier: `persist.vendor.camera.video.bitrate.factor = 1.5`
  - Vendor DCG support flag: `ro.vendor.camera.dcg = 1`
* **AUX Whitelist Check**: verifies `vendor.camera.aux.packagelist` for GCam / AGC / LMC / Shamim packages.
* **Automated Log Export**:  
  📁 `/sdcard/Download/Mi_Camera_Diagnostic_Report.txt` (ready to attach directly to GitHub bug reports).

#### How to Run:

**Option 1: Directly on Device via Termux (Root Required)**
```bash
# Run directly from repository in one step:
curl -sSL https://raw.githubusercontent.com/bjorndith-cmd/Mi_Master_Camera_Combo/main/check_support.sh | su -c sh

# Or run locally if downloaded to storage:
su
sh /sdcard/Download/check_support.sh
```

**Option 2: From PC via ADB**
```bash
adb push check_support.sh /data/local/tmp/
adb shell "su -c sh /data/local/tmp/check_support.sh"
```

---

### 10. Frequently Asked Questions (FAQ) (EN)

<details>
<summary><b>What should I do on Xiaomi 13 Ultra (HyperOS 1.0.14.0 Android 14) if root dropped or screen went black?</b></summary>

This issue is 100% fixed! On Android 14, root dropped because permissive rules in `post-fs-data.sh` triggered Magisk Safe Mode, and the black screen was caused by overwriting the Camera HAL with an incompatible ported library.  
Flash the dedicated **Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip** module — it preserves native Camera HAL and APK, cleans boot scripts, and enables Quad-50MP on all lenses, DCG HDR, and 8K video with zero crash or root loss risk!
</details>

<details>
<summary><b>Does the camera crash on Xiaomi 17 Ultra (SimpleRom 3.0.309.0 - ST)?</b></summary>

No, this issue is 100% resolved in **v5.8**! For SimpleRom ST users, we recommend **X17U_Master_Imaging_MOD_v1.0_Slim**. It does not overwrite the custom camera APK, only applying sensor calibrations, DCG HDR, and video tweaks.
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

### 11. Feedback & Issue Reporting Templates (EN)

If you encounter an issue or wish to propose an enhancement, use our official interactive GitHub Issue forms in [Issues](../../issues/new/choose):

* 🐛 **[Bug Report](../../issues/new?template=bug_report.yml)** — structured bug report form for camera crashes, black screens, or viewfinder freezes. Please specify device model, ROM, and attach the `Mi_Camera_Diagnostic_Report.txt` diagnostic file.
* ⚙️ **[GCam Config & Preset Feedback](../../issues/new?template=config_feedback.yml)** — share your tuned `.agc` / `.xml` profiles, color matrix calibrations, or noise model adjustments for Sony, OmniVision, and Samsung sensors.
* 💡 **[Feature Request](../../issues/new?template=feature_request.yml)** — propose new features, support for new ROMs or camera hardware revisions.

---

## 📄 Technical Audit Report / Технический отчёт
For in-depth register dumps, dynamic linker analysis, and hardware profiles:  
👉 **[DETAILED_AUDIT_REPORT.md](./DETAILED_AUDIT_REPORT.md)**
