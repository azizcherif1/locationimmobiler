from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv
f = open("all_href_page_1.txt", "r")
list_all_href_more = f.readlines()
f.close()


def get_all_info(URL):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome("C:\Program Files\Google\chromedriver\chromedriver.exe",options=options)
    driver.maximize_window()
    driver.get(URL)
    all=[]
    title_all=driver.find_elements(By.CSS_SELECTOR, "h1.searchTitle")
    text_title=[x.text for x in title_all]
    all.append(text_title[0])
    position_all=driver.find_elements(By.CSS_SELECTOR, "p.darkblue.inBlock.float-right.floatL")
    text_adress=[x.text.strip() for x in position_all]
    tab_adress=text_adress[0].split(",")
    all.append(tab_adress[0])
    all.append(tab_adress[1].strip())
    all_price = driver.find_elements(By.CSS_SELECTOR, "div.col-7 h3.orangeTit")
    text_price = [x.text.strip() for x in all_price]
    if(len(text_price)==0):
        text_price="None"
    else:
        text_price=text_price[0]
    all.append(text_price)

    catNav_element = driver.find_element(By.CSS_SELECTOR, "div.catNav")
    tagProp_elements = catNav_element.find_elements(By.CSS_SELECTOR, "span.tagProp")
    chambre_value = "None"
    for element in tagProp_elements:
        if "Chambres" in element.text:
            chambre_value = element.text.strip()
            break
    all.append(chambre_value)

    # Click on the "Afficher le numéro" div to reveal the phone numbers
    driver.execute_script("document.querySelector('div.cookieWarning').remove();")
    show_number_button = driver.find_element(By.CSS_SELECTOR, "div.hide-phone-number-box")
    show_number_button.click()
    time.sleep(1)
    # Find the phone numbers
    phone_numbers = []
    # response_div = driver.find_element(By.ID, "response")
    phone_texts = driver.find_elements(By.CSS_SELECTOR, "div#response p.phoneText")
    phone_number = phone_texts[0].text.strip()
    all.append(phone_number)
    driver.quit()
    return all

header = ['Title', 'Ville', 'Location', 'Price', 'Chambre', 'Contact']
filename = 'scraped_data.csv'
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

    for i in range(0, len(list_all_href_more)):
        list_all_info = get_all_info(list_all_href_more[i])
        writer.writerow(list_all_info)

print('Data has been written to', filename)
    