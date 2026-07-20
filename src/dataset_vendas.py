"""
dataset_vendas.py

Funções utilitárias para o dataset de vendas do projeto.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import random

import numpy as np
import pandas as pd

from .config import DATA_DIR, RAW_DATA


DATASET_FILENAME = "vendas.csv"
RAW_DATASET_PATH = RAW_DATA / DATASET_FILENAME
FINAL_DATASET_PATH = DATA_DIR / "final" / DATASET_FILENAME


def gerar_dataset_vendas(n_registros: int = 150, seed: int = 42) -> pd.DataFrame:
    """Gera um dataset sintético de vendas similar ao notebook."""
    random.seed(seed)
    np.random.seed(seed)
    produtos = ["Notebook", "Smartphone", "Tablet", "Monitor", "Teclado", "Mouse"]
    precos = {
        "Notebook": 3500,
        "Smartphone": 2200,
        "Tablet": 1800,
        "Monitor": 1200,
        "Teclado": 250,
        "Mouse": 120,
    }
    categorias = {
        "Notebook": "Computadores",
        "Smartphone": "Celulares",
        "Tablet": "Celulares",
        "Monitor": "Computadores",
        "Teclado": "Periféricos",
        "Mouse": "Periféricos",
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    clientes = [f"Cliente_{i:03d}" for i in range(1, 31)]
    data_inicio = datetime(2024, 1, 1)
    dados = []
    for i in range(n_registros):
        produto = random.choice(produtos)
        quantidade = random.randint(1, 10)
        preco = precos[produto]
        data = data_inicio + timedelta(days=random.randint(0, 364))

        if random.random() < 0.05:
            quantidade = None
        if random.random() < 0.04:
            preco = None
        if random.random() < 0.03:
            produto = "  " + produto

        data_str = data.strftime("%Y-%m-%d") if random.random() > 0.02 else "DATA INVALIDA"

        dados.append(
            {
                "id_venda": i + 1,
                "data_venda": data_str,
                "cliente": random.choice(clientes),
                "produto": produto,
                "categoria": categorias.get(produto.strip(), "Outros"),
                "regiao": random.choice(regioes),
                "quantidade": quantidade,
                "preco_unitario": preco,
            }
        )
    return pd.DataFrame(dados)