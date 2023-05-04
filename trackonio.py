#!/usr/bin/env python3

import json
import os
import re
import sys
import uuid
import functools
from datetime import datetime, timedelta
from random import randint

import requests

EMAIL = str(os.environ.get('PERSONIO_USERNAME'))
PASSWORD = str(os.environ.get('PERSONIO_PASSWORD'))
CALENDAR_ID = str(os.environ.get('CALENDAR_ID', '59097'))
STARTING_HOUR = str(os.environ.get('WORK_START_TIME', '08'))
BREAK_HOUR = str(os.environ.get('BREAK_START_TIME', '13'))
WORKING_HOURS = int(os.environ.get('WORK_DURATION', 8))
BREAK_TIME_MINUTES = int(os.environ.get('BREAK_DURATION', 60))
RANDOM_TIMES_DELTA = int(os.environ.get('RANDOM_TIMES_DELTA', 0))
RANDOM_DURATIONS_DELTA = int(os.environ.get('RANDOM_TIMES_DELTA', 0))

LOGIN_URL = "https://trackonio2.personio.de/login/index"
ATTENDANCE_URL = f'https://trackonio2.personio.de/api/v1/attendances/periods'
HOLIDAYS_URL = f'https://trackonio2.personio.de/api/v1/holidays?holiday_calendar_ids[]=' 
ABSENCES_URL = f'https://trackonio2.personio.de/api/v1/employees'

def check_date(dateInput):
    return re.fullmatch(r"\A([\d]{4})-([\d]{2})-([\d]{2})", dateInput)


def generate_attendance(
    date, startingHour, breakHour, workingHours, breakDuration, employeeId, randomTimes, randomDurations):
    # First Record
    startTime = datetime.strptime(f"{date} {startingHour}", "%Y-%m-%d %H")
    breakTime = datetime.strptime(f"{date} {breakHour}", "%Y-%m-%d %H")
    workingDuration = (workingHours) * 60
    
    # Randomize input times and durations
    if randomTimes:
        startTime += timedelta(minutes=randint(-randomTimes, randomTimes))
        breakTime += timedelta(minutes=randint(-randomTimes, randomTimes))
    if randomDurations:
        workingDuration = randint(workingDuration - randomDurations, workingDuration + randomDurations)
        breakDuration = randint(breakDuration - randomDurations, breakDuration + randomDurations)
        
    # Second Record
    startTime2 = breakTime + timedelta(minutes=breakDuration)

    workingDuration2 = int(
        workingDuration - (breakTime - startTime).total_seconds() / 60
    )
    end_time = startTime2 + timedelta(minutes=workingDuration2)

    return [
        {
            "id": str(uuid.uuid1()),
            "start": startTime.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": breakTime.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "comment": "",
            "project_id": None,
            "employee_id": employeeId,
            "activity_id": None,
        },
        {
            "id": str(uuid.uuid1()),
            "start": startTime2.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "comment": "",
            "project_id": None,
            "employee_id": employeeId,
            "activity_id": None,
        },
    ]


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "--help" or not check_date(sys.argv[1]):
        print(
            f"""
            Error. No argument or wrong date format\n\n
            Usage: {__file__} [date]\n
            Note: Date format yyyy-mm-dd \n
            """
        )
        exit()

    attendanceDate = sys.argv[1]

    # Create request session
    session = requests.Session()

    # Login into Personio
    response = session.post(
        LOGIN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"email": EMAIL, "password": PASSWORD},
    )
    if 'XSRF-TOKEN' in response.cookies:
        XSRF_TOKEN=response.cookies['XSRF-TOKEN']
        PROFILE_ID=response.text.split("EMPLOYEE={id:")[1].split("}")[0]
    else:
        print("Failed to login")
        exit()
    
    # Check Working Day
    response = session.get(
        f'{HOLIDAYS_URL}{CALENDAR_ID}&start_date={attendanceDate}&end_date={attendanceDate}'
    )
    isHoliday = len(json.loads(response.text)['data'])

    # Check User Abscense
    response = session.get(
        f'{ABSENCES_URL}/{PROFILE_ID}/absences/types'
    )
    absenceTypes = ','.join(list(map(lambda a : str(a['id']), json.loads(response.text)['data'])))
    response = session.get(
        f'{ABSENCES_URL}/{PROFILE_ID}/absences/periods?filter[startDate]={attendanceDate}&filter[endDate]={attendanceDate}&filter[absenceTypes]={absenceTypes}'
    )
    isAbsence = len(json.loads(response.text)['data'])

    if isHoliday or isAbsence:
        message = 'Not working day'
        print(message)
        exit()

    # Log the attendance
    response = session.post(
        ATTENDANCE_URL,
        headers={'x-csrf-token':XSRF_TOKEN},
        json=generate_attendance(
            attendanceDate,
            STARTING_HOUR,
            BREAK_HOUR,
            WORKING_HOURS,
            BREAK_TIME_MINUTES,
            PROFILE_ID,
            RANDOM_TIMES_DELTA,
            RANDOM_DURATIONS_DELTA
        ),
    )

    data = json.loads(response.text)
    try:
        message = f"Error: {attendanceDate} - {data['error']['message']}"
    except KeyError:
        message = f"Success: attendance on {attendanceDate} registered!"

    print(message)
