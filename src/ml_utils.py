import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

def avaliar_regressao(y_real, y_pred, modelo_nome):
    """Calcula e exibe métricas de regressão."""
    mae = mean_absolute_error(y_real, y_pred)
    # Compatibilidade com versões do scikit-learn que não aceitam `squared`
    mse = mean_squared_error(y_real, y_pred)
    rmse = float(np.sqrt(mse))
    r2 = r2_score(y_real, y_pred)
    
    print(f"--- {modelo_nome} ---")
    print(f"MAE: {mae:.2f} | RMSE: {rmse:.2f} | R²: {r2:.2f}")
    return {"MAE": mae, "RMSE": rmse, "R2": r2}

def avaliar_classificacao(y_real, y_pred, modelo_nome):
    """Calcula e exibe métricas de classificação."""
    acc = accuracy_score(y_real, y_pred)
    average = 'weighted'
    prec = precision_score(y_real, y_pred, average=average, zero_division=0)
    rec = recall_score(y_real, y_pred, average=average, zero_division=0)
    f1 = f1_score(y_real, y_pred, average=average, zero_division=0)
    
    print(f"--- {modelo_nome} ---")
    print(f"Acc: {acc:.2f} | Prec: {prec:.2f} | Recall: {rec:.2f} | F1: {f1:.2f}")
    return {"Accuracy": acc, "Precision": prec, "Recall": rec, "F1": f1}

def plot_feature_importance(modelo, colunas, top_n=10):
    """Gera gráfico de importância das variáveis."""
    if hasattr(modelo, 'feature_importances_'):
        importances = modelo.feature_importances_
        if len(colunas) != len(importances):
            colunas = [f'feature_{i}' for i in range(len(importances))]
        importances = pd.Series(importances, index=colunas)
        importances.nlargest(top_n).sort_values().plot(kind='barh', color='skyblue')
        plt.title("Top Variáveis Mais Importantes")
        plt.show()