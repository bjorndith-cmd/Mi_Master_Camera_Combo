# Детальный технический отчёт: Архитектура, Аудит и Исправления Xiaomi Master Camera Combo

**Проект:** Xiaomi Master Camera Combo (Multi-Device Universal Suite)  
**Автор:** `borndead` (feat. itzdfplayer, amitkattal & GeorgeKiarie)  
**Целевые платформы:**
* **Xiaomi 13 Ultra** (`ishtar`, Snapdragon 8 Gen 2 / SM8550)
* **Xiaomi 15** (`dada`, Snapdragon 8 Elite / SM8750)
* **Xiaomi 15 Pro** (`haotian`, Snapdragon 8 Elite / SM8750)
* **Xiaomi 15 Ultra** (`xuanyuan`, Snapdragon 8 Elite / SM8750 — EUXM 3.0.9.0 + Stock AIO)
* **Xiaomi 17 Ultra** (`nezha`, Snapdragon 8 Elite / SM8750)  
**Операционные системы:** HyperOS 2.0 / HyperOS 3.0 (Android 15 / Android 16 — API 35/36)

---

## 1. Диагностика критического бага: зависание видоискателя в режиме «Фото» на Xiaomi 13 Ultra

### 1.1. Симптоматика
Пользователи модов `Mi13U_FULLRES_v0.2_HyperOS3_A16_by_itzdfplayer_port` сталкивались со следующим поведением:
* В модах GCam съемка в 50Мп на всех объективах работала штатно.
* Однако в **стоковом приложении камеры** при переходе в режим «Фото» (Mode 161) видоискатель отрисовывал ровно один первый кадр и **намертво замирал**. Спуск затвора зависал, переключение режимов блокировалось.

### 1.2. Анализ причин (Reverse Engineering)
Вскрытие и дизассемблирование байткода `MiuiCamera.apk` и конфигурационных XML-файлов `device_features/ishtar.xml` выявило две фундаментальные причины:

1. **Конфликт алгоритмов Super Resolution в режиме Mode 161**:
   * В исходном моде в `device_features/ishtar.xml` инжектировались следующие теги:
     ```xml
     <bool name="support_super_resolution">true</bool>
     <string name="support_super_resolution_zoom">0.5:1.0:3.2:5.0</string>
     <bool name="is_support_pixel_model">true</bool>
     <bool name="support_ultra_pixel">true</bool>
     ```
   * При запуске приложения камеры в режиме «Фото» по умолчанию устанавливается фокусное расстояние **1.0x** (основной сенсор Sony IMX989).
   * Метод `SuperResolutionProcessor` камеры Xiaomi проверяет список `support_super_resolution_zoom`. Обнаружив значение `1.0`, камера переключала обработчик кадрового потока в режим цифрового супер-разрешения (`mialgo_sr`).
   * Однако для 1-дюймового сенсора IMX989 аппаратный конвейер супер-разрешения на 1.0x в прошивке не поддерживается (сенсор работает в режиме прямого 4-в-1 биннинга Quad-Bayer). Обработчик кадров `SurfaceView` зависал в бесконечном ожидании буфера от незапущенного пайплайна. Видоискатель навечно застывал на первом кадре.

2. **Поломка логической многокамерности (SAT Arbitration)**:
   * В свойствах `system.prop` стоял параметр:
     ```properties
     vendor.camera.aux.packagelist=com.android.camera,...
     ```
   * Добавление пакета `com.android.camera` в белый список сторонних AUX-камер ломало внутренний механизм **SAT (Spatial Alignment Telephoto)**. Вместо переключения объективов под единым логическим идентификатором ID 0 стоковая камера получала прямой доступ к физическим сенсорам, что приводило к сбою инициализации сессии потоков (`CameraCaptureSession`).

### 1.3. Принятые инженерные решения
1. **Динамическая очистка XML в `customize.sh`**:
   Инсталлятор теперь производит полное удаление конфликтных тегов:
   ```bash
   for tag in \
       support_ultra_hd_zoom ultra_pixel_zoom_ratio_support_list \
       support_ultra_pixel_zoom_ratio support_super_resolution_zoom \
       is_support_ultra_hd is_support_pixel_model support_super_resolution \
       support_ultra_pixel support_50mp support_ultra_raw support_manual_ultra_raw; do
       sed -i "/$tag/d" "$TARGET_XML"
   done
   ```
