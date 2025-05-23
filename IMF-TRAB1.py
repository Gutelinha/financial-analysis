import yfinance as yf
import pandas as pd
import numpy as np
import statsmodels.api as sm
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

# Lista de ações e benchmark
tickers = ["PETR4.SA", "VALE3.SA", "WEGE3.SA", "LREN3.SA", "MGLU3.SA", "B3SA3.SA"]
benchmark = "^BVSP"

# Período da análise
start_date = "2024-01-01"
end_date = "2025-04-30"

# Coleta de dados
data = yf.download(tickers + [benchmark], start=start_date, end=end_date, auto_adjust=True)['Close']
returns = data.pct_change().dropna()

# ---------------------------
# Modelo 1: Retorno acumulado
# ---------------------------
start_date_nearest = data.index[data.index.get_indexer([pd.to_datetime(start_date)], method='nearest')[0]]
end_date_nearest = data.index[data.index.get_indexer([pd.to_datetime(end_date)], method='nearest')[0]]

total_return = (data.loc[end_date_nearest] / data.loc[start_date_nearest] - 1) * 100

# -------------------------------
# Modelo 2: Retorno / Volatilidade
# -------------------------------
monthly_returns = returns.resample('M').mean()
monthly_volatility = returns.resample('M').std()

annualized_return = monthly_returns.mean() * 12 * 100
annualized_volatility = monthly_volatility.mean() * np.sqrt(12) * 100
sharpe_like = annualized_return / annualized_volatility
best_asset = sharpe_like.idxmax()

# -------------------------------
# Modelo 3: Alpha / Beta (CAPM)
# -------------------------------
def capm_regression(stock, market):
    X = sm.add_constant(market)
    model = sm.OLS(stock, X).fit()
    return model.params[0], model.params[1], model.rsquared

alpha_beta = {}
for ticker in tickers:
    alpha, beta, r2 = capm_regression(returns[ticker], returns[benchmark])
    score = alpha / beta if beta != 0 else 0
    alpha_beta[ticker] = {"Alpha": alpha, "Beta": beta, "Score": score, "R²": r2}

capm_df = pd.DataFrame(alpha_beta).T

# ---------------------
# Tabela comparativa
# ---------------------
summary = pd.DataFrame({
    'Total Return (%)': total_return,
    'Sharpe-like': sharpe_like,
    'Alpha/Beta Score': capm_df['Score'],
    'R²': capm_df['R²']
})
summary['Retorno Rank'] = summary['Total Return (%)'].rank(ascending=False)
summary['Sharpe Rank'] = summary['Sharpe-like'].rank(ascending=False)
summary['CAPM Rank'] = summary['Alpha/Beta Score'].rank(ascending=False)
summary['Média Rank'] = summary[['Retorno Rank', 'Sharpe Rank', 'CAPM Rank']].mean(axis=1)

# ---------------------
# Exibição de resultados
# ---------------------
print("Retorno total (%):")
print(total_return.sort_values(ascending=False))

print("\nSharpe-like score (Retorno anual / Volatilidade anual):")
print(sharpe_like.sort_values(ascending=False))

print(f'\nAtivo com a melhor relação retorno/volatilidade: {best_asset}')

print("\nAlpha / Beta score (Modelo CAPM):")
print(capm_df.sort_values("Score", ascending=False))

print("\nResumo comparativo dos modelos:")
print(summary.sort_values("Média Rank"))

# ---------------------
# Gráficos
# ---------------------
plt.figure()
total_return.sort_values().plot(kind='barh', color='skyblue')
plt.title('Retorno Acumulado (%) - Jan/24 a Abr/25')
plt.xlabel('Retorno (%)')
plt.ylabel('Ativo')
plt.grid(True)
plt.tight_layout()

plt.figure()
sharpe_like.sort_values().plot(kind='barh', color='seagreen')
plt.title('Sharpe-like Score (Anualizado)')
plt.xlabel('Sharpe-like')
plt.ylabel('Ativo')
plt.grid(True)
plt.tight_layout()

plt.figure()
capm_df['Score'].sort_values().plot(kind='barh', color='coral')
plt.title('Score Alpha/Beta (Modelo CAPM)')
plt.xlabel('Alpha / Beta')
plt.ylabel('Ativo')
plt.grid(True)
plt.tight_layout()

# Retorno acumulado diário
cumulative_returns = (1 + returns[tickers]).cumprod() - 1
plt.figure(figsize=(12, 6))
cumulative_returns.plot()
plt.title('Retorno Acumulado Diário (%)')
plt.ylabel('Retorno acumulado')
plt.xlabel('Data')
plt.legend(loc='upper left')
plt.grid(True)
plt.tight_layout()

# Heatmap de correlação
correlation = returns[tickers].corr()
plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap="coolwarm")
plt.title("Correlação entre os ativos")
plt.tight_layout()

plt.show()
