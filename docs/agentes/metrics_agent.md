# Analista de Métricas

**Arquivo:** `agents/metrics_agent.py`
**Lista exportada:** `METRICS_TOOLS`

Especializado em KPIs e indicadores de performance. Calcula margens, dashboards consolidados, ranking de melhores e piores e analisa o impacto de descontos na rentabilidade.

## Tools

| Tool | Parâmetros | Descrição |
|---|---|---|
| `identify_available_kpis(filename)` | `filename` | Lista todos os KPIs possíveis com descrição e colunas utilizadas |
| `get_kpi_dashboard(filename)` | `filename` | Painel com receita total, lucro, margem, ticket médio e volume |
| `get_margin_by_dimension(filename, dimension)` | `filename`, `dimension` | Margem de lucro (%) agrupada por qualquer dimensão do dataset |
| `get_top_performers(filename, dimension, metric, n)` | `filename`, `dimension`, `metric`, `n=5` | Top N melhores por Sales, Profit ou Quantity |
| `get_bottom_performers(filename, dimension, metric, n)` | `filename`, `dimension`, `metric`, `n=5` | Bottom N piores por métrica |
| `detect_loss_makers(filename, dimension)` | `filename`, `dimension` | Grupos com lucro total negativo (prejuízo) |
| `get_discount_impact(filename)` | `filename` | Margem de lucro (%) segmentada por faixa de desconto aplicado |

## Palavras-chave de ativação

`métrica`, `metrica`, `kpi`, `kpis`, `dashboard`, `indicador`, `indicadores`, `desempenho`, `performance`, `margem`

## Exemplos de perguntas

- "Mostre o dashboard de KPIs"
- "Quais são os top 5 estados por lucro?"
- "Qual o impacto dos descontos na margem?"
- "Quais categorias têm prejuízo?"
