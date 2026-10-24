import os
import csv

# -------------------------------------------------------------
# 1. Identificação do arquivo
# -------------------------------------------------------------
# Verifica se existe fornecedores_erro.csv ou a cópia com erros aberta no editor
candidatos = [
    os.path.join("dados", "fornecedores_erro.csv"),
    os.path.join("dados", "fornecedores - fornecedores copy.csv"),
    os.path.join("Dados", "fornecedores_erro.csv"),
    os.path.join("Dados", "fornecedores - fornecedores copy.csv"),
]

caminho_csv = None
for c in candidatos:
    if os.path.exists(c):
        caminho_csv = c
        break

if not caminho_csv:
    raise FileNotFoundError("Arquivo de dados não encontrado na pasta dados/.")

print(f"--- Skill conferir-csv: Auditoria em {caminho_csv} ---\n")

# -------------------------------------------------------------
# 2. Leitura da estrutura e cálculo das métricas com código
# -------------------------------------------------------------
with open(caminho_csv, "r", encoding="utf-8") as f:
    linhas_brutas = [linha.rstrip("\r\n") for linha in f if linha.strip()]

linhas_totais = len(linhas_brutas)
cabecalho = [col.strip() for col in linhas_brutas[0].split(",")]
num_colunas = len(cabecalho)
num_registros = linhas_totais - 1

dados = []
ausencias_por_coluna = {col: 0 for col in cabecalho}
problemas = []

for num_linha, linha in enumerate(linhas_brutas[1:], start=2):
    campos = [c.strip() for c in linha.split(",")]
    
    # Valida número de campos
    if len(campos) != num_colunas:
        problemas.append(f"Linha {num_linha}: quantidade de campos ({len(campos)}) diferente do cabeçalho ({num_colunas}).")
    
    registro = {}
    for i, col in enumerate(cabecalho):
        val = campos[i] if i < len(campos) else ""
        # Texto vazio ou somente espaços conta como ausência (regra 4 da skill)
        if val == "":
            ausencias_por_coluna[col] += 1
            fornecedor_nome = campos[0] if campos[0] != "" else f"Registro linha {num_linha}"
            problemas.append(f"Linha {num_linha} (Fornecedor '{fornecedor_nome}'): coluna '{col}' está vazia/ausente.")
        registro[col] = val
    dados.append(registro)

# Duplicatas
linhas_dados = linhas_brutas[1:]
num_duplicadas = len(linhas_dados) - len(set(linhas_dados))

# Verificação de tipos numéricos esperados
colunas_numericas = ["preco_unitario", "prazo_dias", "defeitos_pct", "suporte_nota"]
inconsistencias_tipo = []

for num_linha, reg in enumerate(dados, start=2):
    for col in colunas_numericas:
        val = reg.get(col, "")
        if val != "":
            try:
                num = float(val)
                if num < 0:
                    inconsistencias_tipo.append(f"Linha {num_linha}: número negativo inválido ({num}) na coluna '{col}'.")
            except ValueError:
                inconsistencias_tipo.append(f"Linha {num_linha}: valor não numérico '{val}' na coluna '{col}'.")

# -------------------------------------------------------------
# 3. Exibição no Terminal
# -------------------------------------------------------------
print(f"Total de registros: {num_registros}")
print(f"Total de colunas:   {num_colunas} ({', '.join(cabecalho)})")
print(f"Linhas duplicadas:  {num_duplicadas}")
print("\nValores ausentes por coluna:")
for col, qtd in ausencias_por_coluna.items():
    print(f"  - {col}: {qtd} ausente(s)")

print("\nEvidências dos problemas encontrados:")
if problemas or inconsistencias_tipo:
    for p in problemas:
        print(f"  [PROBLEMA] {p}")
    for it in inconsistencias_tipo:
        print(f"  [PROBLEMA] {it}")
else:
    print("  [OK] Nenhum problema detectado.")

# -------------------------------------------------------------
# 4. Geração do Relatório resultados/qualidade.md (Regra 8 da skill)
# -------------------------------------------------------------
os.makedirs("resultados", exist_ok=True)
caminho_relatorio = os.path.join("resultados", "qualidade.md")

with open(caminho_relatorio, "w", encoding="utf-8") as f:
    f.write("# Relatório de Qualidade e Auditoria do CSV\n\n")
    f.write(f"Este diagnóstico foi gerado com base na skill **conferir-csv**.\n\n")
    f.write(f"- **Arquivo auditado:** `{caminho_csv}`\n")
    f.write(f"- **Finalidade:** Avaliação de fornecedores via Matriz de Decisão.\n")
    f.write(f"- **Total de linhas de dados:** {num_registros}\n")
    f.write(f"- **Total de colunas:** {num_colunas} (`{', '.join(cabecalho)}`)\n")
    f.write(f"- **Linhas duplicadas:** {num_duplicadas}\n\n")

    f.write("## 1. Tabela de Valores Ausentes\n\n")
    f.write("| Coluna | Tipo Esperado | Valores Ausentes | % Ausência |\n")
    f.write("| :--- | :--- | :---: | :---: |\n")
    for col in cabecalho:
        qtd = ausencias_por_coluna[col]
        pct = (qtd / num_registros) * 100 if num_registros > 0 else 0
        tipo = "Texto" if col == "fornecedor" else "Numérico"
        f.write(f"| `{col}` | {tipo} | {qtd} | {pct:.1f}% |\n")
    f.write("\n")

    f.write("## 2. Problemas Encontrados (Evidências Numéricas)\n\n")
    if problemas or inconsistencias_tipo:
        for p in problemas:
            f.write(f"- ⚠️ **Campo Vazio:** {p}\n")
        for it in inconsistencias_tipo:
            f.write(f"- ⚠️ **Tipo Inválido:** {it}\n")
    else:
        f.write("- Nenhum problema foi detectado.\n")
    f.write("\n")

    f.write("## 3. Tratamentos Propostos (Regras da Skill)\n\n")
    f.write("1. **Nunca alterar o arquivo original** localizado em `dados/`.\n")
    f.write("2. **Coluna `preco_unitario` do fornecedor Delta:** Como o preço está vazio, a fórmula da matriz de decisão falharia (divisão por zero ou valor nulo). É necessário solicitar a cotação oficial do Delta à equipe de compras.\n")
    f.write("3. **Coluna `suporte_nota` do fornecedor Beta:** Obter a avaliação de suporte do Beta para completar o registro.\n")
    f.write("4. Se os dados não puderem ser obtidos imediatamente, deve-se explicitar a regra adotada (por exemplo, preenchimento pela média dos outros fornecedores ou exclusão do concorrente incompleto) antes de rodar os modelos.\n")

print(f"\nRelatório de qualidade gerado com sucesso em: {caminho_relatorio}")

