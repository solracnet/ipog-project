"""
Geração automática dos relatórios CEO, Vendas e Produtos em sequência.

Executa os três agentes sem interação do usuário e salva cada relatório
como arquivo Markdown em reports/.

Uso:
    python generate_reports.py
    python generate_reports.py data/SampleSuperstore.csv   # arquivo alternativo
"""

import sys
import threading
from datetime import datetime
from pathlib import Path
from time import monotonic

from agno.agent import Agent
from dotenv import load_dotenv
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.rule import Rule
from rich.text import Text

from agents.ceo_report import CEO_REPORT_TOOLS, INSTRUCTIONS as CEO_INSTRUCTIONS
from agents.model_factory import get_model
from agents.products_report import PRODUCTS_REPORT_TOOLS, INSTRUCTIONS as PRODUCTS_INSTRUCTIONS
from agents.sales_report import SALES_REPORT_TOOLS, INSTRUCTIONS as SALES_INSTRUCTIONS

load_dotenv()

console = Console()

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

DATA_FILE = Path(sys.argv[1]).name if len(sys.argv) > 1 else "SampleSuperstore.csv"
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(exist_ok=True)

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

REPORTS = [
    {
        "label": "CEO",
        "tools": CEO_REPORT_TOOLS,
        "instructions": CEO_INSTRUCTIONS,
        "prompt": (
            f"Gere o relatório executivo completo usando o arquivo {DATA_FILE}. "
            "Siga exatamente o protocolo e o template definidos nas instruções."
        ),
        "output": REPORTS_DIR / f"{TIMESTAMP}_ceo_report.md",
    },
    {
        "label": "Vendas",
        "tools": SALES_REPORT_TOOLS,
        "instructions": SALES_INSTRUCTIONS,
        "prompt": (
            f"Gere o relatório de vendas completo usando o arquivo {DATA_FILE}. "
            "Siga exatamente o protocolo e o template definidos nas instruções."
        ),
        "output": REPORTS_DIR / f"{TIMESTAMP}_sales_report.md",
    },
    {
        "label": "Produtos",
        "tools": PRODUCTS_REPORT_TOOLS,
        "instructions": PRODUCTS_INSTRUCTIONS,
        "prompt": (
            f"Gere o relatório de produtos completo usando o arquivo {DATA_FILE}. "
            "Siga exatamente o protocolo e o template definidos nas instruções."
        ),
        "output": REPORTS_DIR / f"{TIMESTAMP}_products_report.md",
    },
]

# ---------------------------------------------------------------------------
# Execução
# ---------------------------------------------------------------------------

def _run_agent(config: dict, result: dict) -> None:
    """Executa o agente e armazena o resultado em `result`."""
    agent = Agent(
        model=get_model(),
        tools=config["tools"],
        instructions=config["instructions"],
        markdown=True,
    )
    response = agent.run(config["prompt"])
    result["content"] = response.content if response.content else ""


def run_report(config: dict, index: int, total: int) -> float:
    """Exibe spinner durante o processamento e retorna o tempo decorrido."""
    label = config["label"]
    output_path: Path = config["output"]
    result: dict = {}

    progress = Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]{task.description}"),
        BarColumn(bar_width=20),
        TimeElapsedColumn(),
        console=console,
        transient=True,
    )

    task_desc = f"[{index}/{total}] Relatório {label}"

    with progress:
        task = progress.add_task(task_desc, total=None)
        start = monotonic()

        thread = threading.Thread(target=_run_agent, args=(config, result), daemon=True)
        thread.start()
        while thread.is_alive():
            progress.update(task, advance=0.1)
            thread.join(timeout=0.1)

        elapsed = monotonic() - start

    content = result.get("content", "")
    output_path.write_text(content, encoding="utf-8")

    status = Text()
    status.append(f"[{index}/{total}] ", style="dim")
    status.append(f"Relatório {label}", style="bold white")
    status.append("  concluído", style="bold green")
    status.append(f"  ({elapsed:.1f}s)", style="dim")
    status.append(f"  → {output_path}", style="dim cyan")
    console.print(status)

    return elapsed


if __name__ == "__main__":
    console.print()
    console.print(Rule("[bold white]Geração de Relatórios[/bold white]"))
    console.print(f"  Arquivo : [cyan]{DATA_FILE}[/cyan]")
    console.print(f"  Destino : [cyan]{REPORTS_DIR}/[/cyan]")
    console.print(f"  Modelos : [cyan]{len(REPORTS)} relatórios[/cyan]")
    console.print(Rule())
    console.print()

    total = len(REPORTS)
    total_elapsed = 0.0

    for i, report_config in enumerate(REPORTS, start=1):
        total_elapsed += run_report(report_config, i, total)

    console.print()
    console.print(Rule("[bold green]Concluído[/bold green]"))
    console.print(f"  Tempo total : [green]{total_elapsed:.1f}s[/green]")
    console.print(f"  Relatórios  : [cyan]{REPORTS_DIR}/[/cyan]")
    console.print(Rule())
    console.print()
