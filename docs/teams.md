# Agno Teams

**Arquivo:** `agents/agno_teams.py`
**Classe:** `agno_teams`

O projeto utiliza o framework **Teams** do Agno para coordenar os cinco agentes especializados em uma única equipe coesa. O team opera no modo `coordinate`.

## Como Funciona

No modo `coordinate`, um agente líder (o próprio Team) recebe a pergunta do usuário, decide quais membros acionar com base nos seus papéis e consolida as respostas em uma saída única e coerente.

```
Pergunta do usuário
        │
        ▼
┌──────────────────────┐
│  IPOG Analytics Team │  ← Coordenador (modo: coordinate)
│  (Team líder)        │
└──┬──┬──┬──┬──┬───────┘
   │  │  │  │  │
   ▼  ▼  ▼  ▼  ▼
  DA  MA  EA  VA  PA    ← Membros especialistas
```

## Membros do Team

| Atributo | Nome | Tools | Responsabilidade |
|---|---|---|---|
| `data_analyst` | Analista de Dados | `EXCEL_TOOLS` (8) | Leitura e inspeção de arquivos CSV/Excel |
| `metrics_analyst` | Analista de Métricas | `METRICS_TOOLS` (7) | KPIs, dashboards e indicadores de performance |
| `ceo_analyst` | Analista Executivo | `CEO_REPORT_TOOLS` (6) | Relatório estratégico para o CEO |
| `sales_analyst` | Analista de Vendas | `SALES_REPORT_TOOLS` (10) | Performance comercial por região e segmento |
| `products_analyst` | Analista de Produtos | `PRODUCTS_REPORT_TOOLS` (10) | Portfólio de produtos e rentabilidade |

## Configuração do Team

```python
Team(
    name="IPOG Analytics Team",
    mode=TeamMode.coordinate,
    model=get_model(),
    members=[...],          # 5 agentes
    markdown=True,
    show_members_responses=True,
)
```

- `show_members_responses=True` — exibe as respostas individuais de cada membro antes da síntese final
- Cada membro recebe as tools do seu domínio e instruções específicas importadas do seu módulo

## Uso Direto (sem Workflow)

O team pode ser acionado diretamente para perguntas que exijam múltiplas perspectivas:

```python
from agents.agno_teams import agno_teams

t = agno_teams()
t.team.print_response("Gere uma análise completa de vendas e produtos", stream=True)
```

No `AnalyticsWorkflow`, o Team Completo é o fallback quando nenhum domínio específico é identificado pelo Router.
