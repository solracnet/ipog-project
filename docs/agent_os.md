# AgentOS + Agno UI

O projeto suporta uma interface web moderna via [AgentOS](https://docs.agno.com/agent-os/introduction) + [Agent UI](https://github.com/agno-agi/agent-ui), permitindo interagir com o agente via chat visual ao invés do terminal.

## Arquitetura

```
┌─────────────────────────────┐
│   Agno UI (Next.js)         │
│   http://localhost:3000      │
└──────────────┬──────────────┘
               │  HTTP
               ▼
┌─────────────────────────────┐
│   AgentOS (FastAPI)         │
│   http://localhost:7777      │
│   agno_os.py                │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│   AnalyticsWorkflow         │
│   (mesmo do CLI)            │
└─────────────────────────────┘
```

## Arquivos

| Arquivo | Responsabilidade |
|---|---|
| `agno_os.py` | Servidor FastAPI exposto pelo AgentOS na porta `7777` |
| `agent-ui/` | Interface web Next.js + Tailwind CSS |

## Executar

**1. Backend (AgentOS)**

```bash
source .venv/bin/activate
python agno_os.py
```

O servidor sobe em `http://localhost:7777` com hot-reload ativo.

**2. Frontend (Agno UI)**

```bash
cd agent-ui
pnpm install   # apenas na primeira vez
pnpm dev
```

Acesse `http://localhost:3000`.

!!! tip "Alterar endpoint"
    Para apontar a UI para outro servidor, passe o mouse sobre a URL no painel esquerdo e clique em editar.

## Configuração do AgentOS

```python
agent_os = AgentOS(
    id="ipog_project",
    name="IPOG Analytics",
    db=SqliteDb(db_file="db/history.db"),
    workflows=[analytics.workflow],
)
app = agent_os.get_app()
```

O AgentOS registra o `AnalyticsWorkflow` e o expõe via API REST. A UI lista automaticamente os workflows disponíveis e permite iniciar novas sessões ou retomar sessões anteriores.
