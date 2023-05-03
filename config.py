# Personio credentials
EMAIL = 'carles.llobet@personio.de'
PASSWORD = r'password'
PROFILE_ID = '15446511' # This can be found in your personio profile URL
CALENDAR_ID = '8868' #Barcelona: 59097 / Madrid: 8868

# App configuration
STARTING_HOUR = "08:00"  # Hour you usually start working in the morning
BREAK_HOUR = "13:00"  # Hour you usually take your lunch break
WORKING_HOURS = 8 # Number of worked hours
BREAK_TIME_MINUTES = 60 # Number of break minutes
RANDOM_TIMES_DELTA = 0 # Number of random +/- minutes of start time
RANDOM_DURATIONS_DELTA = 5 # Number of random +/- minutes of durations

# Personio Configuration
LOGIN_URL = "https://trackonio2.personio.de/login/index"
ATTENDANCE_URL = f'https://trackonio2.personio.de/api/v1/attendances/periods'
HOLIDAYS_URL = f'https://trackonio2.personio.de/api/v1/holidays?holiday_calendar_ids[]=' 
ABSENCES_URL = f'https://trackonio2.personio.de/api/v1/employees'