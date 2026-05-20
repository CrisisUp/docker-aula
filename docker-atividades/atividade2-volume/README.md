# Atividade 2 — Persistência de Dados com Volumes Docker 💾

Esta atividade demonstra como utilizar **Volumes** no Docker para garantir que os dados gerados por uma aplicação não sejam perdidos quando o container é removido ou reiniciado.

---

## 🎯 Objetivo

Criar um container Python que utiliza um banco de dados **SQLite** para registrar cada vez que o container é executado. O banco de dados deve ser armazenado em um volume persistente.

---

## 📂 Estrutura da Pasta

- `Dockerfile`: Configuração da imagem Docker.
- `app.py`: Script Python que gerencia os registros no banco de dados.
- `README.md`: Este guia de instruções.

---

## 🐳 Explicação Detalhada do Dockerfile

O `Dockerfile` é a "receita" para construir a imagem. Vamos entender cada ingrediente:

1. **`FROM python:3.12-slim`**:
    - Define a imagem base. Usamos a versão `3.12-slim` porque o Python já vem pré-instalado em um sistema operacional Linux (Debian) muito leve. Isso economiza centenas de megabytes de espaço.

2. **`LABEL`**:
    - Adiciona metadados à imagem (descrição, versão). É útil para documentação interna quando você tem muitas imagens no seu computador.

3. **`ENV` (Variáveis de Ambiente)**:
    - `PYTHONDONTWRITEBYTECODE=1`: Instrução para o Python não criar aquelas pastas `__pycache__`, mantendo o container limpo.
    - `PYTHONUNBUFFERED=1`: Faz com que os `print()` do seu código apareçam imediatamente no terminal do Docker, sem ficarem "presos" em memória.
    - `DADOS_DIR=/app/dados`: Cria uma variável que o script Python usará para saber exatamente onde salvar o banco de dados.

4. **`WORKDIR /app`**:
    - Cria a pasta `/app` dentro do container e "entra" nela. É o equivalente ao comando `mkdir /app && cd /app`.

5. **`RUN apt-get update && apt-get install -y sqlite3`**:
    - Como a imagem `slim` é muito básica, ela não vem com o cliente de banco de dados SQLite por padrão. Este comando instala as ferramentas necessárias para que o sistema operacional do container saiba manipular arquivos `.db`.

6. **`COPY app.py .`**:
    - Pega o arquivo `app.py` que está no seu computador e o coloca dentro da pasta `/app` do container.

7. **`VOLUME ["/app/dados"]`**:
    - Esta é a instrução chave. Ela avisa ao Docker: "Ei, esta pasta é especial! Os arquivos aqui dentro podem ser mapeados para fora do container".

8. **`CMD ["python", "app.py"]`**:
    - Define que, assim que o container ligar, ele deve executar o comando `python app.py`.

---

## 🐍 O que o script `app.py` faz?

O script foi desenhado para ser uma prova de conceito:

1. **Criação de Pasta**: Ele garante que a pasta definida em `DADOS_DIR` exista.
2. **Banco de Dados**: Cria um arquivo chamado `registros.db`.
3. **Persistência**: Toda vez que você roda o container, ele insere uma nova linha com o horário atual.
4. **Histórico**: Ele faz um `SELECT` no banco e mostra todas as vezes que o container já rodou. Se o volume estiver funcionando, a lista só cresce!

---

## 🚀 Como executar a atividade

### 1. Construir a Imagem

Abra o terminal na pasta desta atividade e execute:

```bash
docker build -t python-volume-aula .
```

### 2. Rodar SEM Volume (Os dados somem!)

```bash
docker run --name teste-volatil python-volume-aula
```

Rode uma vez, pare e remova o container (`docker rm teste-volatil`). Se rodar de novo, o histórico terá sumido.

### 3. Rodar COM Volume (Persistência Real) 🌟

Vamos mapear uma pasta da sua máquina real para a pasta `/app/dados` do container.

**No Linux/macOS ou PowerShell:**

```bash
docker run --name teste-persistente -v "$(pwd)/meus-dados:/app/dados" python-volume-aula
```

**No Windows (CMD antigo):**

```bash
docker run --name teste-persistente -v "%cd%/meus-dados:/app/dados" python-volume-aula
```

### 4. O Teste Final

- Rode o comando acima várias vezes.
- Remova o container com `docker rm -f teste-persistente`.
- Rode o comando novamente.
- **Mágica**: O histórico continua lá! Você também verá uma pasta chamada `meus-dados` aparecer no seu computador com o arquivo `registros.db` dentro.
