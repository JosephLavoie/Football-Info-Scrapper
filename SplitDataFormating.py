"""
STEP 6 - SplitDataFormating.py
Formats most of the data together and puts it in multiple different csv. Creates
NFLKicksInfo2000-2022WeatherSplit.csv, NFLKicksInfo2000-2022NonSplit.csv,
NFLKicksInfo2000-2022NonSplitClosedDome.csv,
NFLKicksInfo2000-2022WeatherSplitWindChill.csv, and 
NFLKicksInfo2000-2022WeatherSplitBadWindChill.csv .

Functions:
- main: Starts everything and stores information formatted properly in the csv files.
"""


def main():
    """
    Start of the program. Stores information formatted properly in the csv files.
    """ 
    
    formated_csv, weather_csv, bad_windchill_csv, = [], [], []
    windchill_csv, non_csv, closed_dome_csv = [], [], []

    # Opens the original csv, reads and stores information in the formated_csv list
    with open('NFLKicksInfo2000-2022.csv', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            formated_csv.append(line.strip())
    
    # Makes sure the column titles stay intact for final csvs
    titles = formated_csv[0]
    non_csv.append(titles)
    closed_dome_csv.append(titles)
    bad_windchill_csv.append(titles)

    # The criteria of which all csvs will be diferent
    for each in formated_csv:

        if "N/A,N/A" in each:
            non_csv.append(each)
            if not "(open)" in each:
                closed_dome_csv.append(each)

        elif "N/A" in each:
            weather_csv.append(each)
            bad_windchill_csv.append(each)
            
        else:
            weather_csv.append(each)
            windchill_csv.append(each)
    
    # Rest of the code writes the specifc information wanted to each individual csv.
    with open('NFLKicksInfo2000-2022WeatherSplit.csv', 'w') as file:
        for each in weather_csv:
            file.write(each + "\n")
    
    with open('NFLKicksInfo2000-2022NonSplit.csv', 'w') as file:
        for each in non_csv:
            file.write(each + "\n")
    
    with open('NFLKicksInfo2000-2022NonSplitClosedDome.csv', 'w') as file:
        for each in closed_dome_csv:
            file.write(each + "\n")
    
    with open('NFLKicksInfo2000-2022WeatherSplitWindChill.csv', 'w') as file:
        for each in windchill_csv:
            file.write(each + "\n")
    
    with open('NFLKicksInfo2000-2022WeatherSplitBadWindChill.csv', 'w') as file:
        for each in bad_windchill_csv:
            file.write(each + "\n")   


if __name__ == "__main__":
    main()
