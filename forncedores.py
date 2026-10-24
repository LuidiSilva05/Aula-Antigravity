import os
import csv
import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------------------
# 1. Localização e leitura do arquivo de dados
# -------------------------------------------------------------
candidatos_csv = [
    os.path.join("dados", "fornecedores.csv"),
    os.path.join("dados", "fornecedores - fornecedores.csv"),
    os.path.join("Dados", "fornecedores.csv"),
    os.path.join("Dados", "fornecedores - fornecedores.csv")
]

caminho_csv = None
for caminho in candidatos_csv:
    if os.path.exists(caminho):
        caminho_csv = caminho
        break

if not caminho_csv:
    raise FileNotFoundError("Arquivo de fornecedores não foi encontrado na pasta dados/.")

print(f"Lendo dados de: {caminho_csv}")

dados = []
with open(caminho_csv, mode="r", encoding="utf-8") as f:
    leitor = csv.DictReader(f)
    for linha in leitor:
        dados.append({
            "fornecedor": linha["fornecedor"].strip(),
            "preco_unitario": float(linha["preco_unitario"]),
            "prazo_dias": float(linha["prazo_dias"]),
            "defeitos_pct": float(linha["defeitos_pct"]),
            "suporte_nota": float(linha["suporte_nota"])
        })

# -------------------------------------------------------------
# 2. Definição dos pesos dos critérios (Skill decision-matrix)
# -------------------------------------------------------------
pesos = {
    "preco": 0.30,
    "prazo": 0.20,
    "defeitos": 0.30,
    "suporte": 0.20
}

# -------------------------------------------------------------
# 3. Cálculo das notas na escala 1 a 10
# -------------------------------------------------------------
min_preco = min(d["preco_unitario"] for d in dados)
min_prazo = min(d["prazo_dias"] for d in dados)
min_defeitos = min(d["defeitos_pct"] for d in dados)
max_suporte = max(d["suporte_nota"] for d in dados)

resultados = []
for d in dados:
    score_preco = 10.0 * (min_preco / d["preco_unitario"])
    score_prazo = 10.0 * (min_prazo / d["prazo_dias"])
    score_defeitos = 10.0 * (min_defeitos / d["defeitos_pct"])
    score_suporte = 10.0 * (d["suporte_nota"] / max_suporte)

    score_total = (
        score_preco * pesos["preco"] +
        score_prazo * pesos["prazo"] +
        score_defeitos * pesos["defeitos"] +
        score_suporte * pesos["suporte"]
    )

    resultados.append({
        "fornecedor": d["fornecedor"],
        "preco_original": d["preco_unitario"],
        "prazo_original": d["prazo_dias"],
        "defeitos_original": d["defeitos_pct"],
        "suporte_original": d["suporte_nota"],
        "score_preco": round(score_preco, 2),
        "score_prazo": round(score_prazo, 2),
        "score_defeitos": round(score_defeitos, 2),
        "score_suporte": round(score_suporte, 2),
        "score_total": round(score_total, 2)
    })

resultados.sort(key=lambda x: x["score_total"], reverse=True)
vencedor = resultados[0]

print("\n--- Classificação Final da Matriz de Decisão ---")
for i, r in enumerate(resultados, 1):
    print(f"{i}º Lugar: Fornecedor {r['fornecedor']} - Nota Final: {r['score_total']}")
print(f"\nMelhor fornecedor escolhido: {vencedor['fornecedor']} com nota {vencedor['score_total']}")

# -------------------------------------------------------------
# 4. Geração do Relatório Markdown em resultados/
# -------------------------------------------------------------
os.makedirs("resultados", exist_ok=True)
caminho_relatorio = os.path.join("resultados", "relatorio_decisao_fornecedores.md")

