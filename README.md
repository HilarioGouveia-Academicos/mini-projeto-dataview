# 📈 MiniProjeto DataView: Análise Exploratória de Dados de Vendas 

## Sobre o projeto
O DataView PY é um projeto de análise exploratória de dados (EDA) de vendas, desenvolvido em Python em um Jupiter Notebook. O notebook lê, limpa, transforma,  analisa e visualiza um dataset de vendas, gerando métricas e insights.

### O que o projeto analisa  - Receita total e volume de vendas por mês e trimestre  - Top produtos e categorias por receita  - Desempenho por região  - Segmentação de clientes por nível de gasto (Bronze, Prata, Ouro)  - Comparação entre os dados com e sem tratamento de outliers (v1 e v2)  - Exportação de relatórios em CSV e JSON 

## Objetivo
  Praticar os principais conceitos:  
  - Lógica de programação com Python  
  - Variáveis, tipos de dados e operadores  
  - Condicionais (if, elif, else) e repetição (for, while)  
  - Funções com parâmetros, retorno e funções lambda  
  - Funções reutilizáveis  
  - Leitura e escrita de arquivos CSV e JSON  
  - Módulo datetime para manipulação de datas  
  - Expressões regulares com o módulo re  
  - Pandas: DataFrames, limpeza, groupby, filtros e transformações  
  - NumPy: arrays, operações vetorizadas, broadcasting  
  - Detecção e tratamento de outliers (IQR ou z-score)  
  - Matplotlib e Seaborn: gráficos, customização e exportação em PNG  
  - Uso básico do GitHub 

## Como executar  

### No Google Colab (recomendado)  
1. Faça upload do notebook dataview.ipynb  
2. Abra o arquivo carregado no Colab  
3. Execute as células na ordem, de cima para baixo 

### Localmente (em seu computador)  

#### 1️⃣ Instale as dependências
O arquivo `requirements.txt` contém todas as bibliotecas necessárias para executar o projeto. Para instalar, abra o terminal na raiz do projeto e execute:

```bash
pip install -r requirements.txt
```

#### 2️⃣ Execute o notebook
Após instalar as dependências, abra o Jupyter Notebook:

```bash
jupyter notebook notebooks/dataview.ipynb
```

Ou use o VS Code com a extensão Jupyter e execute as células na ordem.

**O que é `requirements.txt`?**  
É um arquivo que lista todas as bibliotecas Python necessárias para o projeto, com suas versões mínimas. Isso garante que qualquer pessoa que clone o repositório tenha exatamente o mesmo ambiente de desenvolvimento.

## Estrutura do Repositório

```
📁 mini-projeto-dataview/
├── 📁 data/                          
│   ├── 📁 raw                       # Dataset bruto gerado
│   └── 📁 processed 
│       ├── 📁 v1_com_outliers/      # Dados de limpeza geral, outliers mantidos  
│       ├── 📁 v2_outliers_tratado/  # Limpeza v1 + tratamento de outliers
|       └── 📁 final/                # Dataset escolhido para uso futuro  │
├── 📁 notebooks/                      
│   └── dataview.ipynb               # Notebook principal de EDA
├── 📁 outputs/
│   ├── metricas_por_mes.csv         #
│   ├── segmentacao_clientes.csv     #
│   ├── estatisticas_gerais.json     #
│   └── 📁 graficos/
└── 📄 README.md
```

## Ferramentas utilizadas  
- Python 3.10+  
- Google Colab / VS Code  
- Bibliotecas: pandas, numpy, matplotlib, seaborn, re, datetime, os, random  
- GitHub para versionamento  

## Vídeo de demonstração  
https://www.loom.com/share/0c8e23788c5d4cbf94007a2abe64bca3Inserir 

## Sugestões de Melhoria para o Notebook

Este notebook já apresenta uma excelente estrutura para a exploração e análise de dados. No entanto, algumas melhorias podem ser implementadas para torná-lo ainda mais robusto, organizado e produtivo, especialmente em cenários de projetos maiores ou em equipe:

1.  **Estruturação com uma Função `main()`**: Embora o notebook seja linear, envolver a execução principal em uma função `main()` e usar `if __name__ == '__main__': main()` pode melhorar a organização. Isso torna o código mais fácil de testar e reutilizar em outros scripts.

2.  **Modularização em Arquivos Python (`.py`)**: As funções definidas (como `gerar_dataset_vendas`, `limpar_dados`, `calcular_metricas`, etc.) poderiam ser extraídas para arquivos `.py` separados em um diretório `src/`. Por exemplo, `src/data_ingestion.py`, `src/data_cleaning.py`, `src/data_analysis.py`. No notebook, essas funções seriam então importadas (ex: `from src.data_cleaning import limpar_dados`), tornando o notebook mais limpo e focado na orquestração e visualização dos resultados, não na definição de cada função.

3.  **Type Hints**: Adicionar anotações de tipo (type hints) às funções (`def limpar_dados(df: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:`) melhora a legibilidade, facilita a depuração e permite que IDEs e ferramentas de análise estática identifiquem potenciais erros mais cedo.

4.  **Uso de Logging**: Em vez de apenas `print()` para mensagens de status e relatórios, a implementação da biblioteca `logging` do Python permite um controle mais granular sobre os logs (níveis de severidade, saída para arquivo, etc.). Isso é crucial para monitoramento e depuração em ambientes de produção.

5.  **Configuração Externa**: Parâmetros como `n_registros` na geração do dataset, limites de segmentação de clientes, ou caminhos de diretório poderiam ser carregados de um arquivo de configuração (YAML, TOML ou JSON). Isso facilita a alteração desses parâmetros sem modificar o código do notebook.

6.  **Tratamento de Exceções**: Embora o notebook já faça um bom trabalho com `errors='coerce'` no `pd.to_datetime`, adicionar blocos `try-except` em pontos críticos pode tornar o código mais resiliente a falhas inesperadas (ex: falha na escrita/leitura de arquivos, problemas de memória com datasets muito grandes).

7.  **Testes Unitários**: Para as funções modularizadas, a criação de testes unitários garante que cada componente funcione conforme o esperado e que as modificações futuras não introduzam regressões. Ferramentas como `pytest` seriam ideais.

8.  **Docstrings Completas**: Expandir as docstrings para seguir convenções como NumPy ou Google style, incluindo seções para parâmetros, retornos, exceções e exemplos de uso, melhora drasticamente a documentação do código.

Implementar essas sugestões gradualmente ajudaria a transformar este notebook em uma solução ainda mais robusta e de nível de produção para análise de dados.

## Últimas alterações
- Notebook movido para `notebooks/dataview.ipynb` (24/06/2026).
- Arquivo de entrega `Mini-Projeto_Avaliativo_AVA_SESI_SC_SENAI_SC.pdf` adicionado ao `.gitignore`.
- Adicionada seção `Sugestões de Melhoria para o Notebook` ao README (02/07/2026).


