import subprocess

# ==========================================
# --- OPTIMIZATION LOGIC ---
# ==========================================

def _run_cmd(command):
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        res = subprocess.run(
            ["powershell", "-Command", command], 
            capture_output=True, text=True, startupinfo=startupinfo
        )
        return res.returncode == 0, res.stdout or res.stderr
    except Exception as e:
        return False, str(e)

# --- A. GAMING & LATENCY ---
def optimize_network_latency():
    ps_script = """
    $interfaces = Get-ItemProperty 'HKLM:\System\CurrentControlSet\Services\Tcpip\Parameters\Interfaces\*'
    foreach($i in $interfaces){
        $path = $i.PSPath
        New-ItemProperty -Path $path -Name "TCPNoDelay" -Value 1 -PropertyType DWORD -Force -ErrorAction SilentlyContinue | Out-Null
        New-ItemProperty -Path $path -Name "TcpAckFrequency" -Value 1 -PropertyType DWORD -Force -ErrorAction SilentlyContinue | Out-Null
        New-ItemProperty -Path $path -Name "TcpDelAckTicks" -Value 0 -PropertyType DWORD -Force -ErrorAction SilentlyContinue | Out-Null
    }
    """
    return _run_cmd(ps_script)

def set_gaming_priority():
    return _run_cmd('Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\PriorityControl" -Name "Win32PrioritySeparation" -Value 38 -Type DWord')

def enable_ultimate_performance():
    cmd = """
    $plan = powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61
    $guid = $plan -match '([0-9a-f]{8}-([0-9a-f]{4}-){3}[0-9a-f]{12})' | ForEach-Object { $matches[0] }
    powercfg -setactive $guid
    """
    return _run_cmd(cmd)

def disable_game_bar():
    cmd = """
    Set-ItemProperty -Path "HKCU:\System\GameConfigStore" -Name "GameDVR_Enabled" -Value 0 -Type DWord -Force
    Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\GameDVR" -Name "AllowGameDVR" -Value 0 -Type DWord -Force
    """
    return _run_cmd(cmd)

# --- B. SYSTEM & DEBLOAT ---
def clean_system_junk():
    cmd = """
    Remove-Item -Path "$env:TEMP\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "C:\Windows\Temp\*" -Recurse -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "C:\Windows\Prefetch\*" -Recurse -Force -ErrorAction SilentlyContinue
    Stop-Service -Name wuauserv -Force -ErrorAction SilentlyContinue
    Remove-Item -Path "C:\Windows\SoftwareDistribution\Download\*" -Recurse -Force -ErrorAction SilentlyContinue
    Start-Service -Name wuauserv -ErrorAction SilentlyContinue
    """
    return _run_cmd(cmd)

def uninstall_bloatware():
    cmd = """
    $apps = @("*bing*", "*zune*", "*solitaire*", "*skypeapp*", "*windowsmaps*", "*xboxapp*")
    foreach ($app in $apps) { Get-AppxPackage $app | Remove-AppxPackage -ErrorAction SilentlyContinue }
    """
    return _run_cmd(cmd)

def disable_cortana():
    return _run_cmd('New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows\Windows Search" -Name "AllowCortana" -Value 0 -PropertyType DWORD -Force')

def disable_background_apps():
    return _run_cmd('New-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\BackgroundAccessApplications" -Name "GlobalUserDisabled" -Value 1 -PropertyType DWORD -Force')

# --- C. SERVICES & PERFORMANCE ---
def disable_telemetry_services():
    cmd = """
    Stop-Service -Name "DiagTrack" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "DiagTrack" -StartupType Disabled -ErrorAction SilentlyContinue
    """
    return _run_cmd(cmd)

def disable_sysmain():
    cmd = """
    Stop-Service -Name "SysMain" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "SysMain" -StartupType Disabled -ErrorAction SilentlyContinue
    """
    return _run_cmd(cmd)

def optimize_search_indexing():
    cmd = """
    Stop-Service -Name "WSearch" -Force -ErrorAction SilentlyContinue
    Set-Service -Name "WSearch" -StartupType Disabled -ErrorAction SilentlyContinue
    """
    return _run_cmd(cmd)

# --- D. VISUALS ---
def disable_windows_animations():
    cmd = """
    Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "UserPreferencesMask" -Value ([byte[]](0x90,0x12,0x03,0x80,0x10,0x00,0x00,0x00)) -Type Binary -Force
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" -Name "VisualFXSetting" -Value 2 -Type DWord -Force
    """
    return _run_cmd(cmd)

def disable_transparency():
    return _run_cmd('Set-ItemProperty -Path "HKCU:\SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize" -Name "EnableTransparency" -Value 0 -Type DWord -Force')

def disable_smooth_scrolling():
    return _run_cmd('Set-ItemProperty -Path "HKCU:\Control Panel\Desktop" -Name "SmoothScroll" -Value 0 -Type DWord -Force')

# --- E. NETWORK & LOGS ---
def flush_dns():
    return _run_cmd("ipconfig /flushdns")

def clear_event_logs():
    return _run_cmd('wevtutil el | Foreach-Object {wevtutil cl "$_"}')

# --- F. USELESS SERVICES (NEW) ---
def disable_print_spooler():
    """Desativa fila de impressão (inútil se não tem impressora)"""
    return _run_cmd('Stop-Service -Name "Spooler" -Force -ErrorAction SilentlyContinue; Set-Service -Name "Spooler" -StartupType Disabled -ErrorAction SilentlyContinue')

def disable_error_reporting():
    """Desativa Windows Error Reporting (Famoso popup de erro que trava o app tentando enviar pra Microsoft)"""
    return _run_cmd('Stop-Service -Name "WerSvc" -Force -ErrorAction SilentlyContinue; Set-Service -Name "WerSvc" -StartupType Disabled -ErrorAction SilentlyContinue')

def disable_maps_broker():
    """Desativa Downloaded Maps Manager"""
    return _run_cmd('Stop-Service -Name "MapsBroker" -Force -ErrorAction SilentlyContinue; Set-Service -Name "MapsBroker" -StartupType Disabled -ErrorAction SilentlyContinue')

def disable_tracking_client():
    """Desativa Distributed Link Tracking Client (Usa muito disco em NTFS)"""
    return _run_cmd('Stop-Service -Name "TrkWks" -Force -ErrorAction SilentlyContinue; Set-Service -Name "TrkWks" -StartupType Disabled -ErrorAction SilentlyContinue')

def disable_push_notifications():
    """Desativa Windows Push Notifications (Bandeira de notificações inútil)"""
    return _run_cmd('Stop-Service -Name "WpnService" -Force -ErrorAction SilentlyContinue; Set-Service -Name "WpnService" -StartupType Disabled -ErrorAction SilentlyContinue')
