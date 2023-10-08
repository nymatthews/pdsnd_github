import time
import pandas as pd
import numpy as np
import calendar

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
    print('Hello! Welcome to the US Bikeshare Data system. Let\'s explore some bikeshare data!\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which city would you like to see bikeshare information for: Chicago, New York City, or Washington? ').lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('You have entered an unregistered city. Please enter one of the presented options.\n')
            
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('Which month would you like to see this data for: January, February, March, April, May, June or All? ').lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('You have entered an incorrect option. Please enter one of the presented options.\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:    
        day = input('Which day of the week would you like to see this data for (Type ALL if you would like to see every day)? ').lower()
        if day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
            break
        else:
            print('You have not entered an appropriate day of the week. Please enter the correct option.\n')
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
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
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

    # display the most common month
    common_month = df['month'].mode()[0]
    common_month_name = calendar.month_name[common_month]
    print('The most common travel month is', common_month_name)

    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common travel day is', common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.strftime('%I:%M%p')
    common_hour = df['hour'].mode()[0]
    print('The most common starting travel hour is', common_hour)

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
    print('The most commonly used end station is', common_end_station)
    
    # display most frequent combination of start station and end station trip
    combo_stations = df['Start Station'] + ' and ' + df['End Station']
    frequent_combo = combo_stations.mode()[0]
    print('The most frequently used start & end station combination is', frequent_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum() / 60)
    print('The total travel time is', total_travel_time, 'minutes')

    # display mean travel time
    average_travel_time = round(df['Trip Duration'].mean() / 60)
    print('The average travel time is', average_travel_time, 'minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types,'\n')
       
    # Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print(gender)
    except:
        print('Gender')
        print('We\'re sorry but this city does not provide any gender data.')

    # Display earliest, most recent, and most common year of birth
    
    #common_year = df['']
    
    print('\nBirth Year')
    try:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]
        print('Earliest user birth year:', earliest_year)
        print('Most recent user birth year:', recent_year)
        print('Most common user birth year:', common_year)
    except:
        print('We\'re sorry but this city does not provide any birth year data.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    start_data = 0
    see_raw_data = input('Would you like to view the bikeshare raw data? Enter yes or no.\n')
    while see_raw_data == 'yes':
        print(df.iloc[start_data:start_data + 5])
        start_data += 5
        continue_raw_data = input('Do you want to continue viewing the raw data? Enter yes or no.\n')
        if continue_raw_data != 'yes':
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart the US Bikeshare Data program? Enter yes or no.\n')
        if restart != 'yes':
            print('Thank you for using our US Bikeshare Data system! Please come again.')
            break


if __name__ == "__main__":
	main()
