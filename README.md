# Trackonio

This tool lets you automatically track working time to your personio Attendance table.

<a href="https://www.buymeacoffee.com/carlesllobet" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Requirements
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/get-started/08_using_compose/#install-docker-compose)

## Getting Started
### Configuration

The only configuration required in order to get started is to create a .env file with your preferred authentication (`PERSONIO_COOKIE` or `PERSONIO_USERNAME` & `PERSONIO_PASSWORD` ). 

If authenticating with Cookie, Trackonio will try to refresh the cookie in order to keep the session alive. For this reason, by default it will wait for 1 minute to execute, making sure next iteration will happen before 24h since last request.
This won't represent any issue in automated deployments, but if you want to manually track an entry, make sure to include the `-f`/`--fast` parameter for a faster execution.

Therefore, the minimal configuration can be as easy as:
```
echo "PERSONIO_COOKIE=eyJpdiI6IkY1TGFieUJUeHc..." > .env
```

The default configuration will assume you work for personio.personio.de and create everyday at 9:00 AM a track record of that day, with two entries without randomization:
* One from 9 to 13 (pre-break)
* One from 14 to 18 (after-break)

However, you can configure many more variables through the .env file, and Trackonio will take care of the rest.
Here are the different variables you can modify:

- `PERSONIO_HOST`: The host of your personio instance, usually companyname.personio.de (_e.g: acme.personio.de_)
- `PERSONIO_USERNAME`: Your Personio username (_e.g: name.surname<span>@</span>company.com_)
- `PERSONIO_PASSWORD`: Your Personio password (_e.g: mySuperStrongPassword!_)
- `PERSONIO_COOKIE`: Your Personio session cookie (_e.g: eyJpdiI6IkY1TGFieUJUeHc..._)
- `CALENDAR_ID`: Personio Public Holidays Calendar assigned to your office (_e.g: #Barcelona:59097 & Madrid:8868_)
- `WORK_START_TIME`: Time you want to track as start of work, in 24h format [00-23]. Double digit with 0 padding if neccessary! (_e.g: 09_)
- `WORK_DURATION`: Work duration in hours (_e.g: 8_)
- `WORK_SATURDAY`: Whether you work on Saturdays and want Saturday to be tracked
- `WORK_SUNDAY`: Whether you work on Sundays and want Sunday to be tracked
- `BREAK_START_TIME`: Time you want to track as start of your break, in 24h format [00-23]. Double digit with 0 padding if neccessary! (_e.g: 13_)
- `BREAK_DURATION`: Work duration in minutes, set to 0 if no break (_e.g: 60_)
- `RANDOM_TIMES_DELTA`: Number of random +/- minutes of start time (_e.g: 5_)
- `RANDOM_DURATIONS_DELTA`: Number of random +/- minutes of durations (_e.g: 15_)

### Usage

#### One-Time tracking
If you don't want to use the solution automatic attendance and rather only track once manually, you can simply execute:
```
docker run -it --name trackonio -e PERSONIO_COOKIE='eyJpdiI...' krowone9/trackonio python trackonio.py 2023-05-24 -f; docker rm trackonio
```

And add any configuration variables from above you need as environment variables with the flag `-e`.

If you want to track a whole period of time, you may also execute something like below:
```
export d=2023-05-01 endDate=2023-06-01
export cookie='eyJpdiI...'
while [ "$(date -d "$d" +%Y%m%d)" -lt "$(date -d "$endDate" +%Y%m%d)" ]; do docker run -it --name trackonio -e PERSONIO_COOKIE=$cookie krowone9/trackonio python trackonio.py $d -f; docker rm trackonio; d=$(date -I -d "$d + 1 day"); done
```

This example would track all May 2023 (from 1st day to 31st day).

*Note: In Mac OSX, date does not allow parameter -d. In order to fix so, substitute the `date` command for `gdate` like below:*
```
brew install coreutils
export d=2023-05-01 endDate=2023-06-01
export cookie='eyJpdiI...'
while [ "$(gdate -d "$d" +%Y%m%d)" -lt "$(gdate -d "$endDate" +%Y%m%d)" ]; do docker run -it --name trackonio -e PERSONIO_COOKIE=$cookie krowone9/trackonio python trackonio.py $d -f; docker rm trackonio; d=$(gdate -I -d "$d + 1 day"); done
```

#### Automatic tracking
To start using the whole power (automatic tracking) of this solution after configuring it at your disguise, you just have to execute:

```
docker-compose up -d
```

Since the hour at which the time entry will be created depends on a cronjob, it has to be configured at image build time.
Therefore, if you want to configure a different time (`9:00 AM` by default), you should pull the whole github repository and build the image from there.
The build format is commented within the docker-compose file, so just uncomment those lines and remove/comment the image one.

#### Manual tracking
If you already have your container in place, but you need to create manual entries for a specific reason (such as having worked extra time a specific day), the solution can also be called Ad-Hoc.
To do so, you just have to call it with the desired date like in the example below:

```
docker exec -it trackonio python trackonio.py 2023-05-21 -f
```

If you want to track a whole period of time, you may also execute something like below:
```
export d=2023-05-01 endDate=2023-06-01
while [ "$(date -d "$d" +%Y%m%d)" -lt "$(date -d "$endDate" +%Y%m%d)" ]; do docker exec -it trackonio python trackonio.py $d -f; d=$(date -I -d "$d + 1 day"); done
```

This example would track all May 2023 (from 1st day to 31st day).

## Built With

* [Python](https://www.python.org/) - The programming language that lets you work quickly and integrate systems more effectively.

## Authors

* **Carles Llobet** - *Complete work* - [Github](https://github.com/CarlesLlobet)

See also the list of [contributors](https://github.com/CarlesLlobet/Trackonio/contributors) who participated in this project.

## Acknowledgments

* Project inspired by https://github.com/RindusIoTJam/personio-timelogger
