"""
data_generator.py

Geração do dataset sintético.
"""

from __future__ import annotations

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from .config import *
from .business_rules import (
    calculate_customer_score,
    cancellation_probability,
    generate_cancelled,
)


class SalesDatasetGenerator:
    """
    Responsável pela geração do dataset sintético.
    """

    def __init__(
        self,
        n_samples: int = N_SAMPLES,
        random_state: int = RANDOM_STATE,
    ):

        self.n_samples = n_samples

        self.rng = np.random.default_rng(random_state)

    def generate(self) -> pd.DataFrame:

        df = pd.DataFrame()

        df["cliente_id"] = np.arange(1, self.n_samples + 1)

        df["idade"] = self.rng.integers(
            18,
            75,
            self.n_samples,
        )

        df["genero"] = self.rng.choice(
            GENDERS,
            self.n_samples,
        )

        df["tempo_cliente_meses"] = self.rng.integers(
            1,
            120,
            self.n_samples,
        )

        df["cliente_recorrente"] = self.rng.choice(
            [True, False],
            self.n_samples,
            p=[0.65, 0.35],
        )

        df["nivel_fidelidade"] = self.rng.choice(
            LOYALTY_LEVELS,
            self.n_samples,
            p=[0.45, 0.35, 0.20],
        )

        df["avaliacao_cliente"] = self.rng.integers(
            1,
            6,
            self.n_samples,
        )

        df["categoria"] = self.rng.choice(
            CATEGORIES,
            self.n_samples,
        )

        df["canal_venda"] = self.rng.choice(
            CHANNELS,
            self.n_samples,
        )

        df["desconto_percentual"] = self.rng.uniform(
            0,
            40,
            self.n_samples,
        ).round(2)

        df["preco_unitario"] = self.rng.uniform(
            20,
            2000,
            self.n_samples,
        ).round(2)

        df["quantidade"] = self.rng.integers(
            1,
            6,
            self.n_samples,
        )

        df["receita_total"] = (
            df["preco_unitario"]
            * df["quantidade"]
        ).round(2)

        scores = []

        cancelled = []

        for _, row in df.iterrows():

            score = calculate_customer_score(
                row["nivel_fidelidade"],
                row["avaliacao_cliente"],
                row["tempo_cliente_meses"],
                row["cliente_recorrente"],
            )

            prob = cancellation_probability(
                row["nivel_fidelidade"],
                row["avaliacao_cliente"],
                row["desconto_percentual"],
                row["cliente_recorrente"],
                row["tempo_cliente_meses"],
            )

            scores.append(score)

            cancelled.append(
                generate_cancelled(prob, self.rng)
            )

        df["score_cliente"] = scores

        df["cancelado"] = cancelled

        return df


def generate_dataset(
    n_samples: int = N_SAMPLES,
) -> pd.DataFrame:

    generator = SalesDatasetGenerator(
        n_samples=n_samples
    )

    return generator.generate()


