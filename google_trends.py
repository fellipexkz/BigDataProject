import pandas as pd
import matplotlib.pyplot as plt

vendas = pd.read_excel('bd/vendas.xlsx', parse_dates=['Data']).set_index('Data')

pizza_trends = pd.read_csv('bd/pizza_gt.csv', parse_dates=['Semana']).set_index('Semana')
salgado_trends = pd.read_csv('bd/salgado_gt.csv', parse_dates=['Semana']).set_index('Semana')

pizza_mensal = pizza_trends.resample('MS').mean()
salgado_mensal = salgado_trends.resample('MS').mean()

trends_mensal = pizza_mensal.join(salgado_mensal, how='inner')
trends_mensal.rename(columns={'Massa de pizza': 'Pizza'}, inplace=True)

dados_completo = vendas.join(trends_mensal, how='inner')

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(dados_completo.index, dados_completo['Total'], color='b', alpha=0.6, label='Total de Vendas (R$)')
ax1.set_xlabel('')
ax1.set_ylabel('Total de Vendas (R$)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.plot(dados_completo.index, dados_completo['Pizza'], color='r', marker='o', label='Interesse por Pizza')
ax2.plot(dados_completo.index, dados_completo['Salgado'], color='g', marker='s', label='Interesse por Salgado')
ax2.set_ylabel('Interesse no Google Trends', color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title('Total de Vendas e Interesse por Pizza e Salgado de Abril até Setembro')
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.show()
