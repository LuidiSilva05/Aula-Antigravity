import os
import matplotlib.pyplot as plt

# 1. Definindo os pontos conhecidos de calibração
# Ponto 1: (0 °C, 4 mA)
# Ponto 2: (100 °C, 20 mA)
x1, y1 = 0.0, 4.0
x2, y2 = 100.0, 20.0

# 2. Calculando os coeficientes da reta (y = a*x + b)
a = (y2 - y1) / (x2 - x1)
b = y1 - (a * x1)

print("--- Calibração do Termômetro ---")
print(f"Valor de A (coeficiente angular): {a}")
print(f"Valor de B (coeficiente linear):  {b}")
print(f"Equação da reta: y = {a} * x + {b}\n")

# 3. Temperatura de teste (x = 50 graus)
x_teste = 50.0
y_teste = a * x_teste + b

print(f"Temperatura informada: {x_teste} °C")
print(f"Corrente calculada:    {y_teste} mA\n")

# 4. Verificação de avisos (fora das faixas padrão)
# Aviso de temperatura: 0 a 100 °C
if x_teste < 0.0 or x_teste > 100.0:
    print("[AVISO] Temperatura fora da faixa de 0 a 100 °C!")
else:
    print("[OK] Temperatura dentro da faixa operacional.")

# Aviso de corrente: 4 a 20 mA
if y_teste < 4.0 or y_teste > 20.0:
    print("[AVISO] Corrente fora da faixa de 4 a 20 mA!")
else:
    print("[OK] Corrente dentro da faixa operacional.")

# 5. Classificação da temperatura
# Baixa: até 30 graus | Média: até 60 graus | Alta: acima de 60 graus
if x_teste <= 30.0:
    classificacao = "Baixa"
elif x_teste <= 60.0:
    classificacao = "Média"
else:
    classificacao = "Alta"

print(f"Classificação da temperatura: {classificacao}\n")

# 6. Criação do gráfico com Matplotlib
# Eixo X = Temperatura (°C) | Eixo Y = Corrente Elétrica (mA)
temperaturas = [0, 20, 40, 60, 80, 100]
correntes = [a * t + b for t in temperaturas]

plt.figure(figsize=(8, 5))

# Linha de calibração
plt.plot(temperaturas, correntes, label="Curva (4-20 mA)", color="blue", linewidth=2)

# Ponto de teste em destaque
plt.scatter([x_teste], [y_teste], color="red", s=100, zorder=5, label=f"Ponto Teste ({x_teste} °C, {y_teste} mA)")

# Linhas pontilhadas indicando as faixas de classificação
plt.axvline(x=30, color="gray", linestyle="--", alpha=0.7, label="Limite Baixa/Média (30 °C)")
plt.axvline(x=60, color="orange", linestyle="--", alpha=0.7, label="Limite Média/Alta (60 °C)")

plt.title("Relação Temperatura x Corrente Elétrica")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Corrente Elétrica (mA)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()

# Garante a criação da pasta 'resultados' conforme combinado da aula e salva o gráfico
os.makedirs("resultados", exist_ok=True)
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")
plt.savefig(caminho_grafico, dpi=150, bbox_inches="tight")
plt.close()

print(f"Gráfico gerado e salvo em: {caminho_grafico}")

print(f"Temperatura informada: {x_teste} °C")
print(f"Corrente calculada:    {y_teste} mA\n")

# 4. Verificação de avisos (fora das faixas padrão)
# Aviso de temperatura: 0 a 100 °C
if x_teste < 0.0 or x_teste > 100.0:
    print("[AVISO] Temperatura fora da faixa de 0 a 100 °C!")
else:
    print("[OK] Temperatura dentro da faixa operacional.")

# Aviso de corrente: 4 a 20 mA
if y_teste < 4.0 or y_teste > 20.0:
    print("[AVISO] Corrente fora da faixa de 4 a 20 mA!")
else:
    print("[OK] Corrente dentro da faixa operacional.")

# 5. Classificação da temperatura
# Baixa: até 30 graus | Média: até 60 graus | Alta: acima de 60 graus
if x_teste <= 30.0:
    classificacao = "Baixa"
elif x_teste <= 60.0:
    classificacao = "Média"
else:
    classificacao = "Alta"

print(f"Classificação da temperatura: {classificacao}\n")

# 6. Criação do gráfico com Matplotlib
# Eixo X = Temperatura (°C) | Eixo Y = Corrente Elétrica (mA)
temperaturas = [0, 20, 40, 60, 80, 100]
correntes = [a * t + b for t in temperaturas]

plt.figure(figsize=(8, 5))

# Linha de calibração
plt.plot(temperaturas, correntes, label="Curva (4-20 mA)", color="blue", linewidth=2)

# Ponto de teste em destaque
plt.scatter([x_teste], [y_teste], color="red", s=100, zorder=5, label=f"Ponto Teste ({x_teste} °C, {y_teste} mA)")

# Linhas pontilhadas indicando as faixas de classificação
plt.axvline(x=30, color="gray", linestyle="--", alpha=0.7, label="Limite Baixa/Média (30 °C)")
plt.axvline(x=60, color="orange", linestyle="--", alpha=0.7, label="Limite Média/Alta (60 °C)")

plt.title("Relação Temperatura x Corrente Elétrica")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Corrente Elétrica (mA)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()

# Garante a criação da pasta 'resultados' conforme combinado da aula e salva o gráfico
os.makedirs("resultados", exist_ok=True)
caminho_grafico = os.path.join("resultados", "grafico_termometro.png")
plt.savefig(caminho_grafico, dpi=150, bbox_inches="tight")
plt.close()

print(f"Gráfico gerado e salvo em: {caminho_grafico}")

