import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# specifying the path to the webdriver and "accept cookies button"
cookiePath = "//*[text()='Accept All Cookies']"

# initiating the website to crawl
driver = webdriver.Edge(EdgeChromiumDriverManager().install())
driver.implicitly_wait(20)
# try...finally to close after completion
try:

    seasons = ['https://www.premierleague.com/players?se=418&cl=-1',
                'https://www.premierleague.com/players?se=363&cl=-1',
                'https://www.premierleague.com/players?se=274&cl=-1',
                'https://www.premierleague.com/players?se=210&cl=-1']

    sites = []

    with open("Tables\Playerweb.csv", 'w', newline='') as file:
        writer = csv.writer(file)

        for season in seasons:
            # initiate the specified page
            driver.get(season)

            if season == seasons[0]:
                # print("yes1")
                driver.find_element(By.XPATH, cookiePath).click()
                mode = 'w'
            else:
                mode = 'a'

            # print("yes2")

            # scrolling to load all players
            SCROLL_PAUSE_TIME = 2
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            # collecting websites for players
            driver.find_element(By.XPATH, "//tbody[@class='dataContainer indexSection']//td/a")
            pWebsites = driver.find_elements(By.XPATH, "//tbody[@class='dataContainer indexSection']//td/a")
            # print(len(pWebsites))

            time.sleep(1)

            for pp in pWebsites:
                if pp.get_attribute('href') not in sites:
                    writer.writerow([pp.get_attribute('href')])
                    sites.append(pp.get_attribute('href'))
                else:
                    pass
finally:
    driver.close()
