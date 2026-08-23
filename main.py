import sys
import os

# Adiciona o diretório raiz no path pra não bugar os imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.utils import run_as_admin
from ui.app import UltimateOptimizerApp

if __name__ == "__main__":
    # Garante que roda como admin, senão os tweaks vão ser bloqueados
    if run_as_admin():
        app = UltimateOptimizerApp()
        app.mainloop()