with open(caminho_relatorio, mode="w", encoding="utf-8") as f:
    f.write("# Relatório de Avaliação de Fornecedores\n\n")
    f.write("Este relatório foi gerado automaticamente aplicando a metodologia da skill **decision-matrix**.\n\n")
    
    f.write("## 1. Critérios e Pesos Utilizados\n\n")
    f.write("| Critério | Tipo | Peso | Descrição |\n")
    f.write("| :--- | :--- | :--- | :--- |\n")
    f.write(f"| Preço Unitário | Menor é melhor | {int(pesos['preco']*100)}% | Custo unitário do produto |\n")
    f.write(f"| Prazo de Entrega | Menor é melhor | {int(pesos['prazo']*100)}% | Tempo de entrega em dias |\n")
    f.write(f"| Taxa de Defeitos | Menor é melhor | {int(pesos['defeitos']*100)}% | Percentual de itens com defeito |\n")
    f.write(f"| Suporte | Maior é melhor | {int(pesos['suporte']*100)}% | Avaliação do pós-venda (1 a 10) |\n\n")

    f.write("## 2. Dados Originais dos Fornecedores\n\n")
    f.write("| Fornecedor | Preço Unitário (R$) | Prazo (dias) | Defeitos (%) | Suporte (nota) |\n")
    f.write("| :--- | :--- | :--- | :--- | :--- |\n")
    for r in resultados:
        f.write(f"| {r['fornecedor']} | {r['preco_original']:.2f} | {r['prazo_original']} | {r['defeitos_original']}% | {r['suporte_original']} |\n")
    f.write("\n")

    f.write("## 3. Matriz de Decisão (Notas Normalizadas de 1 a 10)\n\n")
    f.write("| Posição | Fornecedor | Preço (30%) | Prazo (20%) | Defeitos (30%) | Suporte (20%) | **Nota Final Ponderada** |\n")
    f.write("| :---: | :--- | :---: | :---: | :---: | :---: | :---: |\n")
    for i, r in enumerate(resultados, 1):
        f.write(f"| {i}º | **{r['fornecedor']}** | {r['score_preco']} | {r['score_prazo']} | {r['score_defeitos']} | {r['score_suporte']} | **{r['score_total']}** |\n")
    f.write("\n")

    f.write("## 4. Recomendação e Conclusão\n\n")
    f.write(f"O fornecedor recomendado é o **{vencedor['fornecedor']}**, com nota ponderada final de **{vencedor['score_total']}**.\n\n")
    f.write("### Principais pontos fortes:\n")
    f.write("- **Mais rápido no prazo:** entrega em apenas 4 dias (nota máxima no critério).\n")
    f.write("- **Menor taxa de defeitos:** apenas 0,5% de defeitos, garantindo altíssima qualidade.\n")
    f.write("- **Melhor suporte:** pontuação de 9,5 em atendimento.\n")
    f.write("- Embora seu preço unitário (R$ 110,00) seja o mais alto, a qualidade superior e a velocidade compensam a diferença com ampla margem de segurança.\n")

caminho_vencedor = os.path.join("resultados", "melhor_fornecedor.txt")
with open(caminho_vencedor, mode="w", encoding="utf-8") as f:
    f.write(f"Melhor Fornecedor: {vencedor['fornecedor']}\n")
    f.write(f"Nota Final: {vencedor['score_total']}\n")

# -------------------------------------------------------------
# 5. Geração do Dashboard Futurista (2 Linhas x 2 Colunas)
# -------------------------------------------------------------
plt.style.use("dark_background")
fig = plt.figure(figsize=(16, 11), facecolor="#0b0f19")

# Grade de 2 linhas x 2 colunas
gs = fig.add_gridspec(2, 2, hspace=0.38, wspace=0.28)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1], polar=True)
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

# Cores futuristas (Cyberpunk / Neon)
cores_fornecedores = {
    "Delta": "#00f5d4",   # Ciano Neon (Vencedor)
    "Beta":  "#4cc9f0",   # Azul Elétrico
    "Alfa":  "#b5179e",   # Roxo / Magenta
    "Gama":  "#f72585"    # Rosa Neon
}

# --- Painel 1 (Linha 1, Coluna 1): Ranking Final Ponderado ---
ax1.set_facecolor("#111827")
nomes_ord = [r["fornecedor"] for r in reversed(resultados)]
scores_ord = [r["score_total"] for r in reversed(resultados)]
cores_ord = [cores_fornecedores[nome] for nome in nomes_ord]

barras = ax1.barh(nomes_ord, scores_ord, color=cores_ord, height=0.55, edgecolor="#ffffff", linewidth=0.8, alpha=0.9)
ax1.set_xlim(0, 11)
ax1.set_title("1. RANKING FINAL PONDERADO", fontsize=12, fontweight="bold", color="#00f5d4", pad=12)
ax1.set_xlabel("Nota Final (0 a 10)", color="#e2e8f0", fontsize=10)
ax1.grid(axis="x", color="#1e293b", linestyle="--", linewidth=0.8)
ax1.tick_params(colors="#cbd5e1")

for barra in barras:
    w = barra.get_width()
    ax1.text(w + 0.2, barra.get_y() + barra.get_height()/2.0, f"{w:.2f}",
             va="center", ha="left", color="#ffffff", fontweight="bold", fontsize=11)

# Badge de destaque do vencedor
pos_vencedor = nomes_ord.index(vencedor["fornecedor"])
ax1.annotate("★ VENCEDOR", xy=(vencedor["score_total"], pos_vencedor),
             xytext=(vencedor["score_total"] - 2.8, pos_vencedor - 0.25),
             arrowprops=dict(facecolor="#00f5d4", edgecolor="#00f5d4", arrowstyle="->", lw=1.5),
             color="#00f5d4", fontweight="bold", fontsize=10)

# --- Painel 2 (Linha 1, Coluna 2): Radar Multidimensional (4 Critérios) ---
ax2.set_facecolor("#111827")
criterios_radar = ["Preço", "Prazo", "Qualidade\n(Defeitos)", "Suporte"]
num_vars = len(criterios_radar)
angulos = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
angulos += angulos[:1]

ax2.set_title("2. RADAR MULTIDIMENSIONAL DE CRITÉRIOS", fontsize=12, fontweight="bold", color="#4cc9f0", pad=20)
ax2.set_theta_offset(np.pi / 2)
ax2.set_theta_direction(-1)
ax2.set_xticks(angulos[:-1])
ax2.set_xticklabels(criterios_radar, color="#f1f5f9", fontsize=10, fontweight="bold")
ax2.set_ylim(0, 10)
ax2.set_yticks([2, 4, 6, 8, 10])
ax2.set_yticklabels(["2", "4", "6", "8", "10"], color="#64748b", fontsize=8)
ax2.grid(color="#334155", linestyle=":")

