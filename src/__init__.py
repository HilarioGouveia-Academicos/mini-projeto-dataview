# Inicialização do pacote src
from .data_generator import generate_dataset
from .dataset_vendas import gerar_dataset_vendas
from .data_inspect import inspecionar_dados
from .data_cleaning import limpar_strings_regex, limpar_dados, tratar_outliers
from .features import criar_colunas_derivadas, calcular_metricas, segmentar_clientes, calcular_estatisticas_numpy, aplicar_transformacao
from .visualizations import gerar_visualizacoes
from .export_results import exportar_resultados
from .ml_utils import avaliar_regressao, avaliar_classificacao, plot_feature_importance