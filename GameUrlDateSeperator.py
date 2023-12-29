
def main():
    
    urls = []

    with open('game_url_list.txt', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            urls.append(line.strip())
    
    with open('unformatted_dates.txt', 'w') as file:
        for url in urls:
            file.write(url[49:57] + '\n')
    
    # expected format: 20180906

if __name__ == "__main__":
    main()
