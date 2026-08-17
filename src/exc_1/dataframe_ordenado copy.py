import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import fcluster, linkage, leaves_list
from scipy.spatial.distance import squareform
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def agrupar_por_similaridade_tfidf(df, coluna, limite_similaridade=75):
    """Calcula o Grupo_ID baseado em TF-IDF e similaridade de cosseno.

    Garante alta velocidade de processamento mesmo em DataFrames grandes (>1.000
    linhas).
    """
    df = df.copy()

    # 1. Trata e limpa o texto para padronização
    textos = (
        df[coluna].fillna("").astype(str).str.strip().str.upper().tolist()
    )
    n = len(textos)

    if n == 0:
        df["Grupo_ID"] = []
        return df
    if n == 1:
        df["Grupo_ID"] = 1
        return df

    # 2. Vetorização TF-IDF por n-gramas de caracteres (capta pequenas variações e erros de digitação)
    vectorizer = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4))
    tfidf_matrix = vectorizer.fit_transform(textos)

    # 3. Calcula matriz de similaridade em C/C++ (instantâneo)
    matriz_sim = cosine_similarity(tfidf_matrix)

    # 4. Converte similaridade (0 a 1) para distância
    matriz_distancia = 1.0 - matriz_sim
    np.fill_diagonal(matriz_distancia, 0)

    # 5. Clusterização Hierárquica
    vetor_distancia = squareform(matriz_distancia, checks=False)
    arvore_clusters = linkage(vetor_distancia, method="average")

    # 6. Aplica o corte de grupo (limite_similaridade 0 a 100 -> corte 0 a 1)
    distancia_corte = 1.0 - (limite_similaridade / 100.0)
    grupos_ids = fcluster(
        arvore_clusters, t=distancia_corte, criterion="distance"
    )

    df["Grupo_ID"] = grupos_ids
    return df


def agrupar_em_camadas(
    df, colunas_hierarquia=["DESCRIÇÃO", "MARCA", "MODELO"], limite_sim=75
):
    """Gera o grupo de similaridade para a DESCRIÇÃO e ordena em camadas

    hierárquicas (Grupo_Descricao -> MARCA -> MODELO).
    """
    df_copia = df.copy()

    # 1. Trata e limpa as colunas envolvidas na ordenação
    for col in colunas_hierarquia:
        if col in df_copia.columns:
            df_copia[col] = (
                df_copia[col]
                .fillna("-")
                .astype(str)
                .str.strip()
                .str.upper()
            )

    # 2. Gera os IDs de grupo para a coluna principal (Ex: DESCRIÇÃO)
    col_principal = colunas_hierarquia[0]
    df_copia = agrupar_por_similaridade_tfidf(
        df_copia, coluna=col_principal, limite_similaridade=limite_sim
    )
    df_copia = df_copia.rename(columns={"Grupo_ID": "Grupo_Descricao"})

    # 3. Ordenação determinística e limpa pelas 3 camadas
    colunas_ordenacao = ["Grupo_Descricao"] + colunas_hierarquia[1:]
    df_ordenado = df_copia.sort_values(
        by=colunas_ordenacao, ascending=True
    ).reset_index(drop=True)

    return df_ordenado


if __name__ == "__main__":
    from exc_1.config.constants import Planilha9Headers as p9h
    from exc_1.config.paths import ExcelFilesPaths
    from exc_1.planilhas import criar_planilha_redefinida

    xls = pd.ExcelFile(ExcelFilesPaths.BASE)
    sheet = 9

    # Carrega os dados brutos
    df_redefinida = criar_planilha_redefinida(
        xls, sheet=sheet, texto_chave=p9h.DESCRICAO
    )

    # Agrupa e ordena com alta velocidade
    df_ordenado = agrupar_em_camadas(
        df_redefinida,
        colunas_hierarquia=[p9h.DESCRICAO, p9h.MARCA, p9h.MODELO],
        limite_sim=85,
    )

    print("Prévia após ordenação:")
    print(df_ordenado[[p9h.DESCRICAO, p9h.MARCA, p9h.MODELO]].head(20))

    # Exporta para Excel
    novo_caminho = ExcelFilesPaths.planilha_ordenada(sheet)
    df_ordenado.to_excel(novo_caminho, index=False)
    print(f"\nArquivo salvo com sucesso em: {novo_caminho}")