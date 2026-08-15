# import argparse

# def main():
#     # 1. Cria o orquestrador principal
#     parser = argparse.ArgumentParser(
#         prog="meta_tool",
#         description="Central Command Line Interface for the Obsidian Meta Tool.",
#         epilog="Use 'python cli.py <command> --help' to see specific options for each command."
#     )
    
#     # 2. Cria o gerenciador de subcomandos
#     subparsers = parser.add_subparsers(dest="command", help="Available core commands")

#     # ==========================================
#     # TASK 1: Configuração (do config.ini)
#     # ==========================================
#     parser_config = subparsers.add_parser(
#         "config", 
#         help="Starts the interactive configuration for the vault."
#     )
#     parser_config.add_argument(
#         "--bypass", 
#         action="store_true", 
#         help="Automatically choose the default config option (option_1) without asking inputs."
#     )
#     parser_config.add_argument(
#         "--choice", 
#         type=str, 
#         help="Specify an immediate option number to save the vault (e.g., '3' to save as option_3).", 
#         default=None
#     )

#     # ==========================================
#     # TASK 2: Mapeamento dos caminhos do vault
#     # ==========================================
#     parser_paths = subparsers.add_parser(
#         "update-paths", 
#         help="Captures the vault file paths and saves them to a text document."
#     )
#     parser_paths.add_argument(
#         "--vault", 
#         type=str, 
#         help="Specify the vault number option (e.g., 2). Uses default (1) if omitted.", 
#         default=None
#     )

#     # ==========================================
#     # TASK 3: Criação do DataFrame geral
#     # ==========================================
#     parser_dataframe = subparsers.add_parser(
#         "create-dataframe", 
#         help="Creates the general DataFrame from all vault notes and saves it as a Parquet file."
#     )
#     parser_dataframe.add_argument(
#         "--choice", 
#         type=str, 
#         help="Specify an immediate option number to save the vault (e.g., '3' to save as option_3).", 
#         default=None
#     )

#     # 3. Lê e interpreta o que o usuário digitou no terminal
#     args = parser.parse_args()

#     # 4. Executa a função correspondente ao comando escolhido
#     if args.command == "config":
#         print("Starting configuration...")
#         process_configuration(bypass_input=args.bypass, immediate_choice=args.choice)
        

#     elif args.command == "update-paths":
#         print("Capturing vault file paths...")
#         if args.vault:
#             DataPaths.capture_vault_file_paths(vault_option_digit=args.vault)
#         else:
#             DataPaths.capture_vault_file_paths()
#         print("Paths captured and saved successfully!")

#     elif args.command == "create-dataframe":
#         print("Creating general DataFrame...")
#         if args.choice:
#             dataframe_creation(vault_option_digit=args.choice)
#         else:
#             dataframe_creation()
#         print("DataFrame created and saved successfully!")

#     else:
#         # Se o usuário rodar o arquivo sem passar nenhum comando, exibe a ajuda nativa
#         parser.print_help()


# if __name__ == "__main__":
#     main()