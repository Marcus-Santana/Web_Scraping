from bs4 import BeautifulSoup # O BeautifulSoup é utilizado para fazer a análise do HTML
from selenium import webdriver # O Selenium é utilizado para automatizar a busca no site
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep # O sleep foi utilizado para adicionar pausas durante a execução e garantir que não ocorresse nenhum erro de carregamento
import pandas as pd # O panda é utilizado para manipulação de dados


navegador = webdriver.Chrome()  #inicia o navegador
navegador.get("https://portal.gupy.io/") #Carrega a url

sleep(1)

busca = navegador.find_element('css selector', 'input')
busca.send_keys("estagio")
busca_botao = navegador.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
sleep(0.5)
busca_botao.click() 
#Esse bloco encontra a caixa de pesquisa na página e busca pela palavra chave 'estagio' e logo após, clica no botão para pesquisar

sleep(2)

page_content = navegador.page_source
site = BeautifulSoup(page_content, 'html.parser')
#O código recebe o conteúdo da página e depois analisa utilizando o BS4

def rolar_pagina(x):
   for _ in range(x):
        navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

rolar_pagina(100)
# Função para 'rolar' a página e carregar mais vagas
sleep(2)

page_content = navegador.page_source
site = BeautifulSoup(page_content, 'html.parser')

# Após chamar a função 'rolar_pagina', as novas vagas que apareceram não estam presentes no html 'capturado' 
# anteriormente pelo código, por isso é necessecário repetir esse passo nessa etapa

empresas = site.find_all("p", class_="sc-efBctP dpAAMR sc-a3bd7ea-6 cQyvth") # Extra
lista_empresas = []
for x in empresas:
    lista_empresas.append(x.get_text())


cargo_trabalho = site.find_all("h2", class_="sc-llJcti jgKUZ sc-a3bd7ea-5 XNNQK")
lista_cargo_trabalho = []
for x in cargo_trabalho:
    lista_cargo_trabalho.append(x.get_text())


local_empresa = site.find_all("span", {"data-testid": "job-location", "class": "sc-23336bc7-1 cezNaf"})
lista_local_empresa = []
for x in local_empresa:
    lista_local_empresa.append(x.get_text())

# Nos trechos acima foi utilizado o BS4 para localizar os elementos HTML e depois foram armazenados em suas listas correspondentes


vagas = {"Empresa": lista_empresas, "Cargo": lista_cargo_trabalho, "Local da empresa": lista_local_empresa}
df = pd.DataFrame.from_dict(vagas)

# As listas fora organizadas em um dicionário, que foi utilizado para criar um DataFrame do pandas

df.to_csv("vagas.csv") # Salva o DataFrame em um arquivo Csv




opcao = input("Digite 'close' para fechar o navegador: ")
if opcao == 'close':
    navegador.close
# Criei essa condicional para poder manter o navegador aberto enquanto rodava o script
