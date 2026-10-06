<#
  Сканирование всех релизов: какая база камеры внутри каждого архива.

  Читает MiuiCamera.apk прямо из архива и группирует архивы по SHA-256.
  Файлы по 162 МБ на диск не пишутся — только поток в память, поэтому
  проверка всех релизов занимает меньше минуты.

  Использование:
    .\scan_bases.ps1
    .\scan_bases.ps1 -Releases 'D:\другая\папка'
#>
[CmdletBinding()]
param(
    [string]$Releases = 'C:\Mi_Master_Camera_Combo\github_sync\releases'
)

$ErrorActionPreference = 'Continue'
Add-Type -AssemblyName System.IO.Compression.FileSystem 2>$null

$aapt  = 'E:\Android\Sdk\build-tools\35.0.0\aapt.exe'    # aapt2 не читает часть сборок
$sha   = [System.Security.Cryptography.SHA256]::Create()
$rows  = @()

Write-Host ''
Write-Host "  Папка: $Releases" -ForegroundColor Cyan
Write-Host '  Читаю камеры из архивов...' -ForegroundColor Gray

foreach ($z in Get-ChildItem $Releases -Filter '*.zip' | Sort-Object Name) {
    # Ровно ноль байт означает, что не развернулся Git LFS, а не потерю
    # содержимого. Порог в 1 МБ здесь не годится: в проекте есть рабочие
    # модули и наборы конфигов размером от 5 КБ.
    if ($z.Length -eq 0) {
        $rows += [pscustomobject]@{ Архив = $z.Name; Хеш = 'НЕ РАЗВЁРНУТ LFS'; Размер = '0 б' }
        continue
    }
    try {
        $zip = [System.IO.Compression.ZipFile]::OpenRead($z.FullName)
        $e = $zip.Entries | Where-Object { $_.Name -eq 'MiuiCamera.apk' } | Select-Object -First 1
        if (-not $e) {
            $zip.Dispose()
            $rows += [pscustomobject]@{ Архив = $z.Name; Хеш = 'БЕЗ КАМЕРЫ'; Размер = '—' }
            continue
        }
        $st = $e.Open()
        $ms = New-Object System.IO.MemoryStream
        $st.CopyTo($ms); $st.Close()
        $hash = [BitConverter]::ToString($sha.ComputeHash($ms.ToArray())).Replace('-', '').Substring(0, 12)
        $rows += [pscustomobject]@{
            Архив  = $z.Name
            Хеш    = $hash
            Размер = '{0:N1} МБ' -f ($e.Length / 1MB)
        }
        $zip.Dispose()
    } catch {
        $rows += [pscustomobject]@{ Архив = $z.Name; Хеш = 'ОШИБКА'; Размер = $_.Exception.Message.Substring(0, [Math]::Min(40, $_.Exception.Message.Length)) }
    }
}

# Версию читаем только для уникальных хешей — не гоняем aapt по 20 раз
$tmp = Join-Path $env:TEMP ("basever_" + [guid]::NewGuid().ToString('N').Substring(0, 8))
New-Item -ItemType Directory -Path $tmp -Force | Out-Null
$versions = @{}
foreach ($grp in ($rows | Where-Object { $_.Хеш -notin @('ПУСТОЙ', 'БЕЗ КАМЕРЫ', 'ОШИБКА') } | Group-Object Хеш)) {
    $sample = (Get-ChildItem $Releases -Filter $grp.Group[0].Архив | Select-Object -First 1).FullName
    Remove-Item "$tmp\*" -Recurse -Force -ErrorAction SilentlyContinue
    # Путь берём из самого архива, а не пишем жёстко: в части сборок файл
    # называется MIUICamera.apk заглавными, и tar не находит его по
    # прописанному вручную пути.
    $entryName = (& tar.exe -tf $sample 2>&1 |
                  Where-Object { $_ -match '(?i)MiuiCamera\.apk$' } | Select-Object -First 1)
    if ($entryName) { & tar.exe -xf $sample -C $tmp $entryName 2>$null | Out-Null }
    $apk = Get-ChildItem $tmp -Recurse -Filter '*.apk' -ErrorAction SilentlyContinue | Select-Object -First 1
    $ver = 'не прочитано'
    if ($apk -and (Test-Path $aapt)) {
        # -cmatch и \b обязательны: в строке вывода aapt рядом стоит
        # platformBuildVersionName, а PowerShell по регистр не различает —
        # без этого версия читалась как '11' или '16' вместо названия базы.
        $line = (& $aapt dump badging $apk.FullName 2>&1 |
                 Select-String -Pattern "\bversionName=" | Select-Object -First 1).Line
        if ($line -cmatch "versionName='([^']*)'") { $ver = $matches[1] }
    }
    $versions[$grp.Name] = $ver
}
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ''
foreach ($grp in ($rows | Group-Object Хеш | Sort-Object Count -Descending)) {
    $v = $versions[$grp.Name]
    $head = if ($v) { "$($grp.Name)  —  $v" } else { $grp.Name }
    Write-Host "=== $head  ($($grp.Count) архивов) ===" -ForegroundColor Cyan
    $grp.Group | ForEach-Object { Write-Host ("   {0,-66} {1}" -f $_.Архив, $_.Размер) }
    Write-Host ''
}

$bad  = @($rows | Where-Object Хеш -eq 'НЕ РАЗВЁРНУТ LFS').Count
$slim = @($rows | Where-Object Хеш -eq 'БЕЗ КАМЕРЫ').Count
Write-Host "  Всего архивов: $($rows.Count)" -ForegroundColor White
Write-Host "  Не развёрнут LFS (0 байт): $bad$(if($bad -gt 0){'  — восстановить из .git\lfs\objects, НЕ пересобирать'})" -ForegroundColor $(if ($bad -gt 0) { 'Yellow' } else { 'Green' })
Write-Host "  Без камеры (HAL-модификации и конфиги): $slim" -ForegroundColor Gray
Write-Host ''
