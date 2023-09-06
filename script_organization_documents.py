import os
import shutil
from datetime import datetime


def obter_data_criacao_arquivo(file_path):
    creation_time = os.path.getctime(file_path)
    return datetime.fromtimestamp(creation_time)


def organizar_documentos(source_directory, destination_directory, allowed_extensions):
    # Verifica se a pasta de origem existe
    if not os.path.exists(source_directory):
        print("A pasta de origem não existe.")
        return

    # Verifica se a pasta de destino existe. Se não, cria.
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Percorre todos os arquivos na pasta de origem
    for file_name in os.listdir(source_directory):
        source_file_path = os.path.join(source_directory, file_name)

        # Verifica se é um arquivo
        if os.path.isfile(source_file_path):
            try:
                # Verifica a extensão do arquivo
                file_extension = os.path.splitext(file_name)[1].lower()

                # Verifica se a extensão está na lista de extensões permitidas
                if file_extension in allowed_extensions:
                    # Obtém a data de criação do arquivo
                    creation_date = obter_data_criacao_arquivo(source_file_path)

                    # Cria o caminho de destino com base no ano e mês
                    year = str(creation_date.year)
                    month = str(creation_date.month).zfill(2)  # Zeros à esquerda para o mês
                    destination_path = os.path.join(destination_directory, year, month)

                    # Verifica se a pasta de destino existe. Se não, cria.
                    if not os.path.exists(destination_path):
                        os.makedirs(destination_path)

                    # Move o arquivo para a pasta de destino
                    destination_file_path = os.path.join(destination_path, file_name)
                    shutil.move(source_file_path, destination_file_path)

                    print(f"Arquivo '{file_name}' movido para '{destination_file_path}'.")

            except OSError:
                print(f"Erro ao processar o arquivo '{file_name}'.")

        else:
            print(f"O item '{file_name}' não é um arquivo.")


source_directory = ""  # Insira o caminho do diretório de origem aqui
destination_directory = ""  # Insira o caminho do diretório de destino aqui
allowed_extensions =  ['.jpg', '.bmp', '.html', '.m4v', '.JPG', '.jpeg', '.png', '.gif', '.json', '.mp4', '.avi', '.tar', '.MOV', '.heic', '.mov', '.ico', '.webp', '.wmv', '.mp4']

organizar_documentos(source_directory, destination_directory, allowed_extensions)
