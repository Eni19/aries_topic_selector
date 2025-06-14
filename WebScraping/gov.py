from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configurações do ChromeDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=chrome_options)

# URL de busca
palavra_chave = "antibiótico"
url_base = f"https://www.gov.br/saude/pt-br/search?SearchableText={palavra_chave}"
driver.get(url_base)
time.sleep(3)


try:
    botao_cookie = driver.find_element(By.CSS_SELECTOR, "button.br-button.btn-manage.manage")
    botao_cookie.click()
    print("Botão de cookies clicado.")
    time.sleep(2)
except NoSuchElementException:
    print("Nenhuma barra de cookies encontrada.")

resultados = []

while True:
    # Rola a página para carregar todos os elementos
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    # Pega conteúdo da página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    noticias = soup.find_all("li", class_="item-collective.nitf.content")
    print(f"Encontradas {len(noticias)} notícias nesta página.")

    for item in noticias:
        titulo_tag = item.find("span", class_="titulo")
        a_tag = titulo_tag.find("a") if titulo_tag else None
        titulo = a_tag.get_text(strip=True) if a_tag else ""
        link = a_tag['href'] if a_tag else ""
        if link.startswith('/'):
            link = "https://www.gov.br" + link

        desc_tag = item.find("span", class_="descricao")
        descricao = desc_tag.get_text(strip=True) if desc_tag else ""

        print(f"Coletado: {titulo} | {descricao} | {link}")

        resultados.append([titulo, descricao, link])

    # Tenta encontrar e clicar no botão "Próximo"
    try:
        botao_proximo = driver.find_element(By.CSS_SELECTOR, "ul.paginacao li a.proximo")
        driver.execute_script("arguments[0].scrollIntoView(true);", botao_proximo)
        time.sleep(1)  # Pequena espera
        driver.execute_script("arguments[0].click();", botao_proximo)
        print("Indo para a próxima página...")
        time.sleep(3)
    except NoSuchElementException:
        print("Não há mais páginas. Coleta finalizada.")
        break

# Fecha navegador
driver.quit()

# Salva no Excel
df = pd.DataFrame(resultados, columns=["Titulo", "Descricao", "Link"])
df.to_excel("noticias_govbr.xlsx", index=False)
print("Dados salvos em 'noticias_govbr.xlsx'.")
