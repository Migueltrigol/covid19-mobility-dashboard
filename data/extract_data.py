from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time 
import config


def initialize_driver():
    url = "https://www.mitma.gob.es/ministerio/covid-19/evolucion-movilidad-big-data/opendata-movilidad"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("prefs", {
        "download.default_directory": config.folder_data_raw,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True})
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20) 
    driver.get(url)
    return driver, wait

def locate_iframe(driver, wait):
    iframe = wait.until(EC.presence_of_element_located((By.ID, 'inlineFrameExample')))
    driver.switch_to.frame(iframe)       

def locate_data_feed(wait):
    element = wait.until(EC.presence_of_element_located((By.LINK_TEXT,"maestra2-mitma-distritos")))
    element.click()

def locate_monthly_files(wait):
    element = wait.until(EC.presence_of_element_located((By.LINK_TEXT,'meses-completos')))
    element.click()

def get_monthly_data(wait, months_lst):
    files_in_month = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'file-link')))
    files_selected = [file for file in files_in_month if any(substr in file.text for substr in months_lst)]
    for file in files_selected:
        file.click()
        time.sleep(5)

def wait_for_complete_downloads(driver):
    while True:
        if any([f.endswith(".crdownload") for f in os.listdir(config.folder_data_raw)]):
            time.sleep(1)
        else:
            break
    driver.quit()


def download_data(months_lst):
    """Main function of the module. 
    The parameter 'months_lst' is a list of floats containing the year and month of the months to be downloaded (e.g. 202003.0)
    """
    driver, wait = initialize_driver()
    locate_iframe(driver, wait)
    locate_data_feed(wait)
    locate_monthly_files(wait)
    get_monthly_data(wait,months_lst)
    wait_for_complete_downloads(driver)


