from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import *
from time import sleep
import customtkinter


def start_driver():
    chrome_options = Options()
    arguments = [
                '--lang=pt-BR', 
                '--disable-notifications', 
                '--headless', 
                '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                ]

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option("prefs", {
        'download.prompt_for_download': False,
        'profile.default_content_settings_values.notifications': 2,
        'profile.default_content_settings_values.automatic_downloads': 1
    })

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10, poll_frequency=1, ignored_exceptions=[NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException])

    return driver, wait

def first_site(driver, wait, prod):
    driver.get('https://www.magazineluiza.com.br')
    sleep(3)
    element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="suggestion-input"]')))
    element.send_keys(prod)
    sleep(2)
    element.send_keys(Keys.ENTER)
    sleep(3)
    first_price = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//*[@data-testid='price-value']")))
    price = first_price.text.replace('ou', '').replace('R$', '').replace('.','').replace(',', '.').strip()
    price = float(price)

    return price

def second_site(driver, wait, prod):
    driver.get('https://www.mercadolivre.com.br')
    sleep(3)
    element = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="cb1-edit"]')))
    element.send_keys(prod)
    sleep(2)
    element.send_keys(Keys.ENTER)
    sleep(3)
    second_price = wait.until(expected_conditions.visibility_of_element_located((By.XPATH, "//span[@class='andes-money-amount__fraction' and @aria-hidden='true']")))
    price = second_price.text.replace('ou', '').replace('R$', '').replace('.','').replace(',', '.').strip()
    price = float(price)

    return price

def search():
    nome_prod = text_box.get()

    driver, wait = start_driver()
    price1 = first_site(driver, wait, nome_prod)
    price2 = second_site(driver, wait, nome_prod)

    if price1 < price2:
        text_box_outcome.configure(state='normal')
        text_box_outcome.delete('1.0', 'end')
        text_box_outcome.insert(index='1.0', text=f'{nome_prod}\nMagazine Luiza: R${price1:.2f}.\nMercado Livre: R${price2:.2f}')
        text_box_outcome.configure(state='disable')
    else:
        text_box_outcome.configure(state='normal')
        text_box_outcome.delete('1.0', 'end')
        text_box_outcome.insert(index='1.0', text=f'{nome_prod}\nMercado Livre: R${price2:.2f}.\nMagazine Luiza: R${price1:.2f}')
        text_box_outcome.configure(state='disable')

    driver.quit()

main_window = customtkinter.CTk()

main_window.title('Lower Price')
main_window.grid_anchor('center')
main_window.geometry('300x300')

font_1 = customtkinter.CTkFont(family='Arial', weight='bold', size=18)
font_2 = customtkinter.CTkFont(family='Arial', slant='italic', size=14)

label_1 = customtkinter.CTkLabel(main_window, text='Product', font=font_1)
label_1.grid(row=0, column=0, padx=10, pady=0)

text_box = customtkinter.CTkEntry(main_window, width=180, height=25)
text_box.grid(row=1, column=0, padx=10, pady=0)

buscar_button = customtkinter.CTkButton(main_window, text='Search', width=180, height=25, command=search)
buscar_button.grid(row=2, column=0, padx=10, pady=10)

label_2 = customtkinter.CTkLabel(main_window, text='Result:', font=font_2)
label_2.grid(row=3, column=0, padx=0, pady=0)

text_box_outcome = customtkinter.CTkTextbox(main_window, width=230, height=100)
text_box_outcome.grid(row=4, column=0, padx=0, pady=10)

main_window.mainloop()