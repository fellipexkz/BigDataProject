import pandas as pd
import matplotlib.pyplot as plt

dados_vendas = pd.read_excel('bd/vendas.xlsx', parse_dates=['Data'])
dados_vendas_mensal = dados_vendas.resample('MS', on='Data').sum()

dados_ipca = pd.read_csv('bd/ipca.csv', parse_dates=['Data'])
dados_ipca.columns = dados_ipca.columns.str.strip()

dados_completo = dados_vendas_mensal.merge(dados_ipca, on='Data', how='left').reset_index()

fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(dados_completo['Data'], dados_completo['Lucro'], color='b', alpha=0.6, label='Lucro Total (R$)')
ax1.set_ylabel('Lucro Total (R$)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.plot(dados_completo['Data'], dados_completo['IPCA'], color='r', label='IPCA (%)')
ax2.set_ylabel('IPCA (%)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

plt.title('Lucro Total e IPCA (%) de Abril até Setembro')
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
plt.show()
