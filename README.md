# IPOG :: Projeto Integrador
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
O projeto será realizado com o framework Agno. As tools estão organizadas por responsabilidade em arquivos separados dentro da pasta `tools/`.

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

###### Arquitetura das Tools

```
/
├── main.py                        # Ponto de entrada — registra as tools no agente e gerencia o loop de interação
├── data/
│   └── SampleSuperstore.csv       # Dados de vendas
├── reports/                       # Relatórios gerados em Markdown (criado automaticamente)
├── tools/
│   ├── __init__.py                # Exporta todas as tools para facilitar importação
│   ├── data_tools.py              # Carregamento, limpeza e enriquecimento dos dados
│   ├── analysis_tools.py          # Análises de vendas, lucro, desconto e entrega
│   └── report_tools.py            # Exportação de relatórios em Markdown
└── temp_tests/                    # Scripts temporários para validar funcionalidades isoladas
```

##### tools/data_tools.py — Preparação de Dados
| Função | Descrição |
|---|---|
| `load_data()` | Carrega o CSV em um DataFrame Pandas |
| `check_null_values(df)` | Verifica e remove linhas com valores nulos |
| `calculate_sales_metrics(df)` | Adiciona colunas `Total_Sale` e `Total_Sale_After_Discount` |
| `get_prepared_data()` | Pipeline completo: carrega, limpa e enriquece os dados |

##### tools/analysis_tools.py — Análises de Vendas
| Função | Descrição |
|---|---|
| `get_sales_by_region()` | Total de vendas por região |
| `get_sales_by_category()` | Total de vendas por categoria |
| `get_sales_by_segment()` | Total de vendas por segmento de cliente |
| `get_profit_analysis()` | Lucro total e margem média por categoria e subcategoria |
| `get_discount_analysis()` | Desconto médio por região e impacto no lucro |
| `get_shipping_analysis()` | Vendas, lucro e pedidos por meio de entrega |

##### tools/report_tools.py — Exportação
| Função | Descrição |
|---|---|
| `save_report_to_file(content, filename)` | Salva o relatório em Markdown na pasta `./reports/` |

##### Desenvolvimento
Como o projeto está organizado e como executar em desenvolvimento.
Diretórios:
 * `/` -> Pasta raiz do projeto
 * `/tools` -> Tools do agente organizadas por responsabilidade
 * `/data` -> Arquivo CSV com os dados de vendas
 * `/reports` -> Relatórios gerados pelo agente (criado automaticamente)
 * `/temp_tests` -> Arquivos de teste para validar funcionalidades antes de ir para o projeto principal
 * `/.venv` -> Ambiente virtual do Python para fixar a versão

Libs:
 * uv -> Gestor de pacotes escolhido. [[uv-website](https://docs.astral.sh/uv/#learn-more)]
 * agno e suas dependências -> para criar ferramentas que integram a IA para o usuário. [[agno-website](https://docs.agno.com/introduction)]
 * demais libs estão no requirements.txt (UV fará a gestão das dependências, mas se preferir usar o padrão, pode instalar via requirements)

#### *Semana 04*
##### Agente analista de dados

###### Arquitetura atualizada

```
/
├── main.py                        # Ponto de entrada — agente principal com histórico persistido
├── data/
│   └── SampleSuperstore.csv       # Dados de vendas
├── db/
│   └── history.db                 # Banco SQLite com histórico de sessões (criado automaticamente)
├── agents/
│   ├── __init__.py                # Exporta EXCEL_TOOLS e METRICS_TOOLS
│   ├── excel_analyst.py           # Tools genéricas de leitura e consulta de arquivos CSV/Excel
│   └── metrics_agent.py           # Tools especializadas em KPIs e métricas de negócio
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

