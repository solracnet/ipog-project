# Analista de Produtos

**Arquivo:** `agents/products_report.py`
**Lista exportada:** `PRODUCTS_REPORT_TOOLS`

Especializado em análise de portfólio. Avalia categorias e subcategorias, identifica itens com prejuízo, analisa desconto por categoria e cruza volume com rentabilidade.

## Tools

| Tool | Parâmetros | Descrição |
|---|---|---|
| `get_sales_by_category(filename)` | `filename` | Receita, volume e margem por categoria |
| `get_sales_by_subcategory(filename)` | `filename` | Detalhamento por subcategoria com desconto médio |
| `get_loss_making_products(filename)` | `filename` | Subcategorias com lucro total negativo |
| `get_discount_by_category(filename)` | `filename` | Desconto médio vs. margem por linha de produto |
| `get_top_profitable_subcategories(filename, n)` | `filename`, `n=5` | Top N subcategorias mais lucrativas |
| `get_category_profitability_ranking(filename)` | `filename` | Ranking com classificação: Excelente / Boa / Baixa / Prejuízo |
| `get_category_by_region(filename)` | `filename` | Mix de produto por região |
| `get_shipping_by_category(filename)` | `filename` | Ship Mode utilizado por categoria e impacto na margem |
| `get_shipping_profitability(filename)` | `filename` | Rentabilidade de cada meio de entrega por categoria |
| `get_product_volume_vs_profit(filename)` | `filename` | Volume vs. lucro por unidade — diferencia commodities de produtos premium |

## Palavras-chave de ativação

`produto`, `produtos`, `categoria`, `categorias`, `subcategoria`, `subcategorias`, `portfólio`, `portfolio`, `prejuízo`, `prejuizo`, `lucro`, `rentabilidade`, `lucratividade`

## Exemplos de perguntas

- "Quais categorias têm maior margem?"
- "Mostre as subcategorias com prejuízo"
- "Qual o top 5 de subcategorias mais lucrativas?"
- "Compare volume vs. lucro por produto"
