# Relatório de Qualidade e Auditoria do CSV

Este diagnóstico foi gerado com base na skill **conferir-csv**.

- **Arquivo auditado:** `dados\fornecedores - fornecedores copy.csv`
- **Finalidade:** Avaliação de fornecedores via Matriz de Decisão.
- **Total de linhas de dados:** 4
- **Total de colunas:** 5 (`fornecedor, preco_unitario, prazo_dias, defeitos_pct, suporte_nota`)
- **Linhas duplicadas:** 0

## 1. Tabela de Valores Ausentes

| Coluna | Tipo Esperado | Valores Ausentes | % Ausência |
| :--- | :--- | :---: | :---: |
| `fornecedor` | Texto | 0 | 0.0% |
| `preco_unitario` | Numérico | 1 | 25.0% |
| `prazo_dias` | Numérico | 0 | 0.0% |
| `defeitos_pct` | Numérico | 0 | 0.0% |
| `suporte_nota` | Numérico | 1 | 25.0% |

## 2. Problemas Encontrados (Evidências Numéricas)

- ⚠️ **Campo Vazio:** Linha 3 (Fornecedor 'Beta'): coluna 'suporte_nota' está vazia/ausente.
- ⚠️ **Campo Vazio:** Linha 5 (Fornecedor 'Delta'): coluna 'preco_unitario' está vazia/ausente.

## 3. Tratamentos Propostos (Regras da Skill)

1. **Nunca alterar o arquivo original** localizado em `dados/`.
2. **Coluna `preco_unitario` do fornecedor Delta:** Como o preço está vazio, a fórmula da matriz de decisão falharia (divisão por zero ou valor nulo). É necessário solicitar a cotação oficial do Delta à equipe de compras.
3. **Coluna `suporte_nota` do fornecedor Beta:** Obter a avaliação de suporte do Beta para completar o registro.
4. Se os dados não puderem ser obtidos imediatamente, deve-se explicitar a regra adotada (por exemplo, preenchimento pela média dos outros fornecedores ou exclusão do concorrente incompleto) antes de rodar os modelos.
