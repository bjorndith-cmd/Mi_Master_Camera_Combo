import os
import sys
import json
import subprocess
import urllib.request
import urllib.parse

REPO = "bjorndith-cmd/Mi_Master_Camera_Combo"

def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\npath=bjorndith-cmd/Mi_Master_Camera_Combo.git\n",
            capture_output=True,
            text=True,
            check=True
        )
        for line in proc.stdout.splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1].strip()
    except Exception:
        pass
    return None

TOKEN = get_token()

def create_release(tag_name, name, body, prerelease=False):
    if not TOKEN:
        raise ValueError("GitHub token could not be acquired.")
    url = f"https://api.github.com/repos/{REPO}/releases"
    data = json.dumps({
        "tag_name": tag_name,
        "name": name,
        "body": body,
        "draft": False,
        "prerelease": prerelease
    }).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"token {TOKEN}",
            "User-Agent": "Python",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode())
            print(f"Successfully created release: {res.get('name')} (ID: {res.get('id')})")
            return res
    except urllib.error.HTTPError as e:
        err_body = e.read().decode()
        print(f"HTTP error creating release {tag_name}: {e.code} - {err_body}")
        req_get = urllib.request.Request(
            f"https://api.github.com/repos/{REPO}/releases/tags/{tag_name}",
            headers={
                "Authorization": f"token {TOKEN}",
                "User-Agent": "Python",
                "Accept": "application/vnd.github.v3+json"
            }
        )
        with urllib.request.urlopen(req_get) as resp:
            return json.loads(resp.read().decode())

