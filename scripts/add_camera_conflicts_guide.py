import sys
import os

readme_path = r'C:\Users\ASTA\OneDrive\Документы\GitHub\Mi_Master_Camera_Combo\README.md'

with open(readme_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize line endings to LF first for clean matching
text = text.replace('\r\n', '\n')

# 1. Update RU TOC
old_ru_toc = """7. [Инструкция по установке](#7-инструкция-по-установке-ru)
   - [🚨 Экстренное руководство: Как вернуть телефон из бутлупа](#71-экстренное-руководство-как-вернуть-телефон-из-бутлупа-циклической-перезагрузки-ru)"""

new_ru_toc = """7. [Инструкция по установке](#7-инструкция-по-установке-ru)
   - [🚨 Экстренное руководство: Как вернуть телефон из бутлупа](#71-экстренное-руководство-как-вернуть-телефон-из-бутлупа-циклической-перезагрузки-ru)
   - [⚠️ Разрешение конфликтов: Удаление сторонних модулей камеры](#72-разрешение-конфликтов-удаление-сторонних-модулей-камеры-черный-экран-краши-старый-значок-ru)"""

assert old_ru_toc in text, "RU TOC not found"
text = text.replace(old_ru_toc, new_ru_toc, 1)

# 2. Update EN TOC
old_en_toc = """7. [Installation Guide](#7-installation-guide-en)
   - [🚨 Emergency Bootloop Recovery Guide](#71-emergency-guide-how-to-recover-from-a-bootloop-en)"""

new_en_toc = """7. [Installation Guide](#7-installation-guide-en)
   - [🚨 Emergency Bootloop Recovery Guide](#71-emergency-guide-how-to-recover-from-a-bootloop-en)
   - [⚠️ Resolving Conflicts: Removing Prior Camera Modules](#72-resolving-conflicts-removing-prior-camera-modules-black-screen-crashes-old-icon-en)"""

assert old_en_toc in text, "EN TOC not found"
text = text.replace(old_en_toc, new_en_toc, 1)

# 3. Add Warning in Section 7 RU and update installation steps
old_ru_install = """> [!IMPORTANT]
> **Тестирование на HyperOS 4.x (Android 17) на Xiaomi 17 Ultra (`nezha`):**
> Для новых прошивок HyperOS 4 используйте **СТРОГО SLIM Edition** ([`X17U_Master_Imaging_MOD_Slim_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/X17U_Master_Imaging_MOD_Slim_by_borndead.zip)). Установка FULL-версии на HyperOS 4 категорически запрещена во избежание сбоя подписи `MiuiCamera.apk`. Подробнее см. в [Разделе 5.7](#57-совместимость-с-новейшими-прошивками-hyperos-4x--android-17-тестирование-на-xiaomi-17-ultra-nezha-ru).

#### 📦 Пошаговый процесс установки модуля камеры:

1. **Скачайте необходимый zip-архив** из папки [`releases/`](https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo/tree/main/releases) (см. [Таблицу версий в Разделе 3](#3-таблица-модулей-и-ссылки-на-загрузку-ru)):"""

new_ru_install = """> [!IMPORTANT]
> **Тестирование на HyperOS 4.x (Android 17) на Xiaomi 17 Ultra (`nezha`):**
> Для новых прошивок HyperOS 4 используйте **СТРОГО SLIM Edition** ([`X17U_Master_Imaging_MOD_Slim_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/X17U_Master_Imaging_MOD_Slim_by_borndead.zip)). Установка FULL-версии на HyperOS 4 категорически запрещена во избежание сбоя подписи `MiuiCamera.apk`. Подробнее см. в [Разделе 5.7](#57-совместимость-с-новейшими-прошивками-hyperos-4x--android-17-тестирование-на-xiaomi-17-ultra-nezha-ru).

> [!WARNING]
> #### 🛑 ОБЯЗАТЕЛЬНАЯ ПОДГОТОВКА: Полное удаление сторонних модулей камеры!
> Если ранее в Magisk / KernelSU / APatch были установлены **ЛЮБЫЕ другие модули для камеры** (предыдущие версии мода, Leica Camera mods, Leica sound/features enablers, George Video MOD, Civi camera, AIO camera, 60fps mods и т.д.):  
> ⚠️ **ПРОСТОЕ ОТКЛЮЧЕНИЕ (выключение тумблера) СТАРЫХ МОДУЛЕЙ НЕ ПОМОЖЕТ!**  
> При простом выключении в системе сохраняется скомпилированный кэш в dalvik-cache, остаточные оверлеи OverlayFS и системные свойства `persist.*`, что приводит к **чёрному экрану видоискателя, мгновенному вылету (крашу) камеры или сохранению старого значка/интерфейса**.  
> **ОБЯЗАТЕЛЬНЫЙ ПОРЯДОК ПОДГОТОВКИ:**  
> 1. Полностью **УДАЛИТЕ** старые модули камеры (через значок корзины в Magisk/KernelSU/APatch).  
> 2. Удалите обновления приложения Камера: *Настройки ➔ Приложения ➔ Камера ➔ «Удалить обновления»* (если кнопка есть) и *«Очистить всё»*.  
> 3. **ОБЯЗАТЕЛЬНО ПЕРЕЗАГРУЗИТЕ ТЕЛЕФОН**.  
> 4. Только после чистой перезагрузки устанавливайте наш новый модуль!  
> Подробный технический анализ см. в [Разделе 7.2](#72-разрешение-конфликтов-удаление-сторонних-модулей-камеры-черный-экран-краши-старый-значок-ru).

#### 📦 Пошаговый процесс установки модуля камеры:

1. **Предварительно удалите старые модули камеры и перезагрузите телефон** (см. предупреждение выше).
2. **Скачайте необходимый zip-архив** из папки [`releases/`](https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo/tree/main/releases) (см. [Таблицу версий в Разделе 3](#3-таблица-модулей-и-ссылки-на-загрузку-ru)):"""

assert old_ru_install in text, "RU Install block not found"
text = text.replace(old_ru_install, new_ru_install, 1)

# Also update step numbering in RU:
old_ru_steps_end = """2. Откройте **Magisk (v26+)**, **KernelSU** или **APatch**.
3. Зайдите в раздел **«Модули»** ➔ **«Установить из хранилища»** и выберите скачанный zip-архив.
4. Дождитесь завершения работы скрипта инсталляции и нажмите **«Перезагрузка»**.
5. *(Обязательно)* После перезагрузки очистите данные приложения Камера:  
   *Настройки ➔ Приложения ➔ Все приложения ➔ Камера ➔ Очистить всё*."""

new_ru_steps_end = """3. Откройте **Magisk (v26+)**, **KernelSU** или **APatch**.
4. Зайдите в раздел **«Модули»** ➔ **«Установить из хранилища»** и выберите скачанный zip-архив.
5. Дождитесь завершения работы скрипта инсталляции и нажмите **«Перезагрузка»**.
6. *(Обязательно)* После перезагрузки очистите данные приложения Камера:  
   *Настройки ➔ Приложения ➔ Все приложения ➔ Камера ➔ Очистить всё*."""

assert old_ru_steps_end in text, "RU steps end not found"
text = text.replace(old_ru_steps_end, new_ru_steps_end, 1)

# 4. Add Section 7.2 RU before Section 8 RU
section_7_2_ru = """
<a name="72-разрешение-конфликтов-удаление-сторонних-модулей-камеры-черный-экран-краши-старый-значок-ru"></a>
### 7.2. ⚠️ Разрешение конфликтов: Почему отключение старых модулей камеры не помогает и как правильно очистить систему (RU)

Если после установки модуля вы столкнулись с одним из следующих симптомов:
* 🔲 **Чёрный экран в видоискателе** (видоискатель не выводит изображение или зависает в чёрном окне при открытии приложения);
* 🏷️ **Остался старый значок / старый интерфейс камеры** (после прошивки FULL-версии иконка приложения и меню не обновились до HyperOS 3.0 Leica);
* 💥 **Моментальный вылет (краш / Force Close)** камеры при запуске или при переключении между фокусными расстояниями (0.5x, 1x, 3.2x, 5.0x);
* ⚠️ **Системная ошибка «Не удалось подключиться к камере»** (CameraServer error);

— **в 99% случаев причиной является скрытый конфликт с остатками ранее установленных модулей камеры или закэшированных обновлений**.

---

#### 🔬 Технический анализ: Почему простое отключение (тумблер) в Magisk / KernelSU НЕ РАБОТАЕТ

Многие пользователи считают, что для проверки или перехода на новый мод достаточно сдвинуть переключатель (Disable) старого модуля в менеджере рута. **Однако на уровне подсистем Android и ядра Linux это НЕ устраняет конфликт:**

1. 📂 **Приоритет пользовательских обновлений (`/data/app`) над системными оверлеями**:
   - Если ранее сторонний модуль (или пользователь вручную) устанавливал обновление `MiuiCamera.apk`, операционная система Android помещает его в пользовательский раздел:
     ```text
     /data/app/~~...com.android.camera.../
     ```
   - В архитектуре Android приложения, находящиеся в каталоге `/data/app`, имеют **абсолютный приоритет** над системными приложениями в `/product/priv-app/` и `/system/priv-app/`.
   - Даже когда Magisk монтирует новый полнофункциональный `MiuiCamera.apk` в системный раздел, служба `PackageManagerService` всё равно загружает старый APK из `/data/app`!
   - **Результат**: значок камеры остаётся старым, интерфейс не меняется, а при попытке старого приложения обратиться к новым калибровкам и библиотекам камера немедленно вылетает.

2. 🧠 **Скомпилированный кэш виртуальной машины ART (dalvik-cache)**:
   - При первом запуске любого приложения виртуальная машина Android ART компилирует его dex-байткод в оптимизированный машинный код и сохраняет его в:
     ```text
     /data/dalvik-cache/arm64/
     /data/system/package_cache/
     ```
   - Простое выключение тумблера модуля в Magisk создаёт пустой файл-метку `/data/adb/modules/<mod>/disable`, но **НЕ очищает dalvik-cache**.
   - При следующей загрузке Android подгружает скомпилированный код старой версии камеры со старыми зависимостями библиотек. Несовпадение адресов методов и сигнатур в оперативной памяти приводит к аварийному завершению процесса `com.android.camera` или черному экрану видоискателя.

3. ⚙️ **Персистентные системные свойства (`persist.*`)**:
   - Сторонние модули камер часто выполняют команды `setprop persist.vendor.camera...`.
   - Свойства с префиксом `persist.` сохраняются физически в энергонезависимой базе параметров:
     ```text
     /data/property/persistent_properties
     ```
   - Отключение модуля **никак не сбрасывает** эти свойства. Конфликтные флаги продолжают заставлять драйвер камеры Qualcomm обращаться к некорректным веткам алгоритмов.

4. 🗂️ **Остаточные слои файловой системы OverlayFS**:
   - При отключении модуля без удаления его директория физически остаётся в `/data/adb/modules/`.
   - На некоторых ядрах и версиях Magisk/KernelSU дерево каталогов отключенного модуля может частично попадать в структуру монтирования верхнего слоя оверлея, блокируя монтирование новых файлов нашего модуля.

---

#### 📋 Пошаговый регламент чистой установки (Clean Reinstall Protocol)

Чтобы раз и навсегда исключить любые конфликты и получить стабильную работу камеры:

##### Шаг 1: Полное удаление старых модулей через корзину
1. Откройте **Magisk**, **KernelSU** или **APatch** ➔ перейдите на вкладку **«Модули»**.
2. Найдите **ВСЕ** когда-либо установленные модули, связанные с камерой (Leica Camera, Civi mod, George video, старые версии Mi Master Camera, AIO Camera, модули звуков затвора и т.п.).
3. Нажмите на значок **КОРЗИНЫ (Удалить)** напротив каждого из них.
   > ⚠️ **НЕ просто выключите тумблер, а именно нажмите «Удалить»!**

##### Шаг 2: Удаление обновлений приложения Камера в настройках Android
1. Откройте *Настройки ➔ Приложения ➔ Все приложения ➔ Камера*.
2. Внизу экрана проверьте наличие кнопки **«Удалить обновления»**:
   - Если кнопка есть — **обязательно нажмите её**! Это удалит конфликтующий старый APK из `/data/app`.
3. Нажмите кнопку **«Очистить всё»** (Очистить кэш и стереть все данные приложения камеры).

##### Шаг 3: ОБЯЗАТЕЛЬНАЯ ПРОМЕЖУТОЧНАЯ ПЕРЕЗАГРУЗКА
1. Перезагрузите смартфон.
2. **Зачем это нужно:** во время перезагрузки рут-менеджер физически стирает папки удалённых модулей из `/data/adb/modules/`, освобождает точки монтирования OverlayFS, а Android удаляет устаревшие кэши пакетов.

##### Шаг 4: Установка нашего модуля
1. После чистой перезагрузки откройте Magisk / KernelSU / APatch.
2. Установите скачанный zip-архив нашего модуля (`Mi_Master_Camera_Combo...` / `Mi13U...` / `Mi14U...` / `X17U...` / `Mi15U...` / `Mi15...`).
3. Дождитесь успешного окончания скрипта инсталляции.

##### Шаг 5: Финальная перезагрузка и первый запуск
1. Нажмите кнопку **«Перезагрузка»**.
2. После запуска системы перейдите в *Настройки ➔ Приложения ➔ Все приложения ➔ Камера ➔ Очистить всё*.
3. Откройте камеру. Приложение запустится мгновенно, с новым значком, обновленным интерфейсом Leica и полным доступом ко всем сенсорам без вылетов и зависаний!

---
"""

old_before_s8_ru = """### 8. Инструкция по тестированию и проверке работы модуля (для всех версий) (RU)"""
assert old_before_s8_ru in text, "Section 8 RU start not found"
text = text.replace(old_before_s8_ru, section_7_2_ru + old_before_s8_ru, 1)

# 5. Fix duplicate Xiaomi 14 Ultra English block in Section 8.2 RU
duplicate_14u_block = """##### 📱 Xiaomi 14 Ultra (`aurora`)
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

"""

assert duplicate_14u_block in text, "Duplicate 14U block not found"
# Remove from RU section
text = text.replace(duplicate_14u_block, "", 1)

# And insert it into EN Section 8.2 right before Xiaomi 13 Ultra!
old_en_before_13u = """##### 📱 Xiaomi 13 Ultra (`ishtar`)
* **HyperOS 1.0 (Android 14) Verification**:"""

assert old_en_before_13u in text, "EN 13U block not found"
text = text.replace(old_en_before_13u, duplicate_14u_block + old_en_before_13u, 1)

# 6. Add Section 10 FAQ item in RU
old_ru_faq_end = """<details>
<summary><b>Плавный ли видоискатель в режиме «Фото»?</b></summary>"""

new_ru_faq_item = """<details>
<summary><b>После установки появился черный экран в видоискателе, камера вылетает или остался старый значок приложения. Что делать?</b></summary>

Это классический симптом **конфликта с остатками ранее установленных сторонних модулей камеры** либо наличия старого обновления камеры в `/data/app`:
1. Простое выключение тумблера старых модулей в Magisk/KernelSU **не помогает**, так как в системе сохраняются скомпилированный кэш dalvik-cache и системные параметры `persist.*`.
2. Откройте Magisk / KernelSU / APatch и **полностью УДАЛИТЕ (через значок корзины)** все сторонние модули камеры (старые версии мода, Leica Camera mod, George video, звуки затвора и т.д.).
3. Перейдите в *Настройки ➔ Приложения ➔ Все приложения ➔ Камера*, нажмите **«Удалить обновления»** (если кнопка активна) и **«Очистить всё»**.
4. **Обязательно перезагрузите смартфон** для полной очистки оверлеев OverlayFS и кэша пакетов.
5. Заново установите наш модуль и выполните финальную перезагрузку. Подробный пошаговый мануал см. в [Разделе 7.2](#72-разрешение-конфликтов-удаление-сторонних-модулей-камеры-черный-экран-краши-старый-значок-ru).
</details>

<details>
<summary><b>Плавный ли видоискатель в режиме «Фото»?</b></summary>"""

assert old_ru_faq_end in text, "RU FAQ end anchor not found"
text = text.replace(old_ru_faq_end, new_ru_faq_item, 1)

# 7. Add Warning in Section 7 EN and update installation steps
old_en_install = """> [!IMPORTANT]
> **Testing on HyperOS 4.x (Android 17) on Xiaomi 17 Ultra (`nezha`):**
> For HyperOS 4 builds, use **STRICTLY the SLIM Edition** ([`X17U_Master_Imaging_MOD_Slim_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/X17U_Master_Imaging_MOD_Slim_by_borndead.zip)). Installing the FULL Edition on HyperOS 4 is strictly prohibited due to framework signature incompatibilities. See [Section 5.7](#57-next-gen-firmware-compatibility-hyperos-4x--android-17-testing-on-xiaomi-17-ultra-nezha-en) for details.

#### 📦 Step-by-Step Module Installation:

1. **Download the required zip archive** from the [`releases/`](https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo/tree/main/releases) directory (see [Module Table in Section 3](#3-module-releases--download-links-en)):"""

new_en_install = """> [!IMPORTANT]
> **Testing on HyperOS 4.x (Android 17) on Xiaomi 17 Ultra (`nezha`):**
> For HyperOS 4 builds, use **STRICTLY the SLIM Edition** ([`X17U_Master_Imaging_MOD_Slim_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/X17U_Master_Imaging_MOD_Slim_by_borndead.zip)). Installing the FULL Edition on HyperOS 4 is strictly prohibited due to framework signature incompatibilities. See [Section 5.7](#57-next-gen-firmware-compatibility-hyperos-4x--android-17-testing-on-xiaomi-17-ultra-nezha-en) for details.

> [!WARNING]
> #### 🛑 MANDATORY PREREQUISITE: Complete Removal of Prior Camera Modules!
> If you previously installed **ANY other camera-related modules** in Magisk / KernelSU / APatch (older versions of this combo, Leica Camera mods, Leica sound/feature enablers, George Video MOD, Civi camera, AIO camera, 60fps mods, etc.):  
> ⚠️ **SIMPLY DISABLING (toggling off) OLD MODULES DOES NOT WORK!**  
> Merely disabling modules leaves behind compiled bytecode in dalvik-cache, residual OverlayFS layers, and persistent `persist.*` system properties, causing a **black viewfinder screen, immediate camera force close, or the old camera icon/UI remaining**.  
> **MANDATORY PREPARATION PROTOCOL:**  
> 1. Completely **DELETE** prior camera modules (tap the trash bin icon in Magisk / KernelSU / APatch).  
> 2. Uninstall camera updates: *Settings ➔ Apps ➔ Manage apps ➔ Camera ➔ «Uninstall updates»* (if present) and *«Clear all data»*.  
> 3. **MANDATORILY REBOOT YOUR PHONE**.  
> 4. Only after this clean reboot, proceed with flashing our new module!  
> See the complete technical analysis in [Section 7.2](#72-resolving-conflicts-removing-prior-camera-modules-black-screen-crashes-old-icon-en).

#### 📦 Step-by-Step Module Installation:

1. **Cleanly remove any prior camera modules and reboot** (see prerequisite warning above).
2. **Download the required zip archive** from the [`releases/`](https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo/tree/main/releases) directory (see [Module Table in Section 3](#3-module-releases--download-links-en)):"""

assert old_en_install in text, "EN Install block not found"
text = text.replace(old_en_install, new_en_install, 1)

# Also update step numbering in EN:
old_en_steps_end = """2. Open **Magisk (v26+)**, **KernelSU**, or **APatch**.
3. Go to **Modules** ➔ **Install from storage** and choose the downloaded zip.
4. Wait for the installation script to finish and tap **Reboot**.
5. *(Mandatory)* After reboot, clear Camera app data:  
   *Settings ➔ Apps ➔ Manage apps ➔ Camera ➔ Clear all data*."""

new_en_steps_end = """3. Open **Magisk (v26+)**, **KernelSU**, or **APatch**.
4. Go to **Modules** ➔ **Install from storage** and choose the downloaded zip.
5. Wait for the installation script to finish and tap **Reboot**.
6. *(Mandatory)* After reboot, clear Camera app data:  
   *Settings ➔ Apps ➔ Manage apps ➔ Camera ➔ Clear all data*."""

assert old_en_steps_end in text, "EN steps end not found"
text = text.replace(old_en_steps_end, new_en_steps_end, 1)

# 8. Add Section 7.2 EN before Section 8 EN
section_7_2_en = """
<a name="72-resolving-conflicts-removing-prior-camera-modules-black-screen-crashes-old-icon-en"></a>
### 7.2. ⚠️ Resolving Conflicts: Why Disabling Old Camera Modules Fails & Clean Install Protocol (EN)

If you encounter any of the following symptoms after installing the module:
* 🔲 **Black screen in viewfinder** (the viewfinder fails to stream video or freezes on a black screen upon launch);
* 🏷️ **Old camera icon / old UI remains** (after flashing the FULL edition, the app icon and interface remain un-updated);
* 💥 **Instant crash (Force Close)** upon launching the camera or when switching lenses (0.5x, 1x, 3.2x, 5.0x);
* ⚠️ **System error «Can't connect to camera»** (CameraServer connection failure);

— **in 99% of cases, the root cause is a latent conflict with remnants of previously installed camera modules or cached `/data/app` updates**.

---

#### 🔬 Technical Analysis: Why Simply Disabling (Toggling Off) in Magisk / KernelSU DOES NOT WORK

Many users assume toggling off (disabling) an older module in Magisk Manager or KernelSU is sufficient. **However, at the Android OS and Linux kernel levels, this DOES NOT eliminate module conflicts:**

1. 📂 **Precedence of User App Updates (`/data/app`) over System Overlays**:
   - If an earlier module (or the user manually) installed a camera APK update, Android stores it in:
     ```text
     /data/app/~~...com.android.camera.../
     ```
   - In Android OS architecture, applications inside `/data/app` take **absolute priority** over system apps in `/product/priv-app/` and `/system/priv-app/`.
   - Even when Magisk mounts our full-featured `MiuiCamera.apk` into system partitions, `PackageManagerService` continues executing the stale APK from `/data/app`!
   - **Result**: the camera icon and UI remain outdated, and when the old APK attempts to load new Chromatix tunings and libraries, it immediately crashes.

2. 🧠 **Compiled ART Dalvik-Cache Bytecode Persistence**:
   - On first launch, the Android ART runtime pre-compiles application dex bytecode into optimized native code stored in:
     ```text
     /data/dalvik-cache/arm64/
     /data/system/package_cache/
     ```
   - Merely toggling off a module creates an empty `/data/adb/modules/<mod>/disable` trigger file, but **NEVER purges dalvik-cache**.
   - Upon the next boot, Android loads the cached code of the prior camera version compiled against old library addresses. Pointer and method signature mismatches in memory cause `com.android.camera` to crash or hang on a black screen.

3. ⚙️ **Persistent System Properties (`persist.*`)**:
   - Older camera mods frequently execute `setprop persist.vendor.camera...`.
   - Properties prefixed with `persist.` are saved to non-volatile on-disk storage:
     ```text
     /data/property/persistent_properties
     ```
   - Disabling a module **does not reset** these persistent properties. Conflicting flags keep instructing Qualcomm CamX to execute invalid algorithmic code paths.

4. 🗂️ **Residual OverlayFS Mount Layers**:
   - When a module is merely disabled rather than deleted, its directory remains physically inside `/data/adb/modules/`.
   - On certain kernels and Magisk/KernelSU versions, disabled module folder hierarchies can partially linger in the upperdir mount tree, obstructing our module's clean overlay injection.

---

#### 📋 Step-by-Step Clean Reinstall Protocol

Follow this exact sequence to guarantee zero conflicts and flawless camera operation:

##### Step 1: Permanently Delete Prior Camera Modules via Trash Bin
1. Open **Magisk**, **KernelSU**, or **APatch** ➔ navigate to **Modules**.
2. Identify **ALL** previously installed camera modules (Leica Camera mods, Civi mods, George video, older Mi Master Camera releases, AIO camera, shutter sound mods, etc.).
3. Tap the **TRASH BIN (Delete)** icon next to each one.
   > ⚠️ **DO NOT merely toggle them off — you MUST permanently delete them!**

##### Step 2: Uninstall Stale Camera Updates in Android Settings
1. Navigate to *Settings ➔ Apps ➔ Manage apps ➔ Camera*.
2. Look at the bottom menu for the **«Uninstall updates»** button:
   - If present, **tap it immediately**! This removes conflicting stale APK files from `/data/app`.
3. Tap **«Clear data» ➔ «Clear all data»** (purges stale camera cache and preferences).

##### Step 3: MANDATORY INTERMEDIATE REBOOT
1. Reboot your smartphone.
2. **Why this is critical:** during this reboot, the root manager physically deletes `/data/adb/modules/<old_mod>` directories, unbinds OverlayFS mount points, and Android purges stale package caches.

##### Step 4: Install Our Module
1. After booting into clean Android, open Magisk / KernelSU / APatch.
2. Flash your chosen zip archive (`Mi_Master_Camera_Combo...` / `Mi13U...` / `Mi14U...` / `X17U...` / `Mi15U...` / `Mi15...`).
3. Allow the installer script to finish successfully.

##### Step 5: Final Reboot & First Launch
1. Tap **Reboot**.
2. After booting, go to *Settings ➔ Apps ➔ Manage apps ➔ Camera ➔ Clear all data*.
3. Launch the camera app. It will open instantly with the new Leica icon, modernized UI, and full access to all 50M/200M sensors without crashes or black screens!

---
"""

old_before_s8_en = """### 8. Verification & Testing Guide (All Devices & Versions) (EN)"""
assert old_before_s8_en in text, "Section 8 EN start not found"
text = text.replace(old_before_s8_en, section_7_2_en + old_before_s8_en, 1)

# 9. Add Section 10 FAQ item in EN
old_en_faq_end = """<details>
<summary><b>Is the viewfinder smooth in Photo mode?</b></summary>"""

new_en_faq_item = """<details>
<summary><b>Black viewfinder screen, camera crash, or old camera icon still present after flashing? What should I do?</b></summary>

This is the classic symptom of a **conflict with remnants of previously installed camera modules** or a stale camera update lingering in `/data/app`:
1. Simply disabling old modules in Magisk/KernelSU **does not work**, because compiled dalvik-cache bytecode and persistent properties survive in the system.
2. Open Magisk / KernelSU / APatch and **permanently DELETE (via trash icon)** all other camera modules (older combo releases, Leica mods, George video, shutter mods, etc.).
3. Open *Settings ➔ Apps ➔ Manage apps ➔ Camera*, tap **«Uninstall updates»** (if present), and select **«Clear all data»**.
4. **Mandatorily reboot your smartphone** so the root manager and Android completely tear down old OverlayFS mounts and package caches.
5. Reinstall our module and perform a final reboot. See the comprehensive step-by-step walkthrough in [Section 7.2](#72-resolving-conflicts-removing-prior-camera-modules-black-screen-crashes-old-icon-en).
</details>

<details>
<summary><b>Is the viewfinder smooth in Photo mode?</b></summary>"""

assert old_en_faq_end in text, "EN FAQ end anchor not found"
text = text.replace(old_en_faq_end, new_en_faq_item, 1)

with open(readme_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print("Successfully applied all camera conflict documentation updates to README.md!")
