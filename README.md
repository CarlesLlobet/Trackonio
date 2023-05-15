# Trackonio

This tool lets you automatically track working time to your personio Attendance table.

## Requirements
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/get-started/08_using_compose/#install-docker-compose)

## Getting Started
### Configuration

The only configuration required in order to get started is to create a .env file with your preferred authentication (`PERSONIO_COOKIE` or `PERSONIO_USERNAME` & `PERSONIO_PASSWORD` ). 

If authenticating with Cookie, Trackonio will try to refresh the cookie in order to keep the session alive.

Therefore, the minimal configuration can be as easy as:
```
$ echo "PERSONIO_COOKIE=eyJpdiI6IkY1TGFieUJUeHc..." > .env
```

The default configuration will assume you work for personio.personio.de and create everyday at 9:00 AM a track record of that day, with two entries without randomization:
* One from 8 to 13 (pre-break)
* One from 14 to 17 (after-break)

However, you can configure many more variables through the .env file, and Trackonio will take care of the rest.
Here are the different variables you can modify:

> - `PERSONIO_HOST`: The host of your personio instance, usually companyname.personio.de (_e.g: acme.personio.de_)
> - `PERSONIO_USERNAME`: Your Personio username (_e.g: name.surname<span>@</span>company.com_)
> - `PERSONIO_PASSWORD`: Your Personio password (_e.g: mySuperStrongPassword!_)
> - `PERSONIO_COOKIE`: Your Personio session cookie (_e.g: eyJpdiI6IkY1TGFieUJUeHc..._)
> - `CALENDAR_ID`: Personio Public Holidays Calendar assigned to your office (_e.g: #Barcelona:59097 & Madrid:8868_)
> - `WORK_START_TIME`: Time you want to track as start of work, in 24h format [00-23]. Double digit with 0 padding if neccessary! (_e.g: 08_)
> - `WORK_DURATION`: Work duration in hours (_e.g: 8_)
> - `BREAK_START_TIME`: Time you want to track as start of your break, in 24h format [00-23]. Double digit with 0 padding if neccessary! (_e.g: 13_)
> - `BREAK_DURATION`: Work duration in minutes (_e.g: 60_)
> - `RANDOM_TIMES_DELTA`: Number of random +/- minutes of start time (_e.g: 5_)
> - `RANDOM_DURATIONS_DELTA`: Number of random +/- minutes of durations (_e.g: 15_)

### Usage

#### Automatic tracking
To start using this solution after configuring it at your disguise, you just have to execute:

```
$ docker-compose up -d
```

#### Manual tracking
If you want to create manual entries for a specific reason (such as having worked extra time a specific day), the solution can also be called Ad-Hoc.
In order to use it, you just have to call it with the desired date like in the example below:
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
