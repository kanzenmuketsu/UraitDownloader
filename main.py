# Urait downloader

import os
import img2pdf
from configuration import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def delete_tmp_files(pages)->None:
    for page in pages:
        os.remove(page)

def builtPDF(name, pages)->None:

    homepath = os.getenv('USERPROFILE')
    file_path = homepath + '\\UraitDownloader\\'

    if not os.path.isdir(file_path):
        os.mkdir(file_path)


    with open(f"{file_path}{name}.pdf","ab") as f:
            f.write(img2pdf.convert(pages))


def get_data(URL: str)-> str: # List

    result = []

    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get('https://urait.ru/login')

    AUTH = authorization(driver)

    if AUTH:

        total_pages = get_total_pages(driver, URL)
        erase_useless_elements(driver)

        for pageN in range(total_pages):

            driver.get(URL + str(pageN+1))

            wait_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "page_"+str(pageN+1))))

            page = driver.find_element(By.ID, "page_"+str(pageN+1))
            name = f'page_{pageN+1}.png'
            page.screenshot(name)

            result.append(name)
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

    viewer_bar = driver.find_element(By.ID, "viewer__bar")
    driver.execute_script("arguments[0].style.opacity = '0';",viewer_bar)

    viewer__header = driver.find_element(By.ID, "viewer__header")
    driver.execute_script("arguments[0].style.opacity = '0';",viewer__header)

    notification = driver.find_element(By.ID, "viewer__wrapper__notifications-new-bottom")
    driver.execute_script("arguments[0].style.opacity = '0';", notification)

def get_total_pages(driver,url: str)-> int:

    driver.get(url + '1')  # url to page 1
    wait_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "viewer__bar__pages-scale")))

    element_pages = driver.find_element(By.ID, "viewer__bar__pages-scale").text.split()

    total_pages = int(element_pages[2])

    return total_pages

def main():

    url,bookname = getURL()
    print("загрузка страниц")
    pages = get_data(url)
    print("создание пфд документа")
    builtPDF(bookname, pages)

    delete_tmp_files(pages)

    print("\n\n\nФайл сохранен  в C\\USERS\\ВАШ_ПОЛЬЗОВАТЕЛЬ\\UraitDownloader")
    q = input('\nenter....')

if __name__ == '__main__':
    main()
