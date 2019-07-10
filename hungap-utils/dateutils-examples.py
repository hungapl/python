import datetime

import MyTimeZone
tz = MyTimeZone("US/Pacific")

# Using MyTimeZone.series_as_local_time()
df = pd.DataFrame({'time':[datetime.datetime.now()]})
df.time = tz.series_as_local_time(df.time)
print(df.time)

# Using MyTimeZone.local_time()
print(tz.local_time(2018, 6, 7, 16, 0))
