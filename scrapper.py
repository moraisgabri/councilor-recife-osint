import os
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

URL = "https://transparencia.recife.pe.leg.br/legislativo/verba-indenizatoria/2026"

root_dir = os.path.abspath("./verba-idenizatoria-2026")
custom_dir = os.path.abspath("./downloads")
os.makedirs(custom_dir, exist_ok=True)

# options = webdriver.FirefoxOptions()

# # 0 = Desktop, 1 = Downloads folder, 2 = Custom directory
# options.set_preference("browser.download.folderList", 2)
# options.set_preference("browser.download.dir", custom_dir)
# options.set_preference("browser.download.manager.showWhenStarting", False)

# driver = webdriver.Firefox(options=options)
# wait = WebDriverWait(driver, 20)

options = webdriver.ChromeOptions()

# Define download behavior in a dictionary
prefs = {
    "download.default_directory": custom_dir, # Sets the custom download path
    "download.prompt_for_download": False,    # Disables the 'Save As' popup
    "download.directory_upgrade": True,        # Ensures the directory is used
    "safebrowsing.enabled": True               # Optional: handles security warnings
}

# Add preferences to options
options.add_experimental_option("prefs", prefs)

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options) 
wait = WebDriverWait(driver, 20)

try:
    print("Abrindo página...")
    driver.get(URL)

    time.sleep(5)

    dropdown = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".ui.dropdown")
        )
    )

    dropdown.click()

    time.sleep(10)

    menu = wait.until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, ".menu.transition.visible")
        )
    )

    items = menu.find_elements(
        By.CSS_SELECTOR,
        ".item"
    )

    vereadores = []

    for item in items:
        nome = item.text.strip()

        if nome and nome != "Selecione":
            vereadores.append(nome)

    print(f"\nEncontrados {len(vereadores)} vereadores:\n")

    index = vereadores.index("Zé Neto") -1
    vereadores = vereadores[index:-1]

    print(vereadores)

    for nome in vereadores:
        print(nome)
        botao_do_verador = driver.find_element(By.XPATH, f"//*[contains(text(), '{nome}')]")
        botao_do_verador.click()

        time.sleep(10)
        botao_de_pesquisa = driver.find_element(By.XPATH, f"//*[contains(text(), 'Pesquisar')]")
        botao_de_pesquisa.click()

        time.sleep(10)
        download_csv =  driver.find_element(By.CSS_SELECTOR, "a[download]")
        download_csv.click()

        time.sleep(10)

        arquivo_original = os.path.abspath(
            "./downloads/ceap_52f2b64b252544cca501facd5073069d.csv"
        )

        novo_nome = os.path.join(
            root_dir,
            f"{nome}.csv"
        )

        shutil.move(arquivo_original, novo_nome)

        time.sleep(10)
        botao_nova_consulta = driver.find_element(By.XPATH, f"//*[contains(text(), 'Nova Consulta')]")
        botao_nova_consulta.click()

        print(f"Renomeado para: {novo_nome}")

        dropdown = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".ui.dropdown")
            )
        )

        print("Dropdown encontrado")

        dropdown.click()
        time.sleep(10)

finally:
    input("\nENTER para fechar")
    driver.quit()