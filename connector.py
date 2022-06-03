# imports
import mysql.connector
import os
import time
from getpass import getpass
import re
import sys

# Global Variables
enterMode = ''
dob = ''


class User:
    email = ''


class Connect:
    # connection type [local - remote]
    def __init__(self):
        if sys.argv[1] == 'remote':
            # remote server connection
            self.db = mysql.connector.connect(
                host='db4free.net',
                user='dbtesterrr',
                password='234368000',
                database='data_base_host',
                charset='latin7',
                collation='latin7_general_ci'
            )
        elif sys.argv[1] == 'local':
            # local server connection
            self.db = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='234368000',
                database='milestone1',
                auth_plugin='mysql_native_password')
        else:
            print('Invalid argument')
            quit()

        # initiating the connection object
        self.mycurser = self.db.cursor()


# fetch some data from the data base to be used in some verifications
class Fetch:
    def __init__(self):
        # info of all registered fans
        c.mycurser.execute('''
            select F_email, passwd
            from fan
        ''')
        self.allFans = c.mycurser.fetchall()

        # info of all clubs
        c.mycurser.execute('''
            select C_name 
            from club
        ''')
        self.allClubs = c.mycurser.fetchall()

        # info of all stadiums
        c.mycurser.execute('''
            select S_name 
            from stadium
        ''')
        self.allStadiums = c.mycurser.fetchall()


################################## functions ##############################################
def clear():
    os.system('cls')


def validate_club(arg):
    for club in f.allClubs:
        if arg.lower() == club[0].lower():
            return True
    return False


def validate_stadium(arg):
    for stadium in f.allStadiums:
        if arg.lower() == stadium[0].lower():
            return True
    return False


def validate_pos(arg):
    for pos in ['midfielder', 'defender', 'forward', 'goalkeeper', 'midfielder']:
        if arg.lower() == pos:
            return True
    return False


def validate_email(arg):
    d = re.compile(r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-]+)')
    found = d.findall(arg)

    if len(found):
        for fan in f.allFans:
            if arg == fan[0]:
                return 'exists'
        return 'not exist'
    else:
        return 'not valid'


def validate_date(arg):
    d = re.compile(r"((0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/(\d{4}))")
    found = d.findall(arg)
    if len(found):
        if len(arg) == len(found[0][0]):
            return True
        else:
            x = input(f'Did you mean {found[0][0]}?'
                      f'\n1. Yes'
                      f'\n2. NO'
                      f'\nChoice: ')
            if x == '1':
                dob = found[0][0]
                return True
            elif x == '2':
                return False
    else:
        return False


def validate_password(arg):
    for fan in f.allFans:
        if arg == fan[1]:
            return True
    return False


def validate_gender(arg):
    if arg.upper() in ['M', 'F', 'O']:
        return True
    else:
        return False


# Add a new user review on a match
def add_review():
    clear()
    a_club = input('The away club: ').strip()
    h_club = input('The home club: ').strip()
    mdate = input('Match date: ').strip()
    rate = input('Rate: ').strip()
    treview = input('Comment: ').strip()

    syntax = '''
            insert into review 
            value (%s, %s, %s, %s, %s, %s)
        '''
    values = (current_user.email, a_club, h_club, mdate, rate, treview)
    c.mycurser.execute(syntax, values)
    c.db.commit()
    print('Review added successfully\n')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


#  View existing reviews on a given match
def view_reviews():
    clear()

    while True:
        a_club = input('The away club: ').strip()
        if not validate_club(a_club):
            print('There is no such a club. Re-enter the club name\n')
        else:
            break

    while True:
        h_club = input('The home club: ').strip()
        if not validate_club(h_club):
            print('There is no such a club. Re-enter the club name\n')
        else:
            break

    mdate = input('Match date: ').strip()

    syntax = '''
            select rate, Treview
            from review
            where MDate = %s and A_club = %s and H_club = %s
        '''
    values = (mdate, a_club, h_club)
    c.mycurser.execute(syntax, values)

    all_reviews = c.mycurser.fetchall()

    for r in all_reviews:
        print(f'{r[0]}, {r[1]}')
    print('\n\n')

    if not len(all_reviews):
        print('No reviews exist for the specified match\n')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Show all the players from a certain nationality and their home teams history
