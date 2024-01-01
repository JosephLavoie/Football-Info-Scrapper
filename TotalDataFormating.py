"""
STEP 5 - TotalDataFormating.py
Formats all data together and puts it in a csv, like it should be. Creates
NFLKicksInfo2000-2022.csv.

Functions:
- main: Starts everything and stores information formatted properly in a csv file.
"""

def main():
    """
    Start of the program. Stores information formatted properly in a csv file.
    """ 
    dates, info, formatted_csv = [], [], []

    # Reads datesCSV.txt and stores data within dates
    with open('datesCSV.txt', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            dates.append(line.strip())
    
    # Reads infoCSV.txt and stores data within info
    with open('infoCSV.txt', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            info.append(line.strip())
    
    # Checks if the lenths of each list is the same
    if len(dates) != len(info):
        print("!Lengths are not the same!")

    # Creates the final formatted_csv list
    for each in range(len(info)):
        formatted_csv.append(dates[each] + "," + info[each] + "\n")
    
    # Writes NFLKicksInfo2000-2022.csv
    with open('NFLKicksInfo2000-2022.csv', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for item in formatted_csv:
            file.write(item)


if __name__ == "__main__":
    main()
