# 📊 Trabalho 1 - Introdução à Computação no Mercado Financeiro

**Disciplina:** SSC0964 – Introdução à Computação no Mercado Financeiro  
**Professor:** Denis Fernando Wolf  
**Semestre:** 1º Semestre de 2025  
**Aluno(s):** [Seu nome ou nomes do grupo]  

---

## 🧠 Objetivo

Este trabalho tem como objetivo implementar e analisar **três modelos de fatores** para a seleção de portfólios de ações, utilizando dados do mercado financeiro real. Cada modelo combina pelo menos dois fatores de avaliação e busca identificar os ativos mais promissores com base em critérios quantitativos.

---

## ⚙️ Tecnologias utilizadas

- Python 3
- [yfinance](https://pypi.org/project/yfinance/)
- pandas, numpy
- statsmodels
- matplotlib, seaborn

---

## 📈 Modelos Implementados

### 1. Modelo de **Retorno Total**
> Compara o retorno percentual acumulado de cada ativo entre janeiro de 2024 e abril de 2025.  
📌 Resultado: **WEGE3.SA** teve o maior retorno com **+41,6%**.

---

### 2. Modelo de **Retorno / Volatilidade (Sharpe-like Score)**
> Avalia a eficiência de retorno ajustado ao risco (anualizado).  
📌 Resultado: **WEGE3.SA** apresentou a melhor relação retorno/volatilidade com **Sharpe-like = 0.258**.

---

### 3. Modelo de **Alpha / Beta (CAPM)**
> Estima os parâmetros alpha e beta de cada ativo em relação ao índice Bovespa (^BVSP).  
📌 Resultado: **WEGE3.SA** novamente obteve o melhor desempenho com **Alpha/Beta = 0.00193**.

---

## 🔍 Análise Complementar

- **Heatmap de correlação** entre ativos implementado para avaliar a diversificação.
- Tabela comparativa dos modelos com ranking médio dos ativos.

---

## 📊 Conclusão

O ativo **WEGE3.SA** foi consistentemente o melhor colocado nos três modelos analisados, destacando-se tanto em retorno absoluto quanto ajustado ao risco de mercado e à volatilidade. A análise de correlação reforça a importância de considerar a complementaridade entre ativos na montagem de um portfólio eficiente.

---
