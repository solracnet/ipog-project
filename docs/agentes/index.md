# Agentes Especializados

O projeto possui cinco agentes especializados, cada um com um conjunto de tools Python focado em um domínio específico. Todos compartilham o mesmo modelo LLM configurado via `model_factory.py` e produzem respostas em Markdown.

## Resumo

| Agente | Arquivo | Tools | Domínio |
|---|---|---|---|
| Analista de Dados | `excel_analyst.py` | 8 | Leitura e inspeção de arquivos CSV/Excel |
| Analista de Métricas | `metrics_agent.py` | 7 | KPIs, dashboards e indicadores |
| Analista Executivo | `ceo_report.py` | 6 | Relatório estratégico para o CEO |
| Analista de Vendas | `sales_report.py` | 10 | Performance comercial |
| Analista de Produtos | `products_report.py` | 10 | Portfólio e rentabilidade |

**Total: 41 tools**

## Padrão de Tools

Todas as tools seguem o padrão de funções Python registradas no Agno:

- Recebem `filename` como primeiro parâmetro (nome do arquivo em `data/`)
- Leem e processam o CSV com Pandas
- Retornam strings formatadas ou dicionários serializáveis
- São registradas na lista `*_TOOLS` exportada por cada módulo

## Roteamento

No `AnalyticsWorkflow`, o Router identifica automaticamente qual agente deve responder com base em palavras-chave na pergunta do usuário. Veja a página [Workflow](../workflow.md) para detalhes.