def upload_asset(release_id, file_path):
    if not TOKEN:
        raise ValueError("GitHub token could not be acquired.")
    filename = os.path.basename(file_path)
    filesize = os.path.getsize(file_path)
    print(f"Uploading asset {filename} ({filesize / (1024*1024):.2f} MB)...")
    
    url = f"https://uploads.github.com/repos/{REPO}/releases/{release_id}/assets?name={urllib.parse.quote(filename)}"
    
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    
    req = urllib.request.Request(
        url,
        data=file_bytes,
        headers={
            "Authorization": f"token {TOKEN}",
            "User-Agent": "Python",
            "Content-Type": "application/zip",
            "Content-Length": str(len(file_bytes))
        },
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode())
            print(f"Uploaded {filename}: {res.get('browser_download_url')} (ID: {res.get('id')})")
            return res
    except urllib.error.HTTPError as e:
        print(f"Failed to upload {filename}: {e.code} - {e.read().decode()}")
        return None

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    releases_dir = os.path.join(root, "releases")

    # 1. Release v6.8-Ishtar
    body_68 = """# Xiaomi 13 Ultra — Leica Camera v6.8 Flagship Port & Master Configs Pack 📸⚡
**Author / Автор:** `borndead`  
**Target Device:** Xiaomi 13 Ultra (`ishtar`)  
**Target System:** HyperOS 1.0 / 2.0 / 3.0 (Android 14 / 15 / 16)  

---

### 🌟 Что нового в версии v6.8-Ishtar (Changelog)

#### 1. Устранение бага 1.6 Мп (Native 12.5M & 50M)
- Ликвидирован фатальный таймаут оффлайн-графа Qualcomm Chi-CDK.
- Восстановлено полноценное сохранение снимков в нативном разрешении сенсоров **12.5 Мп (4096x3072)** и **50 Мп (8192x6144)** в JPEG и RAW/DNG.
- Полностью устранен сброс в превью-буфер видоискателя 1440x1080 (~160 КБ).

#### 2. Ликвидация лишнего режима 200 Мп и перегрева устройства
- Удален неподдерживаемый режим 200Мп (`Hongkong.smali`: переопределены методы `c0() -> null`, `Z0() -> ""`, `x() -> 300`).
- Отключен фоновый поток бесконечного опроса мотора непрерывного оптического зума (`8.6-200mm`), нагружавший CPU на 100%. Телефон больше не греется, интерфейс работает плавно и без лагов.

#### 3. Исправление пропорций лица в режиме «Двойная камера» (Dual Video)
- Метод `e0()[I` переопределен на возвращение `null`, восстанавливая нативные пропорции 4:3 для фронтального сенсора OmniVision OV32C (устранено искажение и вытягивание лица 16:9).

#### 4. Восстановление работы AI-фотосцен (AI Scene Detection)
- Метод `o2()Z` переопределен на `false` (0), предотвращая вызов отсутствующего на Snapdragon 8 Gen 2 блока Xiaomi AISP 2.0. Распознавание сцен и оптимизация кадра работают стабильно и корректно.

#### 5. Восстановление авторизации в Xiaomi Account (AI Capture Assist)
- В `system.prop` и скриптах модуля включен сетевой пайплайн авторизации (`persist.vendor.camera.cloud.enable 1`), благодаря чему окно входа в аккаунт Xiaomi отрабатывает штатно.

#### 6. Оптимизация многокамерной логической сессии Qualcomm SAT
- Список `vendor.camera.aux.packagelist` очищен от `com.android.camera`, исключая конфликты логической сессии Snapdragon SAT.

---

### 📦 Вложенные модули (Attachments):
- **`Mi13U_Camera_v6.8_Port_by_borndead.zip`** (141.6 MB) — Системный Magisk/KernelSU/APatch модуль с портом камеры Leica v6.8.
- **`Leica_13U_Configs_Master_Pack.zip`** (4.7 KB) — Полная коллекция авторских конфигов от `borndead` для Leica Camera и GCam (AGC 8.x/9.x, LMC).
"""
    rel_68 = create_release("v6.8-Ishtar", "v6.8-Ishtar: Xiaomi 13 Ultra Leica Camera v6.8 Port & Master Configs Pack", body_68)
    if rel_68:
        rel_id = rel_68["id"]
        upload_asset(rel_id, os.path.join(releases_dir, "Mi13U_Camera_v6.8_Port_by_borndead.zip"))
        upload_asset(rel_id, os.path.join(releases_dir, "Leica_13U_Configs_Master_Pack.zip"))

    # 2. Release v5.9 (Universal Combo)
    body_59 = """# Xiaomi Master Camera Combo Universal Suite v5.9 📸⚡
**Author / Автор:** `borndead`  
**Compatibility:** Xiaomi 13 Ultra, 14 Ultra, 15, 15 Pro, 15 Ultra, 17 Ultra  
**OS:** HyperOS 1.0 / 2.0 / 3.0 / 4.0 • Android 14 / 15 / 16 / 17 (API 34-37)  

---

### 🌟 Основные возможности линейки Universal v5.9:
- **FULL Edition**: Включает модифицированное приложение камеры Leica HyperOS 3.0 со всеми интерфейсными возможностями, водяными знаками, новыми фильтрами, защитой `oat/.replace` от бутлупа и удалением опасных разрешений платформы.
- **SLIM Edition**: Чистый системный оверлей (без изменения системного APK камеры). 100% безопасность на стоковых прошивках без CorePatch и на кастомных прошивках (SimpleRom, Xiaomi.eu).
- **AI Master Camera Suite**: Полный комплекс искусственного интеллекта (Tier 1: Аппаратный NPU AISP, Tier 2: Генеративная фотолаборатория HyperAI Studio, Tier 3: Умный ассистент видоискателя AI Director).
- **Разблокировка FullRes**: Честные 50Мп / 200Мп во всех режимах и Google Камере (AGC, LMC).
- **George Video MOD**: Видеосъемка 8K со всех задних сенсоров и 4K 120fps.
- **Аппаратный DCG HDR**: Двойное аппаратное усиление пикселя без смазов в движении.

---

### 📦 Вложенные модули (Attachments):
- **`Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip`** (182.5 MB)
- **`Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip`** (36.6 MB)
- **`Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip`** (4.1 KB)
"""
    rel_59 = create_release("v5.9", "v5.9-Universal: Universal Flagship Suite for Xiaomi 13U / 14U / 15 / 15 Pro / 15U / 17U", body_59)
    if rel_59:
        rel_id_59 = rel_59["id"]
        upload_asset(rel_id_59, os.path.join(releases_dir, "Mi_Master_Camera_Combo_Universal_Full_by_borndead.zip"))
        upload_asset(rel_id_59, os.path.join(releases_dir, "Mi_Master_Camera_Combo_Universal_Slim_by_borndead.zip"))
        upload_asset(rel_id_59, os.path.join(releases_dir, "Mi_AI_Master_Camera_Suite_AllInOne_by_borndead.zip"))

if __name__ == "__main__":
    main()
