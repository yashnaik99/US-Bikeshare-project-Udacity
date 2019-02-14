import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTH_DATA = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

DAY_DATA = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_name = ''
    while city_name.lower() not in CITY_DATA:
        city_name = str(input('Would you like to see data for Chicago, New York City, or Washington?\n').lower())
        if city_name.lower() in CITY_DATA:
            city = CITY_DATA[city_name.lower()]
        else:
            print('That is an incorrect input. Please enter the correct name of the city.')


    # get user input for month (all, january, february, ... , june)
    month_name = ''
    while month_name.lower() not in MONTH_DATA:
        month_name = input('For which month would you like to see the data for?\nPlease choose  any month from January to June or select "all" to see data for all the months\n')
        if month_name.lower() in MONTH_DATA:
            month = month_name.lower()
        else:
            print('Please input a correct value for the month you want to see.')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_name = ''
    while day_name.lower() not in DAY_DATA:
        day_name = input ('For which day would you like to see the data for?\nPlease choose  any day from Monday to Sunday or select "all" to see data for all the days\n')
        if day_name.lower() in DAY_DATA:
            day = day_name.lower()
        else:
            print('Please enter a correct value for the day you want to see.')
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
    # load datafile into a DataFrame
    df = pd.read_csv(city)

    # convert the Start Time column to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extracting month and day of the week from Start time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    #to filter by month when applicable
    if month != 'all':
        month = MONTH_DATA.index(month)

        #filter by month to create a new DataFrame
        df = df[df['month'] == month]

    #filter by day of the week where applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is', MONTH_DATA[common_month].title())

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_start_hour = df['hour'].mode()[0]
    print('The most common start hour is', common_start_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is ', common_end_station)

    # display most frequent combination of start station and end station trip
    popular_trip = (df['Start Station'] + df['End Station']).mode()[0]
    print('The most frequent combination of start and end station are', popular_trip)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The cumulative travel time is', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The types of users and their numbers are:', user_types)

    if city in ('chicago', 'new york city'):
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print('The gender numbers are as follows:', gender)

        # Display earliest, most recent, and most common year of birth
        earliest_yob = df['Birth Year'].min()
        print('The earliest year of birth is', earliest_yob)

        recent_yob = df['Birth Year'].max()
        print('The most recent year of birth is', recent_yob)

        common_yob = df['Birth Year'].mean()
        print('The most common year of birth is', common_yob)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Display raw data if the user asks for it"""
    print(df.head())
    next = 0
    while True:
        view_raw_data = input('\nDo you want to see the next five rows of raw data?\nEnter "Yes" or "No"\n')
        if view_raw_data.lower() != 'yes':
            return
        next = next + 5
        print(df.iloc[next:next+5])


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        while True:
            view_raw_data = input('\nDo you want to see the raw data for the above information\nEnter "Yes" or "No"\n')
            if view_raw_data.lower() != 'yes':
                break
            raw_data(df)
            break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