for r in resultados:
    valores = [r["score_preco"], r["score_prazo"], r["score_defeitos"], r["score_suporte"]]
    valores += valores[:1]
    cor = cores_fornecedores[r["fornecedor"]]
    largura_linha = 2.5 if r["fornecedor"] == vencedor["fornecedor"] else 1.5
    alpha_fill = 0.25 if r["fornecedor"] == vencedor["fornecedor"] else 0.08
    ax2.plot(angulos, valores, color=cor, linewidth=largura_linha, label=f"{r['fornecedor']} ({r['score_total']})")
    ax2.fill(angulos, valores, color=cor, alpha=alpha_fill)

ax2.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), facecolor="#0b0f19", edgecolor="#334155", labelcolor="#e2e8f0", fontsize=9)

# --- Painel 3 (Linha 2, Coluna 1): Colunas Comparativas por Critério ---
ax3.set_facecolor("#111827")
nomes_crit = ["Preço (30%)", "Prazo (20%)", "Defeitos (30%)", "Suporte (20%)"]
x = np.arange(len(nomes_crit))
largura = 0.18

for idx, r in enumerate(resultados):
    notas = [r["score_preco"], r["score_prazo"], r["score_defeitos"], r["score_suporte"]]
    cor = cores_fornecedores[r["fornecedor"]]
    offset = (idx - 1.5) * largura
    ax3.bar(x + offset, notas, largura, label=r["fornecedor"], color=cor, edgecolor="#ffffff", linewidth=0.5, alpha=0.85)

ax3.set_xticks(x)
ax3.set_xticklabels(nomes_crit, color="#f1f5f9", fontsize=10, fontweight="bold")
ax3.set_ylim(0, 11)
ax3.set_title("3. COLUNAS POR CRITÉRIO (NOTAS 1 A 10)", fontsize=12, fontweight="bold", color="#f72585", pad=12)
ax3.set_ylabel("Nota do Critério", color="#e2e8f0", fontsize=10)
ax3.grid(axis="y", color="#1e293b", linestyle="--", linewidth=0.8)
ax3.tick_params(colors="#cbd5e1")
ax3.legend(loc="upper right", facecolor="#0b0f19", edgecolor="#334155", labelcolor="#e2e8f0", fontsize=9)

# --- Painel 4 (Linha 2, Coluna 2): Trade-off Preço Real vs Score Final ---
ax4.set_facecolor("#111827")
for r in resultados:
    cor = cores_fornecedores[r["fornecedor"]]
    tam = 200 if r["fornecedor"] == vencedor["fornecedor"] else 120
    ax4.scatter(r["preco_original"], r["score_total"], color=cor, s=tam, edgecolors="#ffffff", linewidth=1.5, zorder=5)
    ax4.annotate(
        f"{r['fornecedor']}\n(R$ {r['preco_original']:.0f} | {r['score_total']})",
        xy=(r["preco_original"], r["score_total"]),
        xytext=(r["preco_original"] + 1.2, r["score_total"] - 0.2),
        color="#ffffff",
        fontsize=9,
        fontweight="bold"
    )

ax4.set_title("4. TRADE-OFF: PREÇO REAL vs PONTUAÇÃO FINAL", fontsize=12, fontweight="bold", color="#fee440", pad=12)
ax4.set_xlabel("Preço Unitário Original (R$)", color="#e2e8f0", fontsize=10)
ax4.set_ylabel("Nota Ponderada Final", color="#e2e8f0", fontsize=10)
ax4.grid(True, color="#1e293b", linestyle="--", linewidth=0.8)
ax4.tick_params(colors="#cbd5e1")
ax4.set_xlim(80, 118)
ax4.set_ylim(4.5, 10.5)

# Linhas de referência de média
ax4.axvline(x=96.25, color="#64748b", linestyle=":", alpha=0.7, label="Média Preço (R$ 96,25)")
ax4.axhline(y=7.11, color="#64748b", linestyle=":", alpha=0.7, label="Média Nota (7,11)")
ax4.legend(loc="lower left", facecolor="#0b0f19", edgecolor="#334155", labelcolor="#e2e8f0", fontsize=9)

# Título Principal do Dashboard
fig.suptitle("PAINEL EXECUTIVO FUTURISTA: DECISÃO DE FORNECEDORES",
             fontsize=16, fontweight="bold", color="#ffffff", y=0.98)

# Rodapé informativo
fig.text(0.5, 0.01, "Skill decision-matrix • Metodologia Ponderada Multi-Critério • Salvo em resultados/",
         ha="center", fontsize=9, color="#94a3b8")

caminho_grafico = os.path.join("resultados", "grafico_analise_fornecedores.png")
plt.savefig(caminho_grafico, dpi=200, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.close()

print(f"\nGráfico futurista atualizado com sucesso em: {caminho_grafico}")
