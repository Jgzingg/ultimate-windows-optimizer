import ctypes
import sys
import psutil

# ==========================================
# --- ADMIN & PRIVILEGES ---
# ==========================================

def is_admin():
    """Checa se o script tá rodando com privilégios de admin."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Força o prompt do UAC e reinicia o script como Admin, se precisar."""
    if is_admin():
        return True
    
    print("Pedindo permissão de Administrador...")
    # workaround pra não bugar argumentos de linha de comando
    script = sys.argv[0]
    params = ' '.join(sys.argv[1:])
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        sys.exit() # mata o processo antigo
    except Exception as e:
        print(f"Falha ao escalar privilégios: {e}")
        return False

# ==========================================
# --- SYSTEM INFO ---
# ==========================================

def get_system_stats():
    """Pega uso de CPU e RAM pra mostrar no dashboard."""
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent
    return {"cpu": cpu, "ram": ram}
