# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 14:16:26 2020

@author: Colin
"""

import time
import pandas as pd
import operator

#Dictionary of city names and corresponding data files
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
    print('Hello! Let\'s explore some US bikeshare data!')
    # Gets user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = str(input("Would you like to explore data for Chicago, New York City, or Washington?\n")).lower()
        if city in CITY_DATA:
            break
        print('Please check to make sure you entered the city name properly.')


    # Gets user input for month (all, january, february, ... , june)
    while True:
        month = str(input("What month do you want to see metrics for? We have data for the first half of 2017.\n")).lower()
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        if month in months:
            break
        print("Please enter a valid month.")


    # Gets user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = str(input('What day do you want to see metrics for?\n')).lower()
        days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'saturday', 'sunday']
        if day in days:
            break
        print('Please enter a valid day of the week (ex, Saturday, Thursday)')


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
        df - pandas DataFrame containing city data filtered by month and day
    """

    # Loads data file into a dataframe
    df = pd.read_csv("C:/Users/Colin/Documents/Nanodegree/Python/Project/{}".format(CITY_DATA[city]))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # Filters by month
    if month != 'all':
        # uses the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filters by month to create the new dataframe
        df = df[df['month'] == month]

    # filters by day of week
    if day != 'all':
        # filters by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Displays the most common month
    months = df['Start Time'].dt.month_name()
    trips_by_month = {}
    for month in months:
        trips_by_month[month] = trips_by_month.get(month, 0) + 1

    busiest_month = sorted(trips_by_month.items(), key=operator.itemgetter(1))[-1]

    # alternate way to get busiest month: months.agg(lambda x:x.value_counts().index[0])
    #print('{} was the busiest month with {} trips.'.format(busiest_month[0], busiest_month[1]))

    # Displays the most common day of week
    days = df['Start Time'].dt.day_name()
    trips_by_day = {}
    for day in days:
        trips_by_day[day] = trips_by_day.get(day, 0) + 1

    busiest_day = sorted(trips_by_day.items(), key=operator.itemgetter(1))[-1]

    # alternate way to get busiest day: days.agg(lambda x:x.value_counts().index[0])
    # print('{} was the busiest day with {} trips.'.format(busiest_day[0], busiest_day[1]))

    # Prints a sting returning above information
    print('There were {} trips accross all {}s in {}'.format(busiest_month[1], busiest_day[0], busiest_month[0]))

    # Displays the most common start hour, and converts it to the 12 hour format
    hour_counts = df['Start Time'].dt.hour.value_counts()
    busiest_hour = hour_counts.idxmax(), hour_counts.max()
    if busiest_hour[0] > 12:
        print('{}pm was the busiest hour with {} total occurrences.'.format(busiest_hour[0] - 12,
                                                                      busiest_hour[1]))
    elif busiest_hour[0] == 12:
        print('{}pm was the busiest hour with {} total occurrences.'.format(busiest_hour[0],
                                                                      busiest_hour[1]))
    else:
        print('{}am was the busiest hour with {} total occurrences.'.format(busiest_hour[0],
                                                                      busiest_hour[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    start_station_counts = df['Start Station'].value_counts()
    most_common_start = start_station_counts.idxmax(), start_station_counts.max()
    print('{} is the most common start station with {} total occurrences'.format(most_common_start[0],
                                                                           most_common_start[1]))

    # Displays most commonly used end station
    end_station_counts = df['End Station'].value_counts()
    most_common_end = end_station_counts.idxmax(), end_station_counts.max()
    print('{} is the most common end station with {} total occurrences'.format(most_common_end[0],
                                                                           most_common_end[1]))

    # Displays most frequent combination of start station and end station trip
    trips = df[['Start Station', 'End Station']]
    most_frequent_trip = [trips.groupby(['Start Station', 'End Station']).size().idxmax()[0],
                          trips.groupby(['Start Station', 'End Station']).size().idxmax()[1],
                          trips.groupby(['Start Station', 'End Station']).size().max()]


    print('The most frequent trip starts at {} Station and ends at {} Station. This trip was made {} times!'.format(most_frequent_trip[0],
                                                                                                    most_frequent_trip[1],
                                                                                                    most_frequent_trip[2]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    total_duration = f"{sum(df['Trip Duration']/3600):.2f}"
    total_hours = total_duration.split(".")[0]
    total_minutes = float(total_duration.split(".")[1])/100*60
    print("The total travel time was {} hours and {} minutes.".format(total_hours, total_minutes))

    # Displays mean travel time
    mean_duration = f"{df['Trip Duration'].mean():.2f}"
    mean_hours = float(mean_duration)//3600
    mean_minutes = float(mean_duration)//60
    print("The mean travel time was {} hours and {} minutes.".format(int(mean_hours), float(mean_minutes)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Displays counts of gender
    if 'Gender' in df:
        genders = df['Gender'].value_counts()
        print(genders)

    # Displays earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print("The earliest birth year is {}.".format(int(min(df['Birth Year']))))
        print("The most recent birth year is {}.".format(int(max(df['Birth Year']))))
        birth_year_counts = df['Birth Year'].value_counts()
        most_common_birth_year = birth_year_counts.idxmax()
        print('{} is the most common birth year'.format(int(most_common_birth_year)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    """
        Executes the get_filters(), load_data(), more_stats() functions in succession
        to explore Bikeshare data from Chicago, New York City, and Washington for
        the first half of 2017, depending on user input.

        Users are required to pick a city, month, and day of the week to filter
        the data.
    """

    on = 'on'
    while on == 'on':
        city, month, day = get_filters()
        df = load_data(city, month, day)
        yes = ["yes", "y"]
        no = ["n", "no"]
        on = 'on'
        while True:
            show_header = input('\nWould you like to see the first 5 rows of data? Enter yes or no.\n').lower()
            if show_header in yes:
                print(df.head())
                break
            elif show_header in no:
                break
            print('\nPlease enter yes or no.\n')

        while True:
            more_stats = input('\nWould you like to see more stats about this subset of data?\n').lower()
            if more_stats in yes:
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                break
            elif more_stats in no:
                break
            print('\nPlease enter yes or no.\n')

        while on == 'on':
            on = "on"
            restart = input('\nWould you like to restart the program? Enter yes or no.\n').lower()
            if restart in no:
                on = 'off'
                break
            elif restart in yes:
                break
            print("Please enter yes or no")


if __name__ == "__main__":
	main()
