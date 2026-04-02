"""
Agente gerador de relatório executivo (CEO).

Responsável por consolidar os principais indicadores do negócio em uma visão
estratégica de alto nível: receita, lucro, margem, tendências e destaques por
região, categoria e segmento.
"""

from pathlib import Path

import pandas as pd
from agno.agent import Agent
from dotenv import load_dotenv

from agents.model_factory import get_model

from agents.excel_analyst import _load_file, _df_to_markdown

load_dotenv()

# ---------------------------------------------------------------------------
# Template do relatório executivo
# ---------------------------------------------------------------------------

_TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "ceo_report.md"
_REPORT_TEMPLATE = _TEMPLATE_PATH.read_text(encoding="utf-8")

# ---------------------------------------------------------------------------
# Tools do agente
# ---------------------------------------------------------------------------

def get_executive_summary(filename: str) -> str:
    """
    Gera um resumo executivo completo do negócio com os principais KPIs financeiros
    e de volume, adequado para apresentação ao CEO.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    total_sales   = df["Sales"].sum()
    total_profit  = df["Profit"].sum()
    total_qty     = df["Quantity"].sum()
    margin        = total_profit / total_sales * 100
    avg_ticket    = df["Sales"].mean()
    loss_orders   = (df["Profit"] < 0).sum()
    loss_pct      = loss_orders / len(df) * 100

    best_region   = df.groupby("Region")["Sales"].sum().idxmax()
    best_category = df.groupby("Category")["Profit"].sum().idxmax()
    worst_subcat  = df.groupby("Sub-Category")["Profit"].sum().idxmin()

    lines = [
        "## Resumo Executivo",
        "",
        "### Indicadores Financeiros",
        "| KPI | Valor |",
        "|-----|-------|",
        f"| Receita Total | $ {total_sales:,.2f} |",
        f"| Lucro Total | $ {total_profit:,.2f} |",
        f"| Margem de Lucro | {margin:.2f}% |",
        f"| Ticket Médio por Pedido | $ {avg_ticket:,.2f} |",
        "",
        "### Indicadores Operacionais",
        "| KPI | Valor |",
        "|-----|-------|",
        f"| Volume Total de Itens Vendidos | {total_qty:,} |",
        f"| Pedidos com Prejuízo | {loss_orders:,} ({loss_pct:.1f}%) |",
        f"| Região de Maior Receita | {best_region} |",
        f"| Categoria Mais Lucrativa | {best_category} |",
        f"| Subcategoria com Maior Prejuízo | {worst_subcat} |",
    ]
    return "\n".join(lines)


def get_revenue_by_region_and_segment(filename: str) -> str:
    """
    Retorna a receita e o lucro cruzados por região e segmento de cliente,
    oferecendo visão estratégica de onde o negócio performa melhor.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    pivot = (
        df.groupby(["Region", "Segment"])
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .round(2)
        .reset_index()
    )
    pivot["Margem_%"] = (pivot["Profit"] / pivot["Sales"] * 100).round(2)
    pivot = pivot.sort_values(["Region", "Sales"], ascending=[True, False])

    return "## Receita e Lucro por Região e Segmento\n\n" + _df_to_markdown(pivot)


def get_top_states(filename: str, n: int = 10) -> str:
    """
    Lista os N estados com maior receita total, útil para decisões de expansão
    ou alocação de recursos geográficos.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        n: Quantidade de estados a exibir (padrão: 10)
    """
    df = _load_file(filename)

    result = (
        df.groupby("State")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .round(2)
        .reset_index()
    )
    result["Margem_%"] = (result["Profit"] / result["Sales"] * 100).round(2)
    result = result.nlargest(int(n), "Sales")

    return f"## Top {n} Estados por Receita\n\n" + _df_to_markdown(result)


