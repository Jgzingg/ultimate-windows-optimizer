import customtkinter as ctk
import threading
import time

from core.utils import get_system_stats
from core.backup_manager import backup_system
from core import optimizer

BG_COLOR = "#1e1e2e"
SIDEBAR_COLOR = "#181825"
ACCENT_COLOR = "#89b4fa"
CARD_COLOR = "#313244"
TEXT_COLOR = "#cdd6f4"
MUTED_TEXT = "#a6adc8"

ctk.set_appearance_mode("Dark")

class UltimateOptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Ultimate Windows Optimizer")
        self.geometry("1050x750")
        self.resizable(False, False)
        self.configure(fg_color=BG_COLOR)
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # --- SIDEBAR ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=SIDEBAR_COLOR)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(9, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="⚡ UltOpt", font=ctk.CTkFont(family="Segoe UI Variable Display", size=32, weight="bold"), text_color=ACCENT_COLOR)
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 40))
        
        self.nav_buttons = {}
        self.current_tab = "Dashboard"
        
        self.btn_dash = self.create_nav_button("Dashboard", 1)
        self.btn_gaming = self.create_nav_button("Gaming & Latência", 2)
        self.btn_system = self.create_nav_button("Sistema", 3)
        self.btn_services = self.create_nav_button("Serviços Inúteis", 4)
        self.btn_visuals = self.create_nav_button("Visuais & UI", 5)
        self.btn_network = self.create_nav_button("Rede & Limpeza", 6)
        self.btn_backup = self.create_nav_button("Backup / Restore", 7)
        
        # --- MAIN CONTAINER ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=30, pady=30)
        
        self.frames = {
            "Dashboard": DashboardFrame(self.main_container, self),
            "Gaming & Latência": GamingFrame(self.main_container),
            "Sistema": SystemFrame(self.main_container),
            "Serviços Inúteis": ServicesFrame(self.main_container),
            "Visuais & UI": VisualsFrame(self.main_container),
            "Rede & Limpeza": NetworkFrame(self.main_container),
            "Backup / Restore": BackupFrame(self.main_container)
        }
        
        for f in self.frames.values():
            f.place(relx=1.5, rely=0, relwidth=1, relheight=1)
            
        self._set_active_button("Dashboard")
        self.frames["Dashboard"].place(relx=0, rely=0) 
        self.is_animating = False

    def create_nav_button(self, text, row):
        btn = ctk.CTkButton(self.sidebar, text=text, height=45, corner_radius=8,
                            fg_color="transparent", text_color=MUTED_TEXT, 
                            hover_color=CARD_COLOR, anchor="w", 
                            font=ctk.CTkFont(family="Segoe UI Variable Text", size=15, weight="bold"),
                            command=lambda t=text: self.switch_tab(t))
        btn.grid(row=row, column=0, padx=15, pady=8, sticky="ew")
        self.nav_buttons[text] = btn
        return btn

    def _set_active_button(self, active_name):
        for name, btn in self.nav_buttons.items():
            if name == active_name:
                btn.configure(fg_color=CARD_COLOR, text_color=ACCENT_COLOR)
            else:
                btn.configure(fg_color="transparent", text_color=MUTED_TEXT)

    def switch_tab(self, new_tab):
        if self.current_tab == new_tab or self.is_animating:
            return
            
        self._set_active_button(new_tab)
        old_frame = self.frames[self.current_tab]
        new_frame = self.frames[new_tab]
        
        self.current_tab = new_tab
        self.is_animating = True
        
        new_frame.place(relx=1.2, rely=0, relwidth=1, relheight=1)
        threading.Thread(target=self._animate_slide, args=(old_frame, new_frame), daemon=True).start()

    def _animate_slide(self, old_frame, new_frame):
        steps = 25
        delay = 0.008
        for i in range(steps):
            progress = (i + 1) / steps
            current_old_x = 0 - (1.2 * progress)
            current_new_x = 1.2 - (1.2 * progress)
            
            self.after(0, lambda o=old_frame, ox=current_old_x: o.place(relx=ox))
            self.after(0, lambda n=new_frame, nx=current_new_x: n.place(relx=nx))
            time.sleep(delay)
            
        self.after(0, old_frame.place_forget)
        self.after(0, lambda: setattr(self, 'is_animating', False))


# ==========================================
# --- TAB COMPONENTS ---
# ==========================================

