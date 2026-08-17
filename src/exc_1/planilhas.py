import pandas as pd
from typing import Optional

from exc_1.config.paths import EXCEL_FILE_PATH

def encontra_numero_planilhas(xls: pd.ExcelFile):
    """Encontra o número de planilhas em um arquivo Excel."""
    return len(xls.sheet_names)

def encontra_nomes_planilhas(xls: pd.ExcelFile):
    """Encontra os nomes das planilhas em um arquivo Excel."""
    return xls.sheet_names

def ler_planilha(xls: pd.ExcelFile, sheet_name: Optional[str] = None, sheet_index: Optional[int] = None):
    """Lê uma planilha específica do arquivo Excel."""

    planilhas_nomes = encontra_nomes_planilhas(xls)
    if sheet_name is None:
        if sheet_index is not None:
            if sheet_index < 0 or sheet_index >= len(planilhas_nomes):
                raise IndexError("O índice da planilha está fora do intervalo.")
            sheet_name = planilhas_nomes[sheet_index]
        else:
            raise ValueError("É necessário fornecer o nome ou o índice da planilha.")
    else:
        if sheet_index is not None:
            raise ValueError("Forneça apenas o nome ou o índice da planilha, não ambos.")
        if sheet_name not in planilhas_nomes:
            raise ValueError(f"A planilha '{sheet_name}' não existe no arquivo Excel.")
    return pd.read_excel(xls, sheet_name=sheet_name)

if __name__ == "__main__":
    xls = pd.ExcelFile(EXCEL_FILE_PATH)
    numero_planilhas = encontra_numero_planilhas(xls)
    print(f"Número de planilhas no arquivo: {numero_planilhas}")
    nomes_planilhas = encontra_nomes_planilhas(xls)
    print(f"Nomes das planilhas no arquivo: {nomes_planilhas}")

    planilha = ler_planilha(xls, sheet_index=0)
    print(f"Conteúdo da primeira planilha:\n{planilha.head(20)}")