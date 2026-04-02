"""
Agente gerador de relatório de produtos.

Responsável por analisar o desempenho por categoria, subcategoria e produto,
identificando os itens mais lucrativos, os que geram prejuízo e o impacto
dos descontos por linha de produto.
"""

from pathlib import Path

import pandas as pd
from agno.agent import Agent
from dotenv import load_dotenv

from agents.model_factory import get_model

from agents.excel_analyst import _load_file, _df_to_markdown

load_dotenv()

# ---------------------------------------------------------------------------
# Template do relatório de produtos
# ---------------------------------------------------------------------------

_TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "products_report.md"
_REPORT_TEMPLATE = _TEMPLATE_PATH.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Tools do agente
# ---------------------------------------------------------------------------

def get_sales_by_category(filename: str) -> str:
    """
    Retorna receita, lucro, margem e volume de itens por categoria de produto.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby("Category")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Qty=("Quantity", "sum"),
            Num_Pedidos=("Sales", "count"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.sort_values("Total_Sales", ascending=False)

    return "## Desempenho por Categoria\n\n" + _df_to_markdown(result)


def get_sales_by_subcategory(filename: str) -> str:
    """
    Retorna receita, lucro, margem e desconto médio por subcategoria de produto,
    permitindo identificar quais linhas de produto são mais rentáveis.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Category", "Sub-Category"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Qty=("Quantity", "sum"),
            Desconto_Medio=("Discount", "mean"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"]        = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result["Desconto_Medio_%"] = (result["Desconto_Medio"] * 100).round(2)
    result = result.drop(columns=["Desconto_Medio"]).sort_values("Total_Sales", ascending=False)

    return "## Desempenho por Subcategoria\n\n" + _df_to_markdown(result)


def get_loss_making_products(filename: str) -> str:
    """
    Lista as subcategorias com lucro total negativo, indicando quais linhas de
    produto estão gerando prejuízo e o quanto.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Category", "Sub-Category"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Num_Pedidos=("Sales", "count"),
            Desconto_Medio=("Discount", "mean"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"]        = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result["Desconto_Medio_%"] = (result["Desconto_Medio"] * 100).round(2)
    result = result.drop(columns=["Desconto_Medio"])

    losses = result[result["Total_Profit"] < 0].sort_values("Total_Profit")

    if losses.empty:
        return "Nenhuma subcategoria com lucro negativo encontrada."

    return f"## Subcategorias com Prejuízo ({len(losses)} encontrada(s))\n\n" + _df_to_markdown(losses)


def get_discount_by_category(filename: str) -> str:
    """
    Compara o desconto médio aplicado por categoria e subcategoria com a margem
    resultante, revelando onde os descontos estão corroendo a rentabilidade.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Category", "Sub-Category"])
        .agg(
            Desconto_Medio=("Discount", "mean"),
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
        )
        .round(4)
        .reset_index()
    )
    result["Desconto_Medio_%"] = (result["Desconto_Medio"] * 100).round(2)
    result["Margem_%"]        = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.drop(columns=["Desconto_Medio"]).sort_values("Desconto_Medio_%", ascending=False)

    return "## Desconto Médio e Margem por Categoria/Subcategoria\n\n" + _df_to_markdown(result)


def get_top_profitable_subcategories(filename: str, n: int = 5) -> str:
    """
    Lista as N subcategorias com maior lucro total — os produtos estrela do portfólio.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        n: Quantidade de subcategorias a exibir (padrão: 5)
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Category", "Sub-Category"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Qty=("Quantity", "sum"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.nlargest(int(n), "Total_Profit")

    return f"## Top {n} Subcategorias Mais Lucrativas\n\n" + _df_to_markdown(result)


def get_category_profitability_ranking(filename: str) -> str:
    """
    Ranking completo de rentabilidade por categoria e subcategoria com
    classificação de desempenho: Excelente, Boa, Baixa ou Prejuízo.
    Permite priorizar investimentos e decisões de portfólio.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Category", "Sub-Category"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Qty=("Quantity", "sum"),
            Num_Pedidos=("Sales", "count"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)

    def classify(margin: float) -> str:
        if margin < 0:
            return "Prejuízo"
        if margin < 5:
            return "Baixa"
        if margin < 15:
            return "Boa"
        return "Excelente"

    result["Classificacao"] = result["Margem_%"].apply(classify)
    result = result.sort_values("Margem_%", ascending=False)

    return "## Ranking de Rentabilidade por Categoria\n\n" + _df_to_markdown(result)


