import pandas as pd
from exc_1.config.paths import EXCEL_FILE_PATH

def encontra_numero_planilhas(excel_file_path):
    """Encontra o número de planilhas em um arquivo Excel."""
    xls = pd.ExcelFile(excel_file_path)
    return len(xls.sheet_names)

def encontra_nomes_planilhas(excel_file_path):
    """Encontra os nomes das planilhas em um arquivo Excel."""
    xls = pd.ExcelFile(excel_file_path)
    return xls.sheet_names

# def encontra_header_linha(excel_file_path, nome_procurado): 
#     """Encontra o header de um arquivo Excel."""
#     df = pd.read_excel(excel_file_path)
#     header_linha = df[df.iloc[:, 0] == nome_procurado].index.tolist()
#     return header_linha

if __name__ == "__main__":
    numero_planilhas = encontra_numero_planilhas(EXCEL_FILE_PATH)
    print(f"Número de planilhas no arquivo: {numero_planilhas}")
    nomes_planilhas = encontra_nomes_planilhas(EXCEL_FILE_PATH)
    print(f"Nomes das planilhas no arquivo: {nomes_planilhas}")