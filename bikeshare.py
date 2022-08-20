import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = month = day = "blank"

    city_choices = {'chicago', 'new york city', 'washington'}

    month_choices = {'all', 'january', 'february', 'march', 'april', 'may', 'june',
                     'july', 'august', 'september', 'october', 'november', 'december'}

    day_choices = {'all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'}

    while city == "blank":
        raw_city = input("Pick a city... Chicago, New York City, Washington: ")

        # Determine if input is a string // not performing boolean correctly w/o == "True" suffix
        if isinstance(raw_city, str):
            # set to lower case and trim for better filtering
            x = raw_city.lower().strip()

            # validate input is an expected city choice
            if x in city_choices:
                print("City selected: {}".format(x))
                city = x
            else:
                print("Invalid selection, or spelling error. try again.")
        else:
            print("Sorry, text only. Please try again.")

    while month == "blank":
        raw_month = input("Pick a month, or all for everything: ")
        y = raw_month.lower().strip()

        if y in month_choices:
            print("Month selected: {}".format(y))
            month = y
        else:
            print("Invalid month selection, or spelling. Please try again")

    while day == "blank":
        raw_day = input("Pick a day of the week, or all: ")
        z = raw_day.lower().strip()

        if z in day_choices:
            print("Day selected: {}".format(z))
            day = z
        else:
            print("Invalid day selection, or spelling. Please try again.")

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
    # For month / day strings to int conversion for use in dt calls
    month_data = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8,
                  'september': 9, 'october': 10, 'november': 11, 'december': 12, 'all': 13}

    day_data = {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7,
                'all': 8}

    df = pd.read_csv(CITY_DATA[city])  # Read data from city specific file

    df['Start Time'] = pd.to_datetime(df['Start Time'])  # Convert to datetime for dt usage

    # add filtering if anything but all is selected
    if month_data[month] != 13:
        df = df[df['Start Time'].dt.month == month_data[month]]

    if day_data[day] != 8:
        df = df[df['Start Time'].dt.day == day_data[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('Most common travel month: {}'.format(df['Start Time'].dt.strftime('%m/%Y').value_counts().index[0]))

    print('Most common travel day:   {}'.format(df['Start Time'].dt.strftime('%A').value_counts().index[0]))

    print('Most common start hour:   {}00'.format(df['Start Time'].dt.strftime('%H').value_counts().index[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Start station most commonly used: {}'.format(df['Start Station'].value_counts().index[0]))

    # TO DO: display most commonly used end station
    print('Eend station most used:   {}\n'.format(df['End Station'].value_counts().index[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print('Most frequent start/stop station combination:')
    print(df.groupby(['Start Station', 'End Station']).size().nlargest(1).to_string())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time {} hours'.format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print('Mean travel time: {} hours'.format(df['Trip Duration'].mean().round(2)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):  # Added city param for known data issue filtering by city
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('\n-----User Types----------\n' + df['User Type'].value_counts().to_string())

    # TO DO: Display counts of gender
    if city == "washington":
        print("\nSorry, Gender amd Birth data for Washington statistics are not available at this time.\n")
    else:
        print('\n-----Gender--------------\n' + df['Gender'].value_counts().to_string())

        # TO DO: Display earliest, most recent, and most common year of birth
        print("\n-----Year of Birth Stats-")
        print("Earliest:    {}".format(int(df['Birth Year'].nsmallest(1))))
        print("Most recent: {}".format(int(df['Birth Year'].nlargest(1))))
        print("Most common: {}".format(int(df['Birth Year'].value_counts().index[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def show_data(df):
    bookmark = 0  # Set row reference point
    pd.set_option('display.max_columns', 200)  # Show more data (columns) to the user

    while True:
        # Capture user input and cast to lower and remove leading / trailing space
        display_data = input("\nWould you like to see 5 rows of the raw data? Yes or No\n").lower().strip()
        if display_data not in ['no', 'yes']:
            print("\nYour response is invalid or incorrectly spelled. Try again. \n")
            continue

        if display_data == 'yes':
            while True:
                print(df.iloc[bookmark: bookmark + 5])  # First itteration rows 0-4
                bookmark += 5  # Setup row position for next print portion

                next_five = input("\nWould you like to see 5 more? Yes/No\n").lower().strip()
                if next_five == 'no':
                    display_data = "no"
                    break

        if display_data == "no":
            print("\nAs you wish... Discontinuing raw data presentation...\n")
            break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Determine if dataframe is empty and avoid crashing further logic
        if len(df.index) == 0:
            print("\nYour city, month, day combination yielded no results. Please try again.\n")
            continue
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df, city)  # Missing data on Washington dataset, injecting city param for screening
            show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
