"""
Tool de análise de arquivos Excel/CSV para o agente Agno.

Funcionalidades:
- Listar arquivos disponíveis na pasta data/
- Exibir esquema (colunas e tipos) de um arquivo
- Mostrar amostra dos dados
- Gerar resumo estatístico de colunas numéricas
- Listar valores únicos de colunas categóricas
- Agrupar e agregar dados por uma coluna
- Filtrar dados por valor específico
- Buscar por termo em colunas de texto

As funções abaixo são registradas como tools no agente e podem ser importadas
por outros módulos do projeto.
"""

import json
from pathlib import Path

import pandas as pd
from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = Path(__file__).parent.parent / "data"

# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _load_file(filename: str) -> pd.DataFrame:
    """Carrega um arquivo CSV ou Excel da pasta data/ e retorna um DataFrame."""
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Arquivo '{filename}' não encontrado em {DATA_DIR}")
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(path)
    raise ValueError(f"Formato '{suffix}' não suportado. Use .csv, .xlsx ou .xls")


def _df_to_markdown(df: pd.DataFrame, max_rows: int = 50) -> str:
    """Converte um DataFrame para Markdown, respeitando um limite de linhas."""
    if len(df) > max_rows:
        preview = df.head(max_rows)
        footer = f"\n_(exibindo {max_rows} de {len(df)} linhas)_"
    else:
        preview = df
        footer = ""
    return preview.to_markdown(index=False) + footer


# ---------------------------------------------------------------------------
# Tools do agente
# ---------------------------------------------------------------------------

def list_available_files() -> str:
    """
    Lista todos os arquivos CSV e Excel disponíveis na pasta data/.
    Use esta tool para descobrir quais arquivos podem ser analisados.
    """
    files = sorted(
        p.name
        for p in DATA_DIR.iterdir()
        if p.suffix.lower() in (".csv", ".xlsx", ".xls")
    )
    if not files:
        return "Nenhum arquivo CSV ou Excel encontrado em data/."
    return "Arquivos disponíveis em data/:\n" + "\n".join(f"- {f}" for f in files)


def get_file_schema(filename: str) -> str:
    """
    Retorna o esquema do arquivo: colunas, tipos de dados e quantidade de linhas.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)
    schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
    lines = [
        f"**Arquivo:** {filename}",
        f"**Linhas:** {len(df):,}  |  **Colunas:** {len(df.columns)}",
        "",
        "| Coluna | Tipo |",
        "|--------|------|",
    ]
    for col, dtype in schema.items():
        lines.append(f"| {col} | {dtype} |")
    return "\n".join(lines)


def get_data_sample(filename: str, n_rows: int = 10) -> str:
    """
    Retorna as primeiras N linhas do arquivo para inspecionar os dados.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        n_rows: Quantidade de linhas a retornar (padrão: 10)
    """
    df = _load_file(filename)
    return _df_to_markdown(df.head(int(n_rows)))


def get_statistical_summary(filename: str) -> str:
    """
    Retorna um resumo estatístico (count, mean, min, max, std) das colunas numéricas.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
    """
    df = _load_file(filename)
    summary = df.describe().round(2)
    return _df_to_markdown(summary.reset_index().rename(columns={"index": "Estatística"}))


def get_unique_values(filename: str, column: str) -> str:
    """
    Lista os valores únicos de uma coluna categórica com suas contagens.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        column: Nome da coluna a inspecionar
    """
    df = _load_file(filename)
    if column not in df.columns:
        available = ", ".join(df.columns)
        return f"Coluna '{column}' não encontrada. Colunas disponíveis: {available}"
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "Contagem"]
    return _df_to_markdown(counts)


def aggregate_data(
    filename: str,
    group_by: str,
    agg_column: str,
    operation: str = "sum",
) -> str:
    """
    Agrupa os dados por uma coluna e aplica uma operação de agregação.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        group_by: Coluna para agrupar (ex: 'Region', 'Category')
        agg_column: Coluna numérica a agregar (ex: 'Sales', 'Profit')
        operation: Operação de agregação — 'sum', 'mean', 'min', 'max', 'count' (padrão: 'sum')
    """
    df = _load_file(filename)

    for col in (group_by, agg_column):
        if col not in df.columns:
            available = ", ".join(df.columns)
            return f"Coluna '{col}' não encontrada. Colunas disponíveis: {available}"

    allowed = {"sum", "mean", "min", "max", "count"}
    if operation not in allowed:
        return f"Operação '{operation}' inválida. Use: {', '.join(sorted(allowed))}"

    result = (
        df.groupby(group_by)[agg_column]
        .agg(operation)
        .round(2)
        .reset_index()
        .rename(columns={agg_column: f"{operation}({agg_column})"})
        .sort_values(f"{operation}({agg_column})", ascending=False)
    )
    return _df_to_markdown(result)


def filter_data(filename: str, column: str, value: str, n_rows: int = 20) -> str:
    """
    Filtra as linhas onde uma coluna é igual ao valor informado.

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        column: Coluna a filtrar (ex: 'Region')
        value: Valor a buscar (ex: 'West')
        n_rows: Máximo de linhas a retornar (padrão: 20)
    """
    df = _load_file(filename)
    if column not in df.columns:
        available = ", ".join(df.columns)
        return f"Coluna '{column}' não encontrada. Colunas disponíveis: {available}"

    filtered = df[df[column].astype(str).str.lower() == value.lower()]
    if filtered.empty:
        return f"Nenhuma linha encontrada onde {column} = '{value}'."
    return f"**{len(filtered)} linha(s) encontrada(s):**\n\n" + _df_to_markdown(filtered, max_rows=int(n_rows))


def search_in_data(filename: str, column: str, term: str, n_rows: int = 20) -> str:
    """
    Busca linhas onde uma coluna contém um termo (busca parcial, sem distinção de maiúsculas).

    Args:
        filename: Nome do arquivo (ex: 'SampleSuperstore.csv')
        column: Coluna onde buscar (ex: 'Sub-Category')
        term: Termo a buscar (ex: 'chair')
        n_rows: Máximo de linhas a retornar (padrão: 20)
    """
    df = _load_file(filename)
    if column not in df.columns:
        available = ", ".join(df.columns)
        return f"Coluna '{column}' não encontrada. Colunas disponíveis: {available}"

    mask = df[column].astype(str).str.contains(term, case=False, na=False)
    result = df[mask]
    if result.empty:
        return f"Nenhum resultado para '{term}' na coluna '{column}'."
    return f"**{len(result)} linha(s) encontrada(s):**\n\n" + _df_to_markdown(result, max_rows=int(n_rows))


# ---------------------------------------------------------------------------
# Agente interativo (execução direta)
# ---------------------------------------------------------------------------

EXCEL_TOOLS = [
    list_available_files,
    get_file_schema,
    get_data_sample,
    get_statistical_summary,
    get_unique_values,
    aggregate_data,
    filter_data,
    search_in_data,
]

if __name__ == "__main__":
    agent = Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=EXCEL_TOOLS,
        markdown=True,
        instructions=(
            "Você é um analista de dados. Utilize as tools disponíveis para ler e interpretar "
            "arquivos da pasta data/. Sempre informe o nome do arquivo ao chamar as tools. "
            "Apresente os resultados de forma clara e objetiva, usando tabelas quando apropriado."
        ),
    )

    print("Analista de planilhas iniciado. Digite 'sair' para encerrar.\n")

    while True:
        prompt = input("Pergunta: ").strip()
        if not prompt:
            continue
        if prompt.lower() in ("sair", "exit", "quit"):
            print("Encerrando.")
            break
        agent.print_response(prompt, stream=True)
