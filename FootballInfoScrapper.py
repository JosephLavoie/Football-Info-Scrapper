def generate_urls(start, end):
    url_list = []
    
    for year in range(start, end + 1):
        url = f"https://www.pro-football-reference.com/years/{year}/"
        url_list.append(url)
    
    return url_list

def main():
    # Generate list of years
    urls = generate_urls(2000, 2022)

if __name__ == "__main__":
    main()
