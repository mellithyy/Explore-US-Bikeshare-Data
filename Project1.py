import time
import numpy as np
import pandas as pd

cities_dict = {"chicago":"chicago.csv", "new york city":"new_york_city.csv",
               "nyc":"new_york_city.csv","washington":"washington.csv"}

months_dict = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", "all":"all"}

days_dict   = {1:"Sunday", 2:"Monday", 3:"Tuesday", 4:"Wednesday", 5:"Thursday", 6:"Friday", 7:"Saturday", "all":"all"}


def get_filters():
    """
    Asks user to specify a month and a day to analyze
    
    Returns:
        (str) -- Name of City chosen by a user to analyze.
        (str) -- Name of the month to filter by, or "all" to apply no month filter
        (str) -- Name of the day of week to filter by, or "all" to apply no day filter
    """
    
    ### Asking user to choose a city.
    city = input("Which city do you want to know a bout (Chicago - New York City (NYC) - Washington)?: ").lower()

    while city not in ['chicago','new york city', 'nyc', 'washington']:
        city = input("That city is not valid, please choose from (Chicago - New York City (NYC) - Washington): ").lower()
    print('-'*100)
    
    ### Asking user to choose which month to analyze.
    month = input("Which month do you want to analyze?\nPlease type 'all' to analyze all months, or a number representing the month you want!\nExample: January: 1 - February: 2 ...etc: ")
    while True:
        try:
            if month != "all":
                month = int(month)
                if month > 6:
                    month = input("Months available up to and including June only!\nPlease type 'all' or a number between(1-6): ")
                    continue
                else:
                    month = int(month)
                    break
            
            else:
                break
        
        except:
            month = input("That is not a valid input!\nPlease type 'all' to analyze all months or a number between (1-6): ")
    print('-'*100)
    
    ### Asking user to choose which day of the week to analyze.
    day = input("Which day do you want to analyze?\nPlease type 'all' to analyze all days, or a number representing the day you want!\nExample: Sunday: 1 - Monday: 2 ...etc: ")
    while True:
        try:
            if day != "all":
                day = int(day)
                if day > 7:
                    day = input("A week has only 7 Days!\nPlease type 'all' or a number between (1-7): ")
                    continue
                else:
                    day = int(day)
                    break
            else:
                break
        except:
            day = input("That is not a valid input!\nPlease type 'all' to analyze all days or a number between (1-7)!")
    #while day not in ["1","2","3","4","5","6","7","all"]:
    #    month = input("That is not a valid answer.\nPlease type 'all' to analyze all days or a number between (1-7): ")
    print('-'*100)
    

    return city, month, day

################################################################################################################################

def load_data(city:str, month:int, day:int) -> pd.DataFrame:
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    ## Read Csv file.
    df = pd.read_csv(cities_dict[city])
    
    ## Changing type of "Start Time" Column into Timestamp.
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    ## Extracting month names into a new column.
    df['month'] = df['Start Time'].dt.month_name()
    
    ## Extracting week days' names into a new column.
    df['day_of_week']  = df['Start Time'].dt.day_name()
    
    ## Loading Data based on User's choices:
    ### Checking if User chose to filter by all months or not:
    if month != "all":
        month = months_dict[month]
        df    = df[df['month'] == month]
    
    ### Checking if the user chose to filter by all days or not:
    if day != "all":
        day = days_dict[day]
        df  = df[df['day_of_week'] == day]
    
    
    print(f"Here's a Sample of the based on your choices:\n"
          f"City: {city} - Month: {month} - Day: {day}")
    print('-'*45)
    print(df.head())
    print('\n')
    print('-'*100)

    return df

################################################################################################################################

def time_stats(df: pd.DataFrame):
    """Displays statistics on the most frequent times of travel."""
    print("-"*100)
    print('Calculating The Most Frequent Times of Travel...')
    print('-'*50)
    print('\n')
    start_time = time.time()

    # Display the most common month
    print(f"Most Common Month is: {df['month'].mode()[0]}")

    # Display the most common day of week
    print(f"Most Common Day of week is: {df['day_of_week'].mode()[0]}")

    # Display the most common start hour
    print(f"Most Common Start Hour is: {df['Start Time'].dt.hour.mode()[0]}")

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('\n')
    print('-'*100)
    
################################################################################################################################

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    print("-"*100)
    print('Calculating The Most Popular Stations and Trip...')
    print('-'*50)
    print('\n')
    start_time = time.time()

    # Display most commonly used start station
    print(f"Most commonly used start station is: {df['Start Station'].mode()[0]}")

    # Display most commonly used end station
    print(f"Most commonly used end station is: {df['End Station'].mode()[0]}")

    # Display most frequent combination of start station and end station trip
    start_and_end = df.groupby(['Start Station','End Station']).size().idxmax()
    
    print(f"Most frequent combination of start and end station trip is:\n'{start_and_end[0]}', '{start_and_end[1]}'")
    
    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('\n')
    print('-'*100)
    
################################################################################################################################

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print("-"*100)
    print('Calculating Trip Duration...')
    print('-'*50)
    print('\n')
    start_time = time.time()

    # Display total travel time
    print(f"Total travel time is: {df['Trip Duration'].sum()} Seconds.")

    # Display mean travel time
    print(f"Mean travel time is: {round(df['Trip Duration'].mean())} Seconds.")

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('\n')
    print('-'*100)

################################################################################################################################

def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('-'*100)
    print('Calculating User Stats...')
    print('-'*50)
    print('\n')
    start_time = time.time()

    # Display counts of user types
    print(f"Counts of user types:")
    for key,value in dict(df['User Type'].value_counts()).items():
        print(f" - {key}: {value}")

    # Display counts of gender
    print(f"\nCounts of gender:")
    for key,value in dict(df['Gender'].value_counts()).items():
        print(f" - {key}: {value}")

    # Display earliest, most recent, and most common year of birth
    print('\nBirth Year Stats:')
    print(f" - Earliest Year: {int(df['Birth Year'].min())}\n",
          f"- Most Recent Year: {int(df['Birth Year'].max())}\n",
          f"- Most Common Year: {int(df['Birth Year'].mode()[0])}")

    print("\n\nThis took %s seconds." % (time.time() - start_time))
    print('\n')
    print('-'*100)
    
################################################################################################################################

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        if city not in ['chicago','new york city','nyc']:
            print("\nThis Dataset has no 'Gender' Column to calculate its statistics.\n\n")
            print('-'*100)
        else:
            user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()