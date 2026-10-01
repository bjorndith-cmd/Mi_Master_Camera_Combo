import os
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import publish_github_release

TAG_NAME = "v6.2"
RELEASE_NAME = "Xiaomi Master Camera Combo 5 v6.2: Security & Performance Architecture Overhaul by borndead"
BODY = """# Xiaomi Master Camera Combo 5 v6.2 (Security & Performance Overhaul) 📸⚡
**Lead Developer / Автор:** `borndead`  
**Base APK Generation:** Xiaomi Leica Camera APK 5.x (HyperOS 5-series base)  
**Compatibility:** Xiaomi 13 Ultra (`ishtar`), 14 Ultra (`aurora`), 15 (`dada`), 15 Pro (`haotian`), 15 Ultra, 17 Ultra (`nezha`), and Universal Flagship Lineup  
**Supported Platforms:** Magisk 25.0+ / KernelSU / KernelSU-Next / APatch  
**Android / OS Versions:** HyperOS 1.0 — 4.0 • MIUI 14 • Android 13 — 17 (API 33–37)

---

### 📌 Новая прозрачная система версионирования проекта:
- **`Xiaomi Master Camera Combo 5 v6.2`** — актуальная стабильная ветка на ультра-стабильной базе приложения камеры **5-го поколения** (HyperOS 5.x).
- **`Xiaomi Master Camera Combo 6 v8.2`** — экспериментальная ветка на новейшей базе приложения камеры **6-го поколения** (HyperOS 6.8+).

---

### 🌟 Ключевые изменения и улучшения в выпуске 5 v6.2:

1. ⚡ **Полная разблокировка дополнительных камер в сторонних приложениях (`PROP_VALUE_MAX < 92`)**:
   - В предыдущих версиях Android init молча отбрасывал системные свойства `vendor.camera.aux.packagelist`, превышающие 91 символ.
   - Список пакетов разделен на строгие подгруппы (`.packagelist` и `.packagelistext`), каждая короче 92 символов.
   - Теперь Google Camera (GCam, AGC, LMC, Shamim, OpenCamera) гарантированно видит сверхширокоугольный, телефото (3.2x) и перископический (5x) объективы.

2. 🔋 **Нулевой фоновый расход батареи (Zero-Daemon Architecture)**:
   - Полностью устранены бесконечные циклы `logcat` в фоновом демоне `service.sh`.
   - Внедрён **Режим диагностики по требованию (On-Demand Diagnostics)**: логирование активируется только при создании триггерного флага `/data/local/tmp/mmc_debug` или `/sdcard/Download/mmc_debug` с безопасными правами доступа `0750`.
   - Больше никакого износа флеш-памяти UFS и нагрева в режиме ожидания!

3. 🛡️ **Безопасность ядра и стабильность памяти**:
   - Из библиотек сопутствующих сервисов удалены конфликтующие платформенные аллокаторы (`libdmabufheap.so`, `libion.so`). Это предотвращает конфликты с аллокаторами современных ядер Android 14/15/16 и сбои камеры в памяти.
   - В SLIM-редакции удалено избыточное отключение системных привилегий (`ro.control_privapp_permissions.enforce 0`).

4. ⚙️ **Исправление инсталлятора AI Master Suite и кастомных ROM**:
   - Восстановлен бинарник `update-binary` в AI Suite: полная совместимость с диспетчером Magisk/KernelSU/APatch.
   - Исправлен алгоритм определения кастомных прошивок в инсталляторе (устранено жадное совпадение regex).
   - Инсталлятор теперь строго верифицирует поддерживаемую модель и прерывает установку с понятным предупреждением вместо применения некорректного профиля.
   - Профиль Xiaomi 15 Pro (`haotian`) скорректирован на физический перископ 5x Sony IMX858 и светосилу F1.44.

5. 🚀 **Кроссплатформенная архитектура CI/CD**:
   - Добавлен автоматический инструмент верификации `tools/verify.py` со строгой валидацией всех архивов, скриптов, прав доступа и лимитов свойств Android.

---

### 📦 Загрузка модулей из Git LFS (Direct Download Links):
- [Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip) (488 MB)
- [Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip) (284 MB)
- [Mi13U_Master_Camera_Combo_v6.1_MasterFinal_by_borndead.zip](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi13U_Master_Camera_Combo_v6.1_MasterFinal_by_borndead.zip) (431 MB)
- [Mi13U_Camera_v6.1_MIUI14_EU_Stable_by_borndead.zip](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi13U_Camera_v6.1_MIUI14_EU_Stable_by_borndead.zip) (431 MB)
- [Mi13U_Camera_v6.1_MIUI14_by_borndead.apk](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi13U_Camera_v6.1_MIUI14_by_borndead.apk) (162 MB)
- [Mi14U_Master_Camera_Combo_Full_by_borndead.zip](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi14U_Master_Camera_Combo_Full_by_borndead.zip) (201 MB)
- [Mi15_Master_Camera_Combo_Full_by_borndead.zip](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi15_Master_Camera_Combo_Full_by_borndead.zip) (212 MB)
- [Mi15U_Master_Camera_Combo_Full_by_borndead.zip](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi15U_Master_Camera_Combo_Full_by_borndead.zip) (305 MB)
- [X17U_Master_Camera_Combo_Full_by_borndead.zip](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/X17U_Master_Camera_Combo_Full_by_borndead.zip) (370 MB)
- [Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip](https://media.githubusercontent.com/media/bjorndith-cmd/Mi_Master_Camera_Combo/main/releases/Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip) (10 KB)

---

> 💬 **Официальное сообщество и поддержка проекта:**  
> Telegram: [@Mi_Master_Camera_Combo](https://t.me/Mi_Master_Camera_Combo)  
> Автор сборки: **`borndead`**
"""

def update_release_metadata():
    token = publish_github_release.get_token()
    if not token:
        print("Error: No GitHub token.")
        return
    repo = "bjorndith-cmd/Mi_Master_Camera_Combo"
    tag = TAG_NAME
    
    # Get release id
    req_get = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/releases/tags/{tag}",
        headers={"Authorization": f"token {token}", "User-Agent": "Python"}
    )
    with urllib.request.urlopen(req_get) as resp:
        rel_info = json.loads(resp.read().decode())
        rel_id = rel_info["id"]
    
    print(f"Found release ID: {rel_id}. Updating title and description...")
    patch_data = json.dumps({
        "name": RELEASE_NAME,
        "body": BODY
    }).encode("utf-8")
    
    req_patch = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/releases/{rel_id}",
        data=patch_data,
        headers={
            "Authorization": f"token {token}",
            "User-Agent": "Python",
            "Content-Type": "application/json"
        },
        method="PATCH"
    )
    with urllib.request.urlopen(req_patch) as resp:
        updated = json.loads(resp.read().decode())
        print(f"Successfully updated release name to: {updated.get('name')}")

if __name__ == "__main__":
    update_release_metadata()
