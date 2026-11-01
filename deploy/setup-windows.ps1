# BSM Mekanik - Windows sunucu kurulumu (Caddy)
#
# Kullanım (Yönetici olarak açılmış PowerShell'de):
#   powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1              # demo: bsmmekanik.nesakyazilim.com
#   powershell -ExecutionPolicy Bypass -File .\setup-windows.ps1 -Mode domains # alan adları sunucuya yönlendikten sonra
#   Caddyfile otomatik bulunamazsa:  ... -Caddyfile "C:\caddy\Caddyfile"
#
# Yaptıkları: Git'i kurar (yoksa), repo gizliyse GitHub okuma anahtarı (deploy key) üretir, siteyi C:\bsmmekanik'e çeker,
# Caddyfile'a tek bir import satırı ekler (önce yedek alır, doğrulamadan yeniden yüklemez) ve 5 dakikada bir
# GitHub'dan güncelleyen zamanlanmış görev kurar. Tekrar çalıştırılabilir.

param(
    [ValidateSet('demo', 'domains')][string]$Mode = 'demo',
    [string]$Caddyfile = ''
)

$ErrorActionPreference = 'Stop'
$AppDir   = 'C:\bsmmekanik'
$KeyDir   = 'C:\bsmmekanik-key'
$Key      = 'C:/bsmmekanik-key/id_ed25519'
$Repo     = 'git@github.com:emremuslu42-hub/recep-berk-can.git'
$RepoHttps = 'https://github.com/emremuslu42-hub/recep-berk-can.git'
$Branch   = 'claude/bold-edison-kwvvmm'
$Import   = 'import C:/bsmmekanik/deploy/bsmmekanik-windows.caddy'
$DomainsFile   = 'C:\bsmmekanik-key\domains.caddy'
$DomainsImport = 'import C:/bsmmekanik-key/domains.caddy'
$SshCmd   = "ssh -i $Key -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=C:/bsmmekanik-key/known_hosts"
$Utf8     = New-Object System.Text.UTF8Encoding $false

function Say($m)  { Write-Host "`n==> $m" -ForegroundColor Cyan }
function Warn($m) { Write-Host $m -ForegroundColor Yellow }
function Die($m)  { Write-Host "`nHATA: $m" -ForegroundColor Red; exit 1 }

# Harici programı çalıştırır; çıktıyı gösterir, çıkış kodunu döndürür (PowerShell 5.1/7 uyumlu)
function Exec([string]$File, [string]$Arguments, [switch]$Quiet) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $File
    $psi.Arguments = $Arguments
    $psi.UseShellExecute = $false          # ortam değişkenleri (GIT_SSH_COMMAND) aktarılır
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $p = [System.Diagnostics.Process]::Start($psi)
    $stdout = $p.StandardOutput.ReadToEndAsync()
    $stderr = $p.StandardError.ReadToEnd()
    $p.WaitForExit()
    if (-not $Quiet) {
        ($stdout.Result + "`n" + $stderr) -split "`r?`n" | Where-Object { $_.Trim() } | ForEach-Object { Write-Host "   $_" }
    }
    return $p.ExitCode
}

# --- Yönetici kontrolü
$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $admin) { Die 'PowerShell''i "Yönetici olarak çalıştır" ile açıp tekrar deneyin.' }

# --- Caddy'yi bul
Say 'Caddy aranıyor'
$proc = Get-CimInstance Win32_Process -Filter "Name='caddy.exe'" | Select-Object -First 1
if (-not $proc) { Die 'Çalışan caddy.exe bulunamadı. Caddy açık mı?' }
$CaddyExe = $proc.ExecutablePath
Write-Host "   caddy.exe : $CaddyExe"
Write-Host "   komut     : $($proc.CommandLine)"

$svc = Get-CimInstance Win32_Service | Where-Object { $_.ProcessId -eq $proc.ProcessId -or $_.PathName -like '*caddy*' } | Select-Object -First 1
if (-not $svc) {
    # NSSM gibi sarmalayıcılar: üst süreç hizmet olabilir
    $svc = Get-CimInstance Win32_Service | Where-Object { $_.ProcessId -eq $proc.ParentProcessId } | Select-Object -First 1
}
if ($svc) { Write-Host "   hizmet    : $($svc.Name)" }

