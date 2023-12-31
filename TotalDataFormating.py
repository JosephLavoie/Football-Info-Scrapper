
def main():
    
    dates, info, formated_csv = [], [], []

    with open('datesCSV.txt', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            dates.append(line.strip())
    
    with open('infoCSV.txt', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            info.append(line.strip())
    
    if len(dates) != len(info):
        print("!Lengths are not the same!")

    for each in range(len(dates)):
        formated_csv.append(dates(each) + "," + info(each))
    
    with open('NFLKicksInfo2000-2022.csv', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        for each in formated_csv:
            file.write(each)   

if __name__ == "__main__":
    main()
