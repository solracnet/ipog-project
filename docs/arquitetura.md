# Arquitetura

## Visão Geral

O projeto segue uma arquitetura em camadas: o usuário interage via CLI ou interface web, o `AnalyticsWorkflow` recebe a entrada, a normaliza e roteia para o agente especialista correto.

```
┌─────────────────────────────────────┐
│            Interfaces               │
│  CLI (main.py)  │  Web (agno_os.py) │
└────────────────┬────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────┐
│           AnalyticsWorkflow                │
│  Step: Preparação → Router: Intenção       │
│       (agents/agno_workflow.py)            │
└───────────────────┬────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
 Agente único   Agente único  Team completo
 (domínio       (domínio      (perguntas
  específico)    específico)   mistas)
        │
        ▼
┌───────────────────┐
│   IPOG Analytics  │
│       Team        │
│  (agno_teams.py)  │
│                   │
│ • Analista Dados  │
│ • Analista Métr.  │
│ • Analista Exec.  │
│ • Analista Vend.  │
│ • Analista Prod.  │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│     Agentes       │
│   (agents/*.py)   │
│                   │
│  Tools Python     │
│  + Groq LLM       │
└───────────────────┘
        │
        ▼
┌───────────────────┐
│  SampleSuperstore │
│     .csv          │
│   (Pandas)        │
└───────────────────┘
```

## Estrutura de Diretórios

```
/
├── main.py                    # Ponto de entrada CLI — usa AnalyticsWorkflow
├── agno_os.py                 # Ponto de entrada web — AgentOS + FastAPI
├── pyproject.toml             # Metadados do projeto (UV)
├── requirements.txt           # Dependências com versões fixas
├── .env.example               # Template de variáveis de ambiente
├── data/
│   └── SampleSuperstore.csv   # Dados de vendas (13 colunas)
├── db/
│   └── history.db             # SQLite com histórico de sessões (auto-criado)
├── reports/                   # Relatórios gerados em Markdown (auto-criado)
├── agents/
│   ├── __init__.py            # Exporta todas as listas de tools
│   ├── model_factory.py       # Fábrica de modelos LLM (Groq / OpenAI)
│   ├── excel_analyst.py       # Tools: leitura e inspeção de arquivos
│   ├── metrics_agent.py       # Tools: KPIs e métricas de negócio
│   ├── ceo_report.py          # Tools: relatório executivo para o CEO
│   ├── sales_report.py        # Tools: relatório de vendas
│   ├── products_report.py     # Tools: relatório de produtos
│   ├── agno_teams.py          # Team Agno com 5 agentes especializados
│   └── agno_workflow.py       # Workflow: Step Preparação + Router
├── tests/
│   ├── conftest.py
│   ├── test_excel_analyst.py
│   ├── test_metrics_agent.py
│   ├── test_ceo_report.py
│   ├── test_sales_report.py
│   ├── test_products_report.py
│   ├── test_agno_teams.py
│   └── test_agno_workflow.py
├── agent-ui/                  # Interface web Next.js (Agno UI)
└── temp_tests/                # Scripts manuais para validação isolada
```

## Ciclo de Vida de uma Pergunta

1. Usuário digita a pergunta (CLI ou UI web)
2. `AnalyticsWorkflow` recebe via `workflow.print_response()`
3. **Step Preparação** — injeta `SampleSuperstore.csv` se nenhum arquivo for mencionado
4. **Router de Intenção** — analisa palavras-chave do input original e seleciona o step
5. O agente especialista (ou o Team Completo) recebe a pergunta e executa as tools
6. LLM consolida os dados e retorna resposta em Markdown
7. Sessão é persistida no SQLite (`db/history.db`)

## Modelo LLM

A fábrica `agents/model_factory.py` retorna o modelo conforme `LLM_PROVIDER`:

| `LLM_PROVIDER` | Modelo |
|---|---|
| `groq` (padrão) | `llama-3.3-70b-versatile` |
| `openai` | `gpt-4o-mini` |

## Persistência de Sessão

O Agno gerencia o histórico via `SqliteDb`. Cada execução gera um `session_id` único que pode ser reutilizado para retomar a conversa:

```bash
python main.py <session_id>
```
