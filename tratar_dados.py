import os
import csv

# -------------------------------------------------------------
# 1. Definição dos caminhos
# -------------------------------------------------------------
# Conforme a regra de ouro do AGENTS.md, NUNCA alteramos a pasta dados/
caminho_origem = os.path.join("dados", "fornecedores - fornecedores copy.csv")
if not os.path.exists(caminho_origem):
    caminho_origem = os.path.join("dados", "fornecedores_erro.csv")

os.makedirs("resultados", exist_ok=True)
caminho_destino = os.path.join("resultados", "fornecedores_tratado.csv")

print(f"Lendo dados de entrada de: {caminho_origem}")

# -------------------------------------------------------------
# 2. Regra de tratamento documentada (Skill conferir-csv)
# -------------------------------------------------------------
# Valores recuperados a partir da cotação original de compras:
# - Beta: nota de suporte = 9.0
# - Delta: preço unitário = 110.0
valores_oficiais = {
    "Beta": {"suporte_nota": "9"},
    "Delta": {"preco_unitario": "110"}
}

linhas_corrigidas = []

with open(caminho_origem, mode="r", encoding="utf-8") as f:
    leitor = csv.DictReader(f)
    colunas = leitor.fieldnames
    
    for linha in leitor:
        fornecedor = linha["fornecedor"].strip()
        
        # Verifica se o fornecedor tem campos vazios para preencher
        if fornecedor in valores_oficiais:
            for campo, valor_correto in valores_oficiais[fornecedor].items():
                if linha[campo].strip() == "":
                    print(f"-> [TRATAMENTO] Preenchendo coluna '{campo}' do fornecedor '{fornecedor}' com '{valor_correto}'.")
                    linha[campo] = valor_correto
                    
        linhas_corrigidas.append(linha)

# -------------------------------------------------------------
# 3. Salvamento do arquivo tratado em resultados/
# -------------------------------------------------------------
with open(caminho_destino, mode="w", encoding="utf-8", newline="") as f:
    escritor = csv.DictWriter(f, fieldnames=colunas)
    escritor.writeheader()
    escritor.writerows(linhas_corrigidas)

print(f"\nArquivo corrigido e tratado salvo em: {caminho_destino}")