def show_players():
    clear()
    nat = input('Enter a nationality: ').strip()

    syntax = '''
            select P.P_name, PC.club, PC.season
            from player P inner join pre_clubs PC
            on P.P_name = PC.P_name
            where P.nationality = %s
        '''
    values = [nat]
    c.mycurser.execute(syntax, values)

    all_players = c.mycurser.fetchall()

    for player in all_players:
        print(f'{player[0]}, {player[1]}, {player[2]}')
    print('\n\n')

    if not len(all_players):
        print('No players exist in the specified nationality\n')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Show the top 10 teams by matches won
def top10_teams_wins():
    clear()
    c.mycurser.execute('''
        CREATE OR REPLACE view  match_won as
            (select H_club as club
            from f_match
            where H_goals > A_goals)
            union all
            (select A_club
            from f_match
            where A_goals > H_goals);
    ''')

    c.mycurser.execute('''
        select club, count(club) as wins
        from match_won
        group by club
        order by wins DESC
        limit 10;
    ''')

    top10_winners = c.mycurser.fetchall()
    for winner in top10_winners:
        print(f'{winner[0]}, {winner[1]}')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Show the top 10 teams by home matches won
def top10_teams_home_wins():
    clear()
    c.mycurser.execute('''
        CREATE OR REPLACE view  home_match_won as
            select H_club as club
            from f_match
            where H_goals > A_goals;
    ''')

    c.mycurser.execute('''
        select club, count(club) as Home_wins
        from home_match_won
        group by club
        order by Home_wins DESC
        limit 10;
    ''')

    top10_home_winners = c.mycurser.fetchall()
    for winner in top10_home_winners:
        print(f'{winner[0]}, {winner[1]}')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Show the top 10 teams by yellow cards
def top10_yellow():
    c.mycurser.execute('''
        CREATE OR REPLACE view yellow as
            select H_club as club, H_yellow as y
            from f_match
            union all 
            select A_club, A_yellow
            from f_match;
    ''')

    c.mycurser.execute('''
        select club, max_yellowCards
        from (
            select club, sum(y) as max_yellowCards
            from yellow
            group by club
            order by max_yellowCards DESC
            ) as t 
            limit 10;
    ''')

    clear()
    top10 = c.mycurser.fetchall()
    for y in top10:
        print(f'{y[0]}, {y[1]}')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Show the top 10 teams by shots
def top10_shots():
    c.mycurser.execute('''
        CREATE OR REPLACE view shots as
            select H_club as club, H_shots as s
            from f_match
            union all 
            select A_club, A_shots
            from f_match;
    ''')

    c.mycurser.execute('''
        select club, max_shots
        from (
            select club, sum(s) as max_shots
            from shots
            group by club
            order by max_shots DESC
            ) as t 
            limit 10;
    ''')

    clear()
    top10 = c.mycurser.fetchall()
    for s in top10:
        print(f'{s[0]}, {s[1]}')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Show the top 10 teams by fouls
def top10_fouls():
    c.mycurser.execute('''
        CREATE OR REPLACE view fouls as
            select H_club as club, H_fouls as f
            from f_match
            union all 
            select A_club, A_fouls
            from f_match;
    ''')

    c.mycurser.execute('''
        select club, max_fouls
        from (
            select club, sum(f) as max_fouls
            from fouls
            group by club
            order by max_fouls DESC
            ) as t 
            limit 10;
    ''')

    clear()
    top10 = c.mycurser.fetchall()
    for f in top10:
        print(f'{f[0]}, {f[1]}')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Show all the teams who won the most games by season
def most_wins_per_season():
    # c.mycurser.execute('''
    #     CREATE OR REPLACE view  won as
    #         (select H_club as Club, season
    #         from f_match
    #         where H_goals > A_goals)
    #         union all
    #         (select A_club, season
    #         from f_match
    #         where A_goals > H_goals)
    # ''')
    #
    # c.mycurser.execute('''
    #     select season, club, c
    #     from (
    #         select club , count(*) c, season
    #         from won
    #         group by club, season
    #         order by season, c DESC
    #     )as t
    #     group by season
    # ''')

    c.mycurser.execute('''
        select season, A_club as Club_Name, max(winns) as Maximum_wins
        from
         (select m.season, m.A_club, count(m.A_club) + sub.H_club_wins as winns
         from f_match m inner join
                (select season, H_club, count(H_club) as H_club_wins
                from f_match
                where H_goals > A_goals
                group by season, H_club) as sub
                on m.A_club = sub.H_club and m.season = sub.season
                where m.A_goals > m.H_goals
                group by m.season, m.A_club
                order by winns DESC) as t
            group by season
            order by season;
    ''')

    clear()
    clubs = c.mycurser.fetchall()

    for club in clubs:
        print(f'{club[0], club[1], club[2]}')
    print('\n')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Query and view a given team information