class TitleHeader(ctk.CTkFrame):
    def __init__(self, master, title, subtitle=""):
        super().__init__(master, fg_color="transparent")
        lbl_title = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(family="Segoe UI Variable Display", size=36, weight="bold"), text_color=TEXT_COLOR)
        lbl_title.pack(anchor="w", pady=(0, 5))
        if subtitle:
            lbl_desc = ctk.CTkLabel(self, text=subtitle, font=ctk.CTkFont(family="Segoe UI Variable Text", size=14), text_color=MUTED_TEXT, justify="left")
            lbl_desc.pack(anchor="w", pady=(0, 20))

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, app_root):
        super().__init__(master, fg_color="transparent")
        self.app_root = app_root
        
        self.header = TitleHeader(self, "Dashboard", "Visão geral do seu sistema e otimização em 1-clique.")
        self.header.pack(fill="x")
        
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", pady=20)
        self.stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.cpu_card = ctk.CTkFrame(self.stats_frame, fg_color=CARD_COLOR, corner_radius=15, height=120)
        self.cpu_card.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.cpu_card.grid_propagate(False)
        ctk.CTkLabel(self.cpu_card, text="Uso de CPU", font=ctk.CTkFont(size=14), text_color=MUTED_TEXT).place(relx=0.1, rely=0.2)
        self.cpu_val = ctk.CTkLabel(self.cpu_card, text="--%", font=ctk.CTkFont(size=38, weight="bold"), text_color=ACCENT_COLOR)
        self.cpu_val.place(relx=0.1, rely=0.45)
        
        self.ram_card = ctk.CTkFrame(self.stats_frame, fg_color=CARD_COLOR, corner_radius=15, height=120)
        self.ram_card.grid(row=0, column=1, padx=(10, 0), sticky="ew")
        self.ram_card.grid_propagate(False)
        ctk.CTkLabel(self.ram_card, text="Uso de RAM", font=ctk.CTkFont(size=14), text_color=MUTED_TEXT).place(relx=0.1, rely=0.2)
        self.ram_val = ctk.CTkLabel(self.ram_card, text="--%", font=ctk.CTkFont(size=38, weight="bold"), text_color=ACCENT_COLOR)
        self.ram_val.place(relx=0.1, rely=0.45)
        
        self.btn_quick = ctk.CTkButton(self, text="⚡ INICIAR OTIMIZAÇÃO EXTREMA", 
                                       font=ctk.CTkFont(size=22, weight="bold"), height=80, corner_radius=15,
                                       command=self.do_quick_opt, fg_color=ACCENT_COLOR, text_color=BG_COLOR, hover_color="#749bed")
        self.btn_quick.pack(pady=40, fill="x")
        
        self.progress = ctk.CTkProgressBar(self, height=10, progress_color=ACCENT_COLOR, fg_color=CARD_COLOR)
        self.progress.set(0)
        self.lbl_status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_status.pack()
        
        self.update_stats()

    def update_stats(self):
        stats = get_system_stats()
        self.cpu_val.configure(text=f"{stats['cpu']}%")
        self.ram_val.configure(text=f"{stats['ram']}%")
        self.after(1500, self.update_stats)

    def do_quick_opt(self):
        self.btn_quick.configure(state="disabled", text="APLICANDO OTIMIZAÇÕES...")
        self.progress.pack(pady=10, fill="x")
        self.progress.start()
        threading.Thread(target=self._run_quick_opt, daemon=True).start()

    def _run_quick_opt(self):
        self.lbl_status.configure(text="Fazendo backup de segurança...", text_color="#f9e2af")
        success, msg = backup_system()
        if not success:
            self.lbl_status.configure(text=f"Falha no backup: {msg}", text_color="#f38ba8")
            self._reset_ui()
            return
            
        self.lbl_status.configure(text="Aplicando tweaks base...", text_color="#f9e2af")
        optimizer.clean_system_junk()
        optimizer.disable_telemetry_services()
        optimizer.optimize_network_latency()
        optimizer.flush_dns()
        
        self.lbl_status.configure(text="SISTEMA OTIMIZADO COM SUCESSO! 🚀", text_color="#a6e3a1")
        self._reset_ui()

    def _reset_ui(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.btn_quick.configure(state="normal", text="⚡ INICIAR OTIMIZAÇÃO EXTREMA")


class BaseTweakFrame(ctk.CTkFrame):
    def __init__(self, master, title, desc=""):
        super().__init__(master, fg_color="transparent")
        
        self.header = TitleHeader(self, title, desc)
        self.header.pack(fill="x")
        
        self.switches = []
        
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent", scrollbar_button_color=CARD_COLOR, scrollbar_button_hover_color=ACCENT_COLOR)
        self.scroll.pack(fill="both", expand=True, pady=10)

        self.footer = ctk.CTkFrame(self, fg_color="transparent", height=80)
        self.footer.pack(fill="x", side="bottom")
        
        self.lbl_status = ctk.CTkLabel(self.footer, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.lbl_status.pack(side="left", padx=10)

        # Botão de Ativar Todos
        self.btn_select_all = ctk.CTkButton(self.footer, text="Marcar Todos", command=self.select_all,
                                            height=45, corner_radius=10, font=ctk.CTkFont(size=15, weight="bold"),
                                            fg_color=CARD_COLOR, text_color=TEXT_COLOR, hover_color="#45475a")
        self.btn_select_all.pack(side="right", padx=(10, 0))

        self.btn_apply = ctk.CTkButton(self.footer, text="Aplicar Selecionados", command=self.apply_tweaks, 
                                       height=45, corner_radius=10, font=ctk.CTkFont(size=15, weight="bold"),
                                       fg_color=ACCENT_COLOR, text_color=BG_COLOR, hover_color="#749bed")
        self.btn_apply.pack(side="right", padx=10)

    def select_all(self):
        """Ativa todos os switches desta aba de uma vez."""
        for var, _ in self.switches:
            var.set(True)

    def add_option(self, title, desc, func):
        card = ctk.CTkFrame(self.scroll, fg_color=CARD_COLOR, corner_radius=12)
        card.pack(fill="x", pady=8, ipady=5)
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        
        lbl_title = ctk.CTkLabel(info_frame, text=title, font=ctk.CTkFont(size=16, weight="bold"), text_color=TEXT_COLOR)
        lbl_title.pack(anchor="w")
        
        lbl_desc = ctk.CTkLabel(info_frame, text=desc, font=ctk.CTkFont(size=13), text_color=MUTED_TEXT, justify="left")
        lbl_desc.pack(anchor="w")
        
        var = ctk.BooleanVar(value=False)
        switch = ctk.CTkSwitch(card, text="", variable=var, progress_color=ACCENT_COLOR, button_color=TEXT_COLOR, button_hover_color="#fff")
        switch.pack(side="right", padx=20)
        
        self.switches.append((var, func))

    def apply_tweaks(self):
        if not any(var.get() for var, _ in self.switches):
            self.lbl_status.configure(text="Selecione ao menos um!", text_color="#f9e2af")
            return
            
        self.btn_apply.configure(state="disabled")
        self.lbl_status.configure(text="Gerando backup de segurança...", text_color="#f9e2af")
        threading.Thread(target=self._run_tweaks, daemon=True).start()

    def _run_tweaks(self):
        ok, msg = backup_system()
        if not ok:
            self.lbl_status.configure(text=f"Abortado: Falha Backup: {msg}", text_color="#f38ba8")
            self.btn_apply.configure(state="normal")
            return
            
        self.lbl_status.configure(text="Injetando tweaks...", text_color="#f9e2af")
        
        errors = 0
        for var, func in self.switches:
            if var.get():
                success, out = func()
                if not success:
                    errors += 1
                    
        if errors > 0:
            self.lbl_status.configure(text=f"Concluído com {errors} erro(s).", text_color="#fab387")
        else:
            self.lbl_status.configure(text="Tweaks aplicados! 🚀", text_color="#a6e3a1")
            
        self.btn_apply.configure(state="normal")


# Abas Herdeiras
class GamingFrame(BaseTweakFrame):
    def __init__(self, master):
        super().__init__(master, "Gaming & Latência", "Otimizações severas no stack TCP e priorização de Threads.")
        self.add_option("TCP NoDelay (Nagle's)", "Desativa Nagle's algorithm no registro TCP/IP. Reduz o ping em jogos.", optimizer.optimize_network_latency)
        self.add_option("Win32PrioritySeparation", "Foca recursos de CPU 100% no jogo em primeiro plano.", optimizer.set_gaming_priority)
        self.add_option("Ultimate Performance", "Aplica o plano de energia oculto da Microsoft.", optimizer.enable_ultimate_performance)
        self.add_option("Kill Xbox Game Bar", "Mata serviços de Game DVR que gravam a tela em background.", optimizer.disable_game_bar)

class SystemFrame(BaseTweakFrame):
    def __init__(self, master):
        super().__init__(master, "Sistema Geral", "Remova o peso morto da inicialização.")
        self.add_option("Desinstalar Bloatwares", "Remove a força apps nativos inúteis (Cortana, Bing, etc).", optimizer.uninstall_bloatware)
        self.add_option("Bloquear Telemetria", "Desativa o DiagTrack espiões de diagnóstico do Windows.", optimizer.disable_telemetry_services)
        self.add_option("Morte aos UWP", "Impede que qualquer aplicativo da loja rode em background.", optimizer.disable_background_apps)
        self.add_option("Desativar SysMain (Superfetch)", "Previne uso de 100% do Disco/SSD em cacheamento.", optimizer.disable_sysmain)
        self.add_option("Windows Search Indexer", "Pausa o escaneamento constante de arquivos.", optimizer.optimize_search_indexing)

class ServicesFrame(BaseTweakFrame):
    def __init__(self, master):
        super().__init__(master, "Serviços Inúteis", "Pare serviços ocultos do Windows que comem recursos à toa. Selecione todos para máxima performance.")
        self.add_option("Print Spooler (Fila de Impressão)", "Desative se você NÃO USA impressora. Economiza RAM.", optimizer.disable_print_spooler)
        self.add_option("Windows Error Reporting", "Mata o serviço que tenta enviar logs de erro pra Microsoft toda vez que algo trava.", optimizer.disable_error_reporting)
        self.add_option("Downloaded Maps Manager", "Você usa o app nativo de mapas do Windows? Não? Então desative isso (MapsBroker).", optimizer.disable_maps_broker)
        self.add_option("Distributed Link Tracking", "Usado para rastrear atalhos quebrados em redes corporativas (TrkWks). Muito inútil e consome disco.", optimizer.disable_tracking_client)
        self.add_option("Windows Push Notifications", "Mata o WpnService, aliviando CPU se você não liga pras notificações irritantes do canto da tela.", optimizer.disable_push_notifications)

class VisualsFrame(BaseTweakFrame):
    def __init__(self, master):
        super().__init__(master, "Visuais & UI", "Sacrifique firulas visuais por renderização instantânea.")
        self.add_option("Matar Animações", "Janelas fecham/abrem em 0ms. Navegação ultra rápida.", optimizer.disable_windows_animations)
        self.add_option("Desativar Transparência", "Remove o efeito de vidro/Mica. Alivia processos da GPU.", optimizer.disable_transparency)
        self.add_option("Smooth Scrolling Off", "Desativa a aceleração na rolagem de listas e web.", optimizer.disable_smooth_scrolling)

class NetworkFrame(BaseTweakFrame):
    def __init__(self, master):
        super().__init__(master, "Rede & Limpeza", "Faxina em caches esquecidos pelo SO.")
        self.add_option("Deep System Clean", "Deleta .tmp, Prefetch e limpa o cache do Windows Update.", optimizer.clean_system_junk)
        self.add_option("DNS Flush", "Renova rotas antigas de internet.", optimizer.flush_dns)
        self.add_option("Wipe Event Logs", "Limpa logs de erros inúteis acumulados pelo Windows.", optimizer.clear_event_logs)

class BackupFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.header = TitleHeader(self, "Backup & Restore", "Você fez merda? Volte no tempo.")
        self.header.pack(fill="x")
        
        self.card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=15)
        self.card.pack(fill="x", pady=20, ipady=30)
        
        lbl = ctk.CTkLabel(self.card, text="Ponto de Restauração (System Restore)", font=ctk.CTkFont(size=22, weight="bold"), text_color=TEXT_COLOR)
        lbl.pack(pady=(0, 10))
        
        desc = ctk.CTkLabel(self.card, text="O UltOpt cria automaticamente um backup seguro antes de qualquer ação.\nSe um jogo parar de abrir ou a internet bugar, clique abaixo e restaure o PC.", font=ctk.CTkFont(size=14), text_color=MUTED_TEXT, justify="center")
        desc.pack(pady=(0, 30))
        
        self.btn_restore = ctk.CTkButton(self.card, text="Abrir Painel de Restauração Nativo", 
                                         font=ctk.CTkFont(size=16, weight="bold"), height=55, width=300,
                                         fg_color="#f38ba8", text_color="#11111b", hover_color="#eba0ac",
                                         command=self.open_sys_restore)
        self.btn_restore.pack()
        self.lbl_status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.lbl_status.pack(pady=20)

    def open_sys_restore(self):
        try:
            import subprocess
            subprocess.Popen("rstrui.exe")
        except Exception as e:
            self.lbl_status.configure(text=f"Erro: {e}", text_color="#f38ba8")
