import json
import os

def exportar_resultados(metricas, clientes, stats):
    """
    Exporta os resultados da análise em dois formatos:
    - CSV : métricas mensais e segmentação de clientes
    - JSON: estatísticas gerais calculadas com NumPy
    Após exportar o JSON, faz a leitura de volta com json.load()
    para confirmar que o arquivo foi gravado corretamente —
    demonstrando leitura e escrita de JSON no mesmo fluxo.
    """
    os.makedirs("outputs", exist_ok=True)

    # --- Exportação CSV ---
    # encoding="utf-8-sig" adiciona um BOM (Byte Order Mark) ao arquivo.
    # Isso garante que o Excel abra o CSV com acentos corretamente;
    metricas["por_mes"].to_csv(
        "outputs/metricas_por_mes.csv", index=False, encoding="utf-8-sig"
    )
    print("CSV exportado: outputs/metricas_por_mes.csv")
    clientes.to_csv(
        "outputs/segmentacao_clientes.csv", index=False, encoding="utf-8-sig"
    )
    print("CSV exportado: outputs/segmentacao_clientes.csv")

    # --- Exportação JSON ---
    # ensure_ascii=False permite gravar acentos como caracteres reais (ã, é)
    # round(float(v), 2) converte para float antes de arredondar,
    # evitando comportamento inesperado com o campo 'acima_da_media' (int).
    stats_serializaveis = {k: round(float(v), 2) for k, v in stats.items()}
    caminho_json = "outputs/estatisticas_gerais.json"
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(stats_serializaveis, f, indent=2, ensure_ascii=False)
    # indent=2 formata o JSON com recuo de 2 espaços, mais legível que uma
    # linha só
    print(f"JSON exportado: {caminho_json}")

    # --- Leitura de volta para confirmar ---
    with open(caminho_json, encoding="utf-8") as f:
        lido = json.load(f)
    print("\nJSON lido de volta para confirmação:")
    print(json.dumps(lido, indent=2, ensure_ascii=False))
