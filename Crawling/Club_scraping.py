import csv
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# specifying the path to the webdriver and "accept cookies button"
cookiePath = "/html/body/div[1]/div[1]/div/div[1]/div[5]/button[1]"

# initiating the webdriver
driver = webdriver.Edge(EdgeChromiumDriverManager().install())

# try...finally to close after completion
try:

    websites = ['https://www.premierleague.com/clubs',
                'https://www.premierleague.com/clubs?se=363',
                'https://www.premierleague.com/clubs?se=274',
                'https://www.premierleague.com/clubs?se=210']

    cName = []
    cWebsite = []
    cStadium = []

    for page in websites:

        # initiate the specified page
        driver.implicitly_wait(30)
        driver.get(page)

        if page == websites[0]:
            driver.find_element(By.XPATH, cookiePath).click()
        else:
            pass

        # fetch club name
        driver.find_element(By.XPATH, "//div[@class='clubIndex col-12']//li//h4")
        cName_temp = driver.find_elements(By.XPATH, value="//div[@class='clubIndex col-12']//li//h4")

        # fetch clubs websites
        cWebsite_temp = driver.find_elements(By.XPATH, value="//div[@class='clubIndex col-12']//li//a")

        # fetch clubs home stadiums
        cStadium_temp = driver.find_elements(By.XPATH, value="//div[@class='stadiumName']")

        for i in range(0, len(cName_temp)):
            if cName_temp[i].text in cName:
                pass
            else:
                cName.append(cName_temp[i].text)
                cWebsite.append(cWebsite_temp[i].get_attribute('href'))
                cStadium.append(cStadium_temp[i].text)

    # storing data into csv file
    with open("Tables\Club.csv", "w", encoding='UTF8', newline='') as file:
        writer = csv.writer(file)

        for i in range(0, len(cName)):
            row = [cName[i], cWebsite[i], cStadium[i]]
            writer.writerow(row)
finally:
    # close the tab after completing the crawl process
    driver.close()
