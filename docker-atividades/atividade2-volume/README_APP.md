# 📓 Guia de Evolução de Maturidade: Docker & Python

Este caderno documenta a jornada de transformação de um script simples em uma aplicação resiliente e segura pronta para produção.

---

## 🚀 Nível 1: O Funcional (Onde tudo começou)

O objetivo inicial era apenas provar que o Docker pode salvar dados.

- **Conceito**: Uso de sqlite3 para persistência.
- **Limitação**: Código "hardcoded" (nomes fixos), sem tratamento de erros e rodando como root.
- **Arquivos**: app.py e Dockerfile.

---

## 🛡️ Nível 2: O Resiliente (Engenharia de Software)

Aqui focamos na robustez do código e na flexibilidade do container.

- **Melhorias**:
  - **Variáveis de Ambiente**: Uso de os.getenv para configurar diretórios e nomes de arquivos.
  - **Context Managers**: Uso de "with sqlite3.connect" para evitar corrupção de dados.
  - **Tratamento de Erros**: Verificação proativa de volumes "Read-Only".
  - **PEP 8**: Código documentado com docstrings e formatado profissionalmente.
- **Arquivos**: app_v2.py e Dockerfile2.

---

## 🏢 Nível 3: O Profissional (Segurança e Monitoramento)

O foco final foi a conformidade com padrões de infraestrutura modernos.

- **Melhorias**:
  - **Segurança (Non-Root)**: Criação do appuser. O container não tem mais permissões administrativas.
  - **Monitoramento (Healthcheck)**: O Docker agora vigia a aplicação via comando --health.
  - **Graceful Shutdown**: Tratamento de sinais SIGTERM para fechamento seguro do banco.
- **Arquivos**: app_v3.py e Dockerfile3.

---

## 🧠 Resumo de Conceitos Chave para Revisão

### 1. Persistência vs Efemeridade

Containers são feitos para serem descartáveis. Os Volumes são as "âncoras" que mantêm os dados vivos.

### 2. O Princípio do Menor Privilégio

Sempre rode aplicações Docker com usuários limitados para reduzir riscos.

### 3. Sinais do Sistema Operacional

Aplicações precisam entender sinais como SIGTERM para não corromper arquivos ao serem desligadas.

### 4. Idempotência

Uma aplicação deve poder ser reiniciada várias vezes e se comportar corretamente sempre.

---

## 🧪 Laboratório de Testes (Desafios)

1. Erro de Escrita: Rode com volume em modo :ro.
2. Saúde: Mude DB_NAME para um caminho inválido e veja o status no docker ps.
3. Logs de Parada: Use docker stop e veja o script finalizando graciosamente nos logs.
