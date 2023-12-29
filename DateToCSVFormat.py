# expected format: 20180906
# start date: 20000903

import os

print("Current Working Directory:", os.getcwd())

def main():
    
    unformatted_dates = []
    formatted_dates = []

    with open('unformatted_dates.txt', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            unformatted_dates.append(line.strip())
    
    for date in unformatted_dates:
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])

        relative_year = (year - 2000)

        month_addon = 0
        if month == 10:
            month_addon = 31
            month_name = "October"
        elif month == 11:
            month_addon = 61
            month_name = "November"
        elif month == 12:
            month_addon = 92
            month_name = "December"
        elif month == 1:
            month_addon = 123-365
            month_name = "January"
        elif month == 2:
            month_addon = 151-365
            month_name = "February"
        else:
            month_name = "September"
        
        relative_days_in_year = day - 3 + month_addon

        total_days = (relative_year*365) + relative_days_in_year

        # For adding the extra day due to leap years
        total_days += (relative_year // 4)

        formatted_dates.append([year,month_name,total_days])


    
    with open('datesCSV.txt', 'w') as file:
        # Convert each element of the list to a string and write it to the file
        file.write('"Year","Month","Days Since Sept 3rd 2000"\n')
        for item in formatted_dates:
            file.write(f"{str(item[0])},{str(item[1])},{str(item[2])}\n")

if __name__ == "__main__":
    main()
