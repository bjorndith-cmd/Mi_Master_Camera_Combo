import os
import re

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
readme_path = os.path.join(repo_root, 'README.md')

with open(readme_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize line endings
text = text.replace('\r\n', '\n')

# 1. Update Russian Navigation Menu
old_nav_ru = """## 📑 Меню навигации (RU)
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
   - [Совместимость с HyperOS 4.x / Android 17 (Xiaomi 17 Ultra)](#57-совместимость-с-новейшими-прошивками-hyperos-4x--android-17-тестирование-на-xiaomi-17-ultra-nezha-ru)
6. [Визуальные сравнения «До / После» и галерея интерфейса (Visual Proof)](#6-визуальные-сравнения-до--после-visual-proof-ru)
   - [Аппаратный DCG против программного мульти-кадрового HDR](#61-аппаратный-dcg-против-программного-мульти-кадрового-hdr-движение-в-кадре)
   - [Шумоподавление в видео: Сток ArcSoft AISP против George MOD Bypass](#62-шумоподавление-в-видео-сток-arcsoft-aisp-против-george-mod-bypass)
   - [Разрешающая способность: 12.5Мп Биннинг против 50Мп/200Мп FullRes](#63-разрешающая-способность-125мп-биннинг-против-50мп-и-200мп-fullres-100-crop)
   - [Реальные скриншоты интерфейса и подтверждение функций (UI Gallery)](#64-реальные-скриншоты-интерфейса-и-подтверждение-работы-всех-функций-ui-gallery)
7. [Инструкция по установке](#7-инструкция-по-установке-ru)
   - [🚨 Экстренное руководство: Как вернуть телефон из бутлупа](#71-экстренное-руководство-как-вернуть-телефон-из-бутлупа-циклической-перезагрузки-ru)
   - [⚠️ Разрешение конфликтов: Удаление сторонних модулей камеры](#72-разрешение-конфликтов-удаление-сторонних-модулей-камеры-черный-экран-краши-старый-значок-ru)
8. [Инструкция по тестированию и проверке работы модуля](#8-инструкция-по-тестированию-и-проверке-работы-модуля-для-всех-версий-ru)
   - [Настройка и проверка 50Мп/200Мп в Google Камере (AGC 8.x/9.x, LMC, Shamim)](#86-настройка-и-проверка-50мп--200мп-в-google-камере-agc-8x--9x-lmc-shamim-ru)
9. [Скрипт автоматической диагностики (check_support.sh)](#9-скрипт-автоматической-диагностики-check_supportsh-ru)
10. [Часто задаваемые вопросы (FAQ)](#10-часто-задаваемые-вопросы-faq-ru)
11. [Сообщество, обратная связь и Telegram](#11-сообщество-обратная-связь-и-telegram-ru)"""

new_nav_ru = """## 📑 Меню навигации (RU)
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
   - [Концепция двух линеек (FULL & SLIM) и устранение бутлупа](#57-концепция-двух-линеек-full--slim-и-устранение-бутлупа-на-xiaomi-13-ultra-hyperos-30302-taiwan--android-16-ru)
   - [Совместимость с HyperOS 4.x / Android 17 (Xiaomi 17 Ultra)](#58-совместимость-с-новейшими-прошивками-hyperos-4x--android-17-тестирование-на-xiaomi-17-ultra-nezha-ru)
6. [Экосистема искусственного интеллекта (AI Suite) 🤖🧠](#6-экосистема-искусственного-интеллекта-ai-suite-ru)
   - [Tier 1: Аппаратный ИИ вычислительной фотографии (Xiaomi AISP на NPU)](#61-tier-1-аппаратный-ии-вычислительной-фотографии-xiaomi-aisp-на-npu-snapdragon-ru)
   - [Tier 2: Генеративный ИИ постобработки (HyperAI Studio & ExtraPhoto)](#62-tier-2-генеративный-ии-постобработки-hyperai-studio--extraphoto-ru)
   - [Tier 3: AI-Ассистент видоискателя (AI Director & Vision HUD)](#63-tier-3-ai-ассистент-видоискателя-ai-director--vision-hud-ru)
7. [Визуальные сравнения «До / После» и галерея интерфейса (Visual Proof)](#7-визуальные-сравнения-до--после-visual-proof-ru)
   - [Аппаратный DCG против программного мульти-кадрового HDR](#71-аппаратный-dcg-против-программного-мульти-кадрового-hdr-движение-в-кадре)
   - [Шумоподавление в видео: Сток ArcSoft AISP против George MOD Bypass](#72-шумоподавление-в-видео-сток-arcsoft-aisp-против-george-mod-bypass)
   - [Разрешающая способность: 12.5Мп Биннинг против 50Мп/200Мп FullRes](#73-разрешающая-способность-125мп-биннинг-против-50мп-и-200мп-fullres-100-crop)
   - [Реальные скриншоты интерфейса и подтверждение функций (UI Gallery)](#74-реальные-скриншоты-интерфейса-и-подтверждение-работы-всех-функций-ui-gallery)
8. [Инструкция по установке](#8-инструкция-по-установке-ru)
   - [🚨 Экстренное руководство: Как вернуть телефон из бутлупа](#81-экстренное-руководство-как-вернуть-телефон-из-бутлупа-циклической-перезагрузки-ru)
   - [⚠️ Разрешение конфликтов: Удаление сторонних модулей камеры](#82-разрешение-конфликтов-удаление-сторонних-модулей-камеры-черный-экран-краши-старый-значок-ru)
9. [Инструкция по тестированию и проверке работы модуля](#9-инструкция-по-тестированию-и-проверке-работы-модуля-для-всех-версий-ru)
   - [Настройка и проверка 50Мп/200Мп в Google Камере (AGC 8.x/9.x, LMC, Shamim)](#96-настройка-и-проверка-50мп--200мп-в-google-камере-agc-8x--9x-lmc-shamim-ru)
10. [Скрипт автоматической диагностики (check_support.sh)](#10-скрипт-автоматической-диагностики-check_supportsh-ru)
11. [Часто задаваемые вопросы (FAQ)](#11-часто-задаваемые-вопросы-faq-ru)
12. [Сообщество, обратная связь и Telegram](#12-сообщество-обратная-связь-и-telegram-ru)"""

if old_nav_ru in text:
    text = text.replace(old_nav_ru, new_nav_ru)
    print("[OK] Russian Navigation updated")
else:
    print("[WARN] Russian Navigation not matched directly")

# 2. Add AI Suite table to Section 3 (RU)
ai_table_ru = """#### 🤖 Специализированные модули искусственного интеллекта (AI Suite)

| Модуль | Размер | Уровень | Описание |
|---|---|---|---|
| **[`Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip)** | **3.10 КБ** | **Tier 1 (NPU)** | **Аппаратный нейросетевой движок Xiaomi AISP**. 100% оффлайн на NPU Hexagon. FusionLM, ToneLM, ColorLM, PortraitLM, CyberFocus 2.0, AINR, супер-зум 30x–100x. Чистый оверлей без облачных сбоев. |
| **[`Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip)** | **3.12 КБ** | **Tier 2 (Studio)** | **Генеративный студийный комплекс HyperAI**. Прямая интеграция с видоискателем и галереей: AI Ластик Pro (Eraser 2.0), AI Расширение кадра (Outpainting), AI Небо 3.0 с динамическим релайтингом, 3D студийный свет. |
| **[`Mi_AI_Director_Vision_Companion_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Director_Vision_Companion_by_borndead.zip)** | **2.68 КБ** | **Tier 3 (Vision HUD)** | **Умный ассистент видоискателя AI Director**. Интеллектуальный HUD в реальном времени: динамические линии золотого сечения и третей Leica, высокоточный стабилизатор горизонта (±0.1°), советник по объективам и Pro-настройкам. |

"""

# Insert before Section 4 (RU)
old_sec4_ru = "### 4. Готовые пресеты конфигураций GCam (.agc) (RU)"
text = text.replace(old_sec4_ru, ai_table_ru + old_sec4_ru)
print("[OK] AI Table inserted into Section 3 (RU)")

# 3. Insert Section 6: AI Suite (RU) before Visual Comparisons
sec6_ai_ru = """### 6. Экосистема искусственного интеллекта (AI Suite) 🤖🧠 (RU)

В дополнение к базовым модулям FULL и SLIM разработана полноценная **трёхуровневая экосистема искусственного интеллекта**, раскрывающая аппаратный потенциал нейропроцессоров Qualcomm Hexagon NPU на Snapdragon 8 Gen 2 / 8 Gen 3 / 8 Elite.

<p align="center">
  <img src="./assets/ai_three_tiers_ecosystem.svg" alt="Xiaomi Master Camera AI Suite Ecosystem" width="100%">
</p>

---

#### 6.1. Tier 1: Аппаратный ИИ вычислительной фотографии (Xiaomi AISP на NPU Snapdragon) (RU)

Модуль: **[`Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip)** (3.10 КБ)

* **Что это такое**: Аппаратный пайплайн нейросетевой вычислительной фотографии, выполняющийся в микросекунды непосредственно в момент нажатия на кнопку затвора. Все вычисления производятся локально на NPU Hexagon и ISP Spectra.
* **Архитектура 4-LM (Large Models)**:
  1. ⚡ **FusionLM**: Многокадровое попиксельное слияние экспозиций в реальном времени. Устраняет двоение движущихся объектов (*Motion Ghosting*) и сохраняет чистый динамический диапазон.
  2. 🎨 **ToneLM**: Нейросетевая тональная компрессия. Анализирует карту освещения и формирует легендарную пленочную тональную кривую Leica.
  3. 🌈 **ColorLM**: Нейросетевая колориметрия. Сохраняет естественные оттенки человеческой кожи (*Skin Tone Fidelity*) и фирменные сочные цвета Leica Authentic / Vibrant.
  4. 🎯 **PortraitLM**: 3D-моделирование глубины сцены. Создает субмиллиметровую карту глубины для моделирования физического боке эталонных объективов Leica Noctilux 50mm f/0.95 и Summilux 35mm.
* **Дополнительные нейросетевые фичи**:
  - 🔭 **AISP Ultra Clear Zoom (30x–100x)**: Нейросетевое распознавание и дорисовывание фактуры (текста, архитектуры, листвы) на сверхдальних фокусных расстояниях.
  - 👁️ **CyberFocus 2.0**: Аппаратный нейротрекинг глаз людей, мордочек животных и спортивных объектов со скоростью 60 кадр/с.
  - 🛡️ **AINR (AI Noise Reduction)**: Аппаратный нейросетевой шумодав для съемки в кромешной тьме без смазывания деталей.
* **100% Защита от розового шума**: Облачные китайские эндпоинты принудительно отключены (`support_cloud_process=false`). 0% задержек сети, 0% розового шума!

<p align="center">
  <img src="./assets/ai_aisp_pipeline_architecture.svg" alt="AISP 4-LM Architecture" width="100%">
</p>

<p align="center">
  <img src="./assets/ai_hardware_aisp_diagram.jpg" alt="AISP Hardware Neural Diagram" width="100%" style="border-radius: 12px;">
</p>

---

#### 6.2. Tier 2: Генеративный ИИ постобработки (HyperAI Studio & ExtraPhoto) (RU)

Модуль: **[`Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip)** (3.12 КБ)

* **Что это такое**: Комплекс генеративных инструментов, доступных в один клик прямо из превью только что снятого кадра в камере (`com.android.camera` ➔ `com.miui.extraphoto`).
* **Ключевые генеративные инструменты**:
  - 🪄 **AI Ластик Pro (Eraser 2.0 / Magic Elimination)**: Интеллектуальное удаление прохожих, проводов, мусора и лишних объектов с кадра с мгновенным контекстным заполнением фона нейросетью.
  - 🖼️ **AI Расширение (Image Expansion / Outpainting)**: Генеративное дорисовывание окружения за пределами исходного кадра. Если композиция оказалась слишком тесной, ИИ плавно продолжит улицу, пейзаж или интерьер.
  - 🌌 **AI Небо 3.0 (Dynamic Relighting)**: Замена неба с автоматическим пересчетом освещения всей сцены (наложение естественных солнечных или закатных рефлексов на людей и асфальт).
  - 💡 **AI Студийный свет**: 3D-релайтинг лиц с перемещением виртуального источника света (софтбокс, контурный свет).
  - 🪟 **AI Удаление бликов и теней**: Нейросетевая поляризация, удаляющая отражения из стеклянных витрин и окон.

<p align="center">
  <img src="./assets/ai_genai_studio_ui.jpg" alt="HyperAI Studio Tools" width="100%" style="border-radius: 12px;">
</p>

---

#### 6.3. Tier 3: AI-Ассистент видоискателя (AI Director & Vision HUD) (RU)

Модуль: **[`Mi_AI_Director_Vision_Companion_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Director_Vision_Companion_by_borndead.zip)** (2.68 КБ)

* **Что это такое**: Интеллектуальный помощник фотографа, встроенный прямо в видоискатель камеры Leica. Работает в реальном времени, помогая выстроить композицию шедеврального уровня.
* **Возможности AI Director**:
  - 📐 **Динамические линии композиции**: Сетка золотого сечения (Fibonacci Spiral) и классическое правило третей, проецируемые с учетом геометрии сцены.
  - 🧭 **Высокоточный стабилизатор горизонта (±0.1°)**: Зеленая индикация идеального горизонта, исключающая «заваленные» пейзажи.
  - 🔍 **Умный советник по оптике (Lens Advisor)**: Анализирует расстояние до объекта и ненавязчиво подсказывает фокусное расстояние (например, *«Переключитесь на 3.2x для идеального поясного портрета без искажения пропорций лица»*).
  - ⚙️ **Smart Pro Suggester**: Автоматический анализ освещенности и предложение оптимальных параметров экспопары (ISO, выдержка, Focus Peaking) в режиме Профи.
  - 🔴 **Дизайн в стиле Leica**: Минималистичный полупрозрачный HUD-интерфейс в черных, белых и красных тонах, не перекрывающий видоискатель и элементы управления затвором.

<p align="center">
  <img src="./assets/ai_director_viewfinder_hud.jpg" alt="AI Director Viewfinder HUD" width="100%" style="border-radius: 12px;">
</p>

---

"""

# Renumber sections 6..11 -> 7..12 in RU
text = text.replace("### 6. Визуальные сравнения", sec6_ai_ru + "### 7. Визуальные сравнения")
text = text.replace("#### 6.1.", "#### 7.1.")
text = text.replace("#### 6.2.", "#### 7.2.")
text = text.replace("#### 6.3.", "#### 7.3.")
text = text.replace("#### 6.4.", "#### 7.4.")
text = text.replace("### 7. Инструкция по установке", "### 8. Инструкция по установке")
text = text.replace("#### 7.1.", "#### 8.1.")
text = text.replace("### 7.2.", "### 8.2.")
text = text.replace("### 8. Инструкция по тестированию", "### 9. Инструкция по тестированию")
text = text.replace("#### 8.1.", "#### 9.1.")
text = text.replace("#### 8.2.", "#### 9.2.")
text = text.replace("#### 8.3.", "#### 9.3.")
text = text.replace("#### 8.4.", "#### 9.4.")
text = text.replace("#### 8.5.", "#### 9.5.")
text = text.replace("#### 8.6.", "#### 9.6.")
text = text.replace("### 9. Скрипт автоматической диагностики", "### 10. Скрипт автоматической диагностики")
text = text.replace("### 10. Часто задаваемые вопросы (FAQ) (RU)", "### 11. Часто задаваемые вопросы (FAQ) (RU)")
text = text.replace("### 11. Сообщество, обратная связь и Telegram (RU)", "### 12. Сообщество, обратная связь и Telegram (RU)")

print("[OK] Section 6 inserted and RU sections renumbered")

# 4. Update English Navigation Menu
old_nav_en = """## 📑 Navigation Menu (EN)
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
   - [Anti-Crash Safeguard for Xiaomi 17 Ultra (SimpleRom ST, EU, Elite)](#56-anti-crash-safeguard-for-xiaomi-17-ultra-simplerom-st-eu-elite-and-anti-bootloop-on-xiaomi-13-ultra-taiwan-hos-30-en)
   - [Next-Gen OS Compatibility (HyperOS 4.x / Android 17): Testing on Xiaomi 17 Ultra](#57-next-gen-firmware-compatibility-hyperos-4x--android-17-testing-on-xiaomi-17-ultra-nezha-en)
6. [Visual Proof Gallery & UI Feature Showcase](#6-visual-proof-gallery-before-vs-after-en)
   - [Hardware DCG vs Conventional Multi-Frame Staggered HDR](#61-hardware-dcg-vs-conventional-multi-frame-staggered-hdr-motion-in-frame)
   - [Video Noise Reduction: Stock ArcSoft AISP Smear vs George MOD Bypass](#62-video-noise-reduction-stock-arcsoft-aisp-smear-vs-george-mod-bypass)
   - [Spatial Resolving Power: 12.5MP Binned vs 50MP & 200MP FullRes](#63-spatial-resolving-power-125mp-binned-vs-50mp--200mp-fullres-100-crop)
   - [Real-World Interface Screenshots & UI Feature Showcase](#64-real-world-interface-screenshots--ui-feature-showcase-en)
7. [Installation Guide](#7-installation-guide-en)
   - [🚨 Emergency Bootloop Recovery Guide](#71-emergency-guide-how-to-recover-from-a-bootloop-en)
   - [⚠️ Resolving Conflicts: Removing Prior Camera Modules](#72-resolving-conflicts-removing-prior-camera-modules-black-screen-crashes-old-icon-en)
8. [Verification & Testing Guide (All Devices & Versions)](#8-verification--testing-guide-all-devices--versions-en)
   - [Google Camera (AGC 8.x/9.x, LMC, Shamim) 50MP Setup & Guide](#86-google-camera-agc-8x--9x-lmc-shamim-50mp--200mp-configuration--testing-guide-en)
9. [Automated Diagnostic Tool (check_support.sh)](#9-automated-diagnostic-tool-check_supportsh-en)
10. [Frequently Asked Questions (FAQ)](#10-frequently-asked-questions-faq-en)
11. [Community, Feedback & Telegram Channel](#11-community-feedback--telegram-channel-en)"""

new_nav_en = """## 📑 Navigation Menu (EN)
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
   - [Anti-Crash Safeguard for Xiaomi 17 Ultra (SimpleRom ST, EU, Elite)](#56-anti-crash-safeguard-for-xiaomi-17-ultra-simplerom-st-eu-elite-and-anti-bootloop-on-xiaomi-13-ultra-taiwan-hos-30-en)
   - [Dual-Tier Architecture & Bootloop Elimination (Xiaomi 13 Ultra)](#57-dual-tier-architectural-concept-full--slim--xiaomi-13-ultra-bootloop-elimination-taiwan-hyperos-30--a16-en)
   - [Next-Gen OS Compatibility (HyperOS 4.x / Android 17): Testing on Xiaomi 17 Ultra](#58-next-gen-firmware-compatibility-hyperos-4x--android-17-testing-on-xiaomi-17-ultra-nezha-en)
6. [Artificial Intelligence Ecosystem (AI Suite) 🤖🧠](#6-artificial-intelligence-ecosystem-ai-suite-en)
   - [Tier 1: On-Device Hardware NPU Computational Photography (Xiaomi AISP)](#61-tier-1-on-device-hardware-npu-computational-photography-xiaomi-aisp-en)
   - [Tier 2: Generative Post-Processing Studio (HyperAI & ExtraPhoto)](#62-tier-2-generative-post-processing-studio-hyperai--extraphoto-en)
   - [Tier 3: Real-Time Viewfinder Assistant (AI Director & Vision HUD)](#63-tier-3-real-time-viewfinder-assistant-ai-director--vision-hud-en)
7. [Visual Proof Gallery & UI Feature Showcase](#7-visual-proof-gallery-before-vs-after-en)
   - [Hardware DCG vs Conventional Multi-Frame Staggered HDR](#71-hardware-dcg-vs-conventional-multi-frame-staggered-hdr-motion-in-frame)
   - [Video Noise Reduction: Stock ArcSoft AISP Smear vs George MOD Bypass](#72-video-noise-reduction-stock-arcsoft-aisp-smear-vs-george-mod-bypass)
   - [Spatial Resolving Power: 12.5MP Binned vs 50MP & 200MP FullRes](#73-spatial-resolving-power-125mp-binned-vs-50mp--200mp-fullres-100-crop)
   - [Real-World Interface Screenshots & UI Feature Showcase](#74-real-world-interface-screenshots--ui-feature-showcase-en)
8. [Installation Guide](#8-installation-guide-en)
   - [🚨 Emergency Bootloop Recovery Guide](#81-emergency-guide-how-to-recover-from-a-bootloop-en)
   - [⚠️ Resolving Conflicts: Removing Prior Camera Modules](#82-resolving-conflicts-removing-prior-camera-modules-black-screen-crashes-old-icon-en)
9. [Verification & Testing Guide (All Devices & Versions)](#9-verification--testing-guide-all-devices--versions-en)
   - [Google Camera (AGC 8.x/9.x, LMC, Shamim) 50MP Setup & Guide](#96-google-camera-agc-8x--9x-lmc-shamim-50mp--200mp-configuration--testing-guide-en)
10. [Automated Diagnostic Tool (check_support.sh)](#10-automated-diagnostic-tool-check_supportsh-en)
11. [Frequently Asked Questions (FAQ)](#11-frequently-asked-questions-faq-en)
12. [Community, Feedback & Telegram Channel](#12-community-feedback--telegram-channel-en)"""

if old_nav_en in text:
    text = text.replace(old_nav_en, new_nav_en)
    print("[OK] English Navigation updated")
else:
    print("[WARN] English Navigation not matched directly")

# 5. Add AI Suite table to Section 3 (EN)
ai_table_en = """#### 🤖 Dedicated Artificial Intelligence Suite (AI Modules)

| Module Package | Size | Tier | Description |
|---|---|---|---|
| **[`Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip)** | **3.10 KB** | **Tier 1 (NPU)** | **Xiaomi AISP Hardware Neural Engine**. 100% offline on Snapdragon Hexagon NPU. FusionLM, ToneLM, ColorLM, PortraitLM, CyberFocus 2.0, AINR, 30x–100x Super Resolution. Pure systemless overlay. |
| **[`Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip)** | **3.12 KB** | **Tier 2 (Studio)** | **HyperAI Generative Studio Suite**. Directly linked to Camera Preview & Gallery: AI Eraser Pro (Magic Elimination 2.0), AI Image Expansion (Outpainting), AI Sky 3.0 Dynamic Relighting, and Studio Portrait Light. |
| **[`Mi_AI_Director_Vision_Companion_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Director_Vision_Companion_by_borndead.zip)** | **2.68 KB** | **Tier 3 (Vision HUD)** | **Real-Time Viewfinder Assistant AI Director**. Intelligent live HUD: Leica golden ratio & rule-of-thirds composition guidelines, high-precision horizon leveling indicator (±0.1°), AI lens advisor, and Smart Pro mode coach. |

"""

old_sec4_en = "### 4. Ready-to-Use GCam Config Presets (.agc) (EN)"
text = text.replace(old_sec4_en, ai_table_en + old_sec4_en)
print("[OK] AI Table inserted into Section 3 (EN)")

# 6. Insert Section 6: AI Suite (EN) before Visual Comparisons
sec6_ai_en = """### 6. Artificial Intelligence Ecosystem (AI Suite) 🤖🧠 (EN)

Complementing the base FULL and SLIM editions, the project introduces a dedicated **Tri-Tier Artificial Intelligence Suite** designed to tap into the full hardware potential of Qualcomm Hexagon NPU on Snapdragon 8 Gen 2 / 8 Gen 3 / 8 Elite.

<p align="center">
  <img src="./assets/ai_three_tiers_ecosystem.svg" alt="Xiaomi Master Camera AI Suite Ecosystem" width="100%">
</p>

---

#### 6.1. Tier 1: On-Device Hardware NPU Computational Photography (Xiaomi AISP) (EN)

Module: **[`Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Master_Imaging_AISP_Hardware_by_borndead.zip)** (3.10 KB)

* **What it does**: Direct on-device hardware computational photography executing in real time at shutter click across Snapdragon Hexagon NPU and Spectra ISP.
* **4-LM (Large Models) Computational Architecture**:
  1. ⚡ **FusionLM**: Multi-exposure pixel-by-pixel alignment in real time. Completely prevents motion ghosting while maximizing genuine dynamic range.
  2. 🎨 **ToneLM**: Neural tone curve compression. Analyzes the scene's luminance matrix to model Leica's analog optical contrast curve.
  3. 🌈 **ColorLM**: Neural spectral fidelity. Preserves lifelike human skin tones and true-to-life Leica Authentic & Vibrant aesthetics.
  4. 🎯 **PortraitLM**: 3D spatial depth estimation. Renders millimeter-accurate depth maps to simulate optical bokeh from legendary lenses like Leica Noctilux 50mm f/0.95 and Summilux 35mm.
* **Additional Neural Features**:
  - 🔭 **AISP Ultra Clear Zoom (30x–100x)**: Neural texture synthesis restoring architectural lines, distant typography, and foliage.
  - 👁️ **CyberFocus 2.0**: Hardware eye and subject motion tracking at 60 fps.
  - 🛡️ **AINR (Hardware AI Noise Reduction)**: Raw-domain neural noise filtering for ultra-clean extreme low-light captures.
* **100% Offline & Magenta-Free**: Cloud processing endpoints are completely disabled (`support_cloud_process=false`). Zero cloud lag, zero pink noise!

<p align="center">
  <img src="./assets/ai_aisp_pipeline_architecture.svg" alt="AISP 4-LM Architecture" width="100%">
</p>

<p align="center">
  <img src="./assets/ai_hardware_aisp_diagram.jpg" alt="AISP Hardware Neural Diagram" width="100%" style="border-radius: 12px;">
</p>

---

#### 6.2. Tier 2: Generative Post-Processing Studio (HyperAI & ExtraPhoto) (EN)

Module: **[`Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Studio_GenAI_ExtraPhoto_by_borndead.zip)** (3.12 KB)

* **What it does**: On-device generative editing tools accessible with one tap directly from the camera preview thumbnail (`com.android.camera` ➔ `com.miui.extraphoto`).
* **Generative AI Toolset**:
  - 🪄 **AI Eraser Pro (Magic Elimination 2.0)**: Neural segmentation and contextual inpainting to erase passersby, wires, and unwanted background objects seamlessly.
  - 🖼️ **AI Image Expansion (Outpainting)**: Synthesizes surrounding scenery beyond the frame boundaries if your composition was framed too tightly.
  - 🌌 **AI Sky 3.0 (Dynamic Relighting)**: Replaces overcast skies with sunsets or starry nights while automatically recalculating environmental ambient light reflections on subjects.
  - 💡 **AI Portrait Studio Lighting**: 3D face mesh relighting with virtual softbox and rim light placement.
  - 🪟 **AI Reflection & Shadow Remover**: Neural polariser eliminating window reflections and document shadows.

<p align="center">
  <img src="./assets/ai_genai_studio_ui.jpg" alt="HyperAI Studio Tools" width="100%" style="border-radius: 12px;">
</p>

---

#### 6.3. Tier 3: Real-Time Viewfinder Assistant (AI Director & Vision HUD) (EN)

Module: **[`Mi_AI_Director_Vision_Companion_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Director_Vision_Companion_by_borndead.zip)** (2.68 KB)

* **What it does**: An intelligent live assistant embedded into the Leica Camera viewfinder, coaching composition and framing in real time.
* **Core Capabilities**:
  - 📐 **Dynamic Composition Lines**: Rule-of-thirds grid and Fibonacci Golden Spiral dynamically overlaid over the live scene.
  - 🧭 **High-Precision Horizon Stabilizer (±0.1°)**: Active green level indicator ensuring landscape horizons are perfectly straight.
  - 🔍 **AI Lens Advisor**: Analyzes subject distance and unobtrusively recommends the ideal sensor (e.g. *«Switch to 3.2x Portrait Telephoto for distortion-free portraits»*).
  - ⚙️ **Smart Pro Suggester**: Scene histogram analysis providing optimal ISO, shutter speed, and focus peaking recommendations in Pro mode.
  - 🔴 **Minimalist Leica Aesthetic**: Non-intrusive translucent HUD styled with Leica dark elegance that never obscures shutter or mode controls.

<p align="center">
  <img src="./assets/ai_director_viewfinder_hud.jpg" alt="AI Director Viewfinder HUD" width="100%" style="border-radius: 12px;">
</p>

---

"""

# Renumber sections 6..11 -> 7..12 in EN
text = text.replace("### 6. Visual Proof Gallery", sec6_ai_en + "### 7. Visual Proof Gallery")
text = text.replace("#### 6.1. Hardware DCG", "#### 7.1. Hardware DCG")
text = text.replace("#### 6.2. Video Noise Reduction", "#### 7.2. Video Noise Reduction")
text = text.replace("#### 6.3. Spatial Resolving Power", "#### 7.3. Spatial Resolving Power")
text = text.replace("#### 6.4. Real-World Interface Screenshots", "#### 7.4. Real-World Interface Screenshots")
text = text.replace("### 7. Installation Guide", "### 8. Installation Guide")
text = text.replace("#### 7.1. Emergency Guide", "#### 8.1. Emergency Guide")
text = text.replace("### 7.2. ⚠️ Resolving Conflicts", "### 8.2. ⚠️ Resolving Conflicts")
text = text.replace("### 8. Verification & Testing Guide", "### 9. Verification & Testing Guide")
text = text.replace("#### 8.1. Post-Installation Verification", "#### 9.1. Post-Installation Verification")
text = text.replace("#### 8.2. Verifying 50MP/200MP", "#### 9.2. Verifying 50MP/200MP")
text = text.replace("#### 8.3. Hardware DCG HDR", "#### 9.3. Hardware DCG HDR")
text = text.replace("#### 8.4. George Video MOD", "#### 9.4. George Video MOD")
text = text.replace("#### 8.5. SAT Logical Multi-Camera", "#### 9.5. SAT Logical Multi-Camera")
text = text.replace("#### 8.6. Google Camera", "#### 9.6. Google Camera")
text = text.replace("### 9. Automated Diagnostic Tool", "### 10. Automated Diagnostic Tool")
text = text.replace("### 10. Frequently Asked Questions (FAQ) (EN)", "### 11. Frequently Asked Questions (FAQ) (EN)")
text = text.replace("### 11. Community, Feedback & Telegram Channel (EN)", "### 12. Community, Feedback & Telegram Channel (EN)")

print("[OK] Section 6 inserted and EN sections renumbered")

# 7. Add AI FAQ entry in RU & EN
faq_ai_ru = """<details>
<summary><b>Можно ли устанавливать модули AI Suite вместе с FULL или SLIM версиями? Будут ли конфликты?</b></summary>

**Да, модули AI Suite на 100% совместимы со всеми версиями (FULL и SLIM) и могут устанавливаться как по отдельности, так и все вместе!**
* **Tier 1 (AISP Hardware)** работает на уровне драйверов Qualcomm CamX и чипа Hexagon NPU — он активирует вычислительные алгоритмы при съемке.
* **Tier 2 (HyperAI Studio)** работает на уровне галереи и редактора ExtraPhoto — он активирует генеративный ластик и расширение кадра.
* **Tier 3 (AI Director)** работает в видоискателе — он выводит умные подсказки композиции и горизонт.
Они не перезаписывают одни и те же файлы и не содержат сторонних APK, поэтому риск бутлупа равен **0%**!
</details>

"""

faq_ai_en = """<details>
<summary><b>Can I install AI Suite modules together with FULL or SLIM editions? Are there any conflicts?</b></summary>

**Yes, AI Suite modules are 100% compatible with both FULL and SLIM editions, and can be installed individually or simultaneously!**
* **Tier 1 (AISP Hardware)** operates at Qualcomm CamX driver and Hexagon NPU level, unlocking computational photography algorithms at capture.
* **Tier 2 (HyperAI Studio)** operates at Gallery & ExtraPhoto editor level, unlocking generative eraser and outpainting tools.
* **Tier 3 (AI Director)** operates in the viewfinder, rendering composition coaching guidelines and leveling HUD.
They target separate system layers and do not conflict. Bootloop risk is **0%**!
</details>

"""

text = text.replace("### 12. Сообщество, обратная связь и Telegram (RU)", faq_ai_ru + "### 12. Сообщество, обратная связь и Telegram (RU)")
text = text.replace("### 12. Community, Feedback & Telegram Channel (EN)", faq_ai_en + "### 12. Community, Feedback & Telegram Channel (EN)")

with open(readme_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print(f"[SUCCESS] README.md updated with complete AI Suite documentation at {readme_path}")
