"""
Agente gerador de relatório de vendas.

Responsável por analisar e reportar o desempenho de vendas por região,
segmento, meio de entrega e período, incluindo impacto de descontos e
comparações entre grupos.
"""

from pathlib import Path

import pandas as pd
from agno.agent import Agent
from dotenv import load_dotenv

from agents.model_factory import get_model

from agents.excel_analyst import _load_file, _df_to_markdown

load_dotenv()

# ---------------------------------------------------------------------------
# Template do relatório de vendas
# ---------------------------------------------------------------------------

_TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "sales_report.md"
_REPORT_TEMPLATE = _TEMPLATE_PATH.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Tools do agente
# ---------------------------------------------------------------------------

def get_sales_by_region(filename: str) -> str:
    """
    Retorna o total de vendas, lucro, quantidade e margem agrupados por região.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby("Region")
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

    return "## Vendas por Região\n\n" + _df_to_markdown(result)


def get_sales_by_segment(filename: str) -> str:
    """
    Retorna o desempenho de vendas por segmento de cliente
    (Consumer, Corporate, Home Office).

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby("Segment")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Ticket_Medio=("Sales", "mean"),
            Num_Pedidos=("Sales", "count"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.sort_values("Total_Sales", ascending=False)

    return "## Vendas por Segmento de Cliente\n\n" + _df_to_markdown(result)


def get_sales_by_shipping_mode(filename: str) -> str:
    """
    Analisa vendas, lucro e volume por meio de entrega (Ship Mode),
    identificando quais canais de entrega são mais rentáveis.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby("Ship Mode")
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Num_Pedidos=("Sales", "count"),
            Desconto_Medio=("Discount", "mean"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result["Desconto_Medio_%"] = (result["Desconto_Medio"] * 100).round(2)
    result = result.drop(columns=["Desconto_Medio"]).sort_values("Total_Sales", ascending=False)

    return "## Vendas por Meio de Entrega\n\n" + _df_to_markdown(result)


def get_discount_impact_on_sales(filename: str) -> str:
    """
    Mostra como diferentes faixas de desconto afetam o volume de vendas,
    o lucro e a margem — revelando se descontos altos comprometem a rentabilidade.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)
    df = df.copy()

    bins   = [-0.001, 0.0, 0.1, 0.2, 0.3, 0.5, 1.01]
    labels = ["0% (sem desconto)", "1–10%", "11–20%", "21–30%", "31–50%", "51–100%"]
    df["Faixa_Desconto"] = pd.cut(df["Discount"], bins=bins, labels=labels)

    result = (
        df.groupby("Faixa_Desconto", observed=True)
        .agg(
            Num_Pedidos=("Sales", "count"),
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)

    return "## Impacto do Desconto nas Vendas\n\n" + _df_to_markdown(result)


def get_region_segment_ranking(filename: str) -> str:
    """
    Ranking cruzado de região × segmento por receita total, útil para
    identificar as combinações mais e menos lucrativas.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Region", "Segment"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Num_Pedidos=("Sales", "count"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.sort_values("Total_Sales", ascending=False)

    return "## Ranking Região × Segmento\n\n" + _df_to_markdown(result)


def get_regional_performance_detail(filename: str) -> str:
    """
    Detalha o desempenho de cada região com breakdown por categoria e segmento,
    revelando quais combinações impulsionam ou prejudicam cada território.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    result = (
        df.groupby(["Region", "Category", "Segment"])
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
        ["Region", "Total_Sales"], ascending=[True, False]
    )

    return "## Performance Regional Detalhada (Região × Categoria × Segmento)\n\n" + _df_to_markdown(result)


def get_city_performance(filename: str, region: str = "") -> str:
    """
    Retorna o desempenho de vendas por cidade, com opção de filtrar por região.
    Permite identificar os territórios mais e menos rentáveis dentro de cada área.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        region: Filtro opcional por região (ex: 'West', 'East'). Deixe vazio para todas.
    """
    df = _load_file(filename)

    if region:
        df = df[df["Region"].str.lower() == region.lower()]
        if df.empty:
            regions = ", ".join(sorted(df["Region"].unique()))
            return f"Região '{region}' não encontrada. Disponíveis: {regions}"

    result = (
        df.groupby(["Region", "State", "City"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Num_Pedidos=("Sales", "count"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.sort_values("Total_Sales", ascending=False)

    header = f"## Performance por Cidade{f' — Região {region}' if region else ''}\n\n"
    return header + _df_to_markdown(result)


def get_segment_deep_dive(filename: str, segment: str = "") -> str:
    """
    Análise detalhada de um segmento de cliente: breakdown por região, categoria
    e ticket médio. Permite entender o comportamento de compra de cada perfil.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        segment: Segmento a detalhar — 'Consumer', 'Corporate' ou 'Home Office'.
                 Deixe vazio para comparar todos os segmentos.
    """
    df = _load_file(filename)

    if segment:
        df = df[df["Segment"].str.lower() == segment.lower()]
        if df.empty:
            segments = ", ".join(sorted(df["Segment"].unique()))
            return f"Segmento '{segment}' não encontrado. Disponíveis: {segments}"

    result = (
        df.groupby(["Segment", "Region", "Category"])
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Ticket_Medio=("Sales", "mean"),
            Num_Pedidos=("Sales", "count"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.sort_values(["Segment", "Total_Sales"], ascending=[True, False])

    header = f"## Análise de Segmento{f': {segment}' if segment else 's'}\n\n"
    return header + _df_to_markdown(result)


def get_sales_by_period(filename: str) -> str:
    """
    Analisa a evolução de vendas ao longo do tempo (mensal e anual).
    Requer uma coluna de data no dataset (ex: 'Order Date', 'Date').

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    date_candidates = [c for c in df.columns if any(
        kw in c.lower() for kw in ("date", "data", "periodo", "period", "mes", "month")
    )]

    if not date_candidates:
        return (
            "## Performance por Período\n\n"
            "> **Coluna de data não encontrada no dataset atual.**\n\n"
            "Para habilitar esta análise, adicione ao dataset uma coluna de data com um dos nomes: "
            "`Order Date`, `Ship Date`, `Date`, `Data`.\n\n"
            f"Colunas disponíveis no momento: {', '.join(f'`{c}`' for c in df.columns)}"
        )

    date_col = date_candidates[0]
    df = df.copy()
    df["_date"] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["_date"])
    df["Ano"]  = df["_date"].dt.year
    df["Mes"]  = df["_date"].dt.month

    monthly = (
        df.groupby(["Ano", "Mes"])
        .agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"), Num_Pedidos=("Sales", "count"))
        .round(2)
        .reset_index()
    )
    monthly["Margem_%"] = (monthly["Total_Profit"] / monthly["Total_Sales"] * 100).round(2)

    return f"## Performance por Período (coluna: `{date_col}`)\n\n" + _df_to_markdown(monthly)


def get_sales_by_salesperson(filename: str) -> str:
    """
    Analisa o desempenho individual de vendedores: receita, lucro, ticket médio
    e margem por vendedor. Requer uma coluna de vendedor no dataset.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    rep_candidates = [c for c in df.columns if any(
        kw in c.lower() for kw in ("rep", "vendedor", "salesperson", "seller", "agent", "responsible", "responsavel")
    )]

    if not rep_candidates:
        return (
            "## Performance por Vendedor\n\n"
            "> **Coluna de vendedor não encontrada no dataset atual.**\n\n"
            "Para habilitar esta análise, adicione ao dataset uma coluna com um dos nomes: "
            "`Sales Rep`, `Vendedor`, `Salesperson`, `Seller`.\n\n"
            f"Colunas disponíveis no momento: {', '.join(f'`{c}`' for c in df.columns)}"
        )

    rep_col = rep_candidates[0]
    result = (
        df.groupby(rep_col)
        .agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Ticket_Medio=("Sales", "mean"),
            Num_Pedidos=("Sales", "count"),
        )
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.sort_values("Total_Sales", ascending=False)

    return f"## Performance por Vendedor (coluna: `{rep_col}`)\n\n" + _df_to_markdown(result)


# ---------------------------------------------------------------------------
# Lista de tools exportável
# ---------------------------------------------------------------------------

SALES_REPORT_TOOLS = [
    get_sales_by_region,
    get_sales_by_segment,
    get_sales_by_shipping_mode,
    get_discount_impact_on_sales,
    get_region_segment_ranking,
    get_regional_performance_detail,
    get_city_performance,
    get_segment_deep_dive,
    get_sales_by_period,
    get_sales_by_salesperson,
]

# ---------------------------------------------------------------------------
# Instruções do agente
# ---------------------------------------------------------------------------

INSTRUCTIONS = f"""
Você é um analista de vendas especializado em relatórios comerciais.
Seu objetivo é analisar o desempenho de vendas por região, segmento e canal,
identificar tendências e apontar oportunidades de crescimento.

## Protocolo para geração do relatório completo

Quando solicitado a gerar o relatório de vendas completo, siga EXATAMENTE esta sequência:

1. Chame `get_sales_by_region` → preenche **Visão Geral por Região**
2. Chame `get_sales_by_segment` → preenche **Desempenho por Segmento de Cliente**
3. Chame `get_region_segment_ranking` → preenche **Ranking Região × Segmento**
4. Chame `get_regional_performance_detail` → preenche **Performance Regional Detalhada**
5. Chame `get_city_performance` sem filtro de região → preenche **Performance por Cidade**
6. Chame `get_segment_deep_dive` sem filtro de segmento → preenche **Análise de Segmento**
7. Chame `get_discount_impact_on_sales` → preenche **Impacto dos Descontos nas Vendas**
8. Chame `get_sales_by_shipping_mode` → preenche **Desempenho por Meio de Entrega**
9. Chame `get_sales_by_period` → preenche **Performance por Período**
10. Chame `get_sales_by_salesperson` → preenche **Performance por Vendedor**
11. Com base em todos os dados coletados, redija a seção **Destaques e Recomendações Comerciais**

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
        tools=SALES_REPORT_TOOLS,
        markdown=True,
        instructions=INSTRUCTIONS,
    )

    print("Gerador de relatório de vendas iniciado. Digite 'sair' para encerrar.\n")

    while True:
        prompt = input("Pergunta: ").strip()
        if not prompt:
            continue
        if prompt.lower() in ("sair", "exit", "quit"):
            print("Encerrando.")
            break
        agent.print_response(prompt, stream=True)
