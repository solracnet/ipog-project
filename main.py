from agno.agent import Agent
from agno.db.sqlite import SqliteDb
from agno.models.groq import Groq
from dotenv import load_dotenv

from agents.ceo_report import CEO_REPORT_TOOLS
from agents.excel_analyst import EXCEL_TOOLS
from agents.metrics_agent import METRICS_TOOLS
from agents.products_report import PRODUCTS_REPORT_TOOLS
from agents.sales_report import SALES_REPORT_TOOLS

load_dotenv()

# ---------------------------------------------------------------------------
# Banco de dados SQLite para histórico de sessões
# ---------------------------------------------------------------------------
db = SqliteDb(db_file="db/history.db")

# ---------------------------------------------------------------------------
# Criação do Agente com as tools registradas
# ---------------------------------------------------------------------------
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
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

# ---------------------------------------------------------------------------
# Ponto de entrada — loop de interação com o usuário
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    from pathlib import Path

    Path("db").mkdir(exist_ok=True)

    # Permite retomar uma sessão existente via argumento: python main.py <session_id>
    session_id = sys.argv[1] if len(sys.argv) > 1 else None

    if session_id:
        print(f"Retomando sessão: {session_id}\n")
    else:
        print("Nova sessão iniciada. Para retomar depois, anote o Session ID exibido.\n")

    print("Agente de relatórios de vendas iniciado. Digite 'sair' para encerrar.\n")

    while True:
        user_prompt = input("Digite sua pergunta: ").strip()

        if user_prompt.lower() in ("sair", "exit", "quit"):
            print(f"\nSessão encerrada. Session ID: {agent.session_id}")
            break

        if not user_prompt:
            continue

        agent.print_response(user_prompt, stream=True, session_id=session_id)

        # Após a primeira resposta, usa o session_id gerado pelo agente
        if session_id is None:
            session_id = agent.session_id
            print(f"\n[Session ID: {session_id}]\n")
