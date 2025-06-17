import os

# Caminho para o diretório onde estão as imagens
diretorio = "./imagens"  # Altere para o caminho correto

# Itera sobre todos os arquivos do diretório
for nome_arquivo in os.listdir(diretorio):
    if nome_arquivo.startswith("img_") and nome_arquivo.endswith(".png"):
        try:
            # Extrai o número do índice do nome
            indice_antigo = int(nome_arquivo[4:-4])
            # Calcula o novo índice
            indice_novo = indice_antigo + 2000
            # Cria o novo nome
            novo_nome = f"img_{indice_novo}.png"
            # Caminhos completos
            caminho_antigo = os.path.join(diretorio, nome_arquivo)
            caminho_novo = os.path.join(diretorio, novo_nome)
            # Renomeia o arquivo
            os.rename(caminho_antigo, caminho_novo)
        except ValueError:
            print(f"Nome inválido: {nome_arquivo} — ignorado.")
