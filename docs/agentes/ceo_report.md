# Analista Executivo

**Arquivo:** `agents/ceo_report.py`
**Lista exportada:** `CEO_REPORT_TOOLS`

Gera relatórios estratégicos de alto nível para o CEO. Consolida KPIs financeiros e operacionais, análise de Pareto, cobertura geográfica e indicadores de saúde do negócio.

## Tools

| Tool | Parâmetros | Descrição |
|---|---|---|
| `get_executive_summary(filename)` | `filename` | KPIs financeiros e operacionais consolidados para apresentação ao CEO |
| `get_revenue_by_region_and_segment(filename)` | `filename` | Receita e margem cruzadas por região × segmento |
| `get_top_states(filename, n)` | `filename`, `n=10` | Top N estados por receita total |
| `get_strategic_kpis(filename)` | `filename` | KPIs de alto nível: cobertura geográfica, concentração e eficiência |
| `get_pareto_analysis(filename, dimension)` | `filename`, `dimension` | Análise 80/20 por dimensão (Sub-Category, State, etc.) |
| `get_business_health_indicators(filename)` | `filename` | Distribuição de margens, concentração de lucro e dependência de desconto |

## Palavras-chave de ativação

`ceo`, `executivo`, `estrateg`, `pareto`, `saúde`, `saude`, `negócio`, `resumo executivo`, `alto nível`

## Exemplos de perguntas

- "Gere o relatório executivo para o CEO"
- "Qual a análise de Pareto por subcategoria?"
- "Quais são os indicadores de saúde do negócio?"
- "Mostre os top 10 estados por receita"
