"""
Workflow Agno — IPOG Analytics Workflow

Orquestra o IPOG Analytics Team usando o framework Workflow do Agno.

Estrutura do workflow:
  1. Step "Preparação"  — normaliza a entrada e injeta o arquivo padrão se ausente
  2. Router "Roteador"  — classifica a intenção e delega ao agente especialista correto:
       • Analista de Dados     → consultas sobre arquivos, esquemas e amostras
       • Analista de Métricas  → KPIs, dashboards e indicadores de desempenho
       • Analista Executivo    → relatório estratégico para o CEO
       • Analista de Vendas    → performance comercial por região e segmento
       • Analista de Produtos  → portfólio de produtos e rentabilidade
       • Team Completo         → perguntas mistas ou que exigem múltiplas perspectivas
"""

from agno.db.sqlite import SqliteDb
from agno.workflow import Workflow
from agno.workflow.router import Router
from agno.workflow.step import Step
from agno.workflow.types import StepInput, StepOutput
from dotenv import load_dotenv

from agents.agno_teams import agno_teams

load_dotenv()

_DEFAULT_FILE = "SampleSuperstore.csv"

# ---------------------------------------------------------------------------
# Palavras-chave por domínio — usadas pelo roteador de intenção
# ---------------------------------------------------------------------------

_KEYWORDS_DADOS = {
    "dados", "arquivo", "schema", "esquema", "colunas", "coluna",
    "amostra", "lista", "listar", "inspecionar", "sample", "tipos",
}
_KEYWORDS_METRICAS = {
    "métrica", "metrica", "kpi", "kpis", "dashboard", "indicador",
    "indicadores", "desempenho", "performance", "margem",
}
_KEYWORDS_CEO = {
    "ceo", "executivo", "estrateg", "pareto", "saúde", "saude",
    "saúde do negócio", "negócio", "resumo executivo", "alto nível",
}
_KEYWORDS_VENDAS = {
    "venda", "vendas", "região", "regiao", "segmento", "entrega",
    "desconto", "período", "periodo", "cidade", "estado", "ship",
    "ranking", "canal", "comercial",
}
_KEYWORDS_PRODUTOS = {
    "produto", "produtos", "categoria", "categorias", "subcategoria",
    "subcategorias", "portfólio", "portfolio", "prejuízo", "prejuizo",
    "lucro", "rentabilidade", "lucratividade",
}


def _contains_any(text: str, keywords: set) -> bool:
    return any(kw in text for kw in keywords)


# ---------------------------------------------------------------------------
# Step 1 — Preparação: normaliza entrada e injeta arquivo padrão
# ---------------------------------------------------------------------------

def _prepare_input(step_input: StepInput) -> StepOutput:
    """
    Garante que o arquivo padrão esteja mencionado na entrada do usuário.
    Evita que os agentes peçam o nome do arquivo em toda chamada.
    """
    text = (step_input.input or "").strip()

    if _DEFAULT_FILE.lower() not in text.lower() and ".csv" not in text.lower():
        enriched = f"{text}\n\n> **Arquivo:** {_DEFAULT_FILE}"
    else:
        enriched = text

    return StepOutput(content=enriched, success=True)


# ---------------------------------------------------------------------------
# Classe principal
# ---------------------------------------------------------------------------

class AnalyticsWorkflow:
    """
    Workflow de análise de dados IPOG.

    Uso:
        wf = AnalyticsWorkflow()
        wf.workflow.print_response("Gere o relatório de vendas", stream=True)
    """

    def __init__(self, db_path: str = "db/history.db"):
        self._teams = agno_teams()

        # ------------------------------------------------------------------
        # Steps para cada agente especialista
        # ------------------------------------------------------------------

        step_dados = Step(
            name="Dados",
            description="Leitura e inspeção de arquivos CSV/Excel",
            agent=self._teams.data_analyst,
        )
        step_metricas = Step(
            name="Métricas",
            description="KPIs e indicadores de performance",
            agent=self._teams.metrics_analyst,
        )
        step_ceo = Step(
            name="Executivo",
            description="Relatório estratégico para o CEO",
            agent=self._teams.ceo_analyst,
        )
        step_vendas = Step(
            name="Vendas",
            description="Relatório comercial por região e segmento",
            agent=self._teams.sales_analyst,
        )
        step_produtos = Step(
            name="Produtos",
            description="Análise de portfólio e rentabilidade",
            agent=self._teams.products_analyst,
        )
        step_team = Step(
            name="Team Completo",
            description="Coordenação completa entre todos os especialistas",
            team=self._teams.team,
        )

        # ------------------------------------------------------------------
        # Roteador de intenção
        # ------------------------------------------------------------------

        all_choices = [
            step_dados,
            step_metricas,
            step_ceo,
            step_vendas,
            step_produtos,
            step_team,
        ]

        def route_intent(step_input: StepInput):
            """Classifica a intenção e retorna o Step especialista correspondente."""
            # Usa o conteúdo enriquecido da etapa anterior, se disponível
            text = (step_input.previous_step_content or step_input.input or "").lower()

            if _contains_any(text, _KEYWORDS_DADOS):
                return [step_dados]
            if _contains_any(text, _KEYWORDS_METRICAS):
                return [step_metricas]
            if _contains_any(text, _KEYWORDS_CEO):
                return [step_ceo]
            if _contains_any(text, _KEYWORDS_VENDAS):
                return [step_vendas]
            if _contains_any(text, _KEYWORDS_PRODUTOS):
                return [step_produtos]

            # Fallback: delega ao Team completo para perguntas mistas
            return [step_team]

        router = Router(
            name="Roteador de Intenção",
            description=(
                "Analisa a pergunta e direciona ao especialista mais adequado: "
                "Dados, Métricas, Executivo, Vendas, Produtos ou Team Completo."
            ),
            selector=route_intent,
            choices=all_choices,
        )

        # ------------------------------------------------------------------
        # Workflow
        # ------------------------------------------------------------------

        self.workflow = Workflow(
            name="IPOG Analytics Workflow",
            description=(
                "Workflow de análise de dados de vendas da IPOG. "
                "Classifica a intenção do usuário e delega ao agente especialista correto."
            ),
            db=SqliteDb(db_file=db_path),
            steps=[
                Step(
                    name="Preparação",
                    description="Normaliza a entrada e injeta o arquivo padrão se ausente",
                    executor=_prepare_input,
                ),
                router,
            ],
        )
