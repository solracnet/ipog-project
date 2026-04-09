# Analista de Vendas

**Arquivo:** `agents/sales_report.py`
**Lista exportada:** `SALES_REPORT_TOOLS`

Especializado em análise comercial. Reporta desempenho de vendas por região, segmento, meio de entrega, período e impacto de descontos.

## Tools

| Tool | Parâmetros | Descrição |
|---|---|---|
| `get_sales_by_region(filename)` | `filename` | Vendas, lucro e margem por região |
| `get_sales_by_segment(filename)` | `filename` | Ticket médio e margem por segmento de cliente |
| `get_sales_by_shipping_mode(filename)` | `filename` | Rentabilidade por meio de entrega |
| `get_discount_impact_on_sales(filename)` | `filename` | Vendas e margem por faixa de desconto |
| `get_region_segment_ranking(filename)` | `filename` | Ranking cruzado região × segmento |
| `get_regional_performance_detail(filename)` | `filename` | Breakdown por região × categoria × segmento |
| `get_city_performance(filename, region)` | `filename`, `region=None` | Performance por cidade com filtro opcional de região |
| `get_segment_deep_dive(filename, segment)` | `filename`, `segment` | Análise detalhada de um segmento específico |
| `get_sales_by_period(filename)` | `filename` | Evolução mensal/anual (requer coluna de data no dataset) |
| `get_sales_by_salesperson(filename)` | `filename` | Performance por vendedor (requer coluna de vendedor no dataset) |

## Palavras-chave de ativação

`venda`, `vendas`, `região`, `regiao`, `segmento`, `entrega`, `desconto`, `período`, `periodo`, `cidade`, `estado`, `ship`, `ranking`, `canal`, `comercial`

## Exemplos de perguntas

- "Mostre as vendas por região"
- "Qual segmento tem maior ticket médio?"
- "Qual meio de entrega gera prejuízo?"
- "Análise de vendas por cidade no South"
