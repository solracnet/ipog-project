from agno.db.sqlite import SqliteDb
from agno.os import AgentOS
from dotenv import load_dotenv

from agents.agno_workflow import AnalyticsWorkflow

from pathlib import Path

load_dotenv()

Path("db").mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Workflow principal
# ---------------------------------------------------------------------------
analytics = AnalyticsWorkflow(db_path="db/history.db")

# ---------------------------------------------------------------------------
# AgentOS expondo o workflow via API
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    id="ipog_project",
    name="IPOG Analytics",
    description=(
        "Plataforma de análise de dados de vendas da IPOG. "
        "Orquestra especialistas em dados, métricas, relatórios executivos, "
        "vendas e produtos via workflow inteligente."
    ),
    db=SqliteDb(db_file="db/history.db"),
    workflows=[analytics.workflow],
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="agno_os:app", reload=True)