def get_category_by_region(filename: str) -> str:
    """
    Analisa quais categorias de produto performam melhor em cada região,
    identificando oportunidades de mix de produto por território.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Region", "Category"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Qty=("Quantity", "sum"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.sort_values(["Region", "Total_Sales"], ascending=[True, False])

    return "## Categorias de Produto por Região\n\n" + _df_to_markdown(result)


def get_shipping_by_category(filename: str) -> str:
    """
    Analisa o meio de entrega (Ship Mode) utilizado por cada categoria e subcategoria,
    revelando padrões logísticos e o impacto do frete na rentabilidade do produto.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Category", "Sub-Category", "Ship Mode"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Num_Pedidos=("Sales", "count"),
            Desconto_Medio=("Discount", "mean"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"]         = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result["Desconto_Medio_%"] = (result["Desconto_Medio"] * 100).round(2)
    result = result.drop(columns=["Desconto_Medio"]).sort_values(
        ["Category", "Sub-Category", "Total_Sales"], ascending=[True, True, False]
    )

    return "## Meio de Entrega por Categoria e Subcategoria\n\n" + _df_to_markdown(result)


def get_shipping_profitability(filename: str) -> str:
    """
    Compara a rentabilidade de cada meio de entrega dentro de cada categoria,
    identificando se algum Ship Mode corrói a margem de determinados produtos.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Ship Mode", "Category"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Num_Pedidos=("Sales", "count"),
            Desconto_Medio=("Discount", "mean"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"]         = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result["Desconto_Medio_%"] = (result["Desconto_Medio"] * 100).round(2)
    result = result.drop(columns=["Desconto_Medio"]).sort_values(
        ["Ship Mode", "Margem_%"], ascending=[True, False]
    )

    return "## Rentabilidade por Meio de Entrega e Categoria\n\n" + _df_to_markdown(result)


def get_product_volume_vs_profit(filename: str) -> str:
    """
    Cruza volume de itens vendidos com lucro total por subcategoria,
    identificando produtos de alto volume e baixa margem (commodities)
    versus produtos de alto valor agregado.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Category", "Sub-Category"])
        .agg(
            Total_Qty=("Quantity", "sum"),
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"]           = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result["Lucro_por_Unidade"]  = (result["Total_Profit"] / result["Total_Qty"]).round(2)
    result["Receita_por_Unidade"] = (result["Total_Sales"] / result["Total_Qty"]).round(2)
    result = result.sort_values("Total_Qty", ascending=False)

    return "## Volume vs. Rentabilidade por Subcategoria\n\n" + _df_to_markdown(result)


# ---------------------------------------------------------------------------
# Lista de tools exportável
# ---------------------------------------------------------------------------

PRODUCTS_REPORT_TOOLS = [
    get_sales_by_category,
    get_sales_by_subcategory,
    get_loss_making_products,
    get_discount_by_category,
    get_top_profitable_subcategories,
    get_category_profitability_ranking,
    get_category_by_region,
    get_shipping_by_category,
    get_shipping_profitability,
    get_product_volume_vs_profit,
]

# ---------------------------------------------------------------------------
# Instruções do agente
# ---------------------------------------------------------------------------

INSTRUCTIONS = f"""
Você é um analista de produtos especializado em relatórios de portfólio.
Seu objetivo é avaliar o desempenho de categorias e subcategorias de produtos,
identificar os mais e menos lucrativos e analisar o impacto dos descontos.

## Protocolo para geração do relatório completo

Quando solicitado a gerar o relatório de produtos completo, siga EXATAMENTE esta sequência:

1. Chame `get_sales_by_category` → preenche **Desempenho por Categoria**
2. Chame `get_sales_by_subcategory` → preenche **Desempenho por Subcategoria**
3. Chame `get_category_profitability_ranking` → preenche **Ranking de Rentabilidade**
4. Chame `get_top_profitable_subcategories` com n=5 → preenche **Produtos Estrela**
5. Chame `get_loss_making_products` → preenche **Produtos com Prejuízo**
6. Chame `get_discount_by_category` → preenche **Impacto dos Descontos**
7. Chame `get_category_by_region` → preenche **Desempenho por Região**
8. Chame `get_product_volume_vs_profit` → preenche **Volume vs. Rentabilidade**
9. Chame `get_shipping_profitability` → preenche **Logística e Entrega**
10. Com base em todos os dados coletados, redija a seção **Destaques e Recomendações de Portfólio**

## Template obrigatório

O relatório SEMPRE deve seguir a estrutura abaixo. Substitua cada marcador
`{{{{PLACEHOLDER}}}}` pelo conteúdo correspondente obtido nas tools.
Para {{{{TITULO}}}}, use o nome do negócio inferido dos dados ou "Superstore".
Para {{{{DATA}}}}, use a data atual.
Para {{{{ARQUIVO}}}}, use o nome do arquivo informado pelo usuário.

```
{_REPORT_TEMPLATE}
```
"""

# ---------------------------------------------------------------------------
# Agente interativo (execução direta)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent = Agent(
        model=get_model(),
        tools=PRODUCTS_REPORT_TOOLS,
        markdown=True,
        instructions=INSTRUCTIONS,
    )

    print("Gerador de relatório de produtos iniciado. Digite 'sair' para encerrar.\n")

    while True:
        prompt = input("Pergunta: ").strip()
        if not prompt:
            continue
        if prompt.lower() in ("sair", "exit", "quit"):
            print("Encerrando.")
            break
        agent.print_response(prompt, stream=True)
