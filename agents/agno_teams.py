"""
Team Agno — IPOG Analytics Team

Orquestra os agentes especialistas usando o framework Teams do Agno.
O Team coordena automaticamente qual membro deve responder a cada pergunta,
delegando análises de dados, métricas, relatórios executivos, vendas e produtos
aos agentes correspondentes.

Modo: coordinate — o Team leader distribui o trabalho entre os membros e
consolida as respostas em uma saída coerente.
"""

from agno.agent import Agent
from agno.team import Team
from agno.team.team import TeamMode
from dotenv import load_dotenv

from agents.ceo_report import CEO_REPORT_TOOLS, INSTRUCTIONS as CEO_INSTRUCTIONS
from agents.excel_analyst import EXCEL_TOOLS
from agents.metrics_agent import METRICS_TOOLS, INSTRUCTIONS as METRICS_INSTRUCTIONS
from agents.model_factory import get_model
from agents.products_report import PRODUCTS_REPORT_TOOLS, INSTRUCTIONS as PRODUCTS_INSTRUCTIONS
from agents.sales_report import SALES_REPORT_TOOLS, INSTRUCTIONS as SALES_INSTRUCTIONS

load_dotenv()


class agno_teams:
    """
    Team de análise de dados e relatórios de vendas.

    Membros:
    - Analista de Dados    : leitura e inspeção de arquivos CSV/Excel
    - Analista de Métricas : KPIs e dashboards de performance
    - Analista Executivo   : relatório estratégico para o CEO
    - Analista de Vendas   : relatórios comerciais por região e segmento
    - Analista de Produtos : relatórios de portfólio e rentabilidade
    """

    def __init__(self, model=None):
        if model is None:
            model = get_model()

        # ------------------------------------------------------------------
        # Membros do team
        # ------------------------------------------------------------------

        self.data_analyst = Agent(
            name="Analista de Dados",
            role=(
                "Especialista em leitura e inspeção de arquivos CSV e Excel. "
                "Responsável por listar arquivos disponíveis, exibir esquemas, "
                "amostras e estatísticas dos datasets."
            ),
            model=model,
            tools=EXCEL_TOOLS,
            markdown=True,
            instructions=(
                "Você é um analista de dados. Utilize as tools disponíveis para ler e interpretar "
                "arquivos da pasta data/. Sempre informe o nome do arquivo ao chamar as tools. "
                "Apresente os resultados de forma clara e objetiva, usando tabelas quando apropriado."
            ),
        )

        self.metrics_analyst = Agent(
            name="Analista de Métricas",
            role=(
                "Especialista em KPIs e indicadores de performance. "
                "Calcula margens, dashboards de KPIs, top/bottom performers "
                "e analisa o impacto de descontos na rentabilidade."
            ),
            model=model,
            tools=METRICS_TOOLS,
            markdown=True,
            instructions=METRICS_INSTRUCTIONS,
        )

        self.ceo_analyst = Agent(
            name="Analista Executivo",
            role=(
                "Especialista em relatórios estratégicos para o CEO. "
                "Gera resumos executivos, KPIs de alto nível, análise de Pareto, "
                "top estados por receita e indicadores de saúde do negócio."
            ),
            model=model,
            tools=CEO_REPORT_TOOLS,
            markdown=True,
            instructions=CEO_INSTRUCTIONS,
        )

        self.sales_analyst = Agent(
            name="Analista de Vendas",
            role=(
                "Especialista em análise comercial. "
                "Reporta desempenho de vendas por região, segmento, meio de entrega "
                "e período, além de ranking e impacto de descontos."
            ),
            model=model,
            tools=SALES_REPORT_TOOLS,
            markdown=True,
            instructions=SALES_INSTRUCTIONS,
        )

        self.products_analyst = Agent(
            name="Analista de Produtos",
            role=(
                "Especialista em análise de portfólio. "
                "Avalia categorias e subcategorias de produtos, identifica itens com prejuízo, "
                "analisa desconto por categoria e cruza volume com rentabilidade."
            ),
            model=model,
            tools=PRODUCTS_REPORT_TOOLS,
            markdown=True,
            instructions=PRODUCTS_INSTRUCTIONS,
        )

        # ------------------------------------------------------------------
        # Team
        # ------------------------------------------------------------------

        self.team = Team(
            name="IPOG Analytics Team",
            role=(
                "Equipe de análise de dados e geração de relatórios de vendas. "
                "Coordena especialistas em dados, métricas, relatórios executivos, "
                "vendas e produtos para responder perguntas de negócio de forma completa e precisa."
            ),
            mode=TeamMode.coordinate,
            model=model,
            members=[
                self.data_analyst,
                self.metrics_analyst,
                self.ceo_analyst,
                self.sales_analyst,
                self.products_analyst,
            ],
            markdown=True,
            show_members_responses=True,
            instructions=(
                "Você é o coordenador da equipe de análise de dados do IPOG. "
                "Receba a pergunta do usuário, identifique qual(is) especialista(s) deve(m) "
                "ser acionado(s) e consolide as respostas em uma análise coerente e objetiva. "
                "Use o Analista de Dados para inspeção de arquivos, o Analista de Métricas para KPIs, "
                "o Analista Executivo para visão estratégica, o Analista de Vendas para performance "
                "comercial e o Analista de Produtos para análise de portfólio. "
                "Sempre informe o nome do arquivo (ex: 'SampleSuperstore.csv') ao delegar tarefas. "
                "Apresente os resultados de forma clara, usando tabelas e seções em Markdown."
            ),
        )
