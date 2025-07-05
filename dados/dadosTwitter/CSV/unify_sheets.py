import pandas as pd
import os

# Caminho da pasta com os arquivos
pasta = "C:\\Users\\Pessoal\\Documents\\Unifesp\\Aries\\aries_topic_selector\\dados\\dadosGov"

# Lista todos os arquivos CSV na pasta
arquivos_csv = [f for f in os.listdir(pasta) if f.endswith('.csv')]

# Lista para armazenar os DataFrames
tabelas = []

# Lê e adiciona cada CSV na lista
for arquivo in arquivos_csv:
    caminho_completo = os.path.join(pasta, arquivo)
    try:
        # Tenta com separador vírgula
        df = pd.read_csv(caminho_completo, sep=',', encoding='utf-8', on_bad_lines='skip')
        tabelas.append(df)
    except Exception as e:
        print(f"Erro ao ler {arquivo}: {e}")

# Concatena todos os DataFrames
if tabelas:
    tudo_junto = pd.concat(tabelas, ignore_index=True)
    tudo_junto.to_csv("unificado.csv", index=False)
    tudo_junto.to_excel("unificado.xlsx", index=False)
    print("CSV unificado salvo como 'unificado.csv'")
else:
    print("Nenhum CSV pôde ser lido com sucesso.")
