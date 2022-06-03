import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup
import requests
from lxml import etree

# specifying the path to the webdriver and "accept cookies button"
cookiePath = "//*[text()='Accept All Cookies']"

# initiating the website to crawl
driver = webdriver.Edge(EdgeChromiumDriverManager().install())

clubs = []
stadiumsURL = []

with open("Tables\Club.csv", 'r', encoding='UTF8', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        clubs.append(row[0])

try:
    driver.get("https://www.premierleague.com/clubs")
    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, cookiePath))).click()
    time.sleep(2)

    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//tbody[@class='allTimeDataContainer']//tr")))
    all_clubs = driver.find_elements(By.XPATH, "//tbody[@class='allTimeDataContainer']//tr")

    for club in all_clubs:
        if club.find_element(By.XPATH, ".//h4[@class='clubName']").text in clubs:
            stadiumsURL.append(club.find_element(By.XPATH,".//td[@class='venue']/a").get_attribute('href'))

    # print(len(stadiumsURL))

finally:
    driver.close()

with open("Tables\Stadium.csv", 'w', newline='') as file:
    writer = csv.writer(file)

    for stPage in stadiumsURL:
        source = requests.get(stPage)
        soup = BeautifulSoup(source.content, 'html.parser')
        dom = etree.HTML(str(soup))

        name = (dom.xpath("//title/text()"))[0]
        parts = name.split()[0:2]
        # print(f"{parts[0]} {parts[1]}")

        capacity = (dom.xpath("//div[@class='articleTab']//p//*[contains(text(), 'Capacity') or contains(text(), 'capacity')]/../text()"))[0]
        if len(capacity) > 6:
            capacity = capacity[1:8]

        record_temp = (dom.xpath("//*[contains(text(),'Record PL attendance:')] /../text()"))
        if len(record_temp) > 0:
            record = record_temp[0].split('v')[0]
            if len(record) > 6:
                record = record[1:]
        else:
            record = ''

        built_temp = (dom.xpath("//*[contains(text(),'Built:') or contains(text(),'Opened:')]/../text()"))
        if len(built_temp) > 0:
            built = built_temp[0]
            if len(built) > 4:
                built = built[1:]
        else:
            built = ''

        pitch = (dom.xpath("//*[contains(text(),'Pitch size:')]/../text() "))[0]
        if len(pitch) > 10:
            pitch = pitch[1:]

        addr = (dom.xpath("//*[contains(text(),'Stadium address:')]/../text()"))[0]

        writer.writerow([f"{parts[0]} {parts[1]}", addr, capacity, pitch, built, record])