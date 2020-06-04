import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
import plotly.graph_objects as go
import calendar


def get_viz_user_info(user_id):
  """Function to call necessary information from app database"""
  database_location = DATABASE_URL
  connection = sqlite3.connect(database_location)
  cursor = connection.cursor()
  results = cursor.execute(f"SELECT created_at FROM decks WHERE user_id = {user_id}")
  #gets all dates from the 'decks' table for the given user

  dates_created_decks = []
  for timestamp in results:
    timestamp = timestamp.date()
    dates_created_decks.append(timestamp)
  #adds each of these dates to a list

  dates_created_decks.sort()
  results = cursor.execute(f"SELECT session_start FROM sessions WHERE (user_id = {user_id}) AND (total_looked_at > 0)")
  #gets all dates from 'sessions' table where the given user logged and viewed at least one card

  dates_viewed_cards = []
  for timestamp in results:
    timestamp = timestamp.date()
    dates_viewed_cards.append(timestamp)
  #adds each of these dates to a list
  return dates_created_deck, dates_viewed_cards

def week_of_month(row):
  """Function to convert day of month to week of month"""
  day = (row['From_1st_Monday']) + 1
  #based on index of dataframe, which counts from zero
  if day <=7:
    return '1st Week'
  elif 7 < day <= 14:
    return '2nd Week'
  elif 14 < day <=21:
    return '3rd Week'
  elif 21 < day <= 28:
    return '4th Week'
  elif 28 < day <= 35:
    return '5th Week'
  #this is greater than 31 to account for padded data added at top of dataframe
  else:
    return ''
  #this prevents a month from having six weeks if the 1st of the month is late
  #in the week, instead the graph displays those days but doesn't label them

