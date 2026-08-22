import pandas as pd
from pathlib import Path

from exc_1.config.paths import ExcelFilesPaths


class PlanilhaExcel:

    def __init__(self, nome: str, df: pd.DataFrame) -> None:
        self.nome = nome
        self.df = df

    def __repr__(self) -> str:
        return f"<Planilha: {self.nome} ({len(self.df)} linhas)>"

    def definir_df_limpo(self, texto_chave: str):
        """
        Localiza a primeira linha que contém 'texto_chave' em qualquer coluna,
        define essa linha como o cabeçalho (header) e descarta o conteúdo acima dela.
        """

        # Limpa espaços vazios do texto_chave para evitar problemas de correspondência
        texto_chave = texto_chave.strip()

        # Procura a palavra chave por todas as células de todas as colunas
        # ´lambda row´: Passa de linha em linha da planilha.
        # `astype(str)`: Transforma tudo em texto (para evitar que o Python dê erros se achar um número ou célula vazia).
        # `str.contains(texto_chave, case=False)`: Procura o texto chave (ignorando letras maiúscula/minúscula).
        # `any(axis=1)`: Pergunta se pelo menos uma coluna dessa linha tem a palavra que estou procurando. Retorna `True` ou `False`.
        # `mask_header`: É o resultado, uma lista longa de um booleano para cada linha da tabela.
        mask_header = self.df.apply(lambda row: row.astype(str).str.contains(texto_chave, case = False).any(), axis=1)

        # Filtra apenas as linhas onde a resposta foi `True`, ou seja, onde a palavra foi encontrada.
        indices_encontrados = self.df.index[mask_header].to_list()

        if not indices_encontrados:
            raise ValueError(f"Não foi encontrada nenhuma linha contendo '{texto_chave}'.")

        # Pega a primeira linha em que a palvra apareceu (caso ela aparece em mais de um lugar por engano).
        indice_label = indices_encontrados[0]

        # Descobre a posição numérica real daquela linha na tabela, independente de como o índice esteja nomeado.
        # Converte o índice para lista e depois procura nele.
        posicao_inteira = self.df.index.to_list().index(indice_label)

        # Vai até a linha do cabeçalho que achamos e pega todos os textos dela em uma lista.
        # (Converte a linha em uma lista sem chamar um atributo que pode ser inferido incorretamente como uma Series pelo verificador de tipos.)
        raw_header = list(self.df.iloc[posicao_inteira].astype(str))

        # Passa por cada nome de coluna encontrado. Se houver coluna vazia ou sem nome, o código inventa um nome genérico para o Pandas não quebrar depois.
        novo_header = []
        for i, col in enumerate(raw_header):
            col_limpa = col.strip()
            if col_limpa == "" or col_limpa.lower() == "nan":
                col_limpa = f"coluna_{i}"
            novo_header.append(col_limpa)

        # Remove o que está da linha do cabeçalho para cima e mantém apenas o que está abaixo.
        self.df_limpo = self.df.iloc[posicao_inteira + 1:].copy()

        # Cola os nomes escolhidos para header como os títulos oficiais das colunas da nova tabela.
        self.df_limpo.columns = novo_header

        # Remove linhas totalmente vazias, ae sobrou alguma.
        self.df_limpo = self.df_limpo.dropna(how="all")

        # Reorganiza os indices para começarem do 0.
        self.df_limpo = self.df_limpo.reset_index(drop=True)

        return self.df_limpo



class ExcelOriginal:

    def __init__(self, caminho_arquivo: Path = ExcelFilesPaths.BASE) -> None:
        self.caminho_arquivo = caminho_arquivo
        self.xls = pd.ExcelFile(self.caminho_arquivo)
        self.numero_planilhas = self._encontra_numero_planilhas(self.xls)
        self.planilhas_nomes = self.xls.sheet_names

        # Dicionário de objetos PlanilhaExcel
        self.planilhas = {
            str(nome): PlanilhaExcel(str(nome), self.xls.parse(nome))
            for nome in self.planilhas_nomes
        }

    def _encontra_numero_planilhas(self, xls: pd.ExcelFile) -> int:
        """Encontra o número de planilhas em um arquivo Excel."""
        return len(xls.sheet_names)


# def ler_planilha(xls: pd.ExcelFile, sheet: str | int):
#     """Lê uma planilha específica do arquivo Excel."""

#     if isinstance(sheet, int):
#         try:
#             df_planilha = pd.read_excel(xls, sheet_name=sheet)
#         except ValueError:
#             raise IndexError("O índice da planilha está fora do intervalo.")
#     elif isinstance(sheet, str):
#         try:
#             df_planilha = pd.read_excel(xls, sheet_name=sheet)
#         except ValueError:
#             raise ValueError(f"A planilha '{sheet}' não existe no arquivo Excel.")
#     return df_planilha



# def criar_planilha_redefinida(xls: pd.ExcelFile, sheet: str | int, texto_chave: str):
#     """
#     Lê uma planilha específica do arquivo Excel, redefine o cabeçalho com base em 'texto_chave',
#     e retorna o DataFrame resultante.
#     """
#     df_planilha = ler_planilha(xls, sheet)
#     df_redefinida = definir_cabecalho_por_texto(df_planilha, texto_chave)
#     return df_redefinida

if __name__ == "__main__":
    from exc_1.config.paths import ExcelFilesPaths
    from exc_1.config.constants import Planilha9Headers
    xls = pd.ExcelFile(ExcelFilesPaths.BASE)
    # numero_planilhas = encontra_numero_planilhas(xls)
    print(f"Número de planilhas no arquivo: {numero_planilhas}")
    nomes_planilhas = encontra_nomes_planilhas(xls)
    print(f"Nomes das planilhas no arquivo: {nomes_planilhas}")

    print("-" * 140)

    planilha = ler_planilha(xls, sheet=9)
    print(f"Conteúdo da primeira planilha:\n{planilha.head(20)}")

    print("-" * 140)

    nova_planilha = definir_cabecalho_por_texto(planilha, Planilha9Headers.H1)
    print(f"Conteúdo da planilha após definir o cabeçalho:\n{nova_planilha.head(20)}")
    print(nova_planilha.columns)
    print("\n")
    coluna = Planilha9Headers.H2
    print(f"Conteúdo da coluna '{coluna}':\n{nova_planilha[coluna].head(20)}")