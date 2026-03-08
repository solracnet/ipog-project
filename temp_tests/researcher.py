from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.tavily import TavilyTools

from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    tools=[TavilyTools()],
    model=Groq(id="llama-3.3-70b-versatile"),
    markdown=True
)
agent.print_response("Use suas ferramentas para pesquisar qual é o ticket da ação da petrobras para negociar na bolsa de valores brasileira.")

