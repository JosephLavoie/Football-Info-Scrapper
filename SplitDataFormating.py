
def main():
    
    formated_csv, weather_csv, bad_windchill_csv, windchill_csv, non_csv, closed_dome_csv = [], [], [], [], [], []

    with open('NFLKicksInfo2000-2022.csv', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            formated_csv.append(line.strip())
    
    titles = formated_csv[0]
    non_csv.append(titles)
    closed_dome_csv.append(titles)
    bad_windchill_csv.append(titles)

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
    
    with open('NFLKicksInfo2000-2022WeatherSplit.csv', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for each in weather_csv:
            file.write(each + "\n")
    
    with open('NFLKicksInfo2000-2022NonSplit.csv', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for each in non_csv:
            file.write(each + "\n")
    
    with open('NFLKicksInfo2000-2022NonSplitClosedDome.csv', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for each in closed_dome_csv:
            file.write(each + "\n")
    
    with open('NFLKicksInfo2000-2022WeatherSplitWindChill.csv', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for each in windchill_csv:
            file.write(each + "\n")
    
    with open('NFLKicksInfo2000-2022WeatherSplitBadWindChill.csv', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for each in bad_windchill_csv:
            file.write(each + "\n")   

if __name__ == "__main__":
    main()