def get_strategic_kpis(filename: str) -> str:
    """
    Retorna KPIs estratégicos de alto nível: concentração de receita, cobertura
    geográfica, amplitude do portfólio e eficiência operacional.
    Ideal para apresentações executivas e análise do posicionamento do negócio.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    total_sales  = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    # Cobertura geográfica
    num_states  = df["State"].nunique()
    num_cities  = df["City"].nunique()
    num_regions = df["Region"].nunique()

    # Amplitude do portfólio
    num_categories    = df["Category"].nunique()
    num_subcategories = df["Sub-Category"].nunique()

    # Concentração: % da receita vinda do top-3 estados
    top3_states_sales = df.groupby("State")["Sales"].sum().nlargest(3).sum()
    top3_concentration = top3_states_sales / total_sales * 100

    # Saúde do portfólio: % de subcategorias lucrativas
    subcat_profit = df.groupby("Sub-Category")["Profit"].sum()
    pct_profitable = (subcat_profit > 0).sum() / len(subcat_profit) * 100

    # Dependência de desconto: % de pedidos com desconto > 0
    pct_discounted = (df["Discount"] > 0).sum() / len(df) * 100

    # Eficiência: lucro por item vendido
    profit_per_unit = total_profit / df["Quantity"].sum()

    lines = [
        "## KPIs Estratégicos de Alto Nível",
        "",
        "### Abrangência e Portfólio",
        "| Indicador | Valor |",
        "|-----------|-------|",
        f"| Regiões Atendidas | {num_regions} |",
        f"| Estados Atendidos | {num_states} |",
        f"| Cidades Atendidas | {num_cities:,} |",
        f"| Categorias de Produto | {num_categories} |",
        f"| Subcategorias de Produto | {num_subcategories} |",
        "",
        "### Concentração e Risco",
        "| Indicador | Valor |",
        "|-----------|-------|",
        f"| Concentração Top-3 Estados (% receita) | {top3_concentration:.1f}% |",
        f"| Subcategorias Lucrativas | {pct_profitable:.1f}% |",
        f"| Pedidos com Desconto Aplicado | {pct_discounted:.1f}% |",
        "",
        "### Eficiência",
        "| Indicador | Valor |",
        "|-----------|-------|",
        f"| Lucro por Unidade Vendida | $ {profit_per_unit:.2f} |",
        f"| Margem de Lucro Global | {total_profit / total_sales * 100:.2f}% |",
    ]
    return "\n".join(lines)


def get_pareto_analysis(filename: str, dimension: str = "Sub-Category") -> str:
    """
    Aplica a análise de Pareto (regra 80/20) sobre uma dimensão, mostrando
    quantos itens respondem por 80% da receita total — útil para priorização
    estratégica de produtos, regiões ou segmentos.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        dimension: Dimensão de análise — 'Sub-Category', 'State', 'Segment', 'Category' (padrão: 'Sub-Category')
    """
    df = _load_file(filename)
    if dimension not in df.columns:
        available = ", ".join(df.select_dtypes("str").columns)
        return f"Dimensão '{dimension}' não encontrada. Disponíveis: {available}"

    total_sales = df["Sales"].sum()

    ranked = (
        df.groupby(dimension)["Sales"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .rename(columns={"Sales": "Total_Sales"})
    )
    ranked["Participacao_%"]   = (ranked["Total_Sales"] / total_sales * 100).round(2)
    ranked["Acumulado_%"]      = ranked["Participacao_%"].cumsum().round(2)

    threshold_80 = ranked[ranked["Acumulado_%"] <= 80]
    n_80         = len(threshold_80) + 1
    pct_items_80 = n_80 / len(ranked) * 100

    summary = [
        f"## Análise de Pareto — {dimension}",
        "",
        f"> **{n_80} de {len(ranked)} {dimension}s** ({pct_items_80:.1f}% do total) "
        f"respondem por aproximadamente **80% da receita**.",
        "",
    ]
    return "\n".join(summary) + _df_to_markdown(ranked)


def get_business_health_indicators(filename: str) -> str:
    """
    Avalia a saúde geral do negócio através de indicadores compostos:
    distribuição de margens, dependência de desconto por segmento e
    concentração de lucro por categoria — fornecendo uma visão macro
    dos riscos e oportunidades estratégicas.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    total_profit = df["Profit"].sum()
    total_sales  = df["Sales"].sum()

    # Distribuição de margem por faixas
    df = df.copy()
    df["Margem_linha"] = df["Profit"] / df["Sales"].replace(0, float("nan")) * 100

    bins   = [-float("inf"), 0, 5, 15, 30, float("inf")]
    labels = ["Prejuízo (<0%)", "Baixa (0–5%)", "Média (5–15%)", "Boa (15–30%)", "Ótima (>30%)"]
    df["Faixa_Margem"] = pd.cut(df["Margem_linha"], bins=bins, labels=labels)

    margem_dist = (
        df.groupby("Faixa_Margem", observed=True)
        .agg(Num_Pedidos=("Sales", "count"), Total_Sales=("Sales", "sum"))
        .round(2)
        .reset_index()
    )
    margem_dist["Participacao_%"] = (margem_dist["Total_Sales"] / total_sales * 100).round(2)

    # Concentração de lucro por categoria
    cat_profit = (
        df.groupby("Category")["Profit"]
        .sum()
        .round(2)
        .reset_index()
    )
    cat_profit["Participacao_%"] = (cat_profit["Profit"] / total_profit * 100).round(2)

    # Dependência de desconto por segmento
    discount_dep = (
        df.groupby("Segment")
        .agg(
            Desconto_Medio_pct=("Discount", lambda x: round(x.mean() * 100, 2)),
            Margem_pct=("Profit", lambda x: round(x.sum() / df.loc[x.index, "Sales"].sum() * 100, 2)),
        )
        .reset_index()
    )

    lines = [
        "## Indicadores de Saúde do Negócio",
        "",
        "### Distribuição de Pedidos por Faixa de Margem",
        "",
        _df_to_markdown(margem_dist),
        "",
        "### Concentração do Lucro por Categoria",
        "",
        _df_to_markdown(cat_profit),
        "",
        "### Dependência de Desconto vs. Margem por Segmento",
        "",
        _df_to_markdown(discount_dep),
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Lista de tools exportável
# ---------------------------------------------------------------------------

CEO_REPORT_TOOLS = [
    get_executive_summary,
    get_revenue_by_region_and_segment,
    get_top_states,
    get_strategic_kpis,
    get_pareto_analysis,
    get_business_health_indicators,
]

# ---------------------------------------------------------------------------
# Instruções do agente
# ---------------------------------------------------------------------------

INSTRUCTIONS = f"""
Você é um assistente executivo especializado em relatórios para o CEO.
Seu objetivo é consolidar os principais indicadores do negócio em uma visão
estratégica e objetiva, destacando oportunidades e riscos.

## Protocolo para geração do relatório completo

Quando solicitado a gerar o relatório executivo completo, siga EXATAMENTE esta sequência:

1. Chame `get_executive_summary` → preenche a seção **Resumo Executivo**
2. Chame `get_strategic_kpis` → preenche a seção **KPIs Estratégicos**
3. Chame `get_revenue_by_region_and_segment` → preenche **Desempenho por Região e Segmento**
4. Chame `get_top_states` com n=10 → preenche **Top Estados por Receita**
5. Chame `get_pareto_analysis` com dimension='Sub-Category' → preenche **Análise de Pareto**
6. Chame `get_business_health_indicators` → preenche **Saúde do Negócio**
7. Com base em todos os dados coletados, redija a seção **Destaques e Recomendações**

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
        tools=CEO_REPORT_TOOLS,
        markdown=True,
        instructions=INSTRUCTIONS,
    )

    print("Gerador de relatório executivo iniciado. Digite 'sair' para encerrar.\n")

    while True:
        prompt = input("Pergunta: ").strip()
        if not prompt:
            continue
        if prompt.lower() in ("sair", "exit", "quit"):
            print("Encerrando.")
            break
        agent.print_response(prompt, stream=True)
