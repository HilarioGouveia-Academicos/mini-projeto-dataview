import numpy as np
import pandas as pd

def criar_colunas_derivadas(df):
    """
    Cria colunas calculadas a partir do dataset limpo:
    - receita_total     : valor total da linha de venda (quantidade × preço)
    - mes / trimestre / ano : componentes extraídos da data
    - faixa_receita_item : classificação do valor de cada venda (np.select)

    Nota: receita_total foi calculada temporariamente no RF04 apenas para
    detecção de outliers e depois descartada. Aqui ela é criada de forma
    definitiva sobre df_v2 — já com os outliers tratados — para que todas
    as análises posteriores usem a mesma base consistente.
    """
    df = df.copy()
    # Receita por linha: grandeza central de todas as métricas do projeto
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]
    # Componentes de data — o atributo .dt expõe propriedades de datetime
    df["mes"]       = df["data_venda"].dt.month
    df["trimestre"] = df["data_venda"].dt.quarter.apply(lambda q: f"Q {q}")
    df["ano"]       = df["data_venda"].dt.year
    # -------------------------------------------------------------------
    # np.select: alternativa vetorizada ao if/elif/else para criar
    # colunas categóricas. Recebe duas listas de mesmo tamanho:
    #   condicoes  : lista de máscaras booleanas (testadas em ordem)
    #   valores    : rótulo retornado quando a condição correspondente é True
    # default      : valor usado quando nenhuma condição é satisfeita
    # É equivalente a apply(lambda x: ...) mas muito mais eficiente em
    # datasets grandes, pois opera sobre arrays sem usar loops Python.
    # -------------------------------------------------------------------
    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000,
    ]
    rotulos = ["Baixo Valor", "Médio Valor", "Alto Valor"]  # alinhado ao enunciado
    df["faixa_receita_item"] = np.select(condicoes, rotulos, default="N/D")
    print("COLUNAS DERIVADAS CRIADAS")
    print(df[["data_venda", "receita_total", "mes", "trimestre",
              "faixa_receita_item"]].head())

    return df


