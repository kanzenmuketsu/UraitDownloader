# Urait downloader

import time
import sys
import os
import img2pdf
from configuration import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def delete_tmp_files(pages)->None:
    for page in pages:
        os.remove(page)

def builtPDF(name, pages)->None:
    with open(f"{name}.pdf","ab") as f:
            f.write(img2pdf.convert(pages))

def getURL() -> str:

    bookURL = input('Всавьте ссылку на книгу\n==> ')

    viewerURL = bookURL.replace("book", "viewer") + '#page/'
    bookname = (bookURL.split('/'))[4]

    return (viewerURL, bookname)


def get_data(URL: str, startpage)-> str: # List

    result = []

    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://urait.ru/login')

    AUTH = authorization(driver)

    if AUTH:

        total_pages = get_total_pages(driver, URL)

        for pageN in range(int(startpage), total_pages):
            driver.get(URL + f"{pageN}")
            erase_useless_elements(driver)
            page_name = f"page_{pageN}"

            wait_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, page_name)))

            page = driver.find_element(By.ID, page_name)
            page.screenshot(page_name + ".png")

            result.append(page_name + ".png")
            if(os.system('cls')):
                os.system('clear')
            print(f"{pageN}/{total_pages}")
    driver.quit()

    return result

def authorization(driver)-> bool:
    try:
        login_element  = driver.find_element(By.ID, "email")
        login_element.clear()
        login_element.send_keys(login)

        pass_element  = driver.find_element(By.ID, "password")
        pass_element.clear()
        pass_element.send_keys(password)

        pass_element.send_keys(Keys.RETURN)
        time.sleep(5)

        return True

    except:
        print("ошибка какая-то..")
        driver.quit()
        return False

def erase_useless_elements(driver)-> None:

    elements = ["viewer__bar","viewer__header", "jvLabelWrap"]
    classes = ["flex", "feedback-hotline","notifications", "menu-visible"]

    for el in elements:
        try:
            driver.execute_script(f"{el}.style.opacity = '0';")
        except:
           print("error")

    for clas in classes:
        cmd = f"for (const el of document.getElementsByClassName('{clas}'))" + "{el.style.opacity = '0';}"
        driver.execute_script(cmd)

def collect_pages():
    pages = []
    files = os.listdir()
    for file in files:
        if ".png" in file:
            pages.append(file)
    return pages

def get_total_pages(driver,url: str)-> int:

    driver.get(url + '1')  # url to page 1
    wait_element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, "viewer__bar__pages-scale")))

    element_pages = driver.find_element(By.ID, "viewer__bar__pages-scale").text.split()

    total_pages = int(element_pages[2])

    return total_pages

def main(startpage):

    url,bookname = getURL()
    print(f"загрузка страниц, начиная с {startpage}")
    get_data(url, startpage)
    pages = collect_pages()
    print("создание пфд документа")
    builtPDF(bookname, pages)

  #  delete_tmp_files(pages)

    q = input('\nenter....')

if __name__ == '__main__':
    startpage = sys.argv[1] if len(sys.argv) > 1 else 1
    main(startpage)
