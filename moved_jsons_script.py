import os
import shutil

def move_json_files(source_directory):
    # Verifica se o diretório de origem existe
    if not os.path.exists(source_directory):
        print("O diretório de origem não existe.")
        return

    # Percorre todas as subpastas e arquivos no diretório de origem
    for root, dirs, files in os.walk(source_directory):
        for file in files:
            if file.lower().endswith('.json'):
                source_file_path = os.path.join(root, file)
                dir_name = os.path.basename(root)
                destination_directory = os.path.join(source_directory, dir_name + "_jsons")

                # Verifica se a pasta de destino existe. Se não, cria.
                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)

                destination_file_path = os.path.join(destination_directory, file)

                # Move o arquivo JSON para a pasta de destino
                shutil.move(source_file_path, destination_file_path)

                print(f"Arquivo '{file}' movido para '{destination_file_path}'.")

    print("Movimento de arquivos concluído.")


# Exemplo de uso
source_directory = ""  # Insira o caminho do diretório de origem aqui
move_json_files(source_directory)
