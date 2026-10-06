<#
  Проверка модуля камеры перед отправкой тестерам.

  Главное, что ловит скрипт — окончания строк Windows в шелл-скриптах.
  Именно из-за них модуль не устанавливается с ошибкой
  "syntax error: unexpected word (expecting \"do\")", которая выглядит
  как несовместимость с версией Android, хотя версия тут ни при чём.

  Использование:
    .\verify_module.ps1 -Zip <путь к архиву>
    .\verify_module.ps1 -All      # проверить все архивы в папке релизов
#>
[CmdletBinding()]
param(
    [string]$Zip,
    [switch]$All
)

$ErrorActionPreference = 'Continue'
$releases = 'C:\Mi_Master_Camera_Combo\github_sync\releases'
$aapt  = 'E:\Android\Sdk\build-tools\35.0.0\aapt.exe'    # aapt2 не читает часть сборок
$aapt2 = 'E:\Android\Sdk\build-tools\35.0.0\aapt2.exe'

$script:blocking = 0
function Ok($m)  { Write-Host "  [ок]        $m" -ForegroundColor Green }
function Bad($m) { Write-Host "  [БЛОКИРУЕТ] $m" -ForegroundColor Red; $script:blocking++ }
function Warn($m){ Write-Host "  [внимание]  $m" -ForegroundColor Yellow }

function Test-Module($path) {
    $script:blocking = 0
    Write-Host ''
    Write-Host "── $(Split-Path $path -Leaf)" -ForegroundColor Cyan

    if (-not (Test-Path $path)) { Bad "файла нет: $path"; return }
    $size = (Get-Item $path).Length
    if ($size -eq 0) { Bad 'размер 0 байт — содержимое потеряно'; return }
    Write-Host ("  размер: {0:N1} МБ" -f ($size / 1MB))

    $tmp = Join-Path $env:TEMP ("modcheck_" + [guid]::NewGuid().ToString('N').Substring(0, 8))
    New-Item -ItemType Directory -Path $tmp -Force | Out-Null

    try {
        # ── Окончания строк — блокирующая проверка ──────────────────
        $shFiles = @('customize.sh', 'service.sh', 'post-fs-data.sh')
        $found = 0
        foreach ($s in $shFiles) {
            $dest = Join-Path $tmp $s
            & tar.exe -xf $path -C $tmp $s 2>$null | Out-Null
            if (-not (Test-Path $dest)) { continue }
            $found++
            $b = [System.IO.File]::ReadAllBytes($dest)
            $crlf = 0
            for ($i = 1; $i -lt $b.Length; $i++) {
                if ($b[$i] -eq 10 -and $b[$i - 1] -eq 13) { $crlf++ }
            }
            if ($crlf -gt 0) { Bad "$s — CRLF=$crlf. Модуль НЕ УСТАНОВИТСЯ. Пересобрать с LF." }
            else { Ok "$s — LF, в порядке" }
        }
        if ($found -eq 0) { Warn 'шелл-скриптов в архиве нет — это точно модуль камеры?' }

        # ── Разделители путей в записях архива ──────────────────────
        $names = & tar.exe -tf $path 2>&1
        $back = @($names | Where-Object { $_ -match '\\' })
        if ($back.Count -gt 0) { Bad "в архиве $($back.Count) записей с обратными слэшами — файлы лягут с битыми именами" }
        else { Ok 'разделители путей прямые' }

        # ── Обязательные файлы и версия ─────────────────────────────
        $mp = Join-Path $tmp 'module.prop'
        & tar.exe -xf $path -C $tmp 'module.prop' 2>$null | Out-Null
        # Ни скриптов, ни module.prop — это не модуль Magisk, а набор
        # конфигов или ресурсов (например Leica_13U_Configs_Master_Pack).
        # Требовать от него module.prop нельзя — это не поломка.
        if (-not (Test-Path $mp) -and $found -eq 0) {
            Warn 'это не модуль Magisk (нет customize.sh и module.prop) — набор конфигов, проверки модуля пропущены'
        }
        elseif (-not (Test-Path $mp)) { Bad 'нет module.prop' }
        else {
            $prop = Get-Content $mp -Raw
            $ver = ([regex]::Match($prop, '(?m)^version=(.+)$')).Groups[1].Value.Trim()
            $vc  = ([regex]::Match($prop, '(?m)^versionCode=(.+)$')).Groups[1].Value.Trim()
            Ok "version=$ver  versionCode=$vc"
            $fileVer = ([regex]::Match((Split-Path $path -Leaf), 'v(\d+\.\d+)')).Groups[1].Value
            if ($fileVer -and $ver -and ($ver -notmatch [regex]::Escape($fileVer))) {
                Warn "имя файла говорит v$fileVer, а внутри '$ver' — тестер увидит не ту версию"
            }
        }

        # ── Камера ──────────────────────────────────────────────────
        $camEntry = $names | Where-Object { $_ -match 'MiuiCamera\.apk$' } | Select-Object -First 1
        if (-not $camEntry) { Warn 'MiuiCamera.apk в архиве нет — это HAL-модификация без камеры?' }
        else {
            & tar.exe -xf $path -C $tmp $camEntry 2>$null | Out-Null
            $apk = Get-ChildItem $tmp -Recurse -Filter 'MiuiCamera.apk' -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($apk -and (Test-Path $aapt)) {
                $out = & $aapt dump badging $apk.FullName 2>&1 | Select-String 'versionName|compileSdkVersion' | Select-Object -First 2
                if ($out) { $out | ForEach-Object { Ok ($_.Line.Trim() -replace '\s+', ' ') } }
                else { Warn 'версию камеры прочитать не удалось (aapt молчит)' }
            }
        }
    } finally {
        Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
    }

    if ($script:blocking -eq 0) { Write-Host '  ИТОГ: можно отправлять' -ForegroundColor Green }
    else { Write-Host "  ИТОГ: НЕЛЬЗЯ ОТПРАВЛЯТЬ — $($script:blocking) блокирующих" -ForegroundColor Red }
}

if ($All) {
    $zips = Get-ChildItem $releases -Filter '*.zip' | Sort-Object Name
    foreach ($z in $zips) { Test-Module $z.FullName }
    Write-Host ''
    Write-Host "Проверено архивов: $($zips.Count)" -ForegroundColor Cyan
} elseif ($Zip) {
    Test-Module $Zip
} else {
    Write-Host 'Укажи -Zip <путь> или -All' -ForegroundColor Yellow
}
Write-Host ''