2. **Чистая изоляция режимов**:
   * Режим «Фото» (Mode 161) оставлен в чистом биннинге 12.5Мп с кадровой частотой 60 fps и мгновенным спуском.
   * Полное разрешение 50Мп разблокировано **строго там, где оно должно работать** — в режиме «50M (Ultra HD)» (Mode 175) и в «Ultra RAW» в Pro-режиме:
     ```xml
     <bool name="is_support_ultra_hd">true</bool>
     <bool name="support_50mp">true</bool>
     <string name="support_ultra_hd_zoom">0.5:1.0:3.2:5.0</string>
     <bool name="support_ultra_raw">true</bool>
     <bool name="support_manual_ultra_raw">true</bool>
     ```
3. **Изоляция стоковой камеры от AUX-списка**:
   * Имя пакета `com.android.camera` исключено из `vendor.camera.aux.packagelist`.
   * Доступ оставлен только проверенным модам GCam (AGC, LMC, Shamim, BSG, BigKaka, OpenCamera).

---

## 2. Аппаратная технология DCG (Dual Conversion Gain / iDCG HDR)

### 2.1. Физический принцип
В флагманских сенсорах (Sony IMX989, Sony LYT-900, Light Hunter 900, OmniVision LOFIC) каждый пиксель оснащён двумя конденсаторами считывания с разным коэффициентом преобразования:
* **LCG (Low Conversion Gain)**: низкая чувствительность, но большая ёмкость потенциальной ямы. Предотвращает переэкспонирование (клиппинг) в светлых участках кадра.
* **HCG (High Conversion Gain)**: сверхвысокая чувствительность и предельно низкий шум считывания (Read Noise). Вытягивает чистый сигнал из теней.

В отличие от классического программного HDR (делающего несколько последовательных снимков с разной выдержкой, что приводит к гостингу и смазыванию движущихся объектов), **DCG считывает данные LCG и HCG одновременно с одного единственного кадра экспозиции**.

### 2.2. Реализация в HAL и системных свойствах
1. **В Qualcomm CamX HAL (`camera.qcom.so`)**:
   Задействованы нативные методы управления усилением и слиянием потоков:
   `EnableHDRDCGMode`, `HDRDCGMode`, `isDCGSupported`, `GetDCGHDRGainRatio`, `DCGCOMBINE`.
2. **В системных свойствах `system.prop`**:
   ```properties
   persist.vendor.camera.sensor.hdr=1
   persist.vendor.camera.dcg.enable=1
   persist.vendor.camera.hdr.dcg=1
   persist.vendor.camera.sensor.dcg=1
   ro.vendor.camera.dcg=1
   ```
3. **В вендорных флагах `device_features/*.xml`**:
   ```xml
   <bool name="support_camera_dcg">true</bool>
   <bool name="is_support_dcg">true</bool>
   <bool name="support_dcg_hdr">true</bool>
   <bool name="support_sensor_hdr">true</bool>
   <bool name="support_idcg">true</bool>
   ```

---

## 3. Интеграция официального стека Xiaomi 15 Ultra (`xuanyuan`) и Stock AIO

### 3.1. Разделение платформ `nezha` (прототип 17U) и `xuanyuan` (релиз 15U)
На раннем этапе кодовые имена `nezha` и `xuanyuan` объединялись в общий профиль. Однако после анализа официальной прошивки **EUXM 3.0.9.0** и пакета **Stock AIO 104** профили были разделены:
* **`nezha`**: инженерный прототип Xiaomi 17 Ultra с матрицей OmniVision OVX10500U.
* **`xuanyuan`**: коммерческий глобальный/европейский Xiaomi 15 Ultra с сенсором **Sony LYT-900**.