def calcular_metricas(df: pd.DataFrame) -> dict:
    """
    Calcula e retorna um dicionário com métricas agregadas por quatro dimensões: 
    mês, produto, categoria e região.
    Usa .groupby() + .agg() com nomeação explícita de colunas:
    nova_coluna=("coluna_origem", "função")
    Isso permite criar múltiplas agregações em uma única chamada e 
    nomear cada resultado diretamente, sem precisar renomear depois.
    """
    metricas = {}
    metricas["por_mes"] = (
        df.groupby("mes")
        .agg(
            receita_total=("receita_total", "sum"),
            quantidade=("quantidade", "sum"),
            n_vendas=("id_venda", "count"),
        )
        .reset_index()
        .sort_values("mes")
    )
    metricas["top_produtos"] = (
        df.groupby("produto")["receita_total"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    metricas["por_categoria"] = (
        df.groupby("categoria")["receita_total"]
        .sum()
        .reset_index()
        .sort_values("receita_total", ascending=False)
    )
    metricas["por_regiao"] = (
        df.groupby("regiao")
        .agg(
            receita_total=("receita_total", "sum"),
            media_ticket=("receita_total", "mean"),
        )
        .reset_index()
        .sort_values("receita_total", ascending=False)
    )
    for nome, tabela in metricas.items():
        print(f"\n=== {nome.upper().replace('_', ' ')} ===")
        print(tabela.to_string(index=False))
    return metricas


def segmentar_clientes(df):
    """
    Prata
    Ouro
    Agrupa os dados por cliente, calcula o total gasto por cada um
    e classifica em Bronze / Prata / Ouro conforme os limites abaixo:
    < R$ 5.000          → Bronze
    R$ 5.000–R$ 15.000  → Prata
    > R$ 15.000         → Ouro
    Demonstra o uso de função lambda com condicional encadeado —
    equivalente a um if/elif/else em uma única expressão.
    """
    # Soma a receita total de cada cliente em todas as suas compras
    clientes_df = (
        df.groupby("cliente")["receita_total"]
        .sum()
        .reset_index()
    )
    clientes_df.columns = ["cliente", "total_gasto"]
    # -------------------------------------------------------------------
    # Lambda com ternário aninhado — como ler:
    #   "Se g > 15000  → 'Ouro'
    #    Senão, se g >= 5000  → 'Prata'
    #    Senão  → 'Bronze'"
    #
    # Nota: g > 15000 significa que exatamente R$ 15.000  cai em Prata,
    # consistente com o critério "acima de R$ 15.000"  para Ouro.
    # -------------------------------------------------------------------
    clientes_df["segmento"] = clientes_df["total_gasto"].apply(
        lambda g: "Ouro" if g > 15000 else ("Prata" if g >= 5000 else "Bronze")
    )
    clientes_df = clientes_df.sort_values("total_gasto", ascending=False)
    print("=== SEGMENTAÇÃO DE CLIENTES (Top 10) ===")
    print(clientes_df.head(10).to_string(index=False))
    print(f"\nDistribuição de segmentos:\n  {clientes_df['segmento'].value_counts()}")
    return clientes_df


def calcular_estatisticas_numpy(df):
    """
    Usa NumPy diretamente sobre arrays para calcular estatísticas de receita.
    Demonstra três conceitos:
    1. Operações vetorizadas
    2. Broadcasting (operação escalar aplicada a todo o array de uma vez)
    3. Boolean indexing (filtrar array com máscara booleana)
    """
    # .to_numpy() converte a Series do Pandas em um  array NumPy puro.
    # Isso é necessário para usar funções do NumPy  diretamente e demonstrar
    # que sabemos trabalhar com arrays além do DataFrame.
    receitas = df["receita_total"].to_numpy()
    # --- Estatísticas descritivas (operações vetorizadas)  ---
    # Cada função abaixo opera sobre o array inteiro
    # "float()" garante que os valores sejam serializáveis  em JSON (RF11)
    stats = {
        "media": float(np.mean(receitas)),
        "mediana": float(np.median(receitas)),
        "desvio_padrao": float(np.std(receitas)),
        "total": float(np.sum(receitas)),
        "p25": float(np.percentile(receitas, 25)),
        "p75": float(np.percentile(receitas, 75)),
    }
    # --- Broadcasting: participação percentual de  cada venda ---
    # receitas.sum() é um escalar; NumPy o aplica a  cada elemento do array,
    # calculando o % de cada venda no total.
    # Isso é broadcasting: operação entre um array e um escalar.
    receitas_pct = (receitas / receitas.sum()) * 100
    print(f"  Participação das 5 maiores vendas no total:\n  {np.sort(receitas_pct)[-5:].round(2)} %")
    # --- Boolean indexing (filtro vetorizado) ---
    # (receitas > stats["media"]) gera um array de  True/False para cada linha;
    # .sum() conta os True. Equivale a um for+if, mas  muito mais eficiente.
    acima_da_media = int((receitas > stats["media"]).sum())
    stats["acima_da_media"] = acima_da_media
    # Exibição — formato separado para inteiro evitar  "12.00"
    print("\n=== ESTATÍSTICAS COM NUMPY ===")
    for k, v in stats.items():
        if k == "acima_da_media":
            print(f"  {k} : {v} vendas")
        else:
            print(f"  {k} : R$ {v:.2f} ")
    return stats

def aplicar_transformacao(df, coluna, funcao):
    """
    Função de ordem superior: aplica qualquer função (incluindo lambdas)
    a uma coluna do DataFrame, criando uma coluna '_transformado'.
    Parâmetros:
    df     : DataFrame de entrada
    coluna : nome da coluna a transformar
    funcao : função (ou lambda) a aplicar — o 'callback'
    Retorna uma cópia do DataFrame com a nova coluna; não modifica o original.
    """
    df = df.copy()
    df[f"{coluna}_transformado"] = df[coluna].apply(funcao)
    return df