def team_info():
    clear()

    while True:
        team_name = input("Enter a team's name: ").strip()
        if not validate_club(team_name):
            print('There is no such a club. Re-enter the club name\n')
        else:
            break

    syntax = '''
            select C_name, website, home_stadium
            from club
            where C_name = %s
        '''
    values = [team_name]
    c.mycurser.execute(syntax, values)

    all_info = c.mycurser.fetchall()

    for info in all_info:
        print(f'{info[0]}, {info[1]}, {info[2]}')
    print('\n')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Query and view a given player information (by their first and last name)
def view_player_info():
    clear()

    player_name = input("Enter a player's name: ").strip()
    syntax = '''
            select P_name, position, nationality, height, DOB, current_club
            from player
            where P_name = %s
        '''
    values = [player_name]
    c.mycurser.execute(syntax, values)

    all_info = c.mycurser.fetchall()

    for info in all_info:
        print(f'{info[0]}, {info[1]}, {info[2]}, {info[3]}, {info[4]}, {info[5]}')
    print('\n')

    if not len(all_info):
        print('Player does not exist\n')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Identify the home team for a given stadium name
def home_team_of_stadium():
    clear()

    while True:
        stadium_name = input("Enter a stadium's name: ").strip()
        if not validate_stadium(stadium_name):
            print('There is no such a stadium. Re-enter the stadium name\n')
        else:
            break

    syntax = '''
            select C_name
            from club
            where home_stadium = %s
        '''
    values = [stadium_name]
    c.mycurser.execute(syntax, values)

    club_name = c.mycurser.fetchall()
    print(f'{club_name[0][0]}\n')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# Show all the players who played a certain position
def player_of_pos():
    clear()

    while True:
        pos = input("Enter a position: ").strip()
        if not validate_pos(pos):
            print('There is no such a position. Re-enter the position\n')
        else:
            break

    syntax = '''
            select P_name
            from player
            where position = %s
        '''
    values = [pos]
    c.mycurser.execute(syntax, values)

    players = c.mycurser.fetchall()
    for player in players:
        print(f'{player[0]}')
    print('\n')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


# (Bonus): Identify all the teams in a given city in the UK
def teams_of_city():
    clear()

    city = input("Enter a city's name: ").strip()
    syntax = '''
            select C_name
            from club inner join stadium
            on home_stadium = S_name
            where address like %s
        '''
    values = [f'%{city}%']
    c.mycurser.execute(syntax, values)

    clubs = c.mycurser.fetchall()
    for club in clubs:
        print(f'{club[0]}')
    print('\n')

    if not len(clubs):
        print('No clubs exist in the desired city\n')

    while True:
        x = input('''
                1. Return to previous page\n
                2. Quit\n
                Your Choice: ''')
        if x == '1':
            action()
            break
        elif x == '2':
            quit()
        else:
            print('No valid input\n')


def register():
    clear()
    username = input('User name: ').strip()

    while True:
        email = input('email: ').strip()
        if validate_email(email) == 'exists':
            print('Email already exists. Enter another Email\n')
        elif validate_email(email) == 'not valid':
            print('Email not valid. Enter another Email\n')
        else:
            break

    password = input('Password: ').strip()
    age = input('Age: ').strip()
    while True:
        gender = input('Gender[M, F, O]: ').strip()
        if not validate_gender(gender):
            print('Invalid input\n')
        else:
            break

    while True:
        dob = input('Date of Birth[DD/MM/YYYY]: ').strip()
        if not validate_date(dob):
            print('Invalid date\n')
        else:
            break

    while True:
        fav_club = input('Favourite Club: ').strip()
        if not validate_club(fav_club):
            print('There is no such a club. Re-enter the club name\n')
        else:
            break

    syntax = '''
        insert into fan 
        value (%s, %s, %s, %s, %s, %s, %s)
    '''
    values = (email, age, gender, password, username, dob, fav_club)
    c.mycurser.execute(syntax, values)
    c.db.commit()

    current_user.email = email


