import os
import sqlite3
import sys
from datetime import datetime
from sqlite3 import Error

# Configurações via Variáveis de Ambiente (Boas práticas Docker)
DADOS_DIR = os.getenv("DADOS_DIR", "/app/dados")
DB_NAME = os.getenv("DB_NAME", "registros.db")
DB_PATH = os.path.join(DADOS_DIR, DB_NAME)


def garantir_diretorio():
    """
    Garante que o diretório de dados exista e seja gravável.
    Trata erros de permissão comuns em montagens de volumes.
    """
    try:
        os.makedirs(DADOS_DIR, exist_ok=True)
        # Teste simples de escrita para detectar volumes Read-Only precocemente
        teste_path = os.path.join(DADOS_DIR, ".write_test")
        with open(teste_path, "w") as f:
            f.write("test")
        os.remove(teste_path)
    except (OSError, IOError) as e:
        print(f"❌ ERRO CRÍTICO: Não é possível escrever no diretório {DADOS_DIR}")
        print(f"   Dica: Verifique se o volume foi montado como Read-Only. Detalhes: {e}")
        sys.exit(1)


def conectar_banco():
    """
    Cria a conexão com o banco de dados e inicializa a tabela.
    Utiliza tratamento de exceções para falhas de E/S ou SQL.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS execucoes (
                    id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    horario   TEXT    NOT NULL,
                    mensagem  TEXT    NOT NULL
                )
            """)
            return True
    except Error as e:
        print(f"❌ ERRO DE BANCO DE DADOS: {e}")
        return False


def registrar_execucao():
    """
    Insere um novo registro de log.
    Usa o gerenciador de contexto para garantir o commit e fechamento.
    """
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensagem = f"Container v2 iniciado em {agora}"

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO execucoes (horario, mensagem) VALUES (?, ?)",
                (agora, mensagem)
            )
            print(f"✅ Registro salvo com sucesso!")
    except Error as e:
        print(f"❌ FALHA AO REGISTRAR: {e}")


def exibir_historico():
    """
    Lê e exibe os dados salvos.
    """
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.execute("SELECT id, horario, mensagem FROM execucoes ORDER BY id")
            registros = cursor.fetchall()

            print("\n" + "=" * 60)
            print(f"  HISTÓRICO DE EXECUÇÕES PERSISTENTES ({len(registros)} total)")
            print("=" * 60)

            for reg in registros:
                marcador = " ⭐ ATUAL" if reg[0] == registros[-1][0] else "    "
                print(f"  [{reg[0]:03d}] {reg[1]} | {reg[2]}{marcador}")

            print("=" * 60 + "\n")
    except Error as e:
        print(f"❌ ERRO AO LER HISTÓRICO: {e}")


def main():
    """
    Fluxo principal com verificação de integridade em cada etapa.
    """
    print(f"\n🚀 Iniciando App v2 (Resiliente)")
    print(f"📂 Banco: {DB_PATH}\n")

    garantir_diretorio()

    if conectar_banco():
        registrar_execucao()
        exibir_historico()
    else:
        print("🛑 Finalizando devido a erros no banco de dados.")
        sys.exit(1)


if __name__ == "__main__":
    main()
