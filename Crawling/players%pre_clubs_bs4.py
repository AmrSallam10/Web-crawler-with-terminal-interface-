import csv
from bs4 import BeautifulSoup
import requests
from lxml import etree

sites = []
row = []
seasons = ['2021/2022', '2020/2021', '2019/2020', '2018/2019']
with open("Tables\Playerweb.csv", 'r', encoding='UTF8', newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        sites.append(row[0])

x = 1
print(len(sites))

with open("Tables\Player.csv", 'w', newline='') as file1, \
        open("Tables\Pre_Clubs.csv", 'w', newline='') as file2:

    writer1 = csv.writer(file1)
    writer2 = csv.writer(file2)

    for site in sites:
        source = requests.get(site)
        soup = BeautifulSoup(source.content, 'html.parser')
        dom = etree.HTML(str(soup))

        name = (dom.xpath("//div[@class='playerDetails']//div[@class='name t-colour']/text()"))[0]
        print(name)
        position = (dom.xpath("//*[contains(text(),'Position')]/following-sibling::div/text()"))[0]
        height = (dom.xpath("//*[contains(text(),'Height')]/following-sibling::div/text()"))
        if len(height) > 0:
            height = height[0]
            height = height[0:3]
        else:
            height = ''

        nat = (dom.xpath("//span[@class='playerCountry']/text()"))
        if len(nat) > 0:
            nat = nat[0]
        else:
            nat = ''

        DOB = (dom.xpath("//ul[@class='pdcol2']//div[@class='info']/text()"))
        if len(DOB) > 0:
            DOB = DOB[0]
            DOB = DOB[15:27]
        else:
            DOB = ''

        season = (dom.xpath("//tr[@class='table'][1]//td[@class='season']/p/text()"))[0]
        if season == '2021/2022':
            currentClub = (dom.xpath("//tr[@class='table'][1]//span[@class='long']/text()"))[0]
        else:
            currentClub = 'NULL'

        writer1.writerow([name, position, nat, height, DOB, currentClub])

        # fetch player last up to 4 clubs with the corresponding season
        tempClub = (dom.xpath("//tr[@class='table']//span[@class='long']/text()"))
        tempSeason = (dom.xpath("//tr[@class='table']//td[@class='season']/p/text()"))

        for i in range(0, 4 if len(tempClub) >= 4 else len(tempClub)):
            if tempSeason[i] in seasons:
                writer2.writerow([name, tempClub[i], tempSeason[i]])

        print(x)
        x += 1