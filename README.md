# IPOG :: Projeto Integrador
Link do projeto github: [ipog-project](https://github.com/solracnet/ipog-project)
### Negócio
#### Compreenção do negócio
Uma empresa de móveis (escritório e residencial) e produtos de tecnologia gostaria que fosse criado uma
automação para gerar relatórios para seus colaboradores utilizando linguagem natural. Os dados serão fornecidos através de uma
planilha contendo as principais informações relativas as vendas.
Com os dados disponilizados, o cliente poderá gerar relatórios para seus gestores.
Os relatórios serão disponibilizados em Markdown como resposta direta a pergunta do prompt.

#### Compreenção dos dados
###### Informações presentes na planilha
 * Ship Mode (Meio de entrega)
 * Segment (Segmento)
 * Country (País)
 * City (Cidade)
 * State (Estado)
 * Postal Code (CEP)
 * Region (Região)
 * Category (Categoria)
 * Sub-Category (Sub-Categoria - Produto)
 * Sales (Valor da Venda)
 * Quantity (Quantidade)
 * Discount (Desconto)
 * Profit (Lucro/Prejuízo da operação)

Podemos extrair informações como:
 * Vendas por regiões, categorias, segmento
 * Lucro/Prejuízo
 * Região que mais aplica desconto
 * Se algum meio de entrega gera prejuízo
 * Categorias mais lucrativas

#### Preparação dos dados
Vamos verificar se há valores nulos, padronizar os valores monetários e criar colunas com valores que facilitem as análises,
como Valor Total já calculado com (preço * quantidade) e Valor Líquido (Total - desconto).

#### Modelagem
O projeto será realizado com o framework Agno. As tools estão organizadas por responsabilidade em arquivos separados dentro da pasta `agents/`.

#### Implantação
Preparar o projetos com o padrão do python, uso de requirements e upload no github para que seja validado pela Profa. Fabiana.

### Entregas
#### *Semanas 01 a 03*
###### Definição da proposta.
Projeto em python com o framework Agno, ambiente virtual python e arquivo requirements para facilitar a instalação em qualquer computador.
Farei esse projeto sozinho para que não impacte na agenda de outro colega.

###### Fundamentos dos Agentes e Setup com Agno

**Agentes de IA** são sistemas computacionais projetados para perceber o ambiente, tomar decisões e agir de forma autônoma para atingir objetivos específicos. Diferente de modelos tradicionais que apenas respondem a comandos isolados, agentes são orientados a metas e podem operar em ciclos contínuos de:

Percepção – coletam dados (APIs, arquivos, sensores, bancos de dados, planilhas etc.).

Raciocínio – interpretam informações, aplicam regras ou modelos de linguagem.

Planejamento – definem quais ações executar.

Ação – executam tarefas (gerar relatórios, enviar e-mails, atualizar sistemas).

Memória– armazenam contexto para decisões futuras.

###### Principais componentes

Modelo de linguagem (LLM) – responsável por interpretar linguagem natural e gerar respostas.

Ferramentas (Tools) – funções externas que o agente pode utilizar (ler planilhas, consultar APIs, executar cálculos).

Memória – contexto persistente ou temporário.

Orquestrador – controla o fluxo entre raciocínio e execução de ações.

###### Setup do ambiente
Dependências:
* Python 3.11
* Gerenciador de pacotes python UV (achei melhor de trabalhar que o pip)
* Ambiente virtual do python para separar instalações em diferentes projetos
* Pandas
* Agno e suas dependências
* Groq (LLM)
....
Todas as dependências encontram-se no arquivo requirements.txt
```
python3.11 -m pip venv .venv
```
```
source .venv/bin/activate
```
```
pip install -r requirements.txt
```

#### Exploração dos dados e design dos agentes

##### Desenvolvimento
Como o projeto está organizado e como executar em desenvolvimento.
Diretórios:
 * `/` -> Pasta raiz do projeto
 * `/agents` -> Tools do agente organizadas por responsabilidade
 * `/data` -> Arquivo CSV com os dados de vendas
 * `/db` -> Banco de dados para memória
 * `/reports` -> Relatórios gerados pelo agente (criado automaticamente)
 * `/temp_tests` -> Arquivos de teste para validar funcionalidades antes de ir para o projeto principal
 * `/tests` -> Testes para as classes do projeto
 * `/.venv` -> Ambiente virtual do Python para fixar a versão

Libs:
 * uv -> Gestor de pacotes escolhido. [[uv-website](https://docs.astral.sh/uv/#learn-more)]
 * agno e suas dependências -> para criar ferramentas que integram a IA para o usuário. [[agno-website](https://docs.agno.com/introduction)]
 * demais libs estão no requirements.txt (UV fará a gestão das dependências, mas se preferir usar o padrão, pode instalar via requirements)

#### *Semana 04*

###### Arquitetura atualizada

```
/
├── main.py                        # Ponto de entrada — agente principal com histórico persistido
├── data/
│   └── SampleSuperstore.csv       # Dados de vendas
├── db/
│   └── history.db                 # Banco SQLite com histórico de sessões (criado automaticamente)
├── agents/
│   ├── __init__.py                # Exporta todas as listas de tools
│   ├── excel_analyst.py           # Tools genéricas de leitura e consulta de arquivos CSV/Excel
│   ├── metrics_agent.py           # Tools especializadas em KPIs e métricas de negócio
│   ├── ceo_report.py              # Tools de relatório executivo (visão estratégica)
│   ├── sales_report.py            # Tools de relatório de vendas (região, segmento, período)
│   └── products_report.py         # Tools de relatório de produtos (categorias, rentabilidade)
├── tests/
│   ├── conftest.py                # Fixtures compartilhadas entre os testes
│   ├── test_excel_analyst.py      # Testes do agente de análise de arquivos
│   ├── test_metrics_agent.py      # Testes do agente de métricas e KPIs
│   ├── test_ceo_report.py         # Testes do relatório executivo
│   ├── test_sales_report.py       # Testes do relatório de vendas
│   └── test_products_report.py    # Testes do relatório de produtos
└── temp_tests/                    # Scripts temporários para validar funcionalidades isoladas
```

###### Histórico de conversas com SQLite

O agente persiste todas as sessões de conversa em um banco de dados SQLite (`db/history.db`) gerenciado pelo Agno via SQLAlchemy. Isso permite que o agente mantenha contexto entre interações e que sessões anteriores possam ser retomadas.

**Como funciona:**
- A cada nova execução, uma sessão é criada automaticamente e um `Session ID` é gerado.
- O histórico de mensagens é armazenado no banco e recarregado a cada nova pergunta da mesma sessão.
- Para retomar uma conversa anterior, basta passar o `Session ID` como argumento.

**Executar nova sessão:**
```bash
python main.py
```

**Retomar sessão existente:**
```bash
python main.py <session_id>
```

O `Session ID` é exibido após a primeira resposta e ao encerrar com `sair`.

###### Agentes especializados

**`agents/excel_analyst.py`** — Leitura e consulta de arquivos

| Tool | Descrição |
|---|---|
| `list_available_files()` | Lista arquivos CSV e Excel disponíveis em `data/` |
| `get_file_schema(filename)` | Exibe colunas, tipos e total de linhas |
| `get_data_sample(filename, n_rows)` | Retorna as primeiras N linhas |
| `get_statistical_summary(filename)` | Resumo estatístico das colunas numéricas |
| `get_unique_values(filename, column)` | Valores únicos com contagem de uma coluna |
| `aggregate_data(filename, group_by, agg_column, operation)` | Agrupamento e agregação por dimensão |
| `filter_data(filename, column, value)` | Filtra linhas por valor exato |
| `search_in_data(filename, column, term)` | Busca parcial em uma coluna |

**`agents/metrics_agent.py`** — KPIs e métricas de negócio

| Tool | Descrição |
|---|---|
| `identify_available_kpis(filename)` | Lista todos os KPIs possíveis com descrição e colunas utilizadas |
| `get_kpi_dashboard(filename)` | Painel com receita, lucro, margem, ticket médio e volume |
| `get_margin_by_dimension(filename, dimension)` | Margem de lucro (%) por qualquer dimensão |
| `get_top_performers(filename, dimension, metric, n)` | Top N melhores por Sales, Profit ou Quantity |
| `get_bottom_performers(filename, dimension, metric, n)` | Bottom N piores por métrica |
| `detect_loss_makers(filename, dimension)` | Grupos com lucro total negativo |
| `get_discount_impact(filename)` | Margem de lucro por faixa de desconto aplicado |

**`agents/ceo_report.py`** — Relatório executivo

| Tool | Descrição |
|---|---|
| `get_executive_summary(filename)` | KPIs financeiros e operacionais consolidados para apresentação ao CEO |
| `get_revenue_by_region_and_segment(filename)` | Receita e margem cruzadas por região × segmento |
| `get_top_states(filename, n)` | Top N estados por receita total |
| `get_strategic_kpis(filename)` | KPIs de alto nível: cobertura geográfica, concentração e eficiência |
| `get_pareto_analysis(filename, dimension)` | Análise 80/20 por dimensão (Sub-Category, State, etc.) |
| `get_business_health_indicators(filename)` | Distribuição de margens, concentração de lucro e dependência de desconto |

**`agents/sales_report.py`** — Relatório de vendas

| Tool | Descrição |
|---|---|
| `get_sales_by_region(filename)` | Vendas, lucro e margem por região |
| `get_sales_by_segment(filename)` | Ticket médio e margem por segmento de cliente |
| `get_sales_by_shipping_mode(filename)` | Rentabilidade por meio de entrega |
| `get_discount_impact_on_sales(filename)` | Vendas e margem por faixa de desconto |
| `get_region_segment_ranking(filename)` | Ranking cruzado região × segmento |
| `get_regional_performance_detail(filename)` | Breakdown por região × categoria × segmento |
| `get_city_performance(filename, region)` | Performance por cidade com filtro opcional de região |
| `get_segment_deep_dive(filename, segment)` | Análise detalhada de um segmento |
| `get_sales_by_period(filename)` | Evolução mensal/anual (requer coluna de data no dataset) |
| `get_sales_by_salesperson(filename)` | Performance por vendedor (requer coluna de vendedor no dataset) |

**`agents/products_report.py`** — Relatório de produtos

| Tool | Descrição |
|---|---|
| `get_sales_by_category(filename)` | Receita, volume e margem por categoria |
| `get_sales_by_subcategory(filename)` | Detalhamento por subcategoria com desconto médio |
| `get_loss_making_products(filename)` | Subcategorias com lucro negativo |
| `get_discount_by_category(filename)` | Desconto médio vs. margem por linha de produto |
| `get_top_profitable_subcategories(filename, n)` | Top N subcategorias mais lucrativas |
| `get_category_profitability_ranking(filename)` | Ranking com classificação: Excelente / Boa / Baixa / Prejuízo |
| `get_category_by_region(filename)` | Mix de produto por região |
| `get_shipping_by_category(filename)` | Ship Mode utilizado por categoria e impacto na margem |
| `get_shipping_profitability(filename)` | Rentabilidade de cada meio de entrega por categoria |
| `get_product_volume_vs_profit(filename)` | Volume vs. lucro por unidade — diferencia commodities de produtos premium |

###### Testes

O projeto conta com uma suíte de testes automatizados cobrindo todos os agentes.

**Executar todos os testes:**
```bash
uv run pytest tests/ -v
```

**Executar testes de um agente específico:**
```bash
uv run pytest tests/test_excel_analyst.py -v
uv run pytest tests/test_metrics_agent.py -v
uv run pytest tests/test_ceo_report.py -v
uv run pytest tests/test_sales_report.py -v
uv run pytest tests/test_products_report.py -v
```

**Cobertura da suíte (146 testes):**

| Arquivo de teste | Testes | O que cobre |
|---|---|---|
| `tests/test_excel_analyst.py` | 31 | Carregamento de arquivo, helpers internos e todas as 8 tools de análise |
| `tests/test_metrics_agent.py` | 28 | Todas as 7 tools de KPIs e métricas |
| `tests/test_ceo_report.py` | 24 | Todas as 6 tools do relatório executivo |
| `tests/test_sales_report.py` | 33 | Todas as 10 tools de vendas |
| `tests/test_products_report.py` | 30 | Todas as 10 tools de produtos |

Os testes validam: happy path, mensagens de erro para entradas inválidas, coerção de tipos (o LLM pode passar inteiros como strings) e comportamento com colunas ausentes no dataset.

