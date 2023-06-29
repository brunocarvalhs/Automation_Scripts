import os
import glob
import shutil

source_directory = ""
destination_directory = ""
allowed_extensions = ['.jpg', '.JPG', '.jpeg', '.png', '.gif', '.json', '.mp4', '.avi', '.tar', '.MOV', '.heic', '.mov', '.ico', '.webp', '.wmv']

# Verifica se a pasta de origem existe
if not os.path.exists(source_directory):
    print("A pasta de origem não existe.")
    exit()

# Obtém todos os caminhos de arquivo nas subpastas
file_paths = glob.glob(os.path.join(source_directory, "**/*"), recursive=True)

# Verifica se existem arquivos na pasta de origem
if len(file_paths) == 0:
    print("Não há arquivos na pasta de origem.")
    exit()

# Verifica se a pasta de destino existe. Se não, cria.
if not os.path.exists(destination_directory):
    os.makedirs(destination_directory)

# Conjunto para armazenar os nomes de arquivo já movidos
moved_files = set()

# Percorre todas as subpastas e move os arquivos para o destino
for root, dirs, files in os.walk(source_directory):
    for file in files:
        source_file_path = os.path.join(root, file)
        destination_file_path = os.path.join(destination_directory, file)
        file_extension = os.path.splitext(file)[1].lower()
        
        # Verifica se o arquivo já foi movido, se tem a extensão desejada e se não existe um arquivo com o mesmo nome e extensão no destino
        if file not in moved_files and file_extension in allowed_extensions:
            if os.path.exists(destination_file_path):
                new_filename = f"repet_{file}"
                destination_file_path = os.path.join(destination_directory, new_filename)
            shutil.move(source_file_path, destination_file_path)
            moved_files.add(file)

            # Verifica se o arquivo é um .zip e o descompacta
            if file_extension == '.zip':
                with zipfile.ZipFile(destination_file_path, 'r') as zip_ref:
                    zip_ref.extractall(destination_directory)

print("Movimento de arquivos concluído.")

# Remove pastas vazias no diretório source_directory
for root, dirs, files in os.walk(source_directory, topdown=False):
    for directory in dirs:
        directory_path = os.path.join(root, directory)
        if not os.listdir(directory_path):
            os.rmdir(directory_path)

print("Remoção de pastas vazias concluída.")
