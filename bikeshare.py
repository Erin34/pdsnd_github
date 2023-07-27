import time
import pandas as pd
import numpy as np
import datetime

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities= ['chicago', 'new york city', 'washington']
        city= input("\n Which city would you like to explore? (Chicago, New york City, Washington) \n").lower()
        if city in cities:
            break
        else: 
            print("\n Invalid. Pleae enter another city.")        


    # get user input for month (all, january, february, ... , june)
    while True:
        MONTHS = ['January','February','March','April','May','June','all']
        month= input('''Which month would you like to explore? Enter 'all','January', 'Feburary', 'March', 'April', 'May', or 'June':''').lower()
        if month == 'all':
            print('\nLets get the data for all months.')
            break
        elif month in map(str.lower,MONTHS):
            print('\nLets get data for {}.'.format(month.title()))
            break
        else: 
            print('\nInvalid. Pleae enter another month.\n')     
   
    #TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        DAYS= ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','all']
        day= input('''Which day would you like to explore? Enter 'all', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday':''').lower()
        if day == 'all':
            print('\nLets get the data for all days.')
            break
        elif day in map(str.lower,DAYS):
            print('\nLets get the data for all {}s.'.format(day.title()))
            break
        else: 
            print("\nInvalid. Pleae enter another day.") 
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
    # Load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time Column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    #filter by month if applicable
    if month != 'all' and day == 'all':      
       mdf = df[(df['month']==month.title())]
       return mdf
       
    #filter by day of week if applicable
    elif day != 'all' and month == 'all':
        ddf = df[(df['day_of_week']==day.title())]
        return ddf
    
    #filter by month and day
    elif month != 'all' and day != 'all':
        mddf = df[(df['month']==month.title()) & (df['day_of_week']==day.title())]
        return mddf
    
    #No filter 
    else:  
        return df
   
def totals_no_filter(df):
    
    print('\nNo filter? Lets look at overall...\n')
    start_time = time.time()
    
    #calculate trips per month
    Total_month = df['month'].value_counts()
    print('The following shows the trip count per month:\n')
    for k,v in Total_month.items():
        print('{:10} : {:,}'.format(k, v))
        
    #calculate trips per days
    Total_day = df['day_of_week'].value_counts()
    print('The following shows the trip count per day:\n')
    for k,v in Total_day.items():
        print('{:10} : {:,}'.format(k, v))
        

def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month =='all':
        popular_month = df['month'].mode()[0]
        #months= ['January', 'February', 'March', 'April', 'May', 'June']
        #popular_month= months[popular_month-1]             
        print("The Most Common month is", popular_month)
    
    # TO DO: display the most common day of week
    if day== 'all':
        popular_day = df['day_of_week'].mode()[0]
        print("The Most Common day is", popular_day)



    # TO DO: display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    popular_hour=df['Start Hour'].mode()[0]
    print("The Most Common Start Hour is {}:00 hrs".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station= df['Start Station'].mode()[0]
    print("The most commonly used start station is {}".format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station= df['End Station'].mode()[0]
    print("The most commonly used end station is {}".format(popular_end_station))

    # TO DO: display most frequent combination of start station and end station trip
    df['combination']=df['Start Station']+ " " + "to" + " " + df['End Station']
    popular_com= df['combination'].mode()[0]
    print("The most frequent combination of start and end station trip is {}".format(popular_com))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time=df['Trip Duration'].sum()
    print('The total time of all trips in this data set is {:,.0f} seconds.'.format(total_travel_time))
    print('This is {:,.2f} minutes.'.format(total_travel_time/60))
    print('This is {:,.2f} hours.'.format(total_travel_time/60/60))
    print('This is {:,.2f} days.'.format(total_travel_time/60/60/24))
                         
    # TO DO: display mean travel time
    average_travel_time=df['Trip Duration'].mean()
    print('The average time of all trips in this data set is {:,.2f} seconds.'.format(average_travel_time))
    print('This is {:,.2f} minutes.'.format(average_travel_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

                         
def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\n The user types are:\n",user_types)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)    
  
def raw_data(df):
    """  Display raw data at the users request. """ 
    
    while True:
        response=['yes','no']
        option= input("Would you like to see individual trip data? Enter 'yes' or 'no'\n").lower()
        if option in response:
           if option=='yes':
               start=0
               end=5
               data = df.iloc[start:end,:9]
               print(data)
           break
        else:
            print("Please enter a valid response")
    if option=='yes':
            while True:
                 option_2= input("Would you like to view more trip data? Type 'yes' or 'no'\n").lower()
                 if option_2 in response:
                     if option_2=='yes':
                        start+=5
                        end+=5
                        data = df.iloc[start:end,:9]
                        print(data)
                     else:
                        break
                 else:
                    Print("Please enter a valid response")
     
def main():
   while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)  
        if month == 'all' and day == 'all':
            totals_no_filter(df)        
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
                         
if __name__== "__main__":
    main()
