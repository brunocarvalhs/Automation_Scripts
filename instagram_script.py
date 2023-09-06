import os
from PIL import Image, ImageEnhance

def validate_image_quality(image_path):
    try:
        image = Image.open(image_path)
        image.verify()  # Verifica se a imagem está corrompida
        return True
    except (IOError, SyntaxError):
        return False

def process_image(image_path):
    if validate_image_quality(image_path):
        output_path = f"{os.path.splitext(image_path)[0]}_insta{os.path.splitext(image_path)[1]}"
        target_width = 1080  # Largura desejada para a imagem do Instagram
        target_height = 1080  # Altura desejada para a imagem do Instagram

        image = Image.open(image_path)
        image = image.resize((target_width, target_height))

        # Recorte central da imagem mantendo a proporção original
        width, height = image.size
        left = (width - target_width) // 2
        top = (height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        image = image.crop((left, top, right, bottom))

        image.save(output_path)
        print("A imagem foi processada com sucesso!")
    else:
        print("A imagem fornecida é inválida.")

# Diretorio das imagens:
process_image("")
