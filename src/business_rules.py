"""
business_rules.py

Regras de negócio utilizadas na geração do dataset.
"""

from __future__ import annotations

import numpy as np


def calculate_customer_score(
    loyalty: str,
    rating: int,
    months: int,
    recurring: bool,
) -> int:
    """
    Calcula um score simples para o cliente.
    """

    score = 50

    if loyalty == "Ouro":
        score += 25

    elif loyalty == "Prata":
        score += 10

    score += rating * 5

    score += min(months // 6, 20)

    if recurring:
        score += 15

    return min(score, 100)


def cancellation_probability(
    loyalty: str,
    rating: int,
    discount: float,
    recurring: bool,
    months: int,
) -> float:
    """
    Calcula a probabilidade de cancelamento.
    """

    probability = 0.15

    if rating <= 2:
        probability += 0.25

    elif rating == 3:
        probability += 0.10

    if discount > 35:
        probability += 0.15

    if months < 6:
        probability += 0.15

    if recurring:
        probability -= 0.10

    if loyalty == "Ouro":
        probability -= 0.15

    return float(np.clip(probability, 0.02, 0.95))


def generate_cancelled(
    probability: float,
    rng: np.random.Generator,
) -> int:
    """
    Gera a variável alvo de classificação.
    """

    return int(rng.random() < probability)