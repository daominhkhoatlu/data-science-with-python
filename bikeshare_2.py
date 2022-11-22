import time
import pandas as pd
import numpy as np
from tabulate import tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def validate_input(message, valid_inputs):
    try:
        text = str(input(message)).lower()
        while text not in valid_inputs:
            print("Invalid input! Please try again!")
            text = str(input(message)).lower()
        print("Your choice is: {}".format(text))
        return text
    except:
        print("Invalid input!")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = CITY_DATA.keys()
    message = 'Please choose a city (chicago, new york city, washington):'
    city = validate_input(message, cities)

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all','january','february','march','april','may','june']
    message = 'Please choose a month (all, january, ... , june):'
    month = validate_input(message, months)

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday', 'sunday']
    message = 'Please choose a day (all, monday, ... sunday):'
    day = validate_input(message, days)

    print('-'*40)
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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df["Start Time"].dt.weekday
    df['hour'] = df['Start Time'].dt.hour
    if month != 'all':
        months_dict = {'january': 1,'february': 2,'march': 3,
                  'april': 4,'may': 5,'june': 6}
        month = months_dict[month]
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df["Start Time"].dt.weekday_name == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].value_counts().idxmax()
    print('The most common month is: {}'.format(popular_month))

    # TO DO: display the most common day of week
    popular_weekday = df['weekday'].value_counts().idxmax()
    print('The most common day of week is: {}'.format(popular_weekday))

    # TO DO: display the most common start hour
    popular_hour = df['hour'].value_counts().idxmax()
    print('The most common start hour is: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('The most common start station is: {}'.format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('The most common end station is: {}'.format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    popular_trip = df[['Start Station', 'End Station']].agg(' - '.join, axis=1).value_counts().idxmax()
    print('The most frequent combination of start station and end station trip is: {}'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df["Trip Duration"].sum()
    print('Total travel_time: {}'.format(total_travel_time))

    # TO DO: display mean travel time
    mean_travel_time = df["Trip Duration"].mean()
    print('Mean travel_time: {}'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Counts of user types: {}'.format(user_types))

    # TO DO: Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print('Counts of user gender: {}'.format(user_gender))
    except KeyError:
        print("There isn't a [Gender] column in this spreedsheet!")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest = int(df['Birth Year'].min())
        most_recent = int(df['Birth Year'].max())
        most_common = int(df['Birth Year'].value_counts().idxmax())
        print('\nEarliest year of birth is: {}'.format(earliest))
        print('Most recent year of birth is: {}'.format(most_recent))
        print('Most common year of birth is: {}'.format(most_common))
    except:
        print("There isn't a [Birth Year] column in this spreedsheet!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df: pd.DataFrame):
    # Show 5 raw data
    i = 0
    while True:
        raw_data = input('\nWould you see 5 raw data? Please enter yes or no.\n')
        if raw_data.lower() != 'yes':
            break
        print(tabulate(df.iloc[np.arange(0+i,5+i)], headers ="keys"))
        i+=5
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
