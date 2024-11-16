import pandas as pd
import matplotlib.pyplot as plt

colunas_numericas = ['Quantidade', 'Preço Unitário', 'Total', 'Custo Unitário', 'Custo Total', 'Lucro']
dados = pd.read_excel('bd/vendas.xlsx', parse_dates=['Data'], names=['Data', 'Cliente', 'Produto'] + colunas_numericas)
dados[colunas_numericas] = dados[colunas_numericas].apply(pd.to_numeric, errors='coerce')
dados.dropna(inplace=True)
dados.sort_values('Data', inplace=True)
dados['Ano_Mes'] = dados['Data'].dt.to_period('M')

quantidade_de_vendas_mes = dados.groupby(['Ano_Mes', 'Produto'])['Quantidade'].sum().unstack()
produtos_vendidos = dados.groupby('Produto')['Quantidade'].sum().sort_values(ascending=False)
lucro_produto = dados.groupby('Produto')['Lucro'].sum().sort_values(ascending=False)
total_vendas_produto = dados.groupby('Produto')['Total'].sum()
margem_lucro_produto = (lucro_produto / total_vendas_produto * 100).sort_values(ascending=False)

quantidade_de_vendas_mes.plot(kind='bar', figsize=(10, 6))
plt.title('Quantidade de Vendas por Mês')
plt.ylabel('Quantidade Vendida')
plt.xlabel('')
plt.ylim(0, 200)
plt.tight_layout()
plt.show()

produtos_vendidos.plot(kind='bar', figsize=(10, 6))
plt.title('Produtos Mais Vendidos')
plt.ylabel('Quantidade Vendida')
plt.xlabel('')
plt.tight_layout()
plt.show()

lucro_produto.plot(kind='bar', color='green', figsize=(10, 6))
plt.title('Lucro por Produto')
plt.ylabel('Lucro (R$)')
plt.xlabel('')
plt.tight_layout()
plt.show()

margem_lucro_produto.plot(kind='bar', color='orange', figsize=(10, 6))
plt.title('Margem de Lucro por Produto (%)')
plt.ylabel('Margem de Lucro (%)')
plt.xlabel('')
plt.tight_layout()
plt.show()
