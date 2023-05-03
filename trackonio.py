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

try:
    from config import (
        EMAIL,
        PASSWORD,
        PROFILE_ID,
        CALENDAR_ID,
        STARTING_HOUR,
        BREAK_HOUR,
        WORKING_HOURS,
        BREAK_TIME_MINUTES,
        LOGIN_URL,
        ATTENDANCE_URL,
        HOLIDAYS_URL, 
        ABSENCES_URL,
        RANDOM_TIMES_DELTA,
        RANDOM_DURATIONS_DELTA
    )

except ImportError:
    print("WARNING: no config.py found. Please RTFM!")
    exit()

def _extract_csrf_token(self, html):
        pattern = re.compile(r'name="_csrf_token" value="(\w+)"')
        match = pattern.search(html)
        if match is None:
            return None
        return match.group(1)

def check_date(dateInput):
    return re.fullmatch(r"\A([\d]{4})-([\d]{2})-([\d]{2})", dateInput)


def generate_attendance(
    date, startingHour, breakHour, workingHours, breakDuration, employeeId, randomTimes, randomDurations):
    # First Record
    startTime = datetime.strptime(f"{date} {startingHour}", "%Y-%m-%d %H:%M")
    breakTime = datetime.strptime(f"{date} {breakHour}", "%Y-%m-%d %H:%M")
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

    attendance_date = sys.argv[1]

    # Create request session
    session = requests.Session()

    # Login into Personio
    response = session.post(
        LOGIN_URL,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"email": EMAIL, "password": PASSWORD},
    )
    XSRF_TOKEN=response.cookies['XSRF-TOKEN']

    # Check Working Day
    response = session.get(
        f'{HOLIDAYS_URL}{CALENDAR_ID}&start_date={attendance_date}&end_date={attendance_date}'
    )
    isHoliday = len(json.loads(response.text)['data'])

    # Check User Abscense
    response = session.get(
        f'{ABSENCES_URL}/{PROFILE_ID}/absences/types'
    )
    absenceTypes = ','.join(list(map(lambda a : str(a['id']), json.loads(response.text)['data'])))
    response = session.get(
        f'{ABSENCES_URL}/{PROFILE_ID}/absences/periods?filter[startDate]={attendance_date}&filter[endDate]={attendance_date}&filter[absenceTypes]={absenceTypes}'
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
            attendance_date,
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
        message = f"Error: {attendance_date} - {data['error']['message']}"
    except KeyError:
        message = f"Success: attendance on {attendance_date} registered!"

    print(message)
