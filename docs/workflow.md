# Agno Workflow

**Arquivo:** `agents/agno_workflow.py`
**Classe:** `AnalyticsWorkflow`

O `AnalyticsWorkflow` orquestra o team usando o framework `Workflow` do Agno. A pipeline tem dois estágios: normalização da entrada e roteamento de intenção.

## Pipeline

```
Entrada do usuário
        │
        ▼
┌─────────────────────────────────────────┐
│  Step: Preparação                       │
│  Se nenhum arquivo for mencionado,      │
│  injeta "> Arquivo: SampleSuperstore.csv"│
└───────────────────┬─────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  Router: Roteador de Intenção           │
│  Analisa palavras-chave do input        │
│  original e seleciona o Step correto    │
└──┬────┬────┬────┬────┬──────────────────┘
   │    │    │    │    │
   ▼    ▼    ▼    ▼    ▼          ▼
 Dados Métr. CEO Vend. Prod.  Team Completo
                               (fallback)
```

## Step: Preparação

Garante que o nome do arquivo padrão esteja sempre presente na entrada antes de chegar ao agente. Isso evita que o LLM precise perguntar qual arquivo usar a cada chamada.

```python
def _prepare_input(step_input: StepInput) -> StepOutput:
    text = (step_input.input or "").strip()
    if "SampleSuperstore.csv".lower() not in text.lower() and ".csv" not in text.lower():
        enriched = f"{text}\n\n> **Arquivo:** SampleSuperstore.csv"
    else:
        enriched = text
    return StepOutput(content=enriched, success=True)
```

## Router: Roteador de Intenção

Classifica a intenção baseando-se no **input original** do usuário (não no conteúdo enriquecido pela etapa de Preparação, para evitar falso-positivos).

### Domínios e Palavras-chave

| Domínio | Palavras-chave | Step |
|---|---|---|
| Dados | `arquivo`, `schema`, `esquema`, `colunas`, `coluna`, `amostra`, `lista`, `listar`, `inspecionar`, `sample`, `tipos` | Dados |
| Métricas | `métrica`, `metrica`, `kpi`, `kpis`, `dashboard`, `indicador`, `indicadores`, `desempenho`, `performance`, `margem` | Métricas |
| Executivo | `ceo`, `executivo`, `estrateg`, `pareto`, `saúde`, `saude`, `negócio`, `resumo executivo`, `alto nível` | Executivo |
| Vendas | `venda`, `vendas`, `região`, `regiao`, `segmento`, `entrega`, `desconto`, `período`, `periodo`, `cidade`, `estado`, `ship`, `ranking`, `canal`, `comercial` | Vendas |
| Produtos | `produto`, `produtos`, `categoria`, `categorias`, `subcategoria`, `subcategorias`, `portfólio`, `portfolio`, `prejuízo`, `prejuizo`, `lucro`, `rentabilidade`, `lucratividade` | Produtos |
| *(nenhum)* | — | Team Completo |

!!! note "Fallback"
    Quando nenhuma palavra-chave é encontrada, o Router delega ao **Team Completo**, que coordena todos os agentes para responder perguntas mistas ou abertas.

## Persistência de Sessão

O Workflow usa `SqliteDb` para persistir o histórico de conversa:

```python
Workflow(
    db=SqliteDb(db_file="db/history.db"),
    steps=[step_preparacao, router],
)
```

Cada execução gera um `session_id` único. Para retomar:

```bash
python main.py <session_id>
```

## Uso

```python
from agents.agno_workflow import AnalyticsWorkflow

wf = AnalyticsWorkflow(db_path="db/history.db")
wf.workflow.print_response("Análise de vendas por região", stream=True)
```
