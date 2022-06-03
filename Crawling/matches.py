import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# specifying the path to the webdriver and "accept cookies button"
cookiePath = "//*[text()='Accept All Cookies']"

# webpages for the 4 wanted seasons
seasonsSites = ['https://www.premierleague.com/results?co=1&se=418&cl=-1',
                'https://www.premierleague.com/results?co=1&se=363&cl=-1',
                'https://www.premierleague.com/results?co=1&se=274&cl=-1',
                'https://www.premierleague.com/results?co=1&se=210&cl=-1']

# the corresponding season for each webpage
seasons = ['2021/22', '2020/21', '2019/20', '2018/19']

driver = webdriver.Edge(EdgeChromiumDriverManager().install())
wait = WebDriverWait(driver, 30)

# containers for data
homeClubs = []
awayClubs = []
home_yellow = []
away_yellow = []
home_red = []
away_red = []
home_shots = []
away_shots = []
home_poss = []
away_poss = []
home_fouls = []
away_fouls = []
matchStadium = []
score = []
matchDate = []
season = []

with open("Tables\Matches.csv", 'w', newline='') as file:
    writer = csv.writer(file)
    try:
        c = 1
        for site in seasonsSites:

            urls = []
            for x in range(0, 4):
                if site == seasonsSites[x]:
                    season.append(seasons[x])

            driver.get(site)

            # pass cookies and specify the write mode
            if site == seasonsSites[0]:
                time.sleep(1)
                wait.until(EC.element_to_be_clickable((By.XPATH, cookiePath))).click()
            else:
                pass

            # scrolling to load all players
            SCROLL_PAUSE_TIME = 1
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

            # getting match dates and corresponding matches
            wait.until(EC.presence_of_element_located((By.XPATH, "//time[@class='date long']/strong")))
            dates = driver.find_elements(By.XPATH, "//time[@class='date long']/strong")

            for i in range(0, len(dates)):
                wait.until(EC.presence_of_element_located(
                    (By.XPATH, f"(//time[@class='date long']/strong)[{i + 1}]/../following::div[1]/ul")))
                matches = driver.find_elements(
                    By.XPATH, f"(//time[@class='date long']/strong)[{i + 1}]/../following::div[1]//li")

                print('\n')

                j = 1
                for match in matches:
                    # match date
                    matchDate.append(dates[i].text)

                    print(f"{c}, {dates[i].text}, {j}")

                    # name of home club
                    homeClubs.append(
                        match.find_element(By.XPATH, ".//span[@class ='team'][1]//span[@class='shortname']").text)

                    # name of away club
                    homeClubs.append(
                        match.find_element(By.XPATH, ".//span[@class ='team'][2]//span[@class='shortname']").text)

                    # score
                    score.append(
                        match.find_element(By.XPATH, ".//span[@class='score ']").text)

                    # stadium
                    matchStadium.append(match.get_attribute('data-venue').split(',')[0])

                    # match url
                    urls.append(f"https://{match.find_element(By.XPATH, './div').get_attribute('data-href')[2:]}")

                    j += 1
            c += 1

            for url in urls:
                driver.get(url)
                driver.maximize_window()

                wait.until(EC.element_to_be_clickable((By.XPATH, "//li[text()='Stats']"))).click()
                time.sleep(2)

                try:
                    home_shots.append(driver.find_element(By.XPATH,
                                                          "//p[contains(text(),'Shots') and not (contains(text(),'target'))]/preceding::p[1]").text)
                    away_shots.append(driver.find_element(By.XPATH,
                                                          "//p[contains(text(),'Shots') and not (contains(text(),'target'))]/following::p").text)
                except NoSuchElementException:
                    home_shots.append(None)
                    away_shots.append(None)

                try:
                    home_poss.append(
                        driver.find_element(By.XPATH, "//p[contains(text(),'Possession %')]/preceding::p[1]").text)
                    away_poss.append(
                        driver.find_element(By.XPATH, "//p[contains(text(),'Possession %')]/following::p").text)
                except NoSuchElementException:
                    home_poss.append(None)
                    away_poss.append(None)

                try:
                    home_yellow.append(
                        driver.find_element(By.XPATH, "//p[contains(text(),'Yellow')]/preceding::p[1]").text)
                    away_yellow.append(
                        driver.find_element(By.XPATH, "//p[contains(text(),'Yellow')]/following::p").text)
                except NoSuchElementException:
                    home_yellow.append(None)
                    away_yellow.append(None)

                try:
                    home_red.append(driver.find_element(By.XPATH, "//p[contains(text(),'Red')]/preceding::p[1]").text)
                    away_red.append(driver.find_element(By.XPATH, "//p[contains(text(),'Red')]/following::p").text)
                except NoSuchElementException:
                    home_red.append(None)
                    away_red.append(None)

                try:
                    home_fouls.append(
                        driver.find_element(By.XPATH, "//p[contains(text(),'Fouls')]/preceding::p[1]").text)
                    away_fouls.append(driver.find_element(By.XPATH, "//p[contains(text(),'Fouls')]/following::p").text)
                except NoSuchElementException:
                    home_fouls.append(None)
                    away_fouls.append(None)

    finally:
        driver.close()

    for i in range(0, len(homeClubs)):
        v = score[i].split('-')
        row = [matchDate[i], homeClubs[i], awayClubs[i], matchStadium[i], season[i],
               home_red[i], home_yellow[i], v[0], home_fouls[i], home_poss[i], home_shots[i],
               away_red[i], away_yellow[i], v[1], away_fouls[i], away_poss[i], away_shots[i],
               score[i]]
        writer.writerow(row)
