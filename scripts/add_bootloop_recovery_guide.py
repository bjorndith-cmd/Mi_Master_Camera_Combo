import os
import shutil

repo_readme = r"C:\Users\ASTA\OneDrive\Документы\GitHub\Mi_Master_Camera_Combo\README.md"
antigravity_readme = r"C:\Users\ASTA\OneDrive\Документы\Antigravity\README.md"

with open(repo_readme, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update RU Navigation Menu
ru_nav_target = """7. [Инструкция по установке](#7-инструкция-по-установке-ru)
8. [Инструкция по тестированию и проверке работы модуля](#8-инструкция-по-тестированию-и-проверке-работы-модуля-для-всех-версий-ru)"""

ru_nav_replacement = """7. [Инструкция по установке](#7-инструкция-по-установке-ru)
   - [🚨 Экстренное руководство: Как вернуть телефон из бутлупа](#71-экстренное-руководство-как-вернуть-телефон-из-бутлупа-циклической-перезагрузки-ru)
8. [Инструкция по тестированию и проверке работы модуля](#8-инструкция-по-тестированию-и-проверке-работы-модуля-для-всех-версий-ru)"""

if ru_nav_target in content:
    content = content.replace(ru_nav_target, ru_nav_replacement, 1)
    print("Updated RU Nav Menu")
else:
    print("Warning: RU Nav target not found")

# 2. Update EN Navigation Menu
en_nav_target = """7. [Installation Guide](#7-installation-guide-en)
8. [Verification & Testing Guide (All Devices & Versions)](#8-verification--testing-guide-all-devices--versions-en)"""

en_nav_replacement = """7. [Installation Guide](#7-installation-guide-en)
   - [🚨 Emergency Bootloop Recovery Guide](#71-emergency-guide-how-to-recover-from-a-bootloop-en)
8. [Verification & Testing Guide (All Devices & Versions)](#8-verification--testing-guide-all-devices--versions-en)"""

if en_nav_target in content:
    content = content.replace(en_nav_target, en_nav_replacement, 1)
    print("Updated EN Nav Menu")
else:
    print("Warning: EN Nav target not found")

# 3. Update RU Section 7 step 1 downloads & Insert Section 7.1
ru_sec7_target = """#### 📦 Пошаговый процесс установки модуля камеры:

1. **Скачайте необходимый zip-архив** из папки [`releases/`](./releases/):
   * **Для Xiaomi 13 Ultra (`ishtar`)**: выберите **`Mi13U_Master_Camera_Combo_v5.1_by_borndead.zip`** (278 КБ — обновлённый Pure Systemless Overlay с полной защитой от бутлупа) либо **`Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip`** (для пользователей старой HyperOS 1.0 на Android 14).
   * **Для Xiaomi 17 Ultra (`nezha`) на SimpleRom 3.0.309.0 ST (Non-Leica)**: выберите **`X17U_Master_Imaging_MOD_SimpleRom_ST_NonLeica_by_borndead.zip`** (с фиксом розового шума Leica Essential).
   * **Для Xiaomi 17 Ultra на кастомах/стоке (EU, Elite, China)**: выберите **`X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`**.
   * **Для Xiaomi 15 Ultra (`xuanyuan`)**: выберите **`Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip`** (с нативными калибровками Stock AIO 104).
   * **Универсальный комбайн для всей линейки (13U, 15, 15 Pro, 15U, 17U)**: выберите **`Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip`** (v5.8).
2. Откройте **Magisk (v26+)**, **KernelSU** или **APatch**.
3. Зайдите в раздел **«Модули»** ➔ **«Установить из хранилища»** и выберите скачанный zip-архив.
4. Дождитесь завершения работы скрипта инсталляции и нажмите **«Перезагрузка»**.
5. *(Обязательно)* После перезагрузки очистите данные приложения Камера:  
   *Настройки ➔ Приложения ➔ Все приложения ➔ Камера ➔ Очистить всё*.

---

### 8. Инструкция по тестированию"""

ru_sec7_replacement = """#### 📦 Пошаговый процесс установки модуля камеры:

1. **Скачайте необходимый zip-архив** из папки [`releases/`](./releases/) (см. [Таблицу версий в Разделе 3](#3-таблица-модулей-и-ссылки-на-загрузку-ru)):
   * **FULL Edition (с приложением камеры Leica)**: выберите [`Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip) или специализированный Full-архив для вашей модели (`Mi13U`, `X17U`, `Mi15U`, `Mi15`). Включает новое приложение камеры Leica с защитой `oat/.replace`.
   * **SLIM Edition (чистый оверлей без APK — 100% защита от бутлупа)**: выберите [`Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip) либо Slim-архив для вашей модели. Идеален для тайваньских, глобальных и кастомных прошивок (SimpleRom ST, Xiaomi.eu).
   * **Для HyperOS 1.0 (Android 14)**: архив [`Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip).
2. Откройте **Magisk (v26+)**, **KernelSU** или **APatch**.
3. Зайдите в раздел **«Модули»** ➔ **«Установить из хранилища»** и выберите скачанный zip-архив.
4. Дождитесь завершения работы скрипта инсталляции и нажмите **«Перезагрузка»**.
5. *(Обязательно)* После перезагрузки очистите данные приложения Камера:  
   *Настройки ➔ Приложения ➔ Все приложения ➔ Камера ➔ Очистить всё*.

---

<a name="71-экстренное-руководство-как-вернуть-телефон-из-бутлупа-циклической-перезагрузки-ru"></a>
### 7.1. 🚨 Экстренное руководство: Как вернуть телефон из бутлупа (циклической перезагрузки) (RU)

Если после установки комбинированного модуля камера-пайплайна устройство зависло на загрузочном логотипе (HyperOS / Mi) или ушло в бесконечный рестарт (Bootloop) из-за конфликта подписей APK, несовместимости библиотек или особенностей региональной прошивки (Taiwan, Global, EU), **НЕ ПАНИКУЙТЕ! Ваши данные, фотографии и файлы на 100% в безопасности**.

Воспользуйтесь одним из проверенных способов восстановления в зависимости от вашей ситуации:

---

#### 📱 Способ 1: Аппаратный Безопасный Режим (Safe Mode) через кнопку «Громкость ВНИЗ»
> **Самый простой и быстрый способ: НЕ ТРЕБУЕТ компьютера и кастомного рекавери**, работает даже со стоковым Mi Recovery!

1. Принудительно выключите или перезагрузите смартфон (удерживайте кнопку **Питание** в течение 10–12 секунд, пока экран не погаснет).
2. Как только телефон начнет запускаться и на экране появится **анимация логотипа HyperOS / Mi** (либо сработает повторная вибрация):
   - Сразу же **нажмите и непрерывно удерживайте клавишу Громкость ВНИЗ (Volume Down)**.
3. Удерживайте клавишу «Громкость ВНИЗ» до тех пор, пока система полностью не загрузится на экран блокировки или рабочий стол.
4. **Что происходит под капотом**:
   - Ядро и подсистема Android распознают аппаратный зажим клавиши и активируют штатный **Безопасный Режим (Safe Mode)** (в нижнем левом углу экрана появится надпись *«Безопасный режим»*).
   - Менеджеры рута (**Magisk, KernelSU, APatch**) перехватывают этот сигнал и **автоматически переводят окружение в режим Core-Only (отключая абсолютно все модули)**.
5. Откройте приложение **Magisk** / **KernelSU** / **APatch** ➔ перейдите во вкладку **«Модули»** ➔ **отключите или удалите** модуль камеры.
6. Перезагрузите смартфон в обычном режиме — система запустится штатно, 100% ваших данных сохранены!

---

#### 🛠️ Способ 2: Через кастомный Recovery (TWRP / OrangeFox) — Самый надежный

1. Загрузите телефон в режим Recovery (обычно удерживанием комбинации **Питание + Громкость ВВЕРХ** при включении).
2. Перейдите в раздел **Advanced (Дополнительно)** ➔ **File Manager (Менеджер файлов)**.
3. Перейдите по пути:
   ```text
   /data/adb/modules/
   ```
4. Найдите папку установленного модуля (например, `Mi_Master_Camera_Combo`, `mi_master_camera_combo`, `Mi13U_Master_Camera_Combo`, `X17U_Master_Imaging_MOD` и т.д.) и удалите её.
5. ⚠️ **Критически важно:** обязательно проверьте и очистите папку:
   ```text
   /data/adb/modules_update/
   ```
   *(Если внутри осталась папка модуля, удалите её, иначе Magisk/KernelSU повторно распакует и установит сбойный модуль при следующем старте системы)*.
6. Перезагрузите устройство в систему (**Reboot ➔ System**).

---

#### 🛑 Способ 3: Экстренное отключение всех модулей через файл-заглушку `/data/adb/disable`
> Используйте, если не получается найти конкретную папку или если сбой вызван несколькими модулями одновременно.

1. В том же **File Manager** кастомного рекавери (TWRP / OrangeFox) или через встроенный терминал рекавери перейдите в каталог:
   ```text
   /data/adb/
   ```
2. Создайте пустой файл с именем:
   ```text
   disable
   ```
   Либо в терминале Recovery введите команду:
   ```bash
   touch /data/adb/disable
   ```
3. Перезагрузите телефон.
4. **Результат:** Наличие файла `/data/adb/disable` принудительно заставляет **Magisk, KernelSU и APatch** запуститься в режиме **Core-Only** (все модули будут деактивированы).
5. После успешной загрузки в систему зайдите в менеджер рута (Magisk/KernelSU/APatch), удалите проблемный модуль и удалите созданный файл `/data/adb/disable` (через Root Explorer или терминал), затем перезагрузитесь.

---

#### 🎯 Способ 4: Точечное отключение сбойного модуля без удаления (Файлы-триггеры)
> Если вы хотите временно отключить только модуль камеры, сохранив все остальные модули активными.

1. В File Manager в TWRP / OrangeFox зайдите в директорию нужного модуля:
   ```text
   /data/adb/modules/<имя_папки_модуля>/
   ```
2. Создайте внутри папки пустой файл:
   - **`disable`** — модуль будет отключен при следующем старте (остальные модули продолжат работать);
   - **`remove`** — менеджер рута автоматически и бесследно удалит этот модуль при следующей загрузке.
3. Перезагрузите устройство в систему (**Reboot ➔ System**).

---

#### 💻 Способ 5: Спасение через Fastboot БЕЗ потери данных
> Если кастомный рекавери не установлен, а Безопасный Режим не запускается из-за сбоя на этапе ранней инициализации ядра.

1. Переведите смартфон в режим **Fastboot** (зажмите и удерживайте **Питание + Громкость ВНИЗ** на выключенном смартфоне до появления экрана FASTBOOT).
2. Подключите телефон к компьютеру по кабелю USB.
3. Откройте командную строку на ПК с установленным `platform-tools` (adb/fastboot).
4. Прошейте оригинальный стоковый образ `init_boot.img` (для Android 13/14/15/16 с GKI) или `boot.img` из официальной fastboot-прошивки вашего устройства:
   ```bash
   # Для современных устройств (Xiaomi 13 Ultra, 15, 15 Pro, 15 Ultra, 17 Ultra):
   fastboot flash init_boot init_boot_stock.img

   # Для моделей без отдельного раздела init_boot:
   fastboot flash boot boot_stock.img

   # Перезагрузка в систему:
   fastboot reboot
   ```
5. Смартфон гарантированно загрузится в чистую стоковую систему без рута. **Все ваши приложения, фотографии и настройки останутся абсолютно нетронутыми!**
6. После успешной загрузки вы можете пропатчить стоковый boot/init_boot в Magisk заново и вернуть рут.

---

#### ⚡ Способ 6: Экстренная команда через ADB с компьютера
> Если на телефоне включена отладка по USB и устройство успевает кратковременно определиться в adb при рестарте.

1. Подключите смартфон к ПК кабелем.
2. В терминале на компьютере выполните команду:
   ```bash
   # Для Magisk (удаление всех модулей):
   adb wait-for-device shell magisk --remove-modules

   # Либо универсальное создание файла disable для Magisk/KernelSU/APatch:
   adb wait-for-device shell "su -c 'touch /data/adb/disable'"
   adb reboot
   ```

---

#### 🛡️ Профилактика: Как защитить себя от бутлупов раз и навсегда

1. **Всегда устанавливайте Magisk Bootloop Saver (MBLS)**:  
   👉 Репозиторий: [Magisk Bootloop Saver на GitHub](https://github.com/HuskyDG/magic_overlayfs) / [chiteroman MBLS](https://github.com/chiteroman/BootloopSaver).  
   Этот легковесный сторожевой модуль непрерывно следит за стадиями запуска Android Zygote. Если система перезагружается 2 раза подряд, MBLS автоматически деактивирует все модули без вашего участия!
2. **Используйте SLIM Edition на кастомных прошивка**:  
   Если вы используете стороннюю или региональную прошивку (Taiwan, Global, Xiaomi.eu, SimpleRom ST) без отключения проверки подписей (CorePatch/LuckyPatcher), устанавливайте **SLIM-версию** модуля (*Pure Systemless Overlay*). Она не заменяет системный APK камеры, обладает 0% риска бутлупа и дает все преимущества 50M/200M FullRes, George Video 8K и DCG HDR!

---

### 8. Инструкция по тестированию"""

if ru_sec7_target in content:
    content = content.replace(ru_sec7_target, ru_sec7_replacement, 1)
    print("Updated RU Section 7 and inserted Section 7.1")
else:
    print("Warning: RU Section 7 target not found")

# 4. Update EN Section 7 step 1 downloads & Insert Section 7.1
en_sec7_target = """#### 📦 Step-by-Step Module Installation:

1. **Download the required zip archive** from the [`releases/`](./releases/) directory:
   * **For Xiaomi 13 Ultra (`ishtar`)**: select **`Mi13U_Master_Camera_Combo_v5.1_by_borndead.zip`** (278 KB — updated Pure Systemless Overlay with anti-bootloop protection) or **`Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip`** (for legacy HyperOS 1.0 on Android 14).
   * **For Xiaomi 17 Ultra (`nezha`) on SimpleRom 3.0.309.0 ST (Non-Leica)**: select **`X17U_Master_Imaging_MOD_SimpleRom_ST_NonLeica_by_borndead.zip`** (with Leica Essential magenta noise fix).
   * **For Xiaomi 17 Ultra on custom/stock ROMs (EU, Elite, China)**: select **`X17U_Master_Imaging_MOD_v1.0_Slim_by_borndead.zip`**.
   * **For Xiaomi 15 Ultra (`xuanyuan`)**: select **`Mi15U_X17U_Master_Camera_Combo_v5.1_by_borndead.zip`** (with native Stock AIO 104 tunings).
   * **Universal Combo for All Flagships (13U, 15, 15 Pro, 15U, 17U)**: select **`Mi_Master_Camera_Combo_Universal_MultiDevice_by_borndead.zip`** (v5.8).
2. Open **Magisk (v26+)**, **KernelSU**, or **APatch**.
3. Go to **Modules** ➔ **Install from storage** and choose the downloaded zip.
4. Wait for the installation script to finish and tap **Reboot**.
5. *(Mandatory)* After reboot, clear Camera app data:  
   *Settings ➔ Apps ➔ Manage apps ➔ Camera ➔ Clear all data*.

---

### 8. Verification & Testing Guide"""

en_sec7_replacement = """#### 📦 Step-by-Step Module Installation:

1. **Download the required zip archive** from the [`releases/`](./releases/) directory (see [Module Table in Section 3](#3-module-releases--download-links-en)):
   * **FULL Edition (with Leica Camera APK)**: select [`Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip) or device-specific Full zip (`Mi13U`, `X17U`, `Mi15U`, `Mi15`). Includes latest Leica Camera app with `oat/.replace` bootloop protection.
   * **SLIM Edition (Pure Systemless Overlay — 100% Bootloop Immune)**: select [`Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip`](./releases/Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip) or device-specific Slim zip. Recommended for Taiwan, Global, and custom ROMs (SimpleRom ST, Xiaomi.eu).
   * **For HyperOS 1.0 (Android 14)**: legacy archive [`Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip`](./releases/Mi13U_Master_Imaging_MOD_HOS1_A14_by_borndead.zip).
2. Open **Magisk (v26+)**, **KernelSU**, or **APatch**.
3. Go to **Modules** ➔ **Install from storage** and choose the downloaded zip.
4. Wait for the installation script to finish and tap **Reboot**.
5. *(Mandatory)* After reboot, clear Camera app data:  
   *Settings ➔ Apps ➔ Manage apps ➔ Camera ➔ Clear all data*.

---

<a name="71-emergency-guide-how-to-recover-from-a-bootloop-en"></a>
### 7.1. 🚨 Emergency Guide: How to Recover from a Bootloop (EN)

If your device gets stuck on the boot animation (HyperOS / Mi logo) or enters a continuous restart loop (Bootloop) after installing the combined camera pipeline module due to APK signature mismatches, library incompatibility, or regional ROM variations (Taiwan, Global, EU), **DO NOT PANIC! Your photos, apps, and personal data are 100% safe**.

Follow one of the battle-tested recovery methods below based on your device configuration:

---

#### 📱 Method 1: Hardware Safe Mode via «Volume Down» Key
> **Fastest & easiest method: DOES NOT REQUIRE a computer or custom recovery**, works even on 100% stock Mi Recovery!

1. Force power off or restart your phone (press and hold the **Power** button for 10–12 seconds until the screen turns off).
2. As soon as the phone vibrates and the **HyperOS / Mi boot animation** appears:
   - Immediately **press and hold the Volume Down button**.
3. Keep holding Volume Down continuously until the device reaches the lockscreen or launcher.
4. **How it works behind the scenes**:
   - The Android bootloader and kernel detect the held Volume Down button and boot into native **Safe Mode** (indicated by *"Safe mode"* text in the lower-left corner).
   - Root managers (**Magisk, KernelSU, APatch**) intercept this Android Safe Mode broadcast and **automatically boot in Core-Only mode (disabling all root modules)**.
5. Open your root manager app (**Magisk**, **KernelSU**, or **APatch**) ➔ navigate to **Modules** ➔ **disable or remove** the camera module.
6. Reboot the phone normally — system boots cleanly, 100% of your data remains intact!

---

#### 🛠️ Method 2: Custom Recovery (TWRP / OrangeFox) — Most Reliable

1. Boot into Recovery mode (press and hold **Power + Volume UP** while turning on).
2. Navigate to **Advanced** ➔ **File Manager**.
3. Go to the path:
   ```text
   /data/adb/modules/
   ```
4. Locate the installed camera module directory (e.g., `Mi_Master_Camera_Combo`, `mi_master_camera_combo`, `Mi13U_Master_Camera_Combo`, `X17U_Master_Imaging_MOD`, etc.) and delete it.
5. ⚠️ **Critical Step:** also verify and clean the update directory:
   ```text
   /data/adb/modules_update/
   ```
   *(If the module directory remains inside `modules_update`, Magisk/KernelSU will automatically reinstall the faulty module on next boot)*.
6. Reboot to system (**Reboot ➔ System**).

---

#### 🛑 Method 3: Emergency Systemwide Disable via `/data/adb/disable`
> Use if you cannot locate or delete a specific folder, or if multiple modules are conflicting.

1. In the Recovery File Manager (TWRP / OrangeFox) or via the built-in Recovery Terminal, navigate to:
   ```text
   /data/adb/
   ```
2. Create an empty file named:
   ```text
   disable
   ```
   Or in the Recovery Terminal, execute:
   ```bash
   touch /data/adb/disable
   ```
3. Reboot the device.
4. **Result:** The presence of `/data/adb/disable` forces **Magisk, KernelSU, and APatch** to boot in **Core-Only mode** (all modules are temporarily deactivated).
5. After booting into Android, open your root manager app, uninstall the offending module, and delete the `/data/adb/disable` file, then reboot.

---

#### 🎯 Method 4: Selective Module Disabling via Trigger Files (`disable` / `remove`)
> If you want to disable only the camera module while keeping your other modules active.

1. In the Recovery File Manager (TWRP / OrangeFox), open the target module directory:
   ```text
   /data/adb/modules/<module_name>/
   ```
2. Create an empty file inside the module directory:
   - **`disable`** — the module is disabled on the next boot (other modules remain active);
   - **`remove`** — the root manager cleanly uninstalls this module on the next boot.
3. Reboot into system (**Reboot ➔ System**).

---

#### 💻 Method 5: Fastboot Stock Kernel Flash WITHOUT Data Loss
> If you do not have custom recovery installed and Safe Mode does not catch the bootloop due to early-stage kernel crash.

1. Put your phone into **Fastboot Mode** (hold **Power + Volume Down** until the FASTBOOT screen appears).
2. Connect the phone to your computer via USB.
3. Open a command prompt with Android `platform-tools` (adb/fastboot).
4. Flash the stock `init_boot.img` (for Android 13/14/15/16 with GKI) or stock `boot.img` from your official fastboot firmware package:
   ```bash
   # For modern devices (Xiaomi 13 Ultra, 15, 15 Pro, 15 Ultra, 17 Ultra):
   fastboot flash init_boot init_boot_stock.img

   # For legacy partition layouts (without separate init_boot):
   fastboot flash boot boot_stock.img

   # Reboot back into Android:
   fastboot reboot
   ```
5. Your device boots safely into clean stock non-rooted Android. **All your apps, personal photos, and settings remain 100% intact!**
6. You can subsequently re-patch boot/init_boot in Magisk and restore root safely.

---

#### ⚡ Method 6: Emergency Command via ADB from PC
> If USB debugging is enabled and the device connects to ADB during early boot stages.

1. Connect your device to PC via USB.
2. In your computer's terminal, run:
   ```bash
   # For Magisk (removes all modules):
   adb wait-for-device shell magisk --remove-modules

   # Or universal disable file creation for Magisk/KernelSU/APatch:
   adb wait-for-device shell "su -c 'touch /data/adb/disable'"
   adb reboot
   ```

---

#### 🛡️ Prevention: How to Stay Immune to Bootloops

1. **Always Install Magisk Bootloop Saver (MBLS)**:  
   👉 Repositories: [Magisk Bootloop Saver on GitHub](https://github.com/HuskyDG/magic_overlayfs) / [chiteroman MBLS](https://github.com/chiteroman/BootloopSaver).  
   This watchdog daemon monitors Zygote initialization. If a boot failure recurs twice, MBLS automatically disables all modules before Android enters a recovery panic!
2. **Choose SLIM Edition on Custom/Regional ROMs**:  
   If you run custom or regional builds (Taiwan, Global, Xiaomi.eu, SimpleRom ST) without signature verification patches (CorePatch/LuckyPatcher), choose the **SLIM Edition** (*Pure Systemless Overlay*). It leaves the system camera APK completely untouched, eliminates 100% of signature conflicts, and provides full 50M/200M FullRes, George Video 8K, and DCG HDR!

---

### 8. Verification & Testing Guide"""

if en_sec7_target in content:
    content = content.replace(en_sec7_target, en_sec7_replacement, 1)
    print("Updated EN Section 7 and inserted Section 7.1")
else:
    print("Warning: EN Section 7 target not found")

with open(repo_readme, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print(f"Successfully written {repo_readme}")

with open(antigravity_readme, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)
print(f"Successfully copied to {antigravity_readme}")
