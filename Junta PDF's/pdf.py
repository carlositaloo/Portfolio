import PyPDF2
import os
from tqdm import tqdm

merger = PyPDF2.PdfMerger()

lista_arquivos = os.listdir("Arquivos")
lista_arquivos.sort()
print(f'\n{lista_arquivos}\n')

for arquivo in tqdm(lista_arquivos, desc="Mesclando arquivos"):
    if ".pdf" in arquivo:
        merger.append(f"arquivos/{arquivo}")

os.system("cls")
print("Salvando PDF Final...")
merger.write("PDF Final.pdf")

os.system("cls")
print("PDF Final criado com sucesso!")
merger.close()

print("Fim do programa!")