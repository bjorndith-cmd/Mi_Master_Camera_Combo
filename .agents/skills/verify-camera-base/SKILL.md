---
name: verify-camera-base
description: >-
  Определение, какая база камеры лежит внутри модуля или APK проекта Xiaomi
  Master Camera Combo, и сверка её с устройством. Используй при подготовке
  релиза, при разборе жалоб тестеров и когда нужно понять, на какой камере
  собран архив.
---

# Проверка базы камеры

База камеры — главное решение при сборке. Ошибка в базе означает, что камера
получит XML и карту сенсоров от другого устройства.

## Доступные базы

| База | versionCode | Собрана под | Применение |
|---|---|---|---|
| **Universal 5.0 Beta 8.3** | `599830000` | Android 11 (API 30) | основная |
| **6.8.001960.0** | `680019600` | Android 16 (API 36) | только 13 Ultra |
| HOLYBEAR-5.2.001450.2 | `1520014502` | Android 13 (API 33) | чужая ветка |

База **Universal 5.0 Beta 8.3** собрана под API 30, но ставится на Android
15–16. При странностях на новых системах это первое, что нужно учитывать:
камера родом из эпохи Android 11.

## Как определить базу

### Быстро — по хешу, без распаковки

`scripts/scan_bases.ps1` читает камеру прямо из архивов и группирует их по
хешу. Файлы по 162 МБ на диск не пишутся, поэтому проверка всех релизов
занимает меньше минуты.

```powershell
& 'C:\Mi_Master_Camera_Combo\.agents\skills\verify-camera-base\scripts\scan_bases.ps1'
```

### Точечно — версия из APK

Достать камеру из архива и прочитать версию:

```powershell
$aapt = 'E:\Android\Sdk\build-tools\35.0.0\aapt.exe'
$tmp = "$env:TEMP\camcheck"
New-Item -ItemType Directory -Path $tmp -Force | Out-Null
tar.exe -xf 'C:\путь\к\модулю.zip' -C $tmp 'system/priv-app/MiuiCamera/MiuiCamera.apk'
& $aapt dump badging "$tmp\system\priv-app\MiuiCamera\MiuiCamera.apk" |
  Select-String 'versionName|compileSdkVersion'
```

## Ловушка: `aapt2` молчит на части сборок

На `Mi13U_Camera_6_v8.2_by_borndead.apk` команда `aapt2 dump badging` завершается
ошибкой и не выдаёт ничего. Тот же файл старый **`aapt`** читает нормально.

Оба лежат в `E:\Android\Sdk\build-tools\35.0.0\`.

**Правило: если `aapt2` не дал версию — пробовать `aapt`, и только потом
делать вывод, что APK битый.**

## Ловушка: имя файла камеры в разном регистре

В части сборок APK внутри называется `MIUICamera.apk` (заглавные `UI`), в
остальных `MiuiCamera.apk`. Например так в
`Mi14U_HolyBear_5.2_CleanProp_Beta_by_borndead.zip`.

Если путь к камере прописан в скрипте вручную, на таких архивах распаковка
молча ничего не достанет, и версия останется «не прочитано».

**Брать имя записи из оглавления архива:**

```powershell
$entry = tar.exe -tf $zip | Where-Object { $_ -match '(?i)MiuiCamera\.apk$' } | Select-Object -First 1
tar.exe -xf $zip -C $tmp $entry
```

## Метаданные версии в имени

В именах APK из `Freebuff\workspace` число после `v` — это версия базы:

```
MiuiCamera_v58_aligned.apk   → 5.8  = Universal 5.0 Beta 8.3
MiuiCamera_v59_aligned.apk   → 5.9
MiuiCamera_v60_aligned.apk   → 6.0
MiuiCamera_v6.8_ishtar.apk   → 6.8
```

Суффиксы: `_aligned` — выровненный, `_signed` — подписанный, `_unsigned` —
без подписи.

## Сверка с устройством

База должна соответствовать кодовому имени. Например, для `xuanyuan`
(Xiaomi 15 Ultra) проверять, что перископ — Samsung HP9 на 200 Мп, а не
IMX858. Если в конфиге указан не тот сенсор — камера уйдёт в аварийный режим и
снимки сохранятся уменьшенными.

Список сенсоров по устройствам — в правилах проекта:
`.agents/rules/project.md`

## Известные проблемы в релизах

### «Пустые» архивы — это указатели Git LFS (версия опровергнута)

Ранее считалось, что семь архивов в `releases\` потеряли содержимое и их надо
пересобирать. **Это была неверная версия.** Файлы целы, а нулевой размер
означал другое.

Все `.zip` и `.apk` в проекте хранятся через Git LFS (см. `.gitattributes`).
В репозитории лежит указатель из трёх строк:

```
version https://git-lfs.github.com/spec/v1
oid sha256:97a825251c450c62faf0c0d6da9109481edb563b3a35dfe2dab9ce3850e7978a
size 4807
```

Если фильтр LFS не сработал при checkout, рабочий файл остаётся нулевым, хотя
содержимое лежит в `.git\lfs\objects`. **Ничего пересобирать не нужно** —
файл восстанавливается копированием объекта.

### Как восстановить

```powershell
$r   = 'C:\Mi_Master_Camera_Combo\github_sync'
$lfs = "$r\.git\lfs\objects"
Set-Location $r
$n   = 'Leica_13U_Configs_Master_Pack.zip'
$ptr = (git cat-file -p "HEAD:releases/$n") -join "`n"
$oid = ([regex]::Match($ptr, 'oid sha256:([0-9a-f]{64})')).Groups[1].Value
Copy-Item "$lfs\$($oid.Substring(0,2))\$($oid.Substring(2,2))\$oid" "$r\releases\$n" -Force
```

После копирования проверить, что `git status` по этому файлу молчит — значит
содержимое побайтово совпало.

### Почему фильтр LFS падает

`git-lfs` не запускается, если процесс не может создать именованный канал:

```
fatal: could not create signal pipe, Win32 error 5
error: could not read greeting from subprocess 'git-lfs filter-process'
```

Внутри ограниченной песочницы это ожидаемо. Вне неё LFS работает нормально,
и `git status` проходит без ошибок. Если файлы снова оказались нулевыми —
запускать git вне песочницы, а не пересобирать модули.

### Архивы без `MiuiCamera.apk` — 12 штук, и это нормально

Пять модулей меняют HAL, а не приложение камеры. Внутри только
`system/odm/lib64/hw/camera.qcom.so` и `system/odm/lib64/libmialgo_snsc.so`.
Не считать их битыми.

Остальные семь — небольшие модули и наборы конфигов от 4,8 до 23,7 КБ:
`Leica_13U_Configs_Master_Pack.zip` (пресеты AGC), четыре `Mi_AI_*`
(вспомогательные модули) и два `Mi*_Master_Imaging_MOD_*_Slim`.
Камеры в них нет по замыслу.

**Признак того, что файл действительно битый — ровно 0 байт.** Всё, что больше,
это нормальный файл, каким бы маленьким он ни был. Порог в мегабайт здесь
применять нельзя.

### Архивы с чужой базой

`Mi14U_HolyBear_*.zip` содержат `HOLYBEAR-5.2.001450.2` — это не Universal
5.0 Beta 8.3. Плюс у них сломана упаковка (CRLF). Перед отправкой проверять
навыком `package-magisk-module`.

## Что делать при расхождении базы

1. Не отправлять тестерам, пока не выяснена причина расхождения
2. Проверить, что камера в архиве — та, которую собирались положить
3. Если база не подходит устройству — пересобрать на подходящей