def log_in():
    clear()
    while True:
        email = input('email: ').strip()
        if validate_email(email) == 'not exist':
            print('Email does not exist. Enter another Email\n')
        elif validate_email(email) == 'not valid':
            print('Email not valid. Enter another Email\n')
        else:
            break

    while True:
        password = getpass('Password: ')
        if not validate_password(password):
            print('Password is not correct. Enter again\n')
        else:
            break

    current_user.email = email


################## main code ######################################

# first stage [signup - log in - guest entry]
def main():
    while True:
        clear()
        x = input(
            '''
            Welcome to our Application\n
            Choose 1, 2, or 3 to continue\n
            1. SignUp\n
            2. Log in\n
            3. Guest\n
            4. Quit\n
            Enter your choice: 
            ''').strip()

        if x == '1':
            enterMode = 'SignUp'
            register()
            print('Sign up Successful\n')
            time.sleep(2)
            clear()
            action()
            break

        elif x == '2':
            enterMode = 'Log in'
            log_in()
            print('Log in successful\n')
            time.sleep(2)
            clear()
            action()
            break

        elif x == '3':
            enterMode = 'Guest'
            action()
            break

        elif x == '4':
            quit()

        else:
            clear()
            print('Invalid Input\nPlease, enter your choice again\n')


# second stage [show available options for every entry type]
def action():
    if enterMode in ['Signup', 'Log in']:
        while True:
            clear()
            option = input('''
                Welcome to the main page\n
                You can perform any of the following options\n
                
                1. View existing reviews on a given match\n
                2. Show all the players from a certain nationality and their home teams history\n
                3. Show the top 10 teams by matches won, home matches won, yellow cards, fouls, and shots\n
                4. Show all the teams who won the most games by season\n
                5. Query and view a given team information\n
                6. Query and view a given player name\n
                7. Identify the home team for a given stadium name\n
                8. Show all the players who played a certain position\n
                9. Identify all the teams in a given city in the UK\n
                10. Register a new user\n
                11. Add a new user review on a match\n
                12. Quit\n
                choose the corresponding number of the desired action: ''').strip()

            if 0 < int(option) < 12:
                break
            elif option == '12':
                quit()
            else:
                print('Invalid Input\nPlease, enter your choice again\n')

    else:
        while True:
            clear()
            option = input('''
                Welcome to the main page\n
                You can perform any of the following options\n
        
                1. View existing reviews on a given match\n
                2. Show all the players from a certain nationality and their home teams history\n
                3. Show the top 10 teams by matches won, home matches won, yellow cards, fouls, and shots\n
                4. Show all the teams who won the most games by season\n
                5. Query and view a given team information\n
                6. Query and view a given player name\n
                7. Identify the home team for a given stadium name\n
                8. Show all the players who played a certain position\n
                9. Identify all the teams in a given city in the UK\n
                10. Register a new user\n
                11. Quit\n
                choose the corresponding number of the desired action: 
            ''').strip()

            if 0 < int(option) < 11:
                break
            elif option == '11':
                quit()
            else:
                print('Invalid Input\nPlease, enter your choice again\n')

    # performing the desired query
    if option == '1':
        view_reviews()
    elif option == '2':
        show_players()
    elif option == '3':
        while True:
            clear()
            option = input('''
                        Choose the desired criteria\n
    
                        1. wins ever\n
                        2. home wins\n
                        3. Yellow cards\n
                        4. Fouls\n
                        5. Shots\n
                        choose the corresponding number of the desired criteria: ''').strip()

            if option == '1':
                top10_teams_wins()
                break
            if option == '2':
                top10_teams_home_wins()
                break
            if option == '3':
                top10_yellow()
                break
            if option == '4':
                top10_fouls()
                break
            if option == '5':
                top10_shots()
                break
            else:
                print('Invalid Input\nPlease, enter your choice again\n')
    elif option == '4':
        most_wins_per_season()
    elif option == '5':
        team_info()
    elif option == '6':
        view_player_info()
    elif option == '7':
        home_team_of_stadium()
    elif option == '8':
        player_of_pos()
    elif option == '9':
        teams_of_city()
    elif option == '10':
        register()
        action()
    elif option == '11':
        add_review()
    else:
        print('Invalid Input\nPlease, enter your choice again\n')


c = Connect()
f = Fetch()
current_user = User()
main()
print('Action performed successfully\n')
time.sleep(0)
