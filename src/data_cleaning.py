import re
import pandas as pd


def limpar_strings_regex(df: pd.DataFrame, colunas):
    """Usa expressões regulares para normalizar colunas de texto.

    - Colapsa múltiplos espaços internos em um único espaço
    - Remove espaços nas pontas da string
    - Preserva células nulas sem lançar erro
    """
    df = df.copy()
    for col in colunas:
        df[col] = df[col].apply(
            lambda s: re.sub(r"\s+", " ", str(s)).strip() if pd.notna(s) else s
        )
    return df


def limpar_dados(df: pd.DataFrame):
    """Limpa o DataFrame de vendas em várias etapas e retorna (df_limpo, relatorio).

    Etapas:
    1. Normaliza strings
    2. Converte a coluna `data_venda` para datetime, removendo inválidos
    3. Remove linhas com nulos em `quantidade` e `preco_unitario`
    4. Garante tipos numéricos
    """
    df = df.copy()
    n_inicial = len(df)
    relatorio = {}

    # Etapa 1: limpar strings
    colunas_texto = df.select_dtypes(include="object").columns
    df = limpar_strings_regex(df, colunas_texto)

    # Etapa 2: conversão de datas
    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    relatorio["datas_invalidas_removidas"] = int(df["data_venda"].isnull().sum())
    df = df.dropna(subset=["data_venda"])

    # Etapa 3: remoção de nulos obrigatórios
    n_antes = len(df)
    df = df.dropna(subset=["quantidade", "preco_unitario"])
    relatorio["linhas_nulas_removidas"] = n_antes - len(df)

    # Etapa 4: garantir tipos
    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)

    # Relatório final
    relatorio["registros_iniciais"] = n_inicial
    relatorio["registros_finais"] = len(df)
    relatorio["registros_removidos_total"] = n_inicial - len(df)

    return df, relatorio


def tratar_outliers(df, colunas, fator = 1.5, metodo = 'remover'):
    """
    Trata outliers de colunas numéricas usando o Intervalo Interquartil (IQR).
    Parâmetros:
    colunas : lista de colunas numéricas a verificar
    fator   : multiplicador do IQR para definir os limites (padrão=1.5)
    metodo  : 'remover' exclui as linhas com outliers;
    'limitar' aplica winsorização (substitui pelo limite)
    Retorna o DataFrame tratado sem modificar o original (usa .copy()).
    """
    df = df.copy()  # garante que df_v1 não seja alterado  fora da função
    for col in colunas:
        # Q1 = 25% dos dados estão abaixo desse valor
        # Q3 = 75% dos dados estão abaixo desse valor
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1  # largura do intervalo central  (50% dos dados)
        lim_inf = q1 - fator * iqr  # abaixo disso  = outlier inferior
        lim_sup = q3 + fator * iqr  # acima disso  = outlier superior
        # Conta quantas linhas estão fora dos limites  (| = OR lógico)
        n_out = ((df[col] < lim_inf) | (df[col] > lim_sup)).sum()
        print(f'{col} : {n_out} outliers detectados '
              f'(lim_inf={lim_inf:.2f} , lim_sup={lim_sup:.2f})')
        if metodo == 'remover':
            # Mantém apenas as linhas dentro dos limites
            df = df[(df[col] >= lim_inf) & (df[col] <= lim_sup)]
        else:
            # Winsorização: em vez de remover, "apara"  os valores extremos
            # pelo limite — nenhuma linha é perdida,  só os valores mudam.
            df[col] = df[col].clip(lower=lim_inf, upper=lim_sup)
    return df