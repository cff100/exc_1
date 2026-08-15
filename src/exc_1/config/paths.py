from pathlib import Path

PROJECT_ROOT_FOLDER = Path(__file__).parents[3]
DATA_FOLDER = PROJECT_ROOT_FOLDER / "data"

EXCEL_FILE_PATH = DATA_FOLDER / "excel_estudo.xlsb"


if __name__ == "__main__":
    print(f"Caminho raiz do projeto: {PROJECT_ROOT_FOLDER}")