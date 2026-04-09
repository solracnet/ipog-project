from dotenv import load_dotenv

from agents.agno_workflow import AnalyticsWorkflow

import sys
from pathlib import Path

load_dotenv()

# ---------------------------------------------------------------------------
# Ponto de entrada — loop de interação com o usuário
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    Path("db").mkdir(exist_ok=True)

    analytics = AnalyticsWorkflow()
    workflow = analytics.workflow

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
            print(f"\nSessão encerrada. Session ID: {workflow.session_id}")
            break

        if not user_prompt:
            continue

        workflow.print_response(
            user_prompt,
            stream=True,
            session_id=session_id,
        )

        # Após a primeira resposta, usa o session_id gerado pelo workflow
        if session_id is None:
            session_id = workflow.session_id
            print(f"\n[Session ID: {session_id}]\n")
