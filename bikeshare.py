import pandas as pd
import datetime as datetime
import numpy as np
import time

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

# We are going to use those 3 list to check condiction in functions in our program
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
frame = ['month', 'day', 'both', 'all']


def get_city():
    """
    This function asks the user for the name of the city,
    check is the name is in CITY_DATA dictionary and return
    the name of the city.
    """
    print("Hello! This program explore some US bikesshare data!")
    while True:
        city = input('would you like to see data for Chicago, New York, or Washington?\n' )
        if city in CITY_DATA.keys():
            city = city.lower()
            break
        else:
            print('Check if your spelling is right,you have to choose Chicago, New York, or Washingto.')
            print('Try again!')
            continue
    return city


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all' and month != None:
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']== month]

    # filter by day of week if applicable
    if day != 'all' and day != None:
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']== day.title()]

    # Return a data Frame
    return df

def check_date(time_data):
    """
    This function checks that the month and day
    correspond with the lists of months and days
    Args: time_data (it could be month, day, both, or all )
    return: date
    """
    print("You can choose months from January to June and any day of the week")
    while True:
        date = input('Which {time_data} do you want to filter the data? enter in letters\n'.format(time_data= time_data))
        if date.lower() in months and time_data == 'month':
            date = date.lower()
            break

        elif date.lower() in days and time_data == 'day':
            date = date.lower()
            break
        else:
            print('Check if your spelling is right, You have to write the {time_data} in letters, try again!\n'.format(time_data= time_data))
            continue

    return date

def time_frame():
    """
    this function allows the user to select by day, month or both
    Args: Doesn't have them
    return: month and day
    """
    time_data = []
    while True:
        if time_data == []:
            time_data = input('would you like to filter the data by month, day, both, or not at all? Type "all" for no time filter\n')
            time_data = time_data.lower()
            if time_data not in frame:
                print('You have to chose month, day, both, or none\n')
                time_data = []
                continue

        elif time_data == 'both':
            month= check_date('month')
            day =check_date('day')
            day = day.title()

            break

        elif time_data == 'month':
            month= check_date('month')
            day= None
            break

        elif time_data == 'day':
            day =check_date('day')
            day = day.title()
            month= None
            break

        else:
            month = 'all'
            day = 'all'
            break

    return month, day

def times_travel_stats(df):
    """
    Displays statistics on the most frequent times of travel.
    Arg: df (it's the dataframe filter by month, day, or both)
    """

    print('Calculating  popular times travel...\n')
    start_time = time.time()
    # Shows the most common month
    common_month = df['month'].value_counts().idxmax()
    print('{} is the most common month'.format(months[common_month-1].title()))

    # Shows the most common day
    common_day = df['day_of_week'].value_counts().idxmax()
    print('{} is the most common day'.format(common_day.title()))

    # Shows the most common hour
    common_hour = df['hour'].value_counts().idxmax()
    print('{} is the most common hour\n'.format(common_hour))

    print("calculation time %s seconds." % (time.time() - start_time))
    print('.'*80)
    time.sleep(2)

def popular_station(df):
    """
    Displays statistics on the most popular stations and trip.
    Arg: df (it's the dataframe filter by month, day, or both)
    """

    # shows the most frequent start station
    print('Processing the  most frecuent stations statistics...\n')
    start_time = time.time()
    print( '{} is the most frecuent start station.'.format(df['Start Station'].value_counts().idxmax()))

    # shows the most frequent end station
    print( '{} is the most frecuent end station.'.format(df['End Station'].value_counts().idxmax()))

    # Shows the most frequent start - end station
    print('The combination of the start station and end station are:\n')
    print( df.groupby(['Start Station', 'End Station']).size().nlargest(1))

    print("calculation time %s seconds." % (time.time() - start_time))
    print('.'*80)
    time.sleep(2)

def trip_duration(df):
    """
    Displays statistics on the total and average trip duration
    Arg: df (it's the dataframe filter by month, day, or both)
    """

    # Shows total travel time
    print('Processing travel time information statistics...\n')
    start_time = time.time()
    print("Total travel time: {} days".format(round(df['Trip Duration'].sum()/86400, 2)))

    # Shows average travel time
    print("Average travel time: {} minutes\n".format(round(df['Trip Duration'].mean()/60, 2)))
    print("calculation time %s seconds." % (time.time() - start_time))
    print('.'*80)
    time.sleep(2)

def user_information(df, city):
    """
    Displays statistics on bikeshare users.
    Arg: df and city
    """

    # counts of each user type
    print('Processing user information statistics...\n')
    start_time = time.time()
    print("User types:\n", df['User Type'].value_counts())

    # Counts of each gender (only available for NYC and Chicago)
    if city == 'new york' or city == 'chicago':
        print("\nUser genders:\n",df['Gender'].value_counts())

    # Because there are 61,052 nan in the gender data and 61,019 nan in the year of birth
    # in the chicago data and there are also nan in the New York data, we are going to use
    # try and except to avoid potential break down in the program.
    try:
        Earliest_Year = int(df['Birth Year'].min())
        print('\nEarliest Year:', Earliest_Year)
    except KeyError:
        print("\nEarliest Year:\nNo data available.")

    try:
        Most_Recent_Year = int(df['Birth Year'].max())
        print('\nMost Recent Year:', Most_Recent_Year)
    except KeyError:
        print("\nMost Recent Year:\nNo data available.")

    try:
        Most_Common_Year = df['Birth Year'].value_counts().idxmax()
        print('\nMost Common Year:', int(Most_Common_Year))
    except KeyError:
        print("\nMost Common Year:\nNo data available.")

    print("calculation time %s seconds." % (time.time() - start_time))
    print('.'*80)
    time.sleep(2)

def dataframe_data(df):
    """
    Shows the data frame with the filter data by month, day, both or all.
    if you press enter the program displays the next 1" row
    """

    print('Press enter to see the firts 10 rows of the dataframe or  write quit and press enter to skip')
    i = 0
    while (input()!= 'quit'):

        print(df[i:i+10])
        i = i + 10
        print("\nPress enter if you want to see the next 10 rows or write quit  and press enter to skip")


def main():
    while True:
        city = get_city()
        month, day =time_frame()
        df = load_data(city, month, day)
        times_travel_stats(df)
        popular_station(df)
        trip_duration(df)
        user_information(df,city)
        dataframe_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
