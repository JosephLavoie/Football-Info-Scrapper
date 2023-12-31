
def main():
    
    formated_csv, weather_csv, non_csv = [], [], []

    with open('NFLKicksInfo2000-2022.csv', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            formated_csv.append(line.strip())
    

    for each in formated_csv:
        if "N/A" in each:
            non_csv.append(each)
        else:
            weather_csv.append(each)
    
    with open('NFLKicksInfo2000-2022WeatherSplit.csv', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for each in weather_csv:
            file.write(each)
    
    with open('NFLKicksInfo2000-2022NonSplit.csv', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for each in non_csv:
            file.write(each)   

if __name__ == "__main__":
    main()
