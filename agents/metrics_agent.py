"""
Agente especialista em identificação e cálculo de métricas e KPIs.

Analisa o dataset e expõe ferramentas para descobrir, calcular e comparar
indicadores de desempenho de vendas, lucratividade, desconto e volume.
"""

from pathlib import Path

import pandas as pd
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

from agents.excel_analyst import _load_file, _df_to_markdown

load_dotenv()

# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _profit_margin(df: pd.DataFrame) -> pd.Series:
    """Calcula margem de lucro (%) com proteção contra divisão por zero."""
    return (df["Profit"] / df["Sales"].replace(0, float("nan")) * 100).round(2)


# ---------------------------------------------------------------------------
# Tools do agente de métricas
# ---------------------------------------------------------------------------

def identify_available_kpis(filename: str) -> str:
    """
    Analisa o dataset e lista todos os KPIs e métricas que podem ser calculados,
    com uma breve descrição de cada um.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)
    numeric = df.select_dtypes("number").columns.tolist()
    categorical = [c for c in df.select_dtypes("str").columns if c not in ("Country", "City", "State", "Postal Code")]

    kpis = [
        ("Receita Total (Total Sales)", "Soma de todas as vendas brutas.", "Sales"),
        ("Lucro Total (Total Profit)", "Soma do lucro/prejuízo de todos os pedidos.", "Profit"),
        ("Margem de Lucro Geral (%)", "Lucro / Vendas × 100.", "Profit, Sales"),
        ("Ticket Médio (Avg Order Value)", "Média do valor de venda por linha de pedido.", "Sales"),
        ("Volume Total de Itens", "Soma de todas as quantidades vendidas.", "Quantity"),
        ("Desconto Médio (%)", "Média de desconto aplicado.", "Discount"),
        ("Impacto do Desconto no Lucro", "Correlação entre desconto e lucro.", "Discount, Profit"),
        ("Margem por Categoria", "Margem de lucro (%) agrupada por Category.", "Category, Profit, Sales"),
        ("Margem por Subcategoria", "Margem de lucro (%) por Sub-Category, identifica produtos problemáticos.", "Sub-Category, Profit, Sales"),
        ("Vendas por Região", "Receita total por Region.", "Region, Sales"),
        ("Lucro por Região", "Lucro total e margem por Region.", "Region, Profit, Sales"),
        ("Vendas por Segmento", "Receita por Segment (Consumer, Corporate, Home Office).", "Segment, Sales"),
        ("Vendas por Meio de Entrega", "Receita por Ship Mode.", "Ship Mode, Sales"),
        ("Top Produtos mais Lucrativos", "Sub-Categories com maior lucro total.", "Sub-Category, Profit"),
        ("Produtos com Prejuízo", "Sub-Categories com lucro total negativo.", "Sub-Category, Profit"),
        ("Top Estados por Vendas", "States com maior receita.", "State, Sales"),
        ("Taxa de Desconto por Categoria", "Desconto médio aplicado por Category.", "Category, Discount"),
    ]

    lines = [
        f"## KPIs disponíveis para `{filename}`",
        f"> Dataset: **{len(df):,} linhas** | Colunas numéricas: {', '.join(numeric)}",
        f"> Dimensões de corte: {', '.join(categorical)}",
        "",
        "| # | KPI / Métrica | Descrição | Colunas utilizadas |",
        "|---|---------------|-----------|-------------------|",
    ]
    for i, (name, desc, cols) in enumerate(kpis, 1):
        lines.append(f"| {i} | **{name}** | {desc} | `{cols}` |")

    return "\n".join(lines)


def get_kpi_dashboard(filename: str) -> str:
    """
    Retorna um painel completo com os principais KPIs calculados do dataset.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    overall_margin = total_profit / total_sales * 100
    avg_ticket = df["Sales"].mean()
    total_quantity = df["Quantity"].sum()
    avg_discount = df["Discount"].mean() * 100
    n_orders = len(df)
    loss_orders = (df["Profit"] < 0).sum()
    loss_pct = loss_orders / n_orders * 100

    lines = [
        f"## Dashboard de KPIs — `{filename}`",
        "",
        "### Financeiro",
        f"| KPI | Valor |",
        f"|-----|-------|",
        f"| Receita Total | R$ {total_sales:,.2f} |",
        f"| Lucro Total | R$ {total_profit:,.2f} |",
        f"| Margem de Lucro Geral | {overall_margin:.2f}% |",
        f"| Ticket Médio por Linha | R$ {avg_ticket:,.2f} |",
        "",
        "### Volume e Descontos",
        f"| KPI | Valor |",
        f"|-----|-------|",
        f"| Total de Pedidos (linhas) | {n_orders:,} |",
        f"| Volume Total de Itens | {total_quantity:,} |",
        f"| Desconto Médio Aplicado | {avg_discount:.2f}% |",
        f"| Pedidos com Prejuízo | {loss_orders:,} ({loss_pct:.1f}%) |",
    ]

    return "\n".join(lines)


def get_margin_by_dimension(filename: str, dimension: str) -> str:
    """
    Calcula e compara a margem de lucro (%) para cada valor de uma dimensão categórica.
    Útil para identificar quais grupos são mais ou menos rentáveis.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        dimension: Coluna de agrupamento (ex: 'Category', 'Region', 'Sub-Category', 'Segment')
    """
    df = _load_file(filename)
    if dimension not in df.columns:
        available = ", ".join(df.select_dtypes("str").columns)
        return f"Dimensão '{dimension}' não encontrada. Disponíveis: {available}"

    grouped = df.groupby(dimension).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Qtd_Pedidos=("Sales", "count"),
    ).round(2)

    grouped["Margem_%"] = (grouped["Profit"] / grouped["Sales"] * 100).round(2)
    grouped = grouped.sort_values("Margem_%", ascending=False).reset_index()

    return f"### Margem de Lucro por `{dimension}`\n\n" + _df_to_markdown(grouped)


