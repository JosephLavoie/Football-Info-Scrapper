import time
import requests
from bs4 import BeautifulSoup

def generate_year_urls(start, end):
    url_list = []
    
    for year in range(start, end + 1):
        url = f"https://www.pro-football-reference.com/years/{year}/"
        url_list.append(url)
    
    return url_list

def generate_week_urls(year_url_list, start, end):
    url_list = []
    
    for year in year_url_list:
        for week in range(start, end + 1):
            url = f"{year}week_{week}.htm"
            url_list.append(url)
    
    return url_list

def generate_game_urls(week_url_list):
    url_list = []

    for url in week_url_list[:45]:

        time.sleep(1)
        response = requests.get(url)

        wait_time = int(response.headers.get('Retry-After'))
        print(wait_time)

        if wait_time:
            time.sleep(int(wait_time) + 1)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <a> tags with href attribute starting with "/boxscores/20"
            target_links = soup.find_all('a', href=lambda href: href and href.startswith("/boxscores/20"))

            # Extract and print the href attribute value for each matching link
            for link in target_links:
                url_list.append("https://www.pro-football-reference.com" + link.get('href'))
        else:
            print(f"Failed to retrieve the HTML content. Status code: {response.status_code}")

    return url_list


def main():
    # Generate list of years
    yearUrls = generate_year_urls(2000, 2022)
    weekUrls = generate_week_urls(yearUrls, 1, 21)

    # for years that have an extra week
    weekUrls.append("https://www.pro-football-reference.com/years/2021/week_22.htm")
    weekUrls.append("https://www.pro-football-reference.com/years/2022/week_22.htm")

    gameUrls = generate_game_urls(weekUrls)


    with open('game_url_list.txt', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for item in gameUrls:
            file.write(str(item) + '\n')

if __name__ == "__main__":
    main()
