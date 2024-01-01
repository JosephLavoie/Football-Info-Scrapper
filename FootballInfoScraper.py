"""
STEP 1 - FootballInfoScaper.py

Takes a range of years and returns a txt file named "game_url_list.txt". This contains
a list, where each line is an element, of all regular NFL games played in that range.
These are stored as pro-football-reference.com urls.

Functions:
- generateYearUrls: Creates a list of years.
- generateWeekUrls: Creates a list of weeks.
- generateGameUrls: Creates a lost of games.
- main: Starts everything and stores information gathered.

"""

# Imports
import time
import requests
from bs4 import BeautifulSoup


def generateYearUrls(start:int, end:int):
    """
    Takes a range of years and provides a list of pro-football-reference.com urls that
    correspond to it.

    Parameters:
    - start(int): The year you want to start with.
    - end (int): The year you want to end with (inclusive).

    Returns:
    list: pro-football-reference.com year urls.
    """
    url_list = []

    # Creates urls and stores them in url_list
    for year in range(start, end + 1):
        url = f"https://www.pro-football-reference.com/years/{year}/"
        url_list.append(url)
    
    return url_list


def generateWeekUrls(year_url_list:list, start:int, end:int):
    """
    Takes a list of years in pro-football-reference.com urls form, and provides a list
    of pro-football-reference.com urls that correspond to each specified week within
    the years provided.

    Parameters:
    - year_url_list(list): List of pro-football-reference.com year urls.
    - start(int): The week you want to start with.
    - end (int): The week you want to end with (inclusive).

    Returns:
    list: pro-football-reference.com week urls.
    """
    url_list = []
    
    # Creates urls and stores them in url_list
    for year in year_url_list:
        for week in range(start, end + 1):
            url = f"{year}week_{week}.htm"
            url_list.append(url)
    
    return url_list


def generateGameUrls(week_url_list:list):
    """
    Takes a list of weeks in pro-football-reference.com urls form, and provides a list
    of pro-football-reference.com urls that correspond to each game within
    the weeks provided.

    Parameters:
    - year_url_list(list): List of pro-football-reference.com week urls.

    Returns: list:
    - [0] list: pro-football-reference.com game urls.
    - [1] list: pro-football-reference.com week urls that returned an ERROR.
    """
    url_list, bad_url_list = [], []
    count = 1

    # Finds game urls and stores them in url_list
    # Also storing week urls that gave ERRORs in bad_url_list
    for url in week_url_list:

        # To prevent pro-football-reference from temp IP banning us, we delay each request
        time.sleep(5)
        response = requests.get(url)

        # Checks for a temp ban
        wait_time = response.headers.get('Retry-After')

        # If there is a ban, waits until it is over
        # (1 hour is tipical from pro-football-reference)
        if wait_time:
            print(wait_time)
            time.sleep(int(wait_time) + 1)
            response = requests.get(url)
        
        # Prints the current count of which week your on
        print(f"#{count}")
        count += 1
        
        # Checks if we had a successful request
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <a> tags with href attribute starting with "/boxscores/20"
            target_links = soup.find_all('a', href=lambda href: href and \
                                         href.startswith("/boxscores/20"))

            # Extract the href attribute value for each matching link and adds to list
            for link in target_links:
                url_list.append("https://www.pro-football-reference.com" \
                                + link.get('href'))

        else:
            # if the request was unsuccessful, it adds the week url to bad_url_list
            print(f"Failed to retrieve the HTML content. Status code: \
                  {response.status_code}")
            bad_url_list.append(url)

    return [url_list, bad_url_list]


def main():
    """
    Start of the program, allows the initialization of all other functions. Also stores
    information gathered.
    """
    # Gives the choice of whether to use a created list or create one
    print("Use 'bad_game_url_list.txt' as the weekUrls?")
    user_input = input("Y/N: ")

    if user_input == "N":
        # Generate list of years, then weeks from that years list
        year_urls = generateYearUrls(2000, 2022)
        week_urls = generateWeekUrls(year_urls, 1, 21)

        # For years that have an extra week
        week_urls.append("https://www.pro-football-reference.com/years/2021/week_22.htm")
        week_urls.append("https://www.pro-football-reference.com/years/2022/week_22.htm")

    else:
        week_urls = []

        # Reads the bad_game_url_list.txt, stores in week_urls
        with open('bad_game_url_list.txt', 'r') as file:
            # Read each line from the file and append it to the list
            for line in file:
                week_urls.append(line.strip())

    # Gets the final list of games
    game_urls = generateGameUrls(week_urls)

    # Appends the game_url_list.txt, puts game_urls[0] in
    with open('game_url_list.txt', 'a') as file:
        # Convert each element of the list to a string and write it to the file
        for item in game_urls[0]:
            file.write(str(item) + '\n')

    # Writes the bad_game_url_list.txt, puts game_urls[1] in
    with open('bad_game_url_list.txt', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for item in game_urls[1]:
            file.write(str(item) + '\n')



    # Creates the begining of a file needed for FootballGameInfoScraper.py - STEP 2
    with open('infoCSV.txt', 'w') as file:
        file.write('"#","Statium","Roof Type","Surface Type","Field Goals Made","Field Goals Missed","Temperture","Realtive Humitity","Wind Speed","Wind Chill"\n')


if __name__ == "__main__":
    main()
