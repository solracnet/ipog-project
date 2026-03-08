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
O projeto será realizado com o framework Agno. Faremos tools para as etapas do processo.
 * Leitura do arquivo
 * Tratamento
 * Exportar para cada tipo de solicitação

#### Desenvolvimento
Como o projeto está organizado e como executar em desenvolvimento.
Diretórios:
 * / -> Pasta raiz do projeto
 * /temp_test -> Arquivos de teste para validar funcionalidades antes de ir para o projeto principal.
 * /.venv -> Ambiente virtual do python para fixar a versão.

Libs:
 * uv -> Gestor de pacotes escolhido. [[uv-website](https://docs.astral.sh/uv/#learn-more)]
 * agno e suas dependências -> para criar ferramentas que integram a IA para o usuário. [[agno-website](https://docs.agno.com/introduction)]
 * demais libs estão no requirements.txt (UV fará a gestão das dependências, mas se preferir usar o padrão, pode instalar via requirements)

#### Implantação
Preparar o projetos com o padrão do python, uso de requirements e upload no github para que seja validado pela Profa. Fabiana.

### Entregas
###### *Semanas 01 a 03*
#### Definição da proposta.
Projeto em python com o framework Agno, ambiente virtual python e arquivo requirements para facilitar a instalação em qualquer computador.
Farei esse projeto sozinho para que não impacte na agenda de outro colega.

#### Fundamentos dos Agentes e Setup com Agno

**Agentes de IA** são sistemas computacionais projetados para perceber o ambiente, tomar decisões e agir de forma autônoma para atingir objetivos específicos. Diferente de modelos tradicionais que apenas respondem a comandos isolados, agentes são orientados a metas e podem operar em ciclos contínuos de:

Percepção – coletam dados (APIs, arquivos, sensores, bancos de dados, planilhas etc.).

Raciocínio – interpretam informações, aplicam regras ou modelos de linguagem.

Planejamento – definem quais ações executar.

Ação – executam tarefas (gerar relatórios, enviar e-mails, atualizar sistemas).

Memória– armazenam contexto para decisões futuras.

#### Principais componentes

Modelo de linguagem (LLM) – responsável por interpretar linguagem natural e gerar respostas.

Ferramentas (Tools) – funções externas que o agente pode utilizar (ler planilhas, consultar APIs, executar cálculos).

Memória – contexto persistente ou temporário.

Orquestrador – controla o fluxo entre raciocínio e execução de ações.

#### Setup do ambiente
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
##### Exploração dos dados e Design dos Agentes