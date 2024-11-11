import pandas as pd
import matplotlib.pyplot as plt

dados_vendas = pd.read_excel('bd/vendas.xlsx')
dados_vendas['Data'] = pd.to_datetime(dados_vendas['Data'])
dados_vendas_mensal = dados_vendas.resample('MS', on='Data').sum().reset_index()

dados_chuvas = pd.read_csv('bd/chuvas.csv', sep=';', decimal=',', encoding='utf-8')
dados_chuvas.rename(columns={'Precipitacao (mm)': 'Chuva'}, inplace=True)
dados_chuvas['Data'] = pd.to_datetime(dados_chuvas['Data'], format='%Y-%m-%d')
dados_chuvas['Chuva'] = pd.to_numeric(dados_chuvas['Chuva'], errors='coerce')

dados_completo = pd.merge(dados_vendas_mensal, dados_chuvas[['Data', 'Chuva']], on='Data', how='left')

fig, ax1 = plt.subplots(figsize=(12, 6))

ax1.bar(dados_completo['Data'], dados_completo['Total'], color='g', alpha=0.6, label='Total de Vendas (R$)', width=5)
ax1.set_ylabel('Total de Vendas (R$)', color='g')
ax1.tick_params(axis='y', labelcolor='g')

ax2 = ax1.twinx()
ax2.plot(dados_completo['Data'], dados_completo['Chuva'], color='b', label='Chuva Mensal (mm)')
ax2.set_ylabel('Chuva Mensal (mm)', color='b')
ax2.tick_params(axis='y', labelcolor='b')

plt.title('Total de Vendas e Chuva Mensal de Abril até Setembro')
plt.tight_layout()
plt.show()
