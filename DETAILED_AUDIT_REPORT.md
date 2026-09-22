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

### 3.1. Разделение платформ `nezha` (17U) и `xuanyuan` (15U)
* **`nezha`**: Xiaomi 17 Ultra с 1-дюймовой матрицей OmniVision OVX10500U, телекамерой Samsung HP9 200MP, JN5 и фронтальной OV50M.
* **`xuanyuan`**: Xiaomi 15 Ultra с 1-дюймовым сенсором **Sony LYT-900**, телекамерой Samsung HP9 200MP, IMX858 3x, JN5 и фронтальной OV32B40.

### 3.2. Компоненты, интегрированные для Xiaomi 15 Ultra:
1. **Chromatix калибровки матриц `com.qti.tuned.*.bin`**:
   * `com.qti.tuned.xuanyuan_semco_LYT900_wide_i.bin` (34.27 МБ) — основная камера Sony LYT-900.
   * `com.qti.sensormodule.xuanyuan_semco_LYT900_wide_i.bin` (1.15 МБ) — дескриптор сенсора.
   * `com.qti.tuned.xuanyuan_semco_s5khp9_tele5x_i.bin` (21.45 МБ) — 200Мп перископ Samsung HP9.
   * `com.qti.tuned.xuanyuan_ofilm_imx858_tele3x_i.bin` (14.36 МБ) — 3x телевик Sony IMX858.
   * `com.qti.tuned.xuanyuan_sunny_s5kjn5_ultra_i.bin` (13.87 МБ) — ультраширик Samsung JN5.
   * `com.qti.tuned.xuanyuan_sunny_ov32b40_front_i.bin` (7.54 МБ) — фронтальная камера.
2. **Официальный HAL HyperOS 3.0 (Android 16)**:
   * Библиотека `camera.qcom.so` (10.18 МБ) из официальной сборки EUXM 3.0.9.0 скомпилирована с поддержкой `android.frameworks.sensorservice-V1-ndk.so` и `libbinder_ndk.so`.

---

## 4. Совместимость с Android 15/16 (API 35/36) и VNDK

### 4.1. Проблема устаревших HAL библиотек
В Android 15 и Android 16 компания Google полностью прекратила поддержку и удалила архитектуру **VNDK (Vendor NDK)**, заменив её на Mainline APEX и AIDL HAL.
* Умное ветвление HAL в `customize.sh` гарантирует, что на Android 15/16 для `ishtar`, `dada` и `nezha` сохраняется нативный системный Camera HAL, что предотвращает чёрный экран.

---

## 5. Аудит и устранение вылета камеры на Xiaomi 17 Ultra (`nezha`) (SimpleRom 3.0.309.0 - ST)

### 5.1. Симптоматика проблемы
Пользователь сообщил о фатальном падении камеры при установке модуля `Mi15U_X17U_Master_Camera_Combo_v5.0` на смартфон **Xiaomi 17 Ultra**, прошивка **3.0.309.0 SimpleRom - ST**:
> *«Tried the 15ux17u package and camera fully crashes - нужно исправить модуль»*

### 5.2. Комплексный технический анализ причин аварии (Root Cause Analysis)

1. **Фатальная ошибка динамического компоновщика (Unresolved Dynamic Dependency)**:
   * Пакет `Stock_AIO_104_DAS_FD_MI_LN2_v2.zip` содержал бинарные библиотеки: `libremosaiclib.so` (33.8 МБ), `libmialgo_ainr_ll.so` (11.1 МБ), `libmialgo_ellc.so` (9.0 МБ).
   * Исследование таблицы динамических секций ELF (`.dynamic`, заголовок `DT_NEEDED`) показало:
     ```
     libremosaiclib.so -> DT_NEEDED: libdlrmsc_android15.so
     libmialgo_ainr_ll.so -> DT_NEEDED: libmialgo_aisn.so
     libmialgo_ellc.so -> DT_NEEDED: libSNPE.so
     ```
   * Библиотека `libdlrmsc_android15.so` **отсутствует** в операционной системе Android 16 (HyperOS 3.0) и в прошивке SimpleRom!
   * При монтировании в `/odm/lib64/` системный компоновщик Android `/linker64` при попытке запуска `cameraserver` или процесса камеры немедленно аварийно завершал выполнение:
     `FATAL: CANNOT LINK EXECUTABLE: library "libdlrmsc_android15.so" not found`.

2. **Дефект структуры архива (Hardware Mismatch — подмена сенсоров 15U на 17U)**:
   * В сборке `Mi15U_X17U_Master_Camera_Combo_v5.0` при упаковке была опущена директория `devices/`. Вместо динамического монтажа файлы сенсоров Xiaomi 15 Ultra (`xuanyuan`: Sony LYT-900, IMX858 3x, OV32B40) и HAL `camera.qcom.so` (xuanyuan) были распакованы статически в корень `system/odm/`.
   * При установке на Xiaomi 17 Ultra (`nezha`) скрипт не находил `devices/nezha/odm/` и оставлял файлы `xuanyuan`.
   * Драйвер камеры Qualcomm CamX на Xiaomi 17 Ultra опрашивал сенсоры OmniVision OVX10500U и OV50M, но получал калибровки от Sony LYT-900. Инициализация сенсоров завершалась падением.

