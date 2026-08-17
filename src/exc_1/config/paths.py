from pathlib import Path

PROJECT_ROOT_FOLDER = Path(__file__).parents[3]
DATA_FOLDER = PROJECT_ROOT_FOLDER / "data"

class ExcelFilesPaths:
    BASE = DATA_FOLDER / "excel_base.xlsb"

    @staticmethod
    def planilha_ordenada(sheet: str | int):
        return DATA_FOLDER / f"planilha_ordenada_sheet-{sheet}.xlsx"


if __name__ == "__main__":
    print(f"Caminho raiz do projeto: {PROJECT_ROOT_FOLDER}")