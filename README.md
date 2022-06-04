# Web-crawler-with-terminal-interface
This project does three things: 
- scrap different web pages from the premier league
- host the data collected on either a local or a remote server
- implement a terminal-based interface to query the data base

## The "crawling" folder contains the scripts used to do the crawling part:
- "Club_scraping.py" -> scrap the premier league clubs information, clubs played in the last 4 seasons
- "matches.py" -> scrap the requeired information of all played matches in the last 4 seasons
- "PlayerWebsiteCollection.py" -> collect the webpage urls of all players. This is an auxiliary script used in the comming item.
- "players%pre_clubs_bs4.py" -> scrap the required information of all players along with their home teams in the past 4 seasons
- "stadiums.py" -> scrap information about all stadiums in the premier league.
Every script stores the collect information in a csv file to be loaded later on a data base server

## The terminal interface "connector.py":
- This is the script used to build the terminal-based interface and also connect to the used data base server, either remotely or locally.
- The terminal interface provides choices of some predefined queries

## User Guide:
- You are recommended to run the scripts from the command line.
- In case of running "connector.py", you can specify whether the connection is remote or local by passing an argument in the command line. Either "local" or "remote"
- Ex. type in the terminal "python connector.py remote" That will connect to the remote server.
- Modify the paramerters of the corresponsing connection to suit your own connection.
- All server connection information are supposed to be defined in the script. If you want it to be specified from the user, few changes will be needed in the script.

## Requirements:
Use command "pip install -r requirements.txt" to install all requirements at once. 