3. **Конфликт кастомной прошивки SimpleRom (ST) с системным APK**:
   * В прошивке **SimpleRom 3.0.309.0 - ST** системное приложение `MiuiCamera.apk` модифицировано автором прошивки (деодексировано, пропатчены smali-классы, применены другие ключи подписи).
   * Перезапись файла `/system/priv-app/MiuiCamera/MiuiCamera.apk` стоковым APK приводила к конфликту подписей, несоответствию классов виртуальной машины ART и падению камеры при открытии.

### 5.3. Принятые инженерные исправления

1. **Полное удаление повреждённых библиотек**:
   * Из всех сборок удалены `libremosaiclib.so`, `libmialgo_ainr_ll.so`, `libmialgo_ellc.so`.
   * Сохранена полностью самодостаточная и верифицированная библиотека `libmialgo_snsc.so`.
2. **Восстановление дерева `devices/` в комбо-пакетах**:
   * В `Mi15U_X17U_Master_Camera_Combo_v5.1` и `Mi_Master_Camera_Combo_Universal`:
     * Для `nezha` монтируются строго калибровки 17 Ultra:
       - `com.qti.tuned.nezha_semco_ovx10500u_wide_i.bin` (93.89 МБ)
       - `com.qti.tuned.nezha_semco_s5khpe_tele_i.bin` (50.14 МБ)
       - `com.qti.tuned.nezha_ofilm_s5kjn5_ultra_i.bin` (20.03 МБ)
       - `com.qti.tuned.nezha_sunny_ov50m_front_i.bin` (7.95 МБ)
       - `libqcodec2_v4l2codec.so` (видео-кодек 8K)
     * Для `xuanyuan` монтируются калибровки 15 Ultra и официальный A16 HAL.
3. **Интеллектуальный детектор кастомных прошивок в `customize.sh`**:
   ```bash
   IS_CUSTOM_ROM=false
   case "$BUILD_ID $BUILD_FLAVOR $MOD_DEV $ROM_VER" in
       *[Ss]imple*|*ST*|*st*|*[Ee][Uu]*|*[Ee]lite*|*[Pp]ulse*|*[Cc]ustom*)
           IS_CUSTOM_ROM=true
           ;;
   esac

   if [ "$IS_CUSTOM_ROM" = "true" ] || [ "$DEV_PROFILE" = "nezha" ]; then
       ui_print "- Custom ROM ($BUILD_ID) or Xiaomi 17 Ultra detected:"
       ui_print "  Preserving ROM's native patched MiuiCamera.apk (prevents crash)."
       rm -rf "$MODPATH/system/priv-app/MiuiCamera"
       rm -rf "$MODPATH/system/product/priv-app/MiuiCamera"
       rm -rf "$MODPATH/product/priv-app/MiuiCamera"
   fi
   ```
4. **Выпуск выделенного оверлей-модуля для 17 Ultra**:
   * Создан модуль **`X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`** (13.85 МБ).
   * Модуль работает в режиме чистого оверлея (`Pure Systemless Overlay`): он **вообще не содержит `MiuiCamera.apk`**, сохраняя встроенную камеру прошивки SimpleRom 3.0.309.0 - ST со всеми её модификациями, и внедряет только калибровки сенсоров, DCG Hardware HDR, видеомод 8K со всех линз, 4K120fps и обход шупомодавления AISP.

---

## 6. Сводная таблица результатов аудита модулей

| Модуль | Размер | Отсутствие битых .so | Разделение устройств | Сохранение APK на Custom ROM | Статус |
|---|---|---|---|---|---|
| `X17U_Master_Imaging_MOD_v1.0_Slim` | 13.85 МБ | ✅ 100% | ✅ Nezha only | ✅ APK не затрагивается | **ИДЕАЛЬНО (SimpleRom)** |
| `Mi15U_X17U_Master_Camera_Combo_v5.1` | 177.66 МБ | ✅ 100% | ✅ Дерево `devices/` | ✅ Авто-детект SimpleRom | **ИСПРАВЛЕНО** |
| `Mi_Master_Camera_Combo_Universal` | 195.13 МБ | ✅ 100% | ✅ Все 5 устройств | ✅ Авто-детект SimpleRom | **ИСПРАВЛЕНО** |
| `Mi13U_Master_Camera_Combo_v5.0` | 158.76 МБ | ✅ 100% | ✅ Ishtar only | ✅ Стандарт | **СТАБИЛЬНО** |
| `Mi13U_Master_Imaging_MOD_v1.0_Slim` | 270.4 КБ | ✅ 100% | ✅ Ishtar only | ✅ APK не затрагивается | **СТАБИЛЬНО** |
| `Mi15_Master_Camera_Combo_v5.0` | 151.58 МБ | ✅ 100% | ✅ Dada / Haotian | ✅ Стандарт | **СТАБИЛЬНО** |
