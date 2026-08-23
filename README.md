# ⚡ Ultimate Windows Optimizer (UltOpt)

![GitHub License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

O **Ultimate Windows Optimizer** é uma ferramenta de código aberto construída em Python (CustomTkinter) focada em entregar **performance extrema** para usuários de Windows, Gamers e Desenvolvedores. 

O projeto conta com um design moderno (Dark Mode, Fluent UI estilo Catppuccin) e uma arquitetura estritamente voltada para **segurança em primeiro lugar**. Esqueça os otimizadores que destroem o seu sistema; aqui você tem controle e segurança total.

![UltOpt Screenshot Placeholder](https://via.placeholder.com/800x450.png?text=Ultimate+Windows+Optimizer+-+Interface)

## 🚀 Funcionalidades

O projeto é dividido em módulos de otimização agressiva (via injeção segura de comandos PowerShell e edição profunda de Registry):

- **Gaming & Latência:** 
  - Desativa o algoritmo de Nagle (TCP NoDelay) para redução brutal de ping/input lag.
  - Ajuste de `Win32PrioritySeparation` para prioridade absoluta em foreground (jogos).
  - Morte do Game Bar & Game DVR (que drenam FPS em background).
  - Desbloqueio e ativação do plano de energia *Ultimate Performance*.
- **Serviços Inúteis (NOVO):**
  - Desativação limpa de serviços assassinos de performance: Print Spooler, Windows Error Reporting, MapsBroker, Tracking Client, e Push Notifications.
  - Botão de **Marcar Todos** para quem quer a faca nos dentes.
- **Sistema Geral & Bloatware:** 
  - Desativação do SysMain/Superfetch e Windows Search (salva 100% de uso de disco no gerenciador).
  - Remoção forçada de Bloatware (Zune, Bing, XboxApp).
  - Morte da Cortana e bloqueio de apps UWP rodando "fantasma" em background.
- **Visuais (UI Debloat):** 
  - Desativação de TODAS as animações de janela (navegação em 0ms).
  - Remoção de efeitos de transparência/Mica/Acrílico (alivia uso do DWM na GPU).
  - Corte do Smooth Scrolling (rolagem seca e imediata).
- **Rede & Limpeza:** 
  - Faxina de baixo nível (`Temp`, `Prefetch`, `SoftwareDistribution`).
  - Flush DNS e limpeza de Gigabytes de Event Logs do Windows via `wevtutil`.

## 🛡️ Safety First (O Nosso Diferencial)

A maioria dos scripts .bat no YouTube quebram o seu Windows. Nós fazemos diferente:
Antes de injetar QUALQUER Tweak, o UltOpt **força** a criação de um Ponto de Restauração (System Restore Point). Se um jogo parar de abrir ou a rede der B.O., basta ir na aba **Backup / Restore** e clicar em "Restauração do Sistema" para voltar no tempo em 2 minutos.

## 🛠️ Como Instalar e Executar

### Requisitos:
- Windows 10 ou 11
- Python 3.8+

### Rodando localmente:
```bash
git clone https://github.com/SeuUsuario/ultimate-windows-optimizer.git
cd ultimate-windows-optimizer
pip install -r requirements.txt
python main.py
```
*(Ao rodar o `main.py`, ele solicitará permissão de Administrador via UAC para acessar as chaves de registro. Isso é normal e obrigatório para o funcionamento).*

## 🏗️ Estrutura do Código (Arquitetura)

Mantemos a casa limpa. O código é modularizado para que novos scripts possam ser adicionados em segundos.

- `core/optimizer.py` -> Contém a lógica de backend (PowerShell/CMD/Registry). Aqui fica toda a parte de sysadmin.
- `core/backup_manager.py` -> Gerencia os checkpoints de segurança do SO.
- `core/utils.py` -> Escalada de privilégios via `ctypes` e métricas de psutil.
- `ui/app.py` -> A interface em si. Usa orientação a objetos, engine própria de transição (deslize de abas) e `customtkinter`.
- `main.py` -> Entry point blindado.

## 🤝 Como contribuir (Pull Requests)

Você manja de Windows Internals? Descobriu uma chave secreta no regedit que dá 5 FPS a mais no CS2? Abre um PR!

1. Faça o Fork
2. Crie sua Feature Branch (`git checkout -b feature/SuperOtimizacao`)
3. Jogue sua função dentro de `core/optimizer.py`
4. Vá em `ui/app.py` e adicione a opção na aba correta usando `self.add_option()`
5. Faça o Commit com uma mensagem legal.
6. Push e Pull Request!

---
📜 **Licença:** MIT
Feito com ☕, Python e ódio de travamentos.
