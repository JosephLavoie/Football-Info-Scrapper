import time
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument("disable-quic")

# Set up the WebDriver (for example, using Chrome)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


def Information_Getter(game_url_list):

    infoCSV = []
    bad_infoCSV = []
    line = 0

    for url in game_url_list[:10]:

        response = requests.get(url)

        wait_time = response.headers.get('Retry-After')
        if wait_time:
            print(wait_time)
            time.sleep(int(wait_time) + 1)
            response = requests.get(url)
        
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            #---------------------------------------------------------------------------------------
            # Statium
            #---------------------------------------------------------------------------------------

            statium_element = soup.find('a', href=lambda href: href and href.startswith("/stadiums/"))

            if statium_element:
                statium = statium_element.text
            else:
                print("Missing: Statium")
                statium = "N/A"

            #---------------------------------------------------------------------------------------
            #---------------------------------------------------------------------------------------
            #Selenium
            #---------------------------------------------------------------------------------------
            #---------------------------------------------------------------------------------------
                
            driver.get(url)
            # Introduce a delay (e.g., 4 seconds) to allow dynamic content to load
            driver.implicitly_wait(4)

            #---------------------------------------------------------------------------------------
            # Roof
            #---------------------------------------------------------------------------------------
            try:    
                roof_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//th[@data-stat="info" and text()="Roof"]'))
                )

                roof = roof_element.find_element(By.XPATH, '../td[@data-stat="stat"]').text

            except:
                print("Missing: Roof")
                roof = "N/A"
            #---------------------------------------------------------------------------------------
            # Surface
            #---------------------------------------------------------------------------------------
            try:
                surface_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//th[@data-stat="info" and text()="Surface"]'))
                )

                surface = surface_element.find_element(By.XPATH, '../td[@data-stat="stat"]').text

            except:
                print("Missing: Surface")
                surface = "N/A"

            #---------------------------------------------------------------------------------------
            # Field Goals
            #---------------------------------------------------------------------------------------

            try:
                fgm_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//td[@data-stat="fgm"]'))
                )

                fga_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//td[@data-stat="fga"]'))
                )

                fgm, fga = 0,0
                for fgm_element, fga_element in zip(fgm_elements, fga_elements):
                    fgm_per = fgm_element.text
                    fga_per = fga_element.text

                    if fgm_per:
                        fgm += int(fgm_per)
                    if fga_per:
                        fga += int(fga_per)
            except:
                fgm, fga = 0,0

            #---------------------------------------------------------------------------------------
            # Weather
            #---------------------------------------------------------------------------------------
            try:
                weather_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//th[@data-stat="info" and text()="Weather"]'))
                )

                weather = weather_element.find_element(By.XPATH, '../td[@data-stat="stat"]').text

            except:
                print("Missing: Weather")
                weather = "N/A"

            #---------------------------------------------------------------------------------------
            #---------------------------------------------------------------------------------------
            #---------------------------------------------------------------------------------------

            infoCSV.append(str(line) + "," + statium + "," + roof + "," + surface + "," + str(fgm) + "," + str(fga) + "," + weather)
            print("#" + str(line) + "," + statium + "," + roof + "," + surface + "," + str(fgm) + "," + str(fga) + "," + weather)

        else:
            print(f"Failed to retrieve the HTML content. Status code: {response.status_code}")
            bad_infoCSV.append(str(line) + "," + url)


        print(f"#{line} out of ~8000")
        line += 1

    return [infoCSV, bad_infoCSV]


def main():
    print("Use 'bad_infoCSV.txt' instead of game_url_list.txt?")
    user_input = input("Y/N: ")

    gameUrls = []

    if user_input == "N":
        with open('game_url_list.txt', 'r') as file:
            # Read each line from the file and append it to the list
            for line in file:
                gameUrls.append(line.strip())
        
    else:
        with open('bad_infoCSV.txt', 'r') as file:
            # Read each line from the file and append it to the list
            for line in file:
                gameUrls.append(line.strip())

    infoLine = Information_Getter(gameUrls)

    with open('infoCSV.txt', 'a') as file:
        # Convert each element of the list to a string and write it to the file
        for item in infoLine[0]:
            file.write(str(item) + '\n')
    
    with open('bad_infoCSV.txt', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for item in infoLine[1]:
            file.write(str(item) + '\n')

if __name__ == "__main__":
    main()
