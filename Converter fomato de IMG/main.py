from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm
import os
import shutil

# Registra o manipulador HEIC no Pillow
register_heif_opener()

# os.system('cls')

# Diretórios de origem e destino
dir_origem = "img-cru"
dir_destino = "img-convertidas"
# dir_destino = "D:\\FOTOS FORMATURA"

# Cria o diretório de destino se não existir
if not os.path.exists(dir_destino):
    os.makedirs(dir_destino)

lista_arquivos = os.listdir(dir_origem)

for img in tqdm(lista_arquivos):
    caminho_origem = os.path.join(dir_origem, img)

    # Verifica se o arquivo é HEIC
    if img.lower().endswith('.heic'):
        imagem = Image.open(caminho_origem)
        novo_nome = img.replace('HEIC', 'png')
        caminho_destino = os.path.join(dir_destino, novo_nome)
        imagem.save(caminho_destino)
        os.remove(caminho_origem)  # Remove o arquivo HEIC original após a conversão
    else:
        # Move arquivos que não são HEIC para a pasta de destino
        caminho_destino = os.path.join(dir_destino, img)
        shutil.move(caminho_origem, caminho_destino)

print('Conversão finalizada!')