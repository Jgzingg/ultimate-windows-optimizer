import subprocess
import os
import datetime

# ==========================================
# --- BACKUP LOGIC ---
# ==========================================

BACKUP_DIR = os.path.join(os.environ['USERPROFILE'], "Documents", "UltimateOptimizerBackups")

def ensure_backup_dir():
    """Garante que a pasta de backups exista."""
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def create_restore_point():
    """
    Cria um ponto de restauração do Windows.
    Precisa rodar como Admin. Retorna True se der bom, False se der ruim.
    """
    print("Iniciando criação do Ponto de Restauração (System Restore Point)...")
    ps_cmd = (
        'Enable-ComputerRestore -Drive "C:\"; '
        'Checkpoint-Computer -Description "UltOpt_Backup" -RestorePointType "MODIFY_SETTINGS"'
    )
    
    try:
        # Usa startupinfo pra não piscar janela preta do CMD
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        
        # force powershell to run command
        res = subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True, text=True, startupinfo=startupinfo
        )
        
        if res.returncode == 0:
            print("Ponto de restauração criado com sucesso!")
            return True, "Ponto de Restauração criado."
        else:
            # muitas vezes falha se o cara rodou um recentemente (cooldown de 24h)
            print(f"Erro ao criar ponto: {res.stderr}")
            return False, f"Falha (Cooldown ou erro?): {res.stderr[:50]}"
            
    except Exception as e:
        return False, str(e)

def export_registry(key_path, filename="backup.reg"):
    """Exporta uma chave específica do registro antes da gente mexer nela."""
    ensure_backup_dir()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    full_path = os.path.join(BACKUP_DIR, f"{timestamp}_{filename}")
    
    # ex: reg export HKLM\System\CurrentControlSet\Control\Session Manager\Memory Management C:\backup.reg /y
    cmd = f'reg export "{key_path}" "{full_path}" /y'
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(cmd, shell=True, startupinfo=startupinfo, check=True)
        return True, full_path
    except subprocess.CalledProcessError:
        return False, None

def import_registry(filepath):
    """Restaura as chaves a partir de um .reg (Botão de Undo)"""
    if not os.path.exists(filepath):
        return False, "Arquivo não encontrado."
        
    cmd = f'reg import "{filepath}"'
    try:
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(cmd, shell=True, startupinfo=startupinfo, check=True)
        return True, "Restaurado com sucesso."
    except subprocess.CalledProcessError as e:
        return False, f"Erro ao restaurar: {e}"

def backup_system():
    """Rotina completa de backup chamada antes de qualquer otimização perigosa."""
    # 1. Ponto de restauração
    rp_success, rp_msg = create_restore_point()
    
    # 2. Backup de chaves criticas comuns que a gente altera
    # (Poderia iterar sobre uma lista dependendo do módulo, mas vou focar no global primeiro)
    keys_to_backup = [
        r"HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Multimedia\SystemProfile",
        r"HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management"
    ]
    
    reg_status = []
    for k in keys_to_backup:
        safename = k.split("\\")[-1] + ".reg"
        success, path = export_registry(k, safename)
        reg_status.append(success)
        
    all_regs_ok = all(reg_status)
    
    if rp_success and all_regs_ok:
        return True, "Backup Completo (Restore Point + Registry) realizado com sucesso!"
    elif all_regs_ok:
        return True, "Aviso: Apenas Backup de Registro concluído. (Restore Point falhou/cooldown)."
    else:
        return False, "Falha crítica ao realizar backups."
