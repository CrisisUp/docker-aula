import os
import sqlite3
from datetime import datetime

# Caminho do banco de dados dentro do volume montado.
# A variável de ambiente DADOS_DIR foi definida no Dockerfile.
DADOS_DIR = os.getenv("DADOS_DIR", "/app/dados")
DB_PATH = os.path.join(DADOS_DIR, "registros.db")


def garantir_diretorio():
    """
    Garante que o diretório do volume existe.
    Necessário na primeira execução ou se o volume estiver vazio.
    """
    os.makedirs(DADOS_DIR, exist_ok=True)
    print(f"[INFO] Diretório de dados: {DADOS_DIR}")


def conectar_banco():
    """
    Cria (ou abre) o banco SQLite no volume.
    sqlite3.connect() cria o arquivo se não existir.
    """
    conn = sqlite3.connect(DB_PATH)

    # Cria a tabela de registros se ainda não existir.
    # "IF NOT EXISTS" evita erro se a tabela já foi criada em uma execução anterior.
    conn.execute("""
        CREATE TABLE IF NOT EXISTS execucoes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            horario   TEXT    NOT NULL,
            mensagem  TEXT    NOT NULL
        )
    """)
    conn.commit()
    return conn


def registrar_execucao(conn):
    """
    Insere um novo registro com o horário atual.
    Isso prova que o container rodou mais uma vez.
    """
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensagem = f"Container iniciado em {agora}"

    conn.execute(
        "INSERT INTO execucoes (horario, mensagem) VALUES (?, ?)",
        (agora, mensagem)
    )
    conn.commit()
    print(f"[INFO] Novo registro salvo: {mensagem}")


def exibir_historico(conn):
    """
    Lê e exibe todos os registros salvos no banco.
    Demonstra que dados de execuções anteriores foram persistidos.
    """
    cursor = conn.execute("SELECT id, horario, mensagem FROM execucoes ORDER BY id")
    registros = cursor.fetchall()

    print("\n" + "=" * 50)
    print(f"  HISTÓRICO DE EXECUÇÕES ({len(registros)} total)")
    print("=" * 50)

    for reg in registros:
        marcador = "→ ESTA EXECUÇÃO" if reg[0] == registros[-1][0] else "  execução anterior"
        print(f"  [{reg[0]:03d}] {reg[1]}  {marcador}")

    print("=" * 50)
    print("\n[DICA] Pare o container, crie um novo apontando para o")
    print("       mesmo volume e veja o histórico ser mantido!\n")


def main():
    print("\n🐳 Atividade 2 — Volume persistente com SQLite")
    print(f"   Banco de dados: {DB_PATH}\n")

    garantir_diretorio()

    conn = conectar_banco()

    registrar_execucao(conn)

    exibir_historico(conn)

    conn.close()


if __name__ == "__main__":
    main()