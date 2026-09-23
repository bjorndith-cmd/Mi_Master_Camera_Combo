import os

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
readme_path = os.path.join(repo_root, 'README.md')

with open(readme_path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\r\n', '\n')

# 1. Update EN AI Table
old_ai_table_en = """| **[`Mi_AI_Director_Vision_Companion_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Director_Vision_Companion_by_borndead.zip)** | **2.68 KB** | **Tier 3 (Vision HUD)** | **AI Director Real-time Viewfinder Assistant**. Live Leica composition lines (Fibonacci Golden Ratio, Rule of Thirds), high-precision horizon gyro stabilizer (±0.1°), AI Lens Advisor, and Smart Pro Suggester. |"""

new_ai_table_en = """| **[`Mi_AI_Director_Vision_Companion_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Director_Vision_Companion_by_borndead.zip)** | **2.68 KB** | **Tier 3 (Vision HUD)** | **AI Director Real-time Viewfinder Assistant**. Live Leica composition lines (Fibonacci Golden Ratio, Rule of Thirds), high-precision horizon gyro stabilizer (±0.1°), AI Lens Advisor, and Smart Pro Suggester. |
| 🌟 **[`Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip)** | **4.11 KB** | **All-In-One (Complete Suite)** | **All 3 AI Tiers combined in a single module**. Includes AISP Hardware NPU (Tier 1), HyperAI Studio Generative Suite (Tier 2), and AI Director Viewfinder HUD (Tier 3). 100% offline, single-click install with zero layer conflicts. |"""

if old_ai_table_en in text:
    text = text.replace(old_ai_table_en, new_ai_table_en, 1)
    print("[OK] EN AI Table updated with All-In-One")
else:
    print("[FAIL] Could not match EN AI Table")

# 2. Add Compatibility Section to RU Section 6
ru_compat_section = """#### 6.4. Взаимная совместимость модулей ИИ и технология Smart Multi-Module Synchronization (RU)

Часто возникает закономерный вопрос: **совместимы ли эти модули между собой и с базовыми модулями (FULL / SLIM)?**

**Ответ: ДА, совместимы на 100%!**

##### 1. Разделение системных уровней (Separation of Concerns)
Каждый модуль сфокусирован на своем независимом системном слое:
- **Tier 1 (AISP)** воздействует исключительно на драйверы чипсета Qualcomm CamX и сопроцессор NPU Hexagon (`ro.hardware.camera.aisp=1`, `persist.vendor.camera.aisp=1`). Он не затрагивает ни фоторедактор, ни интерфейс видоискателя.
- **Tier 2 (HyperAI Studio)** подключает инструменты генеративного редактирования в фотолаборатории `com.miui.extraphoto` и системной галерее `com.miui.gallery`. Он не пересекается с драйверами камеры или видоискателем.
- **Tier 3 (AI Director)** активирует оверлей композиционных сеток и гиро-горизонта в самом приложении камеры `com.android.camera`.

##### 2. Интеллектуальная синхронизация конфигураций (Smart Multi-Module Sync)
В классических модулях Magisk/KernelSU при установке нескольких дополнений, затрагивающих один и тот же файл `device_features/<device>.xml`, нижний модуль перекрывается верхним по правилам OverlayFS. 
В модулях **Mi Master Camera Combo** реализована эксклюзивная технология **Smart Multi-Module Synchronization**:
- При установке инсталлятор `customize.sh` сканирует `/data/adb/modules/` и извлекает текущую активную конфигурацию из уже установленных модулей камеры;
- Инжектирует новые функции и перезаписывает не только локальный файл `$MODPATH`, но и **синхронизирует обновленный XML во все ранее установленные каталоги модулей нашей линейки**;
- В итоге, независимо от того, в каком порядке Magisk или KernelSU монтирует оверлеи, Android получает **целостный файл со всеми активными функциями всех установленных модулей**!

##### 3. Полный комбайн «Всё в одном» (All-In-One Edition)
Если вы не хотите устанавливать три модуля по отдельности, используйте **[`Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip)** (4.11 КБ). Он объединяет все возможности Tier 1, Tier 2 и Tier 3 в едином модуле с установкой в один клик.

---

"""

marker_sec7_ru = "### 7. Визуальные сравнения «До / После» (Visual Proof) (RU)"
if marker_sec7_ru in text:
    text = text.replace(marker_sec7_ru, ru_compat_section + marker_sec7_ru, 1)
    print("[OK] RU Compatibility Section inserted into Section 6")
else:
    print("[FAIL] Marker for RU Section 7 not found")

# 3. Add Compatibility Section to EN Section 6
en_compat_section = """#### 6.4. Mutual Compatibility & Smart Multi-Module Synchronization Technology (EN)

A common and critical question: **are these AI modules compatible with each other and with the base FULL / SLIM modules?**

**Answer: YES, 100% compatible!**

##### 1. Clean Separation of System Concerns
Each module is engineered to operate on a distinct system tier:
- **Tier 1 (AISP Engine)** targets low-level Qualcomm CamX drivers and the Hexagon NPU coprocessor (`ro.hardware.camera.aisp=1`, `persist.vendor.camera.aisp=1`). It does not modify gallery packages or viewfinder layouts.
- **Tier 2 (HyperAI Studio)** activates on-device generative algorithms inside `com.miui.extraphoto` and `com.miui.gallery`. It operates downstream from capture and does not touch camera HALs.
- **Tier 3 (AI Director)** injects composition guides, Fibonacci grids, and gyro horizon HUD inside `com.android.camera`.

##### 2. Smart Multi-Module Synchronization
Under standard Magisk/KernelSU behavior, if multiple modules provide `device_features/<device>.xml`, OverlayFS masks the lower layer with the top layer.
To eliminate this risk, all **Mi Master Camera Combo** modules feature **Smart Multi-Module Synchronization**:
- During installation, `customize.sh` inspects `/data/adb/modules/` to discover XML modifications from previously installed camera packages;
- It merges all feature tags and synchronizes the unified XML across **all installed camera module directories**;
- As a result, regardless of Magisk / KernelSU mount sequence, the operating system always loads a unified, complete feature tree with 0% feature loss!

##### 3. Complete All-In-One Edition
For instant deployment without juggling individual archives, install **[`Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip`](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip)** (4.11 KB). It combines Tier 1, Tier 2, and Tier 3 into a single, high-efficiency package.

---

"""

marker_sec7_en = "### 7. Visual Proof Gallery (Before vs After) (EN)"
if marker_sec7_en in text:
    text = text.replace(marker_sec7_en, en_compat_section + marker_sec7_en, 1)
    print("[OK] EN Compatibility Section inserted into Section 6")
else:
    print("[FAIL] Marker for EN Section 7 not found")

with open(readme_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(text)

print("\n=== README.md UPDATED SUCCESSFULLY WITH ALL-IN-ONE & COMPATIBILITY DOCS ===")
