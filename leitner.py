import numpy as np
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta


def leitner_dates(row):
    '''
    Use with pandas DataFrame.apply() method to analyze card-by-card user 
    data after a study session. If the user starred a card, the comfort
    level is set back to 0. If the user did not star a card and the 
    comfort level is less than 5, comfort level is raised by 1. In all
    cases next_due is then updated according to comfort level.
    '''
    if (row['is_starred'] == 0) & (row['comfort_level'] < 5):
        row['comfort_level'] += 1
        row = update_next_due(row)
        
    elif (row['is_starred'] == 0) & (row['comfort_level'] == 5):
        row = update_next_due(row)
        
    else:
        row['comfort_level'] = 1
        row = update_next_due(row)
    
    return row


def update_next_due(row):
    
    comfort_dict = {1 : -1, 2 : 2, 3 : 4, 4 : 9, 5 : 14}
    
    next_due = dt.now() + timedelta(days=comfort_dict[row['comfort_level']])
    row['next_due'] = next_due.strftime('%m-%d-%Y, %H:%M')
    return row
