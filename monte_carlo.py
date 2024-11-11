import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dados_vendas = pd.read_excel('bd/vendas.xlsx')
dados_vendas.columns = ['Data', 'Cliente', 'Produto', 'Quantidade', 'Preço Unitário', 'Total', 'Custo Unitário', 'Custo Total', 'Lucro']
dados_vendas['Data'] = pd.to_datetime(dados_vendas['Data'])
vendas_mensais = dados_vendas.groupby(dados_vendas['Data'].dt.month)['Total'].sum()

dados_ipca = pd.read_csv('bd/ipca.csv', sep=',', parse_dates=['Data'], decimal='.')
dados_ipca.columns = dados_ipca.columns.str.strip()
dados_ipca = dados_ipca.loc[:, dados_ipca.columns.notnull()]
dados_ipca.set_index('Data', inplace=True)

dados_chuvas = pd.read_csv('bd/chuvas.csv', sep=';', parse_dates=['Data'], decimal=',')
dados_chuvas.columns = dados_chuvas.columns.str.strip()
dados_chuvas = dados_chuvas.loc[:, dados_chuvas.columns.notnull()]
dados_chuvas = dados_chuvas.loc[:, ~dados_chuvas.columns.str.contains('^Unnamed')]
dados_chuvas.set_index('Data', inplace=True)

media_vendas = vendas_mensais.mean()
desvio_vendas = vendas_mensais.std()
media_ipca = dados_ipca['IPCA'].mean()
desvio_ipca = dados_ipca['IPCA'].std()
media_chuvas = dados_chuvas['Precipitacao (mm)'].mean()
desvio_chuvas = dados_chuvas['Precipitacao (mm)'].std()

meses = 12
N = 1000
simulacoes_vendas = []
for _ in range(N):
    ipca_simulado = np.random.normal(media_ipca, desvio_ipca, meses)
    chuvas_simuladas = np.random.normal(media_chuvas, desvio_chuvas, meses)
    vendas_simuladas = []
    for mes in range(meses):
        efeito_ipca = (1 - ipca_simulado[mes] / 100)
        efeito_chuvas = (1 - chuvas_simuladas[mes] / 1000)
        venda_simulada = media_vendas * efeito_ipca * efeito_chuvas
        vendas_simuladas.append(venda_simulada)
    simulacoes_vendas.append(vendas_simuladas)
simulacoes_df = pd.DataFrame(simulacoes_vendas).T
simulacoes_df.columns = [f'Simulação {i+1}' for i in range(N)]

vendas_projetadas = simulacoes_df.mean(axis=1)
intervalo_inferior = simulacoes_df.quantile(0.05, axis=1)
intervalo_superior = simulacoes_df.quantile(0.95, axis=1)
meses_range = range(1, meses + 1)

plt.figure(figsize=(14, 8))
plt.bar(meses_range, vendas_projetadas, color='skyblue', label='Média Simulada de Vendas')
plt.fill_between(meses_range, intervalo_inferior, intervalo_superior, color='b', alpha=0.2, label='Intervalo de 90% de Confiança')
plt.title('Projeção de Vendas Mensais para 2025')
plt.xlabel('Mês')
plt.ylabel('Vendas (R$)')
plt.xticks(meses_range)
plt.legend()
plt.grid(True)
plt.show()
