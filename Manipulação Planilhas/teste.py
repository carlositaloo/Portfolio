import pandas as pd

# 1) LEITURA DAS PLANILHAS
# Carrega a planilha "biblioteca.xlsx" que serve como tabela de referência
# Esta planilha contém as descrições e seus respectivos identificadores
bt = pd.read_excel('biblioteca.xlsx', engine='openpyxl')

# Carrega a planilha principal que precisa ser preenchida com os IDs
# Esta planilha contém os cargos que precisam receber os códigos correspondentes
df = pd.read_excel('FUNCOES-RM-AIAMIS-PARA-PREENCHER-CODCARGO.xlsx', engine='openpyxl')

# 2) NORMALIZAÇÃO DOS DADOS
# Normaliza a coluna 'Descricao' da planilha de referência:
# - Converte para string (caso tenha valores não-texto)
# - Remove espaços em branco no início e fim (.strip())
# - Converte tudo para minúsculas (.lower())
bt['Descricao_norm'] = bt['Descricao'].astype(str).str.strip().str.lower()

# Faz a mesma normalização na coluna 'Cargo' da planilha principal
# Isso garante que a comparação entre os textos seja consistente
df['CODCARGORM'] = df['Cargo'].astype(str).str.strip().str.lower()

# 3) CRIAÇÃO DO DICIONÁRIO DE MAPEAMENTO
# Cria um dicionário onde:
# - Chave: descrição normalizada
# - Valor: identificador correspondente
# Exemplo: {'analista de sistemas': 'ID001', 'desenvolvedor': 'ID002'}
map_desc_para_id = dict(zip(bt['Descricao_norm'], bt['Identificador']))

# 4) APLICAÇÃO DO MAPEAMENTO
# Usa o método .map() para buscar cada cargo normalizado no dicionário
# e retornar o ID correspondente. Se não encontrar, retorna NaN
df['ID_correspondente'] = df['CODCARGORM'].map(map_desc_para_id)

# 5) LIMPEZA DOS DADOS TEMPORÁRIOS
# Remove a coluna auxiliar criada para normalização
# inplace=True modifica o DataFrame original sem criar uma cópia
df.drop(columns=['CODCARGORM'], inplace=True)

# 6) FORMATAÇÃO DOS IDs COMO TEXTO COM ZEROS À ESQUERDA
# Converte números para formato de 4 dígitos com zeros à esquerda
# Exemplo: 1 → "0001", 2 → "0002", etc.
df['ID_correspondente'] = df['ID_correspondente'].apply(
    lambda x: f"{int(x):04d}" if pd.notna(x) and str(x) != 'nan' else x
)

# 7) EXPORTAÇÃO DO RESULTADO
# Salva o DataFrame final em uma nova planilha Excel
# index=False evita que os índices do pandas sejam salvos como uma coluna
df.to_excel('resultado_com_ids.xlsx', index=False)