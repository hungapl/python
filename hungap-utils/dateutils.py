import pytz
import datetime
import pandas as pd

# Encapsulates helper method (or variables in the future) for timezone related constructions and conversions
class MyTimeZone:
    
    # Initialise with a valid time zone name - i.e. the local time zone
    def __init__(self, tz_name):
        self.tz = pytz.timezone(tz_name)

    # Change timezone of a panda series to local time zone
    def series_as_local_time(self, d):
        return pd.to_datetime(d).dt.tz_localize(self.tz)

    # Create a new datetime object in local time
    def local_time(self, year, month, day, hour, minute):
        return self.tz.localize(datetime.datetime(year, month, day, hour, minute))
    
