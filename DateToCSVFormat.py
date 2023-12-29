# expected format: 20180906
# start date: 20000903

import os

print("Current Working Directory:", os.getcwd())

def main():
    
    unformatted_dates = []

    with open('unformatted_dates.txt', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            unformatted_dates.append(line.strip())
    
    for date in unformatted_dates:
        year = date[:4]
        month = date[4:6]
        day = date[6:]
        print(f"Year: {year}, Month: {month}, Day: {day}")

    
    #with open('bad_game_url_list.txt', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        #for item in gameUrls[1]:
            #file.write(str(item) + '\n')

if __name__ == "__main__":
    main()
