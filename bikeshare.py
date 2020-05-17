import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Would you like to see data for Chicago, New York City or Washington?:\n").lower()
    cities = ['chicago', 'newyork', 'new york city', 'new york', 'washington']
    while city not in cities:
        print("Oops, your entry is not valid.")
        city = input("Please enter a city - Chicago, New York or Washington:\n").lower()
    if city == 'new york' or city == 'newyork': city = 'new york city'

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = input("Would you like to filter data by month? Type January, February ... June or type 'all':\n").lower()
    while month not in months:
        print("Oops, your entry is not valid.")
        month = input("Please choose January, February, March, April, May, June or type 'all':\n").lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Would you like to filter data by day of the week? Type Monday, Tuesday ... Sunday or type 'all':\n").lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day not in days:
        print("Oops, your entry is not valid.")
        day = input("Please enter a day of week - Monday, Tuesday, ... Sunday or type 'all':\n").lower()


    print('-' * 40)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    # converting start time to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    print("Most common month: {}".format(df['month'].mode()[0]))

    # TO DO: display the most common day of week

    print("Most common day of week: {}".format(df['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most common start hour: {}".format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("Most common start station: {}".format(df['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("Most common end station: {}".format(df['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print("Most common start/end stations combination: {}"
          .format(df.groupby(['Start Station', 'End Station']).size().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time: around {} days".format(df['Trip Duration'].sum() // 86400))

    # TO DO: display mean travel time
    print("Average travel time: around {} minutes".format(df['Trip Duration'].mean() // 60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("USER TYPE COUNT: \n{}".format(df['User Type'].value_counts()))

    # TO DO: Display counts of gender only for new york and Chicago
    print('')
    if city != 'washington':
        print("GENDER COUNT:\n{}".format(df['Gender'].value_counts()))
        print("")
        # TO DO: Display earliest, most recent, and most common year of birth
        print("The earliest year of birth of the user: {}".format(int(df['Birth Year'].min())))
        print("The most recent year of birth of the user: {}".format(int(df['Birth Year'].max())))
        print("The most common year of birth of the user: {}".format(int(df['Birth Year'].mode()[0])))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    data = input("Do you want to see a Raw Data? Type 'yes' or 'no':\n")
    while data != 'yes' and data != 'no':
        print("Ops, you've made a mistake.")
        data = input("Type 'yes' or 'no'")
    n = 0
    while data == 'yes':
        print(df[n:n+5])
        data = input("Do you want to see next 5 rows?:\n")
        n += 5
    print('-' * 40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
