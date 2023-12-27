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

def main():
    # Generate list of years
    yearUrls = generate_year_urls(2000, 2020)
    weekUrls = generate_week_urls(yearUrls, 1, 21)

    print(weekUrls)



    print(weekUrls)

if __name__ == "__main__":
    main()
