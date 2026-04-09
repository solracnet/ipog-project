# Testes

O projeto conta com uma suíte de testes automatizados cobrindo todos os agentes, o Team e o Workflow.

## Executar

```bash
# Todos os testes
uv run pytest tests/ -v

# Agente específico
uv run pytest tests/test_excel_analyst.py -v
uv run pytest tests/test_metrics_agent.py -v
uv run pytest tests/test_ceo_report.py -v
uv run pytest tests/test_sales_report.py -v
uv run pytest tests/test_products_report.py -v
uv run pytest tests/test_agno_teams.py -v
uv run pytest tests/test_agno_workflow.py -v
```

## Cobertura

| Arquivo | Testes | Escopo |
|---|---|---|
| `test_excel_analyst.py` | 31 | Carregamento, helpers internos e todas as 8 tools |
| `test_metrics_agent.py` | 28 | Todas as 7 tools de KPIs e métricas |
| `test_ceo_report.py` | 24 | Todas as 6 tools do relatório executivo |
| `test_sales_report.py` | 33 | Todas as 10 tools de vendas |
| `test_products_report.py` | 30 | Todas as 10 tools de produtos |
| `test_agno_teams.py` | 22 | Instanciação, membros, tools e modo do team |
| `test_agno_workflow.py` | 28 | Helpers, keywords, roteamento e workflow |
| **Total** | **196** | |

## O que é validado

- **Happy path** — resposta correta para entradas válidas
- **Mensagens de erro** — entradas inválidas retornam mensagens descritivas
- **Coerção de tipos** — o LLM pode passar inteiros como strings; as tools tratam corretamente
- **Colunas ausentes** — comportamento esperado quando o dataset não tem a coluna solicitada

## Testes do Team (`test_agno_teams.py`)

```python
class TestAgnoTeamsInstantiation:
    # instanciação com modelo padrão e explícito
    # nome, modo (coordinate), role e markdown

class TestAgnoTeamsMembers:
    # 5 membros com nome, role, tools e instruções corretas
    # contagem de tools por membro corresponde à lista exportada
```

## Testes do Workflow (`test_agno_workflow.py`)

```python
class TestContainsAny:
    # helper de detecção de palavras-chave

class TestPrepareInput:
    # injeção do arquivo padrão
    # não duplica se arquivo já presente
    # preserva texto original

class TestRoutingKeywords:
    # cada domínio detecta suas palavras-chave

class TestAnalyticsWorkflowInstantiation:
    # nome, descrição, steps, router e choices

class TestAnalyticsWorkflowRouting:
    # roteamento correto por domínio
    # fallback para Team Completo
    # bug de falso-positivo: previous_content com "arquivo" não desvia para Dados
```

!!! warning "Bug documentado em teste"
    O test `test_previous_content_with_arquivo_does_not_override_routing` documenta e verifica a correção de um bug onde o Router usava `previous_step_content` (que continha "arquivo" injetado pela etapa de Preparação) em vez do `input` original, fazendo toda pergunta rotear para o step Dados.
