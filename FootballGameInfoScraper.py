"""
STEP 2 - FootballGameInfoScraper.py
This  should take a long time, therfore do STEP 3 & 4 while waiting.

Takes a list of pro-football-reference game urls within "game_url_list.txt" and returns
the wanted data via webscraping. This is kick data, weather data, and statium data.

Functions:
- formatWeather: Properly formats weather data, so it can be stored correctly.
- informationScraper: Gets all information for the output file, via bs4 and selenium.
- main: Starts everything and stores information seperated by reading a txt file.
"""

import time
import requests
import re
from bs4 import BeautifulSoup

# Imports needed for selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Options added to the chromedriver, so we can webscrape without havoc
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("disable-quic")
options.add_argument("--disable-proxy-certificate-handler")
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--pageLoadStrategy=eager')


def FormatWeather(weather_text:str):
    """
    Takes a string of weather info and correctly formats it.

    Parameters:
    - weather_text(string): Weather data scraped from pro-football-reference.com

    Returns:
    string: Formated weather data.
    """

    # Replaces "no wind" with 0
    if "no wind" in weather_text:
        weather_text = weather_text.replace("no wind", "0")

    # Defines a list of words to remove
    words_to_remove = ["degrees", "relative humidity", "wind", "mph", "chill"]

    # Create a regex pattern by joining the words with the "|" (OR) operator
    pattern = re.compile(r'\b(?:' + '|'.join(map(re.escape, words_to_remove)) + \
                         r')\b\s*|\%', flags=re.IGNORECASE)

    # Use the sub function to replace the matched words, spaces,
    # and percentage signs with an empty string, keeping the commas
    weather = re.sub(pattern, '', weather_text)

    # Gets rid of spaces
    weather = weather.replace(" ", "")

    # Checks if the wind chill data doesn't exist, if not adds N/A in its collum
    comma_count = weather.count(',')
    if comma_count == 2:
        weather += ",N/A"

    return weather


