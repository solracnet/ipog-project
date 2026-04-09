# Analista de Dados

**Arquivo:** `agents/excel_analyst.py`
**Lista exportada:** `EXCEL_TOOLS`

Responsável pela leitura, inspeção e consulta de arquivos CSV e Excel disponíveis na pasta `data/`. É o ponto de entrada para exploração inicial de qualquer dataset.

## Tools

| Tool | Parâmetros | Descrição |
|---|---|---|
| `list_available_files()` | — | Lista todos os arquivos CSV e Excel disponíveis em `data/` |
| `get_file_schema(filename)` | `filename` | Exibe colunas, tipos e total de linhas do arquivo |
| `get_data_sample(filename, n_rows)` | `filename`, `n_rows=5` | Retorna as primeiras N linhas |
| `get_statistical_summary(filename)` | `filename` | Resumo estatístico (count, mean, std, min, max) das colunas numéricas |
| `get_unique_values(filename, column)` | `filename`, `column` | Valores únicos com contagem de ocorrências de uma coluna |
| `aggregate_data(filename, group_by, agg_column, operation)` | `filename`, `group_by`, `agg_column`, `operation` | Agrupamento e agregação (`sum`, `mean`, `count`, `max`, `min`) |
| `filter_data(filename, column, value)` | `filename`, `column`, `value` | Filtra linhas por valor exato em uma coluna |
| `search_in_data(filename, column, term)` | `filename`, `column`, `term` | Busca parcial (case-insensitive) em uma coluna de texto |

## Palavras-chave de ativação

O Router do Workflow direciona para este agente quando a pergunta contém:

`arquivo`, `schema`, `esquema`, `colunas`, `coluna`, `amostra`, `lista`, `listar`, `inspecionar`, `sample`, `tipos`

## Exemplos de perguntas

- "Liste os arquivos disponíveis"
- "Mostre o esquema do SampleSuperstore.csv"
- "Quais são os valores únicos da coluna Region?"
- "Filtre os dados onde Segment é Consumer"
