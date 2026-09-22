# Xiaomi Master Camera Combo (Universal Flagship Edition)

<p align="center">
  <b>Ультимативный комбайн камеры Leica для флагманов Xiaomi</b><br>
  <i>13 Ultra (ishtar) | 15 (dada) | 15 Pro (haotian) | 15 Ultra (xuanyuan) | 17 Ultra (nezha)</i><br>
  <b>HyperOS 2.0 / HyperOS 3.0 (Android 15 / Android 16 — API 35/36)</b>
</p>

<p align="center">
  <b>Автор сборки:</b> <code>borndead</code><br>
  <i>(feat. itzdfplayer, amitkattal & GeorgeKiarie)</i><br>
  <b>Версия:</b> <code>v5.7-Universal-DCG-AIO-A16</code>
</p>

---

## 📖 Оглавление
* [Что такое Master Camera Combo](#-что-такое-master-camera-combo)
* [Поддерживаемые устройства и характеристики](#-поддерживаемые-устройства-и-характеристики)
* [Ключевые технологии и возможности](#-ключевые-технологии-и-возможности)
  * [1. Устранение фриза видоискателя «Фото»](#1-устранение-фриза-видоискателя-фото)
  * [2. Аппаратный DCG (Dual Conversion Gain / iDCG HDR)](#2-аппаратный-dcg-dual-conversion-gain--idcg-hdr)
  * [3. Разблокировка 50Мп и 200Мп FullRes](#3-разблокировка-50мп-и-200мп-fullres)
  * [4. Stock AIO 104: сенсор Sony LYT-900 и нейросети](#4-stock-aio-104-сенсор-sony-lyt-900-и-нейросети)
  * [5. George Video MOD (8K, 4K120, чистый AISP)](#5-george-video-mod-8k-4k120-чистый-aisp)
  * [6. Интеллектуальный HAL-менеджер Android 15/16](#6-интеллектуальный-hal-менеджер-android-1516)
* [Доступные модули для загрузки](#-доступные-модули-для-загрузки)
* [Инструкция по установке](#-инструкция-по-установке)
* [Решение проблем (FAQ)](#-решение-проблем-faq)
* [Подробный технический отчёт](#-подробный-технический-отчёт)

---

## 📌 Что такое Master Camera Combo?

**Xiaomi Master Camera Combo** — это флагманский системный модуль для **Magisk (v26/27+)**, **KernelSU** и **APatch**, решающий все известные аппаратные и программные ограничения стоковой камеры Xiaomi на прошивках **HyperOS 2.0 и HyperOS 3.0** (Android 15 и Android 16).

Модуль оснащён **интеллектуальным инсталлятором**: при прошивке скрипт `customize.sh` на лету определяет кодовое имя подключенного смартфона (`ishtar`, `dada`, `haotian`, `xuanyuan` или `nezha`), монтирует индивидуальные сенсорные калибровки Qualcomm Chromatix, настраивает сетку зума 50M/200M и активирует безопасную конфигурацию для вашей платформы.

---

## 📱 Поддерживаемые устройства и характеристики

| Устройство | Кодовое имя | Процессор | Набор сенсоров | Сетка зума 50M/200M |
|---|---|---|---|---|
| **Xiaomi 13 Ultra** | `ishtar` | Snapdragon 8 Gen 2 (SM8550) | 1" Sony IMX989 + 3x Sony IMX858 + OV32C | **0.5x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15** | `dada` | Snapdragon 8 Elite (SM8750) | Light Hunter 900 + JN1 + JN5 + OV32B | **0.6x : 1.0x : 3.2x** |
| **Xiaomi 15 Pro** | `haotian` | Snapdragon 8 Elite (SM8750) | Light Hunter 900 + JN1 + IMX858 (5x) | **0.6x : 1.0x : 3.2x : 5.0x** |
| **Xiaomi 15 Ultra** | `xuanyuan` | Snapdragon 8 Elite (SM8750) | 1" Sony LYT-900 + Samsung HP9 200MP + IMX858 + JN5 | **0.5x : 1.0x : 3.0x : 5.0x** (до 200Мп!) |
| **Xiaomi 17 Ultra** | `nezha` | Snapdragon 8 Elite (SM8750) | 1" OVX10500U + Samsung HP9 200MP + JN5 + OV50M | **0.5x : 1.0x : 3.0x : 5.0x** (до 200Мп!) |

---

## ⚡ Ключевые технологии и возможности

### 1. Устранение фриза видоискателя «Фото»
* **Проблема прошлых модов**: в режиме «Фото» (Mode 161) на основном зуме 1.0x видоискатель делал один кадр и намертво замирал.
* **Причина**: паразитные теги `support_super_resolution`, `is_support_pixel_model` и `support_ultra_pixel` в `device_features` заставляли камеру запускать неподдерживаемый конвейер ремозаики `SuperResolutionProcessor` для 1-дюймовых матриц.
* **Исправление**: инсталлятор динамически вычищает конфликтные теги. Режим «Фото» работает на чистых 60 fps с мгновенным спуском затвора и оригинальными профилями **Leica Authentic** и **Leica Vibrant**.

### 2. Аппаратный DCG (Dual Conversion Gain / iDCG HDR)
* В каждом пикселе матрицы работают два параллельных узла считывания заряда:
  * **LCG (Low Conversion Gain)**: предотвращает пересвет источников света и неба.
  * **HCG (High Conversion Gain)**: сверхвысокая чувствительность и экстремально низкий шум в глубоких тенях.
* **Синхронное считывание с одного кадра**: в отличие от мульти-кадрового брекетинга, движущиеся объекты (дети, животные, авто) **не двоятся и не смазываются** (Zero Motion Ghosting).

### 3. Разблокировка 50Мп и 200Мп FullRes
* Параметр `persist.vendor.camera.maxRAWSizes=55` разблокирует вывод полноразмерного RAW в Qualcomm CamX.
* Режим «50M (Ultra HD)» доступен **на всех камерах** смартфона.
* Все моды Google Камеры (AGC, LMC, Shamim, BSG, BigKaka) и Pro-приложения получают полный доступ к физическим сенсорам в 50Мп/200Мп благодаря изолированному белому списку `vendor.camera.aux.packagelist`.
* Пакет стока `com.android.camera` строго исключён из aux-списка, что защищает штатную логическую многокамерность (SAT).

### 4. Stock AIO 104: сенсор Sony LYT-900 и нейросети
Специально для **Xiaomi 15 Ultra (`xuanyuan`)** интегрирован официальный релизный стек:
* Полная Chromatix калибровка `com.qti.tuned.xuanyuan_semco_LYT900_wide_i.bin` (**34.27 МБ**) для 1-дюймовой матрицы **Sony LYT-900**.
* **`libremosaiclib.so` (33.82 МБ)** — аппаратная ремозаика для сбора кристально резких 50Мп и 200Мп на базе современного Linux DMA-BUF heap.
* **`libmialgo_ellc.so` (9.03 МБ)** — алгоритм Extremely Low Light Capture для съёмки в темноте.
* **`libmialgo_ainr_ll.so` (11.13 МБ)** — нейросетевое шумоподавление AI Noise Reduction.

### 5. George Video MOD (8K, 4K120, чистый AISP)
* Запись видео **8K 24fps со всех задних сенсоров**.
* Режимы **4K 120fps**, **Dolby Vision 4K 60fps**, **LOG** и **Director Mode**.
* Твик `aisp.json` и свойство `persist.vendor.camera.arcsoft.aisp_algo_nr.bypass=1` отключают агрессивное размытие ArcSoft AISP, возвращая видео резкость и микроконтраст.
* Дамп отладки выключен (`dump: 0`), предотвращая забивание памяти тяжелыми логами.

### 6. Интеллектуальный HAL-менеджер Android 15/16
* **На Android 14 (API 34)**: монтируется кастомный `camera.qcom.so` для разблокировки 50Мп.
* **На Android 15/16 (API 35/36)**:
  * Для `ishtar` (13U) и `dada` (15): инсталлятор автоматически очищает старый A14 HAL, сохраняя нативный системный AIDL HAL и предотвращая чёрный экран.
  * Для `xuanyuan` (15U): монтируется официальный нативный HyperOS 3.0.9.0 A16 HAL с поддержкой `android.frameworks.sensorservice-V1-ndk.so`.

---

## 📦 Доступные модули для загрузки

Все архивы размещены в папке [`releases/`](./releases/):

| Файл модуля | Размер | Назначение |
|---|---|---|
| **[`Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip)** | **216.99 МБ** | **Универсальный комбайн (Рекомендуется!)** Автоматически определяет любое устройство из линейки (13U, 15, 15 Pro, 15U, 17U). Включает всё: Leica APK, FullRes, DCG, Stock AIO LYT-900, видеомод George. |
| **[`Mi15U_X17U_Master_Camera_Combo_v5.0_by_borndead.zip`](./releases/Mi15U_X17U_Master_Camera_Combo_v5.0_by_borndead.zip)** | **186.28 МБ** | **Выделенная сборка для Xiaomi 15 Ultra (`xuanyuan`) и 17 Ultra (`nezha`)**. Включает официальные калибровки Sony LYT-900, Samsung HP9 200MP, библиотеки AINR/ELLC/Remosaic и нативный A16 HAL. |
| **[`Mi13U_Master_Camera_Combo_v5.0_by_borndead.zip`](./releases/Mi13U_Master_Camera_Combo_v5.0_by_borndead.zip)** | **158.76 МБ** | **Выделенная сборка для Xiaomi 13 Ultra (`ishtar`)**. Полная Leica камера, Quad-50MP, DCG HDR, 8K со всех линз, фикс зависания видоискателя. |
| **[`Mi15_Master_Camera_Combo_v5.0_by_borndead.zip`](./releases/Mi15_Master_Camera_Combo_v5.0_by_borndead.zip)** | **151.58 МБ** | **Выделенная сборка для Xiaomi 15 (`dada`) и 15 Pro (`haotian`)**. |
| **[`Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip)** | **270.4 КБ** | **Облегченная версия для 13 Ultra (без приложения камеры)**. Только твики, калибровки сенсоров, DCG и George Video MOD. |
| **[`Mi13U_Master_Imaging_MOD_v1.0_Universal_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_v1.0_Universal_by_borndead.zip)** | **12.33 МБ** | Универсальная версия твиков для 13 Ultra с A14 HAL для старых прошивок. |

---

## 🚀 Инструкция по установке

1. Скачайте нужный архив из папки [`releases/`](./releases/).
2. Откройте **Magisk (v26+)**, **KernelSU** или **APatch**.
3. Перейдите в раздел **«Модули»** ➔ **«Установить из хранилища»**.
4. Выберите архив и дождитесь завершения установки.
5. Нажмите **«Перезагрузка»**.
6. *(Рекомендуется)* После первого включения очистите данные приложения «Камера» (`com.android.camera`) в «Настройки ➔ Приложения», чтобы сбросить старый кеш.

---

## ❓ Решение проблем (FAQ)

<details>
<summary><b>В режиме «Фото» видоискатель плавно работает?</b></summary>
Да, на 100%! Зависание на первом кадре полностью устранено благодаря удалению тегов Super Resolution из стандартного фото-режима.
</details>

<details>
<summary><b>Работает ли 50Мп в сторонних Google Camera (GCam)?</b></summary>
Да! Благодаря <code>maxRAWSizes=55</code> и правильной настройке <code>vendor.camera.aux.packagelist</code> все моды GCam (AGC, LMC, Shamim, BSG) видят физические камеры и снимают в полном разрешении 50Мп / 200Мп.
</details>

<details>
<summary><b>Почему модуль не требует Kitsune Magisk?</b></summary>
Оригинальные моды Джорджа требовали Kitsune из-за структуры <code>root/odm</code>. Мы перестроили файловую структуру в стандартный <code>system/odm/</code> и адаптировали SELinux, поэтому модуль шьётся через стандартный Magisk, KernelSU и APatch.
</details>

---

## 📄 Подробный технический отчёт

Полное техническое описание багов, дампы регистров, анализ библиотек и пошаговый отчёт об аудите доступны в отдельном документе:  
👉 **[DETAILED_AUDIT_REPORT.md](./DETAILED_AUDIT_REPORT.md)**
