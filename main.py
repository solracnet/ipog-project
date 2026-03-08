from agno.agent import Agent
from agno.models.groq import Groq
from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------------------------------------------
# Create Agent
# ---------------------------------------------------------------------------
agent = Agent(model=Groq(id="llama-3.3-70b-versatile"), markdown=True)

# ---------------------------------------------------------------------------
# Run Agent
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    user_prompt = input("Digite sua pergunta: ")

    # --- Sync + Streaming ---
    agent.print_response(user_prompt, stream=True)