# Trackonio
===========

This tool lets you automatically track working time to your personio Attendance table.

## Requirements
- Docker
- Docker-compose

## Getting Started
### Configuration
You can configure your docker-compose file by setting up the necessary environment variables before deploying the container.
Here are the different variables you can modify (note that the first two are mandatory in order to authenticate, the rest are optional to modify the default value):

- PERSONIO_USERNAME: Your Personio username (e.g: name.surname@company.com)
- PERSONIO_PASSWORD: Your Personio password (e.g: mySuperStrongPassword!)
- CALENDAR_ID: Personio Public Holidays Calendar assigned to your office (e.g: #Barcelona:59097 & Madrid:8868)
- WORK_START_TIME: Time you want to track as start of work, in 24h format [00-23]. Double digit with 0 padding if neccessary! (e.g: 08)
- WORK_DURATION: Work duration in hours (e.g: 8)
- BREAK_START_TIME: Time you want to track as start of your break, in 24h format [00-23]. Double digit with 0 padding if neccessary! (e.g: 13)
- BREAK_DURATION: Work duration in minutes (e.g: 60)
- RANDOM_TIMES_DELTA: Number of random +/- minutes of start time (e.g: 5)
- RANDOM_DURATIONS_DELTA: Number of random +/- minutes of durations (e.g: 15)


The default configuration will create everyday at 9:00 AM a track record of that day, with two entries without randomization:
* One from 8 to 13 (pre-break)
* One from 14 to 17 (after-break)

### Usage

#### Automatic tracking
To start using this solution after configuring it at your disguise, you just have to execute:
`$ docker-compose up -d`

#### Manual tracking
If you want to create manual entries for a specific reason (such as having worked extra time a specific day), the solution can also be called Ad-Hoc.
In order to use it, you just have to call it with the desired date like below:
```
$ docker exec -it trackonio python trackonio.py 2023-05-21
```

## Built With

* [Python](https://www.python.org/) - The programming language that lets you work quickly and integrate systems more effectively.

## Authors

* **Carles Llobet** - *Complete work* - [Github](https://github.com/CarlesLlobet)

See also the list of [contributors](https://github.com/CarlesLlobet/Trackonio/contributors) who participated in this project.

## Acknowledgments

* Project inspired by https://github.com/RindusIoTJam/personio-timelogger
