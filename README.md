# Xiaomi Master Camera Combo 5
**Magisk / KernelSU / SukiSU / Kitsune module for Xiaomi 13 Ultra (ishtar) & 14 Pro (shennong)**
Base: Universal 5.0 Beta 8.3 · xiaomi.eu HyperOS 3.0 / Android 16 · by `borndead`

**Latest:** [v5.57.0-EU-Definitive](https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo/releases/tag/v5.57.0-EU-Definitive)

---

## What's fixed in v5.56 / Что исправлено в v5.56

**English**
- Camera not launching on any Magisk (stable & Alpha): removed a stale `oat/` dir that broke dexopt (`run-from-apk`) — the root cause.
- Added automatic AOT compile of the camera on first boot (one-time, background).
- Action menu language corrected: 1 = Русский, 2 = English (was swapped), default English.
- WebUI Russian messages no longer hang (recursion bug fixed in `webui.sh`).
- Version strings updated in menu / WebUI / logs.
- Front-camera beauty flags enabled (selfie sliders).

**Русский**
- Камера не запускалась на любом Magisk (стабильный и Alpha): удалена битая папка `oat/`, ломавшая dexopt (`run-from-apk`) — первопричина.
- Добавлена авто AOT-компиляция камеры при первом буте (разово, в фоне).
- Язык меню Action исправлен: 1 = Русский, 2 = English (было наоборот), по умолчанию английский.
- Русские сообщения WebUI больше не зависают (исправлена рекурсия в `webui.sh`).
- Строки версий обновлены в меню / WebUI / логах.
- Включены флаги бьютификации фронталки (ползунки селфи).

---

## Install / Установка

**EN:** 1) Magisk → Modules → Install from storage → select zip. 2) Reboot, wait 1–2 min (background AOT compile), reboot once more. 3) Open Camera.
If the camera still fails: Action menu → item 4 (AOT Speed compile).

**RU:** 1) Magisk → Модули → Установить из хранилища → выбрать zip. 2) Перезагрузка, подождать 1–2 мин (фоновая AOT-компиляция), ещё раз перезагрузиться. 3) Открыть камеру.
Если камера всё ещё не работает: меню Action → пункт 4 (AOT Speed compile).

---

## How to report an issue / Как сообщить о проблеме

**Screenshots (normal) / Скриншоты (обычные):** `Power + Volume Down` (или жест).
**Live logs / Живые логи:**
- EN: Action menu → item 15 (Collect live session logs, 60 s). Reproduce the issue ~30 s, then send `Download/CameraMod_Logs/session_log.txt`.
- RU: меню Action → пункт 15 (Собрать живые логи сессии, 60 с). Воспроизвести проблему ~30 с, затем отправить `Download/CameraMod_Logs/session_log.txt`.

---

## Action menu reference / Справка по меню Action

| # | EN | RU |
|---|----|----|
| 1 | Status & camera module check | Статус и проверка модуля |
| 2 | Restore MIVI contract (cache inject) | Восстановить контракт MIVI (инжект кэша) |
| 3 | Restart camera on the fly | Перезапустить камеру |
| 4 | AOT speed compile camera (~5s) | AOT-компиляция камеры (~5с) |
| 5 | Clear camera cache | Очистить кэш камеры |
| 6 | Toggle AISP / ASD (Leica AI Render) | Вкл/выкл AISP / ASD |
| 7 | Toggle 50 MP FullRes envelope | Вкл/выкл конверт 50 МП |
| 8 | Toggle LOCAL AI Pack (NPU/DSP) | Вкл/выкл LOCAL AI Pack |
| 9 | Inject 30 native 3D LUTs | Внедрить 30 3D LUT |
| 10 | Inject 24 watermarks into Gallery | Внедрить 24 водяных знака в Галерею |
| 11 | Choose Leica watermark style | Выбрать стиль водяного знака Leica |
| 12 | Toggle shutter sound | Переключить звук затвора |
| 13 | Inject CineStill 800T & Chromatic shaders | Внедрить шейдеры CineStill |
| 14 | Delete camera logs | Удалить логи камеры |
| 15 | Collect live session logs (60s) | Собрать живые логи сессии (60с) |
| 16 | Language / Язык | Язык / Language |
| q | Exit | Выход |

**WebUI** (в приложении Magisk → иконка модуля): те же настройки графически, включая язык и статус.

---

## Links / Ссылки
- Releases: https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo/releases
- Telegram: https://t.me/Mi_Master_Camera_Combo
- Manuals / Мануалы: `MANUAL_Mi13U_v6.6_EU_RU.md`, `ADVANCED_SETTINGS_GUIDE_Mi13U.md`, `LAB_SETTINGS_GUIDE_Mi13U.md`, `UNIVERSAL_SETTINGS_GUIDE_Mi13U.md`
