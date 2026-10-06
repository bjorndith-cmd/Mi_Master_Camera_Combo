# Xiaomi Master Camera Combo

Модификация системной камеры Xiaomi для флагманов 13U / 14U / 15 / 15 Pro /
15 Ultra / 17 Ultra. Автор сборок — `borndead`.

## Перед началом работы прочитай правила

**`C:\Mi_Master_Camera_Combo\.agents\rules\project.md`**

Там устройства и их кодовые имена, базы камер, грабли, на которых уже
спотыкались, и правила для инструкций тестерам. Читается автоматически, но
если сомневаешься — открой явно.

## Навыки

| Навык | Когда применять |
|---|---|
| `.agents/skills/package-magisk-module/` | собираешь или проверяешь модуль перед отправкой |
| `.agents/skills/verify-camera-base/` | нужно узнать, какая камера внутри архива |

## Три вещи, которые ломали работу чаще всего

**1. Окончания строк CRLF в шелл-скриптах.** Модуль не устанавливается с
ошибкой `syntax error: unexpected word (expecting "do")`, а выглядит это как
несовместимость с версией Android. Всегда проверяй перед отправкой:

```powershell
& 'C:\Mi_Master_Camera_Combo\.agents\skills\package-magisk-module\scripts\verify_module.ps1' `
  -Zip 'C:\путь\к\модулю.zip'
```

**2. Подмена кодового имени.** Строка `resetprop ro.product.device "ishtar"`
заставляет камеру думать, что она на 13 Ultra, и на других устройствах ломает
карту сенсоров. Не подменять.

**3. Расхождение версии.** Имя файла может говорить `v6.4`, а внутри
`module.prop` стоять `v6.1` с тем же `versionCode` — тестер поставит старое и
не заметит. Версия и `versionCode` обязаны увеличиваться.

## Пути

| Что | Где |
|---|---|
| Репозиторий | `C:\Mi_Master_Camera_Combo\github_sync` |
| Релизы | `C:\Mi_Master_Camera_Combo\github_sync\releases` |
| Конфиги устройств | `C:\Mi_Master_Camera_Combo\github_sync\configs` |
| Рабочие сборки | `C:\Mi_Master_Camera_Combo\Freebuff\workspace` |

## Файлы в ответах

Рядом с именем файла всегда печатать полный путь — без него файл из чата не
открывается:

```
Mi15U_Master_Camera_Combo_5_v6.4_A16_Final.zip
C:\Mi_Master_Camera_Combo\github_sync\releases\Mi15U_Master_Camera_Combo_5_v6.4_A16_Final.zip
```
