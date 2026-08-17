
import pandas as pd
import numpy as np
from rapidfuzz import fuzz
from scipy.cluster.hierarchy import linkage, fcluster, leaves_list
from scipy.spatial.distance import squareform

from exc_1.planilhas import criar_planilha_redefinida

def agrupar_e_ordenar_por_similaridade(df, coluna, limite_similaridade=75):
    """
    Cria uma coluna 'Grupo_ID' com um número para cada família de textos similares
    e reordena o DataFrame para manter itens do mesmo grupo juntos.
    
    :param df: DataFrame do Pandas
    :param coluna: Nome da coluna de texto a ser analisada
    :param limite_similaridade: Porcentagem mínima de similaridade (0 a 100) para pertencer ao mesmo grupo.
    """
    textos = df[coluna].fillna("").astype(str).tolist()
    n = len(textos)
    
    if n <= 1:
        df['Grupo_ID'] = 1
        return df
    
    # 1. Cria a matriz de similaridade (Todos contra Todos)
    matriz_sim = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            sim = 100.0 if i == j else fuzz.WRatio(textos[i], textos[j])
            matriz_sim[i, j] = sim
            matriz_sim[j, i] = sim

    # 2. Converte similaridade (0 a 100) em distância (0 a 1)
    matriz_distancia = 1.0 - (matriz_sim / 100.0)
    np.fill_diagonal(matriz_distancia, 0)

    # 3. Agrupamento Hierárquico
    vetor_distancia = squareform(matriz_distancia)
    arvore_clusters = linkage(vetor_distancia, method='average')
    
    # 4. Define o corte no grupo com base na distância limite
    # Exemplo: limite_similaridade de 75% equivale a uma distância de corte de 0.25 (1.0 - 0.75)
    distancia_corte = 1.0 - (limite_similaridade / 100.0)
    grupos_ids = fcluster(arvore_clusters, t=distancia_corte, criterion='distance')
    
    # 5. Adiciona a coluna de Grupo ao DataFrame original
    df = df.copy()
    df['Grupo_ID'] = grupos_ids
    
    # 6. Reordena os índices para manter a sequência visual agrupada
    ordem_indices = leaves_list(arvore_clusters)
    df_ordenado = df.iloc[ordem_indices].reset_index(drop=True)
    
    return df_ordenado



def agrupar_em_camadas(df, colunas_hierarquia=['DESCRIÇÃO', 'MARCA', 'MODELO'], limite_sim=75):
    """
    Aplica o agrupamento por similaridade hierarquicamente.
    Cada nível é agrupado apenas DENTRO do grupo do nível anterior.
    """
    df = df.copy()
    
    # Nível 1: Grupo principal pela DESCRIÇÃO
    df = agrupar_e_ordenar_por_similaridade(df, coluna=colunas_hierarquia[0], limite_similaridade=limite_sim)
    df = df.rename(columns={'Grupo_ID': 'Grupo_Descricao'})

    # Nível 2 e 3: Subgrupos por MARCA e MODELO dentro de cada Grupo da Descrição
    # Ordena sequencialmente criando chaves compostas
    df_ordenado = df.groupby('Grupo_Descricao', group_keys=False).apply(
        lambda sub_df: sub_df.sort_values(by=colunas_hierarquia[1:])
    ).reset_index(drop=True)

    return df_ordenado


if __name__ == "__main__":
    from exc_1.config.paths import ExcelFilesPaths
    from exc_1.config.constants import Planilha9Headers as p9h
    from exc_1.planilhas import criar_planilha_redefinida

    xls = pd.ExcelFile(ExcelFilesPaths.BASE)
    sheet = 9

    df_redefinida = criar_planilha_redefinida(xls, sheet=sheet, texto_chave=p9h.DESCRICAO)

    df_ordenado = agrupar_em_camadas(df_redefinida, colunas_hierarquia=[p9h.DESCRICAO, p9h.MARCA, p9h.MODELO], limite_sim=85)

    print(f"DataFrame após agrupar e ordenar por similaridade:\n{df_ordenado[p9h.DESCRICAO].head(20)}")

    #salvar o DataFrame ordenado em um novo arquivo Excel
    novo_caminho = ExcelFilesPaths.planilha_ordenada(sheet)
    df_ordenado.to_excel(novo_caminho, index=False)


