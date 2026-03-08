from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.yfinance import YFinanceTools

from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    tools=[YFinanceTools()],
    model=Groq(id="llama-3.3-70b-versatile"),
    markdown=True,
    instructions="Utilize uma tabela para exibir a informação atual"
)
agent.print_response("Qual é a cotação da Petrobras na ibovespa hoje?")

