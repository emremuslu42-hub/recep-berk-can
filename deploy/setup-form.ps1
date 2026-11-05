# BSM Mekanik - teklif formu alıcısının Windows sunucuya kurulumu
#
# Önce setup-windows.ps1 ile site kurulmuş olmalı (C:\bsmmekanik, Caddy).
# Kullanım (Yönetici olarak açılmış PowerShell'de):
#   powershell -ExecutionPolicy Bypass -File C:\bsmmekanik\deploy\setup-form.ps1
#
# Yaptıkları: gönderen Google Workspace hesabını ve uygulama şifresini sorar, C:\bsmmekanik-key\form.json'a
# yazar (yalnızca Yönetici/SYSTEM okuyabilir), deneme e-postası gönderir, form alıcıyı sunucu açılışında
# otomatik başlayan bir görev olarak kurar ve Caddy'yi yeniden yükler. Tekrar çalıştırılabilir
# (ör. şifre değişince).

param(
    [string]$To = 'mert@bsmmechanical.com',
    [string]$Account = '',   # uygulama şifresinin ait olduğu Google Workspace hesabı
    [string]$From = ''       # gönderen adresi (hesabın kendisi ya da onun takma adı, ör. bildirim@)
)

$ErrorActionPreference = 'Stop'
$AppDir  = 'C:\bsmmekanik'
$KeyDir  = 'C:\bsmmekanik-key'
$Config  = "$KeyDir\form.json"
$Runner  = "$KeyDir\form-runner.ps1"
$LogFile = "$KeyDir\form.log"
$Server  = "$AppDir\deploy\form-server\server.js"
$Task    = 'BSM Mekanik Form'
$Utf8    = New-Object System.Text.UTF8Encoding $false

function Say($m)  { Write-Host "`n==> $m" -ForegroundColor Cyan }
function Die($m)  { Write-Host "`nHATA: $m" -ForegroundColor Red; exit 1 }

$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $admin) { Die 'PowerShell''i "Yönetici olarak çalıştır" ile açıp tekrar deneyin.' }

# --- Siteyi en güncel sürüme çek
Say 'Site dosyaları güncelleniyor'
if (Test-Path "$KeyDir\update.ps1") { & powershell -NoProfile -ExecutionPolicy Bypass -File "$KeyDir\update.ps1" }
if (-not (Test-Path $Server)) { Die "Form alıcı bulunamadı: $Server. Önce setup-windows.ps1 ile siteyi kurun." }

# --- Node.js
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) { Die 'Node.js bulunamadı (node -v çalışmıyor).' }
$Node = $nodeCmd.Source
Write-Host "   node: $Node ($(& $Node -v))"

# --- Gönderen hesap ve uygulama şifresi
Say 'E-posta gönderim hesabı'
if (-not $Account) {
    $Account = Read-Host 'Giriş yapılacak Google Workspace hesabı [iletisim@nesakyazilim.com]'
    if (-not $Account) { $Account = 'iletisim@nesakyazilim.com' }
}
if (-not $From) {
    $From = Read-Host "Gönderen adresi (bu hesap ya da takma adı, ör. bildirim@nesakyazilim.com) [$Account]"
    if (-not $From) { $From = $Account }
}
$sec = Read-Host "$Account hesabının 16 haneli uygulama şifresi (yazarken görünmez)" -AsSecureString
$bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($sec)
try { $pass = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr) } finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr) }
$pass = ($pass -replace '\s', '')
if ($pass.Length -lt 8) { Die 'Uygulama şifresi boş ya da çok kısa görünüyor.' }

if (-not (Test-Path $KeyDir)) { New-Item -ItemType Directory -Path $KeyDir | Out-Null }
icacls $KeyDir /inheritance:r /grant:r 'Administrators:(OI)(CI)F' 'SYSTEM:(OI)(CI)F' | Out-Null
$cfg = [ordered]@{
    smtpHost = 'smtp.gmail.com'; smtpPort = 465
    smtpUser = $Account; smtpPass = $pass
    from = $From; fromName = 'BSM Mekanik Web Sitesi'
    to = $To; port = 8787
}
[IO.File]::WriteAllText($Config, ($cfg | ConvertTo-Json), $Utf8)
$pass = $null
Write-Host "   ayarlar kaydedildi: $Config (yalnızca Yönetici/SYSTEM erişebilir)"
Write-Host "   hesap: $Account   gönderen: $From  ->  alıcı: $To"