if (-not $Caddyfile) {
    $cands = @()
    if ($proc.CommandLine -match '--config[ =]+"([^"]+)"') { $cands += $Matches[1] }
    elseif ($proc.CommandLine -match '--config[ =]+(\S+)') { $cands += $Matches[1] }
    $exeDir = Split-Path $CaddyExe
    $cands += (Join-Path $exeDir 'Caddyfile')
    if ($svc) {
        $nssm = "HKLM:\SYSTEM\CurrentControlSet\Services\$($svc.Name)\Parameters"
        if (Test-Path $nssm) {
            $dir = (Get-ItemProperty $nssm -ErrorAction SilentlyContinue).AppDirectory
            if ($dir) { $cands += (Join-Path $dir 'Caddyfile') }
        }
    }
    foreach ($c in $cands) {
        $full = if ([IO.Path]::IsPathRooted($c)) { $c } else { Join-Path $exeDir $c }
        if (Test-Path $full) { $Caddyfile = $full; break }
    }
}
if (-not $Caddyfile -or -not (Test-Path $Caddyfile)) {
    Die "Caddyfile bulunamadı. Yolunu belirtin:  -Caddyfile ""C:\...\Caddyfile"""
}
if ($Caddyfile -like '*.json') { Die "Caddy JSON ayarıyla çalışıyor ($Caddyfile); bu betik Caddyfile bekliyor. Bana yazın." }
Write-Host "   Caddyfile : $Caddyfile"

# --- Git
Say 'Git kontrol ediliyor'
$gitCmd = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitCmd) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        Die 'Git yüklü değil ve winget yok. https://git-scm.com/download/win adresinden Git''i kurup tekrar çalıştırın.'
    }
    Write-Host '   Git kuruluyor (winget)...'
    winget install --id Git.Git -e --source winget --silent --accept-package-agreements --accept-source-agreements | Out-Host
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
    $gitCmd = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitCmd) { Die 'Git kuruldu ama bulunamadı. PowerShell''i kapatıp açın ve betiği tekrar çalıştırın.' }
}
$GitExe = $gitCmd.Source
$GitRoot = Split-Path (Split-Path $GitExe)
$SshKeygen = Join-Path $GitRoot 'usr\bin\ssh-keygen.exe'
if (-not (Test-Path $SshKeygen)) { $SshKeygen = 'ssh-keygen' }
Write-Host "   git : $GitExe"

# --- Repo erişimi: herkese açıksa HTTPS, gizliyse okuma anahtarı (deploy key)
$env:GIT_TERMINAL_PROMPT = '0'
$UseSsh = $false
Say 'GitHub erişimi kontrol ediliyor'
if ((Exec $GitExe "ls-remote -q $RepoHttps" -Quiet) -eq 0) {
    Write-Host '   repo herkese açık, HTTPS ile çekilecek'
    $Repo = $RepoHttps
} else {
    $UseSsh = $true
    if (-not (Test-Path $KeyDir)) { New-Item -ItemType Directory -Path $KeyDir | Out-Null }
    icacls $KeyDir /inheritance:r /grant:r 'Administrators:(OI)(CI)F' 'SYSTEM:(OI)(CI)F' | Out-Null
    if (-not (Test-Path "$KeyDir\id_ed25519")) {
        Say 'GitHub okuma anahtarı oluşturuluyor'
        $null = Exec $SshKeygen "-q -t ed25519 -N `"`" -C bsmmekanik-vds -f `"$KeyDir\id_ed25519`""
        if (-not (Test-Path "$KeyDir\id_ed25519.pub")) { Die 'Anahtar oluşturulamadı.' }
    }
    $env:GIT_SSH_COMMAND = $SshCmd
    while ((Exec $GitExe "ls-remote -q $Repo" -Quiet) -ne 0) {
        Warn "`nRepo gizli. Sunucunun okuyabilmesi için bu anahtarı GitHub'a ekleyin:"
        Write-Host '  https://github.com/emremuslu42-hub/recep-berk-can/settings/keys  ->  Add deploy key'
        Write-Host '  Title: bsmmekanik-vds   -   "Allow write access" İŞARETLEMEYİN'
        Write-Host ''
        Write-Host (Get-Content "$KeyDir\id_ed25519.pub") -ForegroundColor Green
        Write-Host ''
        Read-Host 'Ekledikten sonra Enter''a basın (çıkmak için Ctrl+C)' | Out-Null
    }
}
if (-not (Test-Path $KeyDir)) { New-Item -ItemType Directory -Path $KeyDir | Out-Null }
Write-Host '   erişim tamam'