### 3.2. Компоненты, интегрированные из Stock AIO 104:
1. **Chromatix калибровки матриц `com.qti.tuned.*.bin`**:
   * `com.qti.tuned.xuanyuan_semco_LYT900_wide_i.bin` (34.27 МБ) — основная камера Sony LYT-900.
   * `com.qti.sensormodule.xuanyuan_semco_LYT900_wide_i.bin` (1.15 МБ) — дескриптор сенсора.
   * `com.qti.tuned.xuanyuan_semco_s5khp9_tele5x_i.bin` (21.45 МБ) — 200Мп перископ Samsung HP9.
   * `com.qti.tuned.xuanyuan_ofilm_imx858_tele3x_i.bin` (14.36 МБ) — 3x телевик Sony IMX858.
   * `com.qti.tuned.xuanyuan_sunny_s5kjn5_ultra_i.bin` (13.87 МБ) — ультраширик Samsung JN5.
   * `com.qti.tuned.xuanyuan_sunny_ov32b40_front_i.bin` (7.54 МБ) — фронтальная камера.
2. **Фирменные нейросетевые библиотеки обработки**:
   * `libremosaiclib.so` (33.82 МБ) — библиотека аппаратной ремозаики для 50Мп и 200Мп с поддержкой DMA-BUF heap под Android 15/16.
   * `libmialgo_ellc.so` (9.03 МБ) — алгоритм Extremely Low Light Capture (ночная съемка при освещении < 0.1 люкс).
   * `libmialgo_ainr_ll.so` (11.13 МБ) — нейросетевой алгоритм AI Noise Reduction.
3. **Официальный HAL HyperOS 3.0**:
   * Библиотека `camera.qcom.so` (10.18 МБ) скомпилирована с поддержкой `android.frameworks.sensorservice-V1-ndk.so` и `libbinder_ndk.so`.

---

## 4. Совместимость с Android 15/16 (API 35/36) и VNDK

### 4.1. Проблема устаревших HAL библиотек
В Android 15 и Android 16 компания Google полностью прекратила поддержку и удалила архитектуру **VNDK (Vendor NDK)**, заменив её на Mainline APEX и AIDL HAL.
* Попытка смонтировать в `/vendor/lib64/` старые библиотеки (например, `libqcodec2_v4l2codec.so`, требовавший `libcodec2_vndk.so`), приводит к фатальной ошибке динамического компоновщика:
  `CANNOT LINK EXECUTABLE ... library "libcodec2_vndk.so" not found`
* Поэтому в нашем комбайне повышение битрейта видео реализовано без опасных подмен библиотек, через нативные свойства системы:
  ```properties
  persist.vendor.camera.video.bitrate.factor=1.5
  media.camera.bitrate.factor=1.5
  ```

### 4.2. Умное ветвление HAL в `customize.sh`:
```bash
if [ "$API" -ge 35 ]; then
    ui_print "- Android 15/16 detected (API $API):"
    if [ "$DEV_PROFILE" = "xuanyuan" ]; then
        ui_print "  Deploying native HyperOS 3.0 / A16 HAL (EUXM 3.0.9.0) for Xiaomi 15 Ultra."
    else
        ui_print "  Preserving native A16 Camera HAL (prevents black screen)."
        ui_print "  FullRes unlocked via Chromatix bins + maxRAWSizes."
        rm -rf "$MODPATH/system/odm/lib64/hw"
        rm -rf "$MODPATH/system/vendor/odm/lib64/hw"
    fi
else
    ui_print "- Android 14 detected (API $API): keeping patched camera.qcom.so."
fi
```

---

## 5. Результаты автоматизированного аудита пакетов

Все собранные модули прошли валидацию с помощью скриптов аудита:
* ✅ **Целостность архивов (ZipTest)**: 0 битых файлов, CRC подтверждён для 100% файлов.
* ✅ **Отсутствие паразитных тегов**: блоки инжекции XML очищены от `support_super_resolution`.
* ✅ **Защита SAT-маршрутизации**: пакет `com.android.camera` отсутствует в `aux.packagelist`.
* ✅ **Безопасность SELinux**: в `customize.sh` и `post-fs-data.sh` прописаны правила `magiskpolicy` и контексты `vendor_file:s0` для всех `.so` и `.bin`.
* ✅ **Отключение отладочного дампа**: параметр `dump: 0` установлен во всех копиях `aisp.json`.
