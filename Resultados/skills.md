# Relatório das Skills do Projeto

Este documento lista e explica todas as skills disponíveis no projeto, com destaque especial para a **nova skill** adicionada à pasta `.agents/skills`.

---

## 1. Nova Skill Adicionada: `Conferir.csv` (`conferir-csv`)

A pasta `.agents/skills/Conferir.csv` foi adicionada recentemente ao projeto.

* **Nome oficial:** `conferir-csv`
* **Finalidade:** Conferir a estrutura e a qualidade de qualquer arquivo CSV antes de iniciar uma análise exploratória ou treinar modelos de Machine Learning.
* **Quando utilizar:**
  - Sempre que uma base de dados nova chegar na pasta `dados/`.
  - Quando for solicitada uma auditoria de qualidade dos dados.

### Checklist e Regras da Skill `Conferir.csv`:
1. **Identificar o objetivo:** Saber qual problema o CSV quer resolver antes de analisar.
2. **Conferir estrutura básica:** Separador (vírgula, ponto-e-vírgula), cabeçalho e o significado de cada linha.
3. **Calcular métricas via código:**
   - Quantidade total de linhas e colunas.
   - Tipos de dados de cada coluna (texto, número inteiro, decimal).
   - Contagem de valores ausentes/nulos (lembrando que espaços em branco contam como ausentes e zero não é nulo).
   - Verificação de linhas duplicadas.
4. **Validar consistência:** Encontrar números armazenados como texto ou valores fora de padrão.
5. **Preservação:** Nunca alterar os arquivos originais em `dados/`.
6. **Prevenção de vazamento (Data Leakage):** Apontar a coluna alvo e checar se há colunas que entregam a resposta antecipadamente.
7. **Entregável obrigatório:** Salvar o resumo da análise em `resultados/qualidade.md`.

---

## 2. Resumo de Todas as Skills Locais do Projeto

Atualmente, o projeto possui **3 skills locais** configuradas em `.agents/skills`:

| # | Pasta / Skill | Descrição e Finalidade | Principal Entregável |
| :-: | :--- | :--- | :--- |
| **1** | **`Conferir.csv`** *(Nova)* | Auditoria e conferência de integridade de arquivos CSV | `resultados/qualidade.md` |
| **2** | **`decision-matrix`** | Matriz de decisão ponderada multi-critério para escolha de alternativas | `resultados/relatorio_decisao_fornecedores.md` |
| **3** | **`chart-image`** | Criação de gráficos analíticos de alta qualidade visual com Matplotlib | Imagens em `resultados/*.png` |

---

## 3. Skills Embutidas do Sistema Antigravity

Além das 3 skills locais do projeto, o sistema conta com 7 utilitários nativos:

1. **`agy-customizations`:** Guia de referência do sistema de personalização (skills, regras e plugins).
2. **`antigravity-guide`:** Manual e guia completo da interface e CLI do Antigravity.
3. **`automation`:** Configuração de rotinas e agendamento de tarefas em segundo plano.
4. **`generative_ui`:** Criação de componentes visuais e interfaces interativas em HTML.
5. **`migrate-workflows`:** Ferramenta para migração de fluxos antigos para o padrão moderno de skills.
6. **`plugin`:** Criação e gerenciamento de pacotes e plugins.
7. **`ui-plugin-navigation`:** Controle dos painéis laterais de navegação da interface.