# --- Deneme e-postası
Say "Deneme e-postası gönderiliyor ($To)"
$env:BSM_FORM_CONFIG = $Config
$ErrorActionPreference = 'Continue'
& $Node $Server --test
$testCode = $LASTEXITCODE
$ErrorActionPreference = 'Stop'
if ($testCode -ne 0) {
    Write-Host ''
    Write-Host 'Olası sebepler:' -ForegroundColor Yellow
    Write-Host '  - Uygulama şifresi yanlış kopyalandı (boşluklar önemli değil, harfler önemli)'
    Write-Host '  - Bu hesapta 2 Adımlı Doğrulama açık değil / uygulama şifresi o hesaba ait değil'
    Write-Host '  - Sunucudan dışarıya 465 portu kapalı (güvenlik duvarı)'
    Write-Host '  - Gönderen adresi takma adsa: Gmail > Ayarlar > Hesaplar > Farklı bir adresten posta gönder kısmına eklenmeli'
    Die 'Deneme e-postası gönderilemedi. Betiği düzeltip tekrar çalıştırın.'
}

# --- Çalıştırıcı (kapanırsa 5 sn sonra yeniden başlatır; server.js güncellenince yeni sürüme geçer)
Say 'Form alıcı hizmeti kuruluyor'
$runnerText = @'
$env:BSM_FORM_CONFIG = '__CONFIG__'
while ($true) {
    if ((Test-Path '__LOG__') -and ((Get-Item '__LOG__').Length -gt 5MB)) { Move-Item '__LOG__' '__LOG__.1' -Force }
    & '__NODE__' '__SERVER__' *>> '__LOG__'
    Start-Sleep -Seconds 5
}
'@
$runnerText = $runnerText.Replace('__CONFIG__', $Config).Replace('__LOG__', $LogFile).Replace('__NODE__', $Node).Replace('__SERVER__', $Server)
[IO.File]::WriteAllText($Runner, $runnerText, (New-Object System.Text.UTF8Encoding $true))

if (Get-ScheduledTask -TaskName $Task -ErrorAction SilentlyContinue) {
    Stop-ScheduledTask -TaskName $Task -ErrorAction SilentlyContinue
    Unregister-ScheduledTask -TaskName $Task -Confirm:$false
}
# Eski çalıştırıcıdan kalan node süreçlerini kapat (yalnızca bu form alıcı)
Get-CimInstance Win32_Process -Filter "Name='node.exe'" | Where-Object { $_.CommandLine -like '*form-server*server.js*' } |
    ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }

$action    = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$Runner`""
$trigger   = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId 'SYSTEM' -LogonType ServiceAccount -RunLevel Highest
$settings  = New-ScheduledTaskSettingsSet -ExecutionTimeLimit ([TimeSpan]::Zero) -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName $Task -Action $action -Trigger $trigger -Principal $principal -Settings $settings | Out-Null
Start-ScheduledTask -TaskName $Task
Write-Host "   görev: $Task (sunucu açılışında otomatik başlar)"

# --- Sağlık kontrolü
$ok = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 1
    try {
        $r = Invoke-WebRequest -Uri 'http://127.0.0.1:8787/api/teklif/saglik' -UseBasicParsing -TimeoutSec 3
        if ($r.StatusCode -eq 200) { $ok = $true; break }
    } catch { }
}
if (-not $ok) { Die "Form alıcı başlamadı. Kayıt: $LogFile" }
Write-Host '   form alıcı çalışıyor (127.0.0.1:8787)'

# --- Caddy'yi yeniden yükle (/api/teklif yönlendirmesi)
Say 'Caddy yeniden yükleniyor'
$proc = Get-CimInstance Win32_Process -Filter "Name='caddy.exe'" | Select-Object -First 1
if ($proc) {
    $caddyfile = $null
    if ($proc.CommandLine -match '--config[ =]+"([^"]+)"') { $caddyfile = $Matches[1] }
    elseif ($proc.CommandLine -match '--config[ =]+(\S+)') { $caddyfile = $Matches[1] }
    if ($caddyfile) {
        $ErrorActionPreference = 'Continue'
        & $proc.ExecutablePath reload --config $caddyfile --adapter caddyfile 2>&1 | Out-Null
        $ErrorActionPreference = 'Stop'
    }
}

# --- Dışarıdan kontrol
foreach ($h in 'https://www.bsmmekanik.com', 'https://bsmmekanik.nesakyazilim.com') {
    try {
        $r = Invoke-WebRequest -Uri "$h/api/teklif/saglik" -UseBasicParsing -TimeoutSec 10
        Write-Host "   $h/api/teklif -> $($r.StatusCode)"
    } catch { Write-Host "   $h/api/teklif -> ulaşılamadı ($($_.Exception.Message))" -ForegroundColor Yellow }
}

Say 'Bitti'
Write-Host "   $To adresine bir deneme e-postası gönderildi; gelen kutusunu (ve spam klasörünü) kontrol edin."
Write-Host "   Form kayıtları: $LogFile"
