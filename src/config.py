"""
config.py

Configurações globais do projeto SalesInsight AI.
"""

from pathlib import Path

# ============================================================================
# Projeto
# ============================================================================

PROJECT_NAME = "SalesInsight AI"
VERSION = "2.0.0"

# ============================================================================
# Random
# ============================================================================

RANDOM_STATE = 42

# ============================================================================
# Dataset
# ============================================================================

N_SAMPLES = 5000

START_DATE = "2023-01-01"
END_DATE = "2025-12-31"

# ============================================================================
# Clientes
# ============================================================================

GENDERS = [
    "Masculino",
    "Feminino"
]

LOYALTY_LEVELS = [
    "Bronze",
    "Prata",
    "Ouro"
]

INCOME_LEVELS = [
    "Baixa",
    "Média",
    "Alta"
]

# ============================================================================
# Produtos
# ============================================================================

CATEGORIES = [
    "Eletrônicos",
    "Informática",
    "Casa",
    "Esportes",
    "Moda"
]

SUPPLIERS = [
    "Fornecedor A",
    "Fornecedor B",
    "Fornecedor C",
    "Fornecedor D"
]

# ============================================================================
# Marketing
# ============================================================================

CHANNELS = [
    "Loja Física",
    "E-commerce",
    "Aplicativo"
]

PAYMENTS = [
    "Pix",
    "Cartão",
    "Boleto"
]

CAMPAIGNS = [
    "Nenhuma",
    "Black Friday",
    "Natal",
    "Premium"
]

# ============================================================================
# Vendedores
# ============================================================================

SELLERS = [
    f"Vendedor {i}"
    for i in range(1, 11)
]

# ============================================================================
# Caminhos
# ============================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"

RAW_DATA = DATA_DIR / "raw"

PROCESSED_DATA = DATA_DIR / "processed"

EXPORT_DATA = DATA_DIR / "exports"

MODELS_DIR = ROOT_DIR / "models"