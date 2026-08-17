import pandas as pd
from typing import Optional


def encontra_numero_planilhas(xls: pd.ExcelFile):
    """Encontra o número de planilhas em um arquivo Excel."""
    return len(xls.sheet_names)

def encontra_nomes_planilhas(xls: pd.ExcelFile):
    """Encontra os nomes das planilhas em um arquivo Excel."""
    return xls.sheet_names

def ler_planilha(xls: pd.ExcelFile, sheet: str | int):
    """Lê uma planilha específica do arquivo Excel."""

    if isinstance(sheet, int):
        try:
            df_planilha = pd.read_excel(xls, sheet_name=sheet)
        except ValueError:
            raise IndexError("O índice da planilha está fora do intervalo.")
    elif isinstance(sheet, str):
        try:
            df_planilha = pd.read_excel(xls, sheet_name=sheet)
        except ValueError:
            raise ValueError(f"A planilha '{sheet}' não existe no arquivo Excel.")
    return df_planilha

def definir_cabecalho_por_texto(df, texto_chave):
    """
    Localiza a primeira linha que contém 'texto_chave' em qualquer coluna,
    define essa linha como o cabeçalho (header) e descarta o conteúdo acima dela.
    """

    # Limpa espaços vazios do texto_chave para evitar problemas de correspondência
    texto_chave = texto_chave.strip()

    # Localiza a primeira linha que contém o texto_chave
    linha_header = df.apply(lambda row: row.astype(str).str.contains(texto_chave, case=False).any(), axis=1)
    indices_header = linha_header[linha_header].index.tolist()
    if not indices_header:
        raise ValueError(f"Não foi encontrada nenhuma linha contendo o texto '{texto_chave}'.")
    indice = indices_header[0]

    # Usa a linha encontrada como nomes de coluna e remove as linhas acima (incluindo a própria)
    novo_header = df.loc[indice].astype(str).tolist()
    df_novo = df.loc[indice + 1 :].copy()
    df_novo.columns = novo_header
    df_novo = df_novo.reset_index(drop=True)

    return df_novo

def criar_planilha_redefinida(xls: pd.ExcelFile, sheet: str | int, texto_chave: str):
    """
    Lê uma planilha específica do arquivo Excel, redefine o cabeçalho com base em 'texto_chave',
    e retorna o DataFrame resultante.
    """
    df_planilha = ler_planilha(xls, sheet)
    df_redefinida = definir_cabecalho_por_texto(df_planilha, texto_chave)
    return df_redefinida

if __name__ == "__main__":
    from exc_1.config.paths import EXCEL_FILE_PATH
    xls = pd.ExcelFile(EXCEL_FILE_PATH)
    numero_planilhas = encontra_numero_planilhas(xls)
    print(f"Número de planilhas no arquivo: {numero_planilhas}")
    nomes_planilhas = encontra_nomes_planilhas(xls)
    print(f"Nomes das planilhas no arquivo: {nomes_planilhas}")

    print("-" * 140)

    planilha = ler_planilha(xls, sheet=9)
    print(f"Conteúdo da primeira planilha:\n{planilha.head(20)}")

    print("-" * 140)

    nova_planilha = definir_cabecalho_por_texto(planilha, "COTAÇÃO")
    print(f"Conteúdo da planilha após definir o cabeçalho:\n{nova_planilha.head(20)}")
    print(nova_planilha.columns)
    print("\n")
    coluna = "CONCATENADO"
    print(f"Conteúdo da coluna '{coluna}':\n{nova_planilha[coluna].head(20)}")