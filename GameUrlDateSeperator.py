"""
STEP 3 - GameUrlDateSeperator.py

Takes a list of pro-football-reference game urls within "game_url_list.txt" and returns
the date of each to "unformatted_dates.txt" line by line.

Functions:
- main: Starts everything and stores information seperated by reading a txt file.
"""


def main():
    """
    Start of the program. Stores information seperated from a list within a txt file.
    """
    urls = []

    # Reads from game_url_list.txt, stores information in urls
    with open('game_url_list.txt', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            urls.append(line.strip())
    
    # Writes to unformatted_dates.txt, parts of information stored in urls
    with open('unformatted_dates.txt', 'w') as file:
        for url in urls:
            file.write(url[49:57] + '\n')
    
    # expected output format: 20180906


if __name__ == "__main__":
    main()