def get_viz(month_to_show=datetime.now().month, year_to_show=datetime.now().year):
  """Function to show calendar heatmap for user interaction with the app. Takes in
  a month to show as an integer between 1 and 12, and a year as a four-digit 
  integer between 0000 and 9999. Defaults to current month and year if
  no date is provided."""

  all_dates = pd.date_range('1/15/2019', periods=120, freq='D')
  dates_created_decks = np.random.choice(all_dates, 25)
  dates_viewed_cards = np.random.choice(all_dates, 250)
  #this is just creating the dummy data to test the code, creates two lists of dates randomly
  #to be replaced with calls to get_viz_user_info once database is ready

  dates_created_decks.sort()
  dates_viewed_cards.sort()
  #sorts the two lists in date order

  dates = {}
  for d in dates_created_decks:
    if d in dates_viewed_cards:
      dates[d] = 2
  #if a date is in both "viewed" and "created" lists, that's two events
    else:
      dates[d] = 1
  #if a date is only in "created", that's one event
  for d in dates_viewed_cards:
    if d not in dates_created_decks:
      dates[d] = 1
  #if a date is in "created" and not in "viewed", that's one event


  if dates_created_decks[0] <= dates_viewed_cards[0]:
    #start with the first dates from the "created" list if those are first
    year = dates_created_decks[0].astype('M8[ms]').astype('O').year
    #this line converts the datetime64 objects to datetime objects
    #may need to change once we are dealing with the pulled database info
    start_day = datetime(year=year, month=1, day=1)
    #first day of visualization data is the 1st of the month the user started
    next_month = datetime.now().month + 1
    year = datetime.now().year
    end_day = datetime(year=year, month=next_month, day=1)
    #sets the last day of visualization data as the first of next month
    #ensures all days of current month are included even if they haven't happened yet
    all_days = pd.Series(pd.date_range(start=start_day, end=end_day))
    #creates a dataframe of every day between each of those dates
  else:
    #same as above but starts with "viewed" list
    year = dates_viewed_cards[0].astype('M8[ms]').astype('O').year
    start_day = datetime(year=year, month=1, day=1)
    next_month = datetime.now().month + 1
    year = datetime.now().year
    end_day = datetime(year=year, month=next_month, day=1)
    all_days = pd.Series(pd.date_range(start=start_day, end=end_day))

  def create_events(date_obj):
    """Function to add use events to dates dataframe. Nested to be able to access
    dates dictionary."""
    keys = list(dates.keys())
    #all the dates in the dictionary as a list
    for i in range(len(keys)):
      keys[i] = str(keys[i])[:10]
    #converts all the datetime64 keys to strings containing just year-month-day
    #in the format %Y-%m-%d
    str_date_obj = str(date_obj)[:10]
    #converts this timestamp object to a string of the same format so they can be compared
    date_obj = pd.Timestamp.to_datetime64(date_obj)
    #converts the Pandas Timestamp object to a native Python datetime64 object
    if str_date_obj in keys:
      return dates[date_obj]
    #if the date is in the dictionary keys, return the number of events from the dict
    else:
      return 0


  used_app = pd.DataFrame()
  used_app['Date'] = all_days
  #uses date series from above as the 'Date' column in the dataframe
  used_app['Events'] = used_app['Date'].apply(create_events)
  #applies function to the 'Events' column 

  used_app['Month'] = used_app['Date'].apply(lambda x: x.month)
  used_app['Day'] = used_app['Date'].apply(lambda x: x.day)
  used_app['Weekday'] = used_app['Date'].apply(lambda x: x.strftime('%A'))
  used_app['Day_Numeric'] = used_app['Date'].apply(lambda x: int(x.weekday()))
  used_app['Year'] = used_app['Date'].apply(lambda x: x.year)
  #creates separate columns for the month, day of the month,
  #weekday, numeric day of the week, and year for each date in the range 

  current_month_used = used_app[used_app['Month'] == month_to_show]
  current_month_used = current_month_used[current_month_used['Year'] == year_to_show]
  #creates new dataframe containing only the data from the relevant month

  current_month_used = current_month_used.sort_values(by=['Day'])

  weekdays = list(calendar.day_name)
  #this creates a list of weekday names
  while current_month_used['Weekday'].iloc[0] != 'Monday':
  #if the first day of the month given isn't a Monday, this will run until there
  #is dummy data in the dataframe that starts with a Monday
    day_numeric = int(current_month_used['Day_Numeric'].iloc[0]) - 1
    #gets the numeric weekday of the day before the first in the dataframe
    weekday = weekdays[day_numeric]
    #gets name for the new weekday
    new_top_row = pd.DataFrame([[np.NaN, np.NaN, month_to_show, 0, weekday, day_numeric, np.NaN, np.NaN]], 
                              columns=['Date', 'Events', 'Month', 'Day', 'Weekday', 'Day_Numeric', 'Year'])
    #creates a dummy row that contains only the month, weekday, and numeric day of the week
    current_month_used = pd.concat([new_top_row, current_month_used])
    #adds this dummy data row to the dataframe
  current_month_used = current_month_used.reset_index(drop=True)
  #resets the current_month_used dataframe index to start at 0
  current_month_used['From_1st_Monday'] = current_month_used.index
  #creates a new column that is the index values
  current_month_used['Week'] = current_month_used.apply(week_of_month, axis=1)
  #runs dataframe through week_of_month function, applies this to new column
  figure = go.Figure(data=go.Heatmap(z=current_month_used['Events'], x=current_month_used['Weekday'], 
                                    y=current_month_used['Week'], 
                                    colorscale=
                                    [[0, 'rgb(152,251,152)'],  
                                      [1, 'rgb(0,100,0)']], connectgaps=False, 
                                      showscale=False, xgap=3, ygap=3, 
                                    autocolorscale=False, hoverongaps=False
                                    ))
  #creates a heatmap comparing the number of events (z) on each day, with the 
  #weekday as the x-axis and week of the month as the y-axis. Colorscale runs from 
  #pale green to dark forest green. No data shown for NaN values on hover,
  #and NaN values are not averaged out (leaves a blank space for days with no data)
  figure.update_layout(autosize=False, width=1200, height=800,
          title={
          'text': "Days Used App This Month",
          'x':0.5,
          'xanchor': 'center',
          'yanchor': 'top',
          'pad': {'t':10},},
          xaxis_type='category', 
          yaxis_type='category',
          plot_bgcolor='rgb(225,255,225)')
  return figure.write_html('templates/heatmap.html')

