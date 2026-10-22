from PIL import Image
from pillow_heif import register_heif_opener
from tqdm import tqdm
import os
import shutil
import sys

# Registra o manipulador HEIC no Pillow
register_heif_opener()

# Obtém o diretório onde o executável está (funciona tanto para .py quanto .exe)
if getattr(sys, 'frozen', False):
    # Se estiver rodando como executável
    dir_origem = os.path.dirname(sys.executable)
else:
    # Se estiver rodando como script Python
    dir_origem = os.path.dirname(os.path.abspath(__file__))

dir_destino = os.path.join(dir_origem, "Imagens PNG")

# Cria o diretório de destino se não existir
if not os.path.exists(dir_destino):
    os.makedirs(dir_destino)
    print(f"Pasta criada: {dir_destino}\n")

# Lista apenas arquivos (ignora diretórios)
try:
    lista_arquivos = [f for f in os.listdir(dir_origem) if os.path.isfile(os.path.join(dir_origem, f))]
except FileNotFoundError:
    print(f"Erro: Não foi possível acessar a pasta {dir_origem}")
    input("Pressione Enter para sair...")
    exit()

# Lista arquivos já convertidos na pasta de destino
try:
    arquivos_destino = set(os.listdir(dir_destino))
except:
    arquivos_destino = set()

# Filtra apenas imagens
extensoes_imagem = ('.heic', '.jpg', '.jpeg', '.png', '.bmp', '.gif')
lista_imagens = [f for f in lista_arquivos if f.lower().endswith(extensoes_imagem) and not f.endswith(('.py', '.exe'))]

if not lista_imagens:
    print("Nenhuma imagem encontrada na pasta!")
    print(f"Procurando em: {dir_origem}")
    input("Pressione Enter para sair...")
    exit()

print("Iniciando processamento de imagens...")
print(f"Pasta de trabalho: {dir_origem}")
print(f"Total de imagens encontradas: {len(lista_imagens)}\n")

contador_convertidos = 0
contador_copiados = 0
contador_pulados = 0

for img in tqdm(lista_imagens, desc="Progresso", unit="arquivo", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{percentage:.1f}%]'):
    caminho_origem = os.path.join(dir_origem, img)
    
    # Verifica se o arquivo é HEIC
    if img.lower().endswith('.heic'):
        # Verifica se já foi convertido
        novo_nome = os.path.splitext(img)[0] + '.png'
        caminho_destino = os.path.join(dir_destino, novo_nome)
        
        if novo_nome in arquivos_destino:
            contador_pulados += 1
            tqdm.write(f"⊘ Já convertido: {img}")
            continue
        
        try:
            imagem = Image.open(caminho_origem)
            imagem.save(caminho_destino, 'PNG')
            contador_convertidos += 1
            arquivos_destino.add(novo_nome)  # Adiciona ao set para evitar reconversão
            tqdm.write(f"✓ Convertido: {img} → {novo_nome}")
        except Exception as e:
            tqdm.write(f"✗ Erro ao converter {img}: {str(e)}")
    
    # Copia arquivos JPEG para a pasta de destino
    elif img.lower().endswith(('.jpg', '.jpeg')):
        # Verifica se já foi copiado
        caminho_destino = os.path.join(dir_destino, img)
        
        if img in arquivos_destino:
            contador_pulados += 1
            tqdm.write(f"⊘ Já copiado: {img}")
            continue
        
        try:
            shutil.copy2(caminho_origem, caminho_destino)
            contador_copiados += 1
            arquivos_destino.add(img)  # Adiciona ao set
            tqdm.write(f"✓ Copiado: {img}")
        except Exception as e:
            tqdm.write(f"✗ Erro ao copiar {img}: {str(e)}")

print('\n' + '='*60)
print('✓ PROCESSAMENTO FINALIZADO!')
print(f'  - HEIC convertidos para PNG: {contador_convertidos}')
print(f'  - JPEG copiados: {contador_copiados}')
print(f'  - Arquivos já existentes (pulados): {contador_pulados}')
print(f'  - Arquivos salvos em: {dir_destino}')
print('='*60)
input("\nPressione Enter para sair...")