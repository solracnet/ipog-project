# IPOG Analytics

Agente de IA em Python para geração automatizada de relatórios de vendas via linguagem natural.

## O Problema

Uma empresa de móveis (escritório e residencial) e produtos de tecnologia precisa de uma automação para gerar relatórios para seus colaboradores utilizando linguagem natural. Os dados são fornecidos por uma planilha com informações de vendas e os relatórios são entregues em Markdown como resposta direta ao prompt do usuário.

## Solução

Pipeline de agentes especializados orquestrados pelo framework **Agno**, com LLM **Groq (llama-3.3-70b-versatile)**, que interpreta perguntas em linguagem natural, analisa os dados da planilha `SampleSuperstore.csv` e entrega relatórios prontos.

## Stack

| Componente | Tecnologia |
|---|---|
| Linguagem | Python 3.11 |
| Framework de agentes | [Agno](https://docs.agno.com/introduction) v2.5.3 |
| LLM principal | Groq — `llama-3.3-70b-versatile` |
| LLM alternativo | OpenAI — `gpt-4o-mini` |
| Dados | Pandas + NumPy |
| API web | FastAPI + Uvicorn |
| Frontend | Next.js (Agno UI) |
| Persistência | SQLite via SQLAlchemy |
| Gerenciador de pacotes | [UV](https://docs.astral.sh/uv/) |
| Testes | Pytest |

## Dataset — SampleSuperstore.csv

| Campo | Descrição |
|---|---|
| Ship Mode | Meio de entrega |
| Segment | Segmento do cliente |
| Country / City / State / Region | Localização geográfica |
| Category | Categoria do produto |
| Sub-Category | Subcategoria / produto |
| Sales | Valor da venda |
| Quantity | Quantidade |
| Discount | Desconto aplicado |
| Profit | Lucro ou prejuízo da operação |

## Análises disponíveis

- Vendas por região, categoria e segmento
- Lucro/prejuízo por dimensão
- Regiões com maior aplicação de desconto
- Impacto do meio de entrega na rentabilidade
- Categorias e subcategorias mais lucrativas
- Relatório executivo consolidado para o CEO
