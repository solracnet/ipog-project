# Setup do Ambiente

## Pré-requisitos

- Python 3.11
- [UV](https://docs.astral.sh/uv/) (gerenciador de pacotes)
- Node.js + pnpm (apenas para o frontend Agno UI)

## Instalação

**1. Clonar o repositório**

```bash
git clone https://github.com/solracnet/ipog-project
cd ipog-project
```

**2. Criar e ativar o ambiente virtual**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

**3. Instalar dependências**

```bash
uv pip install -r requirements.txt
```

**4. Configurar variáveis de ambiente**

```bash
cp .env.example .env
```

Edite o `.env` e preencha as chaves:

```env
GROQ_API_KEY=...         # obrigatório
OPENAI_API_KEY=...       # opcional — ativa o provider OpenAI
TAVILY_API_KEY=...       # opcional — busca web
LLM_PROVIDER=groq        # "groq" (padrão) ou "openai"
```

## Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `GROQ_API_KEY` | Sim | Chave da API Groq (LLM principal) |
| `OPENAI_API_KEY` | Não | LLM alternativo (`gpt-4o-mini`) |
| `TAVILY_API_KEY` | Não | Ferramenta de busca web |
| `LLM_PROVIDER` | Não | Provider ativo: `groq` (padrão) ou `openai` |

## Executar

=== "Terminal (CLI)"

    ```bash
    python main.py
    ```

    Para retomar uma sessão existente:

    ```bash
    python main.py <session_id>
    ```

=== "Interface Web (AgentOS + Agno UI)"

    Backend:
    ```bash
    python agno_os.py
    ```

    Frontend (em outro terminal):
    ```bash
    cd agent-ui
    pnpm install
    pnpm dev
    ```

    Acesse em `http://localhost:3000`. O backend roda em `http://localhost:7777`.

## Testes

```bash
uv run pytest tests/ -v
```