def informationScraper(game_url_list:list, start_line:int):
    """
    Obtains all information needed for the "infoCSV.txt" to be created. Uses
    BeautifulSoup and Selenium on pro-football-reference.com via the given game urls to
    obtain information about each game.

    Parameters:
    - game_url_list(list): A url list of games to be scraped.
    - start_line(int): Line number within "game_url_list.txt" to start scraping at.

    Returns: list:
    - [0] list: scraped data that is properly formated.
    - [1] list: pro-football-reference.com game urls that returned an ERROR.
    """

    info_csv, bad_info_csv = [], []
    line = start_line

    # Set up the WebDriver (for example, using Chrome)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    # Takes each game individually and scraps
    for url in game_url_list[start_line:]:

        # To prevent pro-football-reference from temp IP banning us, we delay each request
        time.sleep(6)
        response = requests.get(url)

        # Checks for a temp ban
        wait_time = response.headers.get('Retry-After')

        # If there is a ban, waits until it is over
        # (1 hour is tipical from pro-football-reference)
        if wait_time:
            print(wait_time)
            time.sleep(int(wait_time) + 1)
            response = requests.get(url)
        
        # Checks if we had a successful request
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            #----------------------------------------------------------------------------
            # Statium
            #----------------------------------------------------------------------------

            # Find first 'a' element with an 'href' attribute starting with "/stadiums/"
            stadium_element = soup.find('a', href=lambda href: href and \
                                        href.startswith("/stadiums/"))

            # Check if a stadium element was found
            if stadium_element:
                # Extract the text content of the stadium element
                stadium = stadium_element.text
            else:
                # If no stadium element is found, print a message and set the stadium to "N/A"
                print("Missing: Stadium")
                stadium = "N/A"

            #----------------------------------------------------------------------------
            #----------------------------------------------------------------------------
            # Selenium
            #----------------------------------------------------------------------------
            #----------------------------------------------------------------------------
            
            # Gives the selenium webdriver the url
            driver.get(url)
            # Introduce a delay (e.g., 4 seconds) to allow dynamic content to load
            driver.implicitly_wait(4)

            #----------------------------------------------------------------------------
            # Roof
            #----------------------------------------------------------------------------
            try:   
                # Use WebDriverWait to wait for the presence of an element with specific XPATH 
                roof_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH,'//th[@data-stat="info" and text()="Roof"]'))
                )

                # If element is found, extract text content of the corresponding 'td' element
                roof = roof_element.find_element(By.XPATH, '../td[@data-stat="stat"]').text

            except:
                # If there's an exception (element not found or timeout), set 'roof' to "N/A"
                print("Missing: Roof")
                roof = "N/A"
            #----------------------------------------------------------------------------
            # Surface
            #----------------------------------------------------------------------------
            try:
                # Use WebDriverWait to wait for presence of an element with specific XPATH 
                surface_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//th[@data-stat="info" and text()="Surface"]'))
                )

                # If the element is found, extract the text content of the corresponding 'td' element
                surface = surface_element.find_element(By.XPATH, '../td[@data-stat="stat"]').text

            except:
                # If there's an exception (element not found or timeout), print a message and set 'surface' to "N/A"
                print("Missing: Surface")
                surface = "N/A"

            #----------------------------------------------------------------------------
            # Field Goals
            #----------------------------------------------------------------------------

            try:
                # Use WebDriverWait to wait for the presence of all elements with specific XPATH
                fgm_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//td[@data-stat="fgm"]'))
                )

                # Use WebDriverWait to wait for the presence of all elements with specific XPATH
                fga_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//td[@data-stat="fga"]'))
                )

                fgm, fga = 0,0

                # Iterate through corresponding FGM and FGA elements, calculating the total FGM and FGA
                for fgm_element, fga_element in zip(fgm_elements, fga_elements):
                    fgm_per = fgm_element.text
                    fga_per = fga_element.text

                    # If FGM or FGA data is present, add it to the running total
                    if fgm_per:
                        fgm += int(fgm_per)
                    if fga_per:
                        fga += int(fga_per)
            except:
                # If there's an exception (elements not found or timeout), set FGM and FGA to 0
                fgm, fga = 0,0

            #----------------------------------------------------------------------------
            # Weather
            #----------------------------------------------------------------------------
            
            # Check if roof element is not in the specified list
            if roof not in ["dome", "(closed)"]:
                try:
                    # Use WebDriverWait to wait for the presence of an element with specific XPATH for 'Weather'
                    weather_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//th[@data-stat="info" and text()="Weather"]'))
                    )

                    # Extract the text content of the corresponding 'td' element
                    weather = weather_element.find_element(By.XPATH, '../td[@data-stat="stat"]').text

                    # Format weather
                    weather = FormatWeather(weather)

                except:
                    # If there's an exception (element not found or timeout), set weather to default
                    print("Missing: Weather")
                    weather = "N/A,N/A,N/A,N/A"
            else:
                # Set weather to default
                weather = "N/A,N/A,N/A,N/A"

            #----------------------------------------------------------------------------
            #----------------------------------------------------------------------------
            #----------------------------------------------------------------------------

            # Appends all grabbed information to the info_csv list and prints it
            info_csv.append(str(line) + "," + stadium + "," + roof + "," + surface + "," + str(fgm) + "," + str(fga) + "," + weather)
            print(str(line) + "," + stadium + "," + roof + "," + surface + "," + str(fgm) + "," + str(fga) + "," + weather)

        else:
            # if the request was unsuccessful, it adds the week url to badinfo_csv
            print(f"Failed to retrieve the HTML content. Status code: {response.status_code}")
            bad_info_csv.append(str(line) + "," + url)

        # Notifies you which line you are on
        print("out of 6162")
        # Add to the count
        line += 1

        # Saves the data collected every 100 lines
        if (line % 100) == 0:
            print("Saving...")

            # Saves to infoCSV.txt
            with open('infoCSV.txt', 'a') as file:
                # Convert each element of the list to a string and write it to the file
                for item in info_csv:
                    file.write(str(item) + '\n')

            if bad_info_csv:
                with open('bad_infoCSV.txt', 'a') as file:
                    # Convert each element of the list to a string and write it to the file
                    for item in bad_info_csv:
                        file.write(str(item) + '\n')

            # Erases data in info_csv
            info_csv = []

    # Stops chromedriver
    driver.quit()

    return [info_csv, bad_info_csv]


def main():
    """
    Start of the program, allows the initialization of all other functions. Also stores
    information gathered.
    """
    # Gives the choice of wwhich list to use
    print("Use 'bad_infoCSV.txt' instead of game_url_list.txt?")
    user_input = input("Y/N: ")

    game_urls = []

    if user_input == "N":
        # Reads game_url_list.txt, stores information in game_urls
        with open('game_url_list.txt', 'r') as file:
            # Read each line from the file and append it to the list
            for line in file:
                game_urls.append(line.strip())
        
        # Asks for the line number to start scraping at
        print("Which line are we starting at?")
        line_number = int(input("#: "))

        
    else:
        # Reads bad_infoCSV.txt, stores information in game_urls
        with open('bad_infoCSV.txt', 'r') as file:
            # Read each line from the file and append it to the list
            for line in file:
                game_urls.append(line.strip())
        
        line_number = 0

    # Inistalizes the webscraping of information, and stores the information in infoLine
    information = informationScraper(game_urls, line_number)

    # Appends infoLine[0] information to infoCSV.txt
    with open('infoCSV.txt', 'a') as file:
        # Convert each element of the list to a string and write it to the file
        for item in information[0]:
            file.write(str(item) + '\n')
    
    # Appends infoLine[1] information to bad_infoCSV.txt
    with open('bad_infoCSV.txt', 'a') as file:
        # Convert each element of the list to a string and write it to the file
        for item in information[1]:
            file.write(str(item) + '\n')


if __name__ == "__main__":
    main()