def get_top_performers(filename: str, dimension: str, metric: str = "Profit", n: int = 10) -> str:
    """
    Retorna os N maiores valores de uma métrica agrupada por uma dimensão.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        dimension: Coluna de agrupamento (ex: 'Sub-Category', 'State', 'City')
        metric: Coluna numérica a ranquear — 'Sales', 'Profit' ou 'Quantity' (padrão: 'Profit')
        n: Quantidade de itens a retornar (padrão: 10)
    """
    df = _load_file(filename)
    for col in (dimension, metric):
        if col not in df.columns:
            return f"Coluna '{col}' não encontrada."

    result = (
        df.groupby(dimension)[metric]
        .sum()
        .round(2)
        .nlargest(int(n))
        .reset_index()
        .rename(columns={metric: f"Total_{metric}"})
    )
    return f"### Top {n} por `{metric}` — dimensão `{dimension}`\n\n" + _df_to_markdown(result)


def get_bottom_performers(filename: str, dimension: str, metric: str = "Profit", n: int = 10) -> str:
    """
    Retorna os N piores valores de uma métrica agrupada por uma dimensão.
    Ideal para detectar produtos, regiões ou segmentos com baixo desempenho.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        dimension: Coluna de agrupamento (ex: 'Sub-Category', 'State', 'City')
        metric: Coluna numérica a ranquear — 'Sales', 'Profit' ou 'Quantity' (padrão: 'Profit')
        n: Quantidade de itens a retornar (padrão: 10)
    """
    df = _load_file(filename)
    for col in (dimension, metric):
        if col not in df.columns:
            return f"Coluna '{col}' não encontrada."

    result = (
        df.groupby(dimension)[metric]
        .sum()
        .round(2)
        .nsmallest(int(n))
        .reset_index()
        .rename(columns={metric: f"Total_{metric}"})
    )
    return f"### Bottom {n} por `{metric}` — dimensão `{dimension}`\n\n" + _df_to_markdown(result)


def detect_loss_makers(filename: str, dimension: str = "Sub-Category") -> str:
    """
    Identifica grupos com lucro total negativo (geradores de prejuízo).

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        dimension: Coluna de agrupamento (padrão: 'Sub-Category')
    """
    df = _load_file(filename)
    if dimension not in df.columns:
        available = ", ".join(df.select_dtypes("str").columns)
        return f"Dimensão '{dimension}' não encontrada. Disponíveis: {available}"

    grouped = df.groupby(dimension).agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Qtd_Pedidos=("Sales", "count"),
    ).round(2)
    grouped["Margem_%"] = (grouped["Total_Profit"] / grouped["Total_Sales"] * 100).round(2)
    loss = grouped[grouped["Total_Profit"] < 0].sort_values("Total_Profit").reset_index()

    if loss.empty:
        return f"Nenhum grupo com prejuízo encontrado em `{dimension}`."

    return (
        f"### Grupos com Prejuízo em `{dimension}` ({len(loss)} encontrado(s))\n\n"
        + _df_to_markdown(loss)
    )


def get_discount_impact(filename: str) -> str:
    """
    Analisa o impacto do desconto na margem de lucro, agrupando pedidos por faixas de desconto.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)

    bins = [-0.001, 0.0, 0.1, 0.2, 0.3, 0.5, 1.01]
    labels = ["0% (sem desconto)", "1–10%", "11–20%", "21–30%", "31–50%", "51–100%"]
    df = df.copy()
    df["Faixa_Desconto"] = pd.cut(df["Discount"], bins=bins, labels=labels)

    result = (
        df.groupby("Faixa_Desconto", observed=True)
        .agg(
            Qtd_Pedidos=("Sales", "count"),
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
        )
        .round(2)
    )
    result["Margem_%"] = (result["Total_Profit"] / result["Total_Sales"] * 100).round(2)
    result = result.reset_index()

    return "### Impacto do Desconto na Margem de Lucro\n\n" + _df_to_markdown(result)


# ---------------------------------------------------------------------------
# Lista de tools exportável
# ---------------------------------------------------------------------------

METRICS_TOOLS = [
    identify_available_kpis,
    get_kpi_dashboard,
    get_margin_by_dimension,
    get_top_performers,
    get_bottom_performers,
    detect_loss_makers,
    get_discount_impact,
]

# ---------------------------------------------------------------------------
# Agente interativo (execução direta)
# ---------------------------------------------------------------------------

INSTRUCTIONS = """
Você é um analista de negócios especialista em métricas e KPIs de vendas.

Seu trabalho é identificar, calcular e interpretar indicadores de desempenho
a partir dos dados disponíveis na pasta data/.

Ao responder:
- Sempre comece identificando os KPIs disponíveis se o usuário não souber o que pedir.
- Use as tools para calcular os números e apresente-os em tabelas.
- Após exibir os dados, adicione uma breve análise interpretando os resultados
  (o que está bem, o que merece atenção, possíveis causas).
- Sempre informe o nome do arquivo ao chamar as tools.
"""

if __name__ == "__main__":
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=METRICS_TOOLS,
        markdown=True,
        instructions=INSTRUCTIONS,
    )

    print("Analista de métricas e KPIs iniciado. Digite 'sair' para encerrar.\n")

    while True:
        prompt = input("Pergunta: ").strip()
        if not prompt:
            continue
        if prompt.lower() in ("sair", "exit", "quit"):
            print("Encerrando.")
            break
        agent.print_response(prompt, stream=True)
