"""
STEP 4 - DateToCSVFormat.py

Takes a list of unformatted dates from "unformatted_dates.txt" and formats them, putting
them in "datesCSV.txt". Start date for default settings: 20000903.

Functions:
- main: Starts everything and stores information that it formats to and from a txt file.
"""


def main():
    """
    Start of the program. Stores information formatted from a list within a txt file.
    """
    
    unformatted_dates, formatted_dates = [], []

    # Reads unformatted_dates.txt, puts information in unformatted_dates
    with open('unformatted_dates.txt', 'r') as file:
        # Read each line from the file and append it to the list
        for line in file:
            unformatted_dates.append(line.strip())
    
    # Formats each date
    for date in unformatted_dates:
        # Seperates the year, month, and day
        year = int(date[:4])
        month = int(date[4:6])
        day = int(date[6:])

        # Gets a relative year, if years started at 2000
        relative_year = (year - 2000)

        # turns months into total days from 20000903 (the first game)
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
        
        # Gets the relative days within the year
        relative_days_in_year = day - 3 + month_addon

        # Gets total days since 20000903
        total_days = (relative_year*365) + relative_days_in_year

        # For adding the extra day due to leap years
        total_days += (relative_year // 4)

        # adds formated date to the formatted_dates list
        formatted_dates.append([year,month_name,total_days])


    # Writes to datesCSV.txt
    with open('datesCSV.txt', 'w') as file:
        # Column titles
        file.write('"Year","Month","Days Since Sept 3rd 2000"\n')

        # Convert each element of the list to a string and write it to the file
        for item in formatted_dates:
            file.write(f"{str(item[0])},{str(item[1])},{str(item[2])}\n")


if __name__ == "__main__":
    main()
