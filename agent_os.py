from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from dotenv import load_dotenv

from agents.ceo_report import CEO_REPORT_TOOLS
from agents.excel_analyst import EXCEL_TOOLS
from agents.metrics_agent import METRICS_TOOLS
from agents.model_factory import get_model
from agents.products_report import PRODUCTS_REPORT_TOOLS
from agents.sales_report import SALES_REPORT_TOOLS

import sys
from pathlib import Path

load_dotenv()

# ---------------------------------------------------------------------------
# Banco de dados SQLite para histórico de sessões
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="db/history.db")

# ---------------------------------------------------------------------------
# Criação do Agente com as tools registradas
# ---------------------------------------------------------------------------
agent = Agent(
    model=get_model(),
    tools=[*EXCEL_TOOLS, *METRICS_TOOLS, *CEO_REPORT_TOOLS, *SALES_REPORT_TOOLS, *PRODUCTS_REPORT_TOOLS],
    db=db,
    add_history_to_context=True,
    enable_user_memories=True,
    # add_memories_to_context=True,
    # enable_agentic_memory=True,
    markdown=True,
    instructions=(
        "Você é um analista de dados. Utilize as tools disponíveis para ler e interpretar "
        "arquivos da pasta data/. Sempre informe o nome do arquivo ao chamar as tools. "
        "Apresente os resultados de forma clara e objetiva, usando tabelas quando apropriado."
    ),
)

agent_os = AgentOS(
    id="ipog_project",
    description="Agente para análise de dados de vendas, produtos e métricas, com foco em relatórios para CEO.",
    agents=[agent],
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="agent_os:app", reload=True)