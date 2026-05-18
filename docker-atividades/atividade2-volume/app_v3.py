import os
import sqlite3
import sys
import signal
import time
from datetime import datetime
from sqlite3 import Error

# Configurações
DADOS_DIR = os.getenv("DADOS_DIR", "/app/dados")
DB_NAME = os.getenv("DB_NAME", "producao.db")
DB_PATH = os.path.join(DADOS_DIR, DB_NAME)

# Variável global para controle de encerramento
keep_running = True

def handle_signal(signum, frame):
    """Lida com sinais de interrupção (SIGTERM/SIGINT) para encerramento gracioso."""
    global keep_running
    print(f"\n[SINAL {signum}] Recebido comando de parada. Finalizando com segurança...")
    keep_running = False

# Registra os sinais de parada do Docker
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGINT, handle_signal)

def check_health():
    """Função usada pelo Docker HEALTHCHECK para verificar se o banco está acessível."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("SELECT 1")
        print("Healthy")
        sys.exit(0)
    except Exception as e:
        print(f"Unhealthy: {e}")
        sys.exit(1)

def garantir_diretorio():
    try:
        os.makedirs(DADOS_DIR, exist_ok=True)
    except OSError as e:
        print(f"❌ ERRO DE DIRETÓRIO: {e}")
        sys.exit(1)

def registrar_execucao():
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS execucoes (id INTEGER PRIMARY KEY, horario TEXT)")
            conn.execute("INSERT INTO execucoes (horario) VALUES (?)", (agora,))
            print(f"✅ Registro persistido: {agora}")
    except Error as e:
        print(f"❌ ERRO AO SALVAR: {e}")

def main():
    # Verifica se o script foi chamado apenas para verificação de saúde (Healthcheck)
    if len(sys.argv) > 1 and sys.argv[1] == "--health":
        check_health()

    print(f"🚀 App v3 Iniciado (Usuário: {os.getlogin() if hasattr(os, 'getlogin') else 'unknown'})")
    garantir_diretorio()
    
    # Simula um serviço que fica rodando e registrando a cada 10 segundos
    while keep_running:
        registrar_execucao()
        print("💤 Aguardando próxima iteração... (Pressione Ctrl+C para parar)")
        for _ in range(10): # Espera 10 segundos em pequenos intervalos para responder ao sinal rápido
            if not keep_running: break
            time.sleep(1)

    print("👋 Container finalizado com sucesso.")

if __name__ == "__main__":
    main()