# --- Site dosyaları
Say 'Site dosyaları GitHub''dan alınıyor'
$safe = '-c safe.directory=*'
if (Test-Path "$AppDir\.git") {
    if ((Exec $GitExe "$safe -C `"$AppDir`" fetch -q --depth 1 origin $Branch") -ne 0) { Die 'git fetch başarısız.' }
    if ((Exec $GitExe "$safe -C `"$AppDir`" reset -q --hard origin/$Branch") -ne 0) { Die 'git reset başarısız.' }
} else {
    if (Test-Path $AppDir) { Rename-Item $AppDir "$AppDir.yedek-$(Get-Date -Format yyyyMMddHHmmss)" }
    if ((Exec $GitExe "clone -q --depth 1 --branch $Branch $Repo `"$AppDir`"") -ne 0) { Die 'git clone başarısız.' }
}
if ($UseSsh) { $null = Exec $GitExe "$safe -C `"$AppDir`" config core.sshCommand `"$SshCmd`"" }
if (-not (Test-Path "$AppDir\deploy\bsmmekanik-windows.caddy")) { Die 'Depoda deploy\bsmmekanik-windows.caddy bulunamadı.' }

# --- Caddy ayarı
Say 'Caddy ayarı ekleniyor'
$backup = "$Caddyfile.yedek-bsm"
if (-not (Test-Path $backup)) { Copy-Item $Caddyfile $backup; Write-Host "   yedek: $backup" }
$current = [IO.File]::ReadAllText($Caddyfile)
if ($current -notmatch [regex]::Escape($Import)) {
    [IO.File]::AppendAllText($Caddyfile, "`r`n# BSM Mekanik`r`n$Import`r`n", $Utf8)
}
if ($Mode -eq 'domains') {
    $domains = @"
www.bsmmekanik.com, www.bsmmechanical.com {
	import bsm_site
}
bsmmekanik.com {
	redir https://www.bsmmekanik.com{uri} permanent
}
bsmmechanical.com {
	redir https://www.bsmmechanical.com{uri} permanent
}
"@
    [IO.File]::WriteAllText($DomainsFile, $domains, $Utf8)
    $current = [IO.File]::ReadAllText($Caddyfile)
    if ($current -notmatch [regex]::Escape($DomainsImport)) {
        [IO.File]::AppendAllText($Caddyfile, "$DomainsImport`r`n", $Utf8)
    }
}

$cfgArgs = "--config `"$Caddyfile`" --adapter caddyfile"
if ((Exec $CaddyExe "validate $cfgArgs") -ne 0) {
    Copy-Item $backup $Caddyfile -Force
    Die "Caddy ayarı geçersiz çıktı; Caddyfile yedekten geri yüklendi ($backup). Çıktıyı bana gönderin."
}
Say 'Caddy yeniden yükleniyor'
if ((Exec $CaddyExe "reload $cfgArgs") -ne 0) {
    if ($svc) {
        Warn "   reload olmadı, '$($svc.Name)' hizmeti yeniden başlatılıyor"
        Restart-Service -Name $svc.Name -Force
    } else {
        Warn '   Caddy yeniden yüklenemedi. Caddy''yi kapatıp yeniden başlatın.'
    }
}

# --- Otomatik güncelleme
Say 'Otomatik güncelleme görevi (5 dakikada bir)'
$update = @'
$ErrorActionPreference = 'Continue'
if ('__SSH__') { $env:GIT_SSH_COMMAND = '__SSH__' }
$git = '__GIT__'; $app = 'C:\bsmmekanik'; $log = 'C:\bsmmekanik-key\update.log'
$before = & $git -c safe.directory=* -C $app rev-parse HEAD
& $git -c safe.directory=* -C $app fetch -q --depth 1 origin __BRANCH__ 2>&1 | Out-Null
$after = & $git -c safe.directory=* -C $app rev-parse origin/__BRANCH__
if ($after -and $before -ne $after) {
    & $git -c safe.directory=* -C $app reset -q --hard origin/__BRANCH__ 2>&1 | Out-Null
    & '__CADDY__' reload --config '__CADDYFILE__' --adapter caddyfile 2>&1 | Out-Null
    Add-Content $log "$(Get-Date -Format s) güncellendi: $after"
}
'@
$sshForUpdate = if ($UseSsh) { $SshCmd } else { '' }
$update = $update.Replace('__SSH__', $sshForUpdate).Replace('__GIT__', $GitExe).Replace('__BRANCH__', $Branch).Replace('__CADDY__', $CaddyExe).Replace('__CADDYFILE__', $Caddyfile)
[IO.File]::WriteAllText("$KeyDir\update.ps1", $update, (New-Object System.Text.UTF8Encoding $true))
schtasks /Create /TN 'BSM Mekanik Guncelleme' /SC MINUTE /MO 5 /RU SYSTEM /RL HIGHEST /F `
    /TR "powershell -NoProfile -ExecutionPolicy Bypass -File $KeyDir\update.ps1" | Out-Null
Write-Host '   görev: BSM Mekanik Guncelleme (Görev Zamanlayıcı)'

# --- DNS bilgisi
Say 'DNS durumu'
$hosts = @('bsmmekanik.nesakyazilim.com')
if ($Mode -eq 'domains') { $hosts += 'www.bsmmekanik.com', 'bsmmekanik.com', 'www.bsmmechanical.com', 'bsmmechanical.com' }
foreach ($h in $hosts) {
    try { $ips = (Resolve-DnsName $h -Type A -Server 1.1.1.1 -ErrorAction Stop | Where-Object { $_.IPAddress }).IPAddress -join ', ' }
    catch { $ips = 'kayıt yok' }
    Write-Host "   $h -> $ips"
}

Say 'Bitti'
Write-Host '   Demo: https://bsmmekanik.nesakyazilim.com  (SSL sertifikasını Caddy ilk açılışta alır)'
if ($Mode -eq 'domains') { Write-Host '   Siteler: https://www.bsmmekanik.com  -  https://www.bsmmechanical.com/en/' }
Write-Host "   Güncelleme kaydı: $KeyDir\update.log"
