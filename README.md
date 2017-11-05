# Overview
Simple cron based scheduler that can be used to ensure that an external program can be run per the specified frequency

This is useful when you want to run some script at a frequency till it is successful. i.e. you want to run a daily
backup, but the script is not successful everytime you run (e.g. no network). In such cases, you want to ensure that
the script is able to run succesfully at least once every day and you want to keep trying till then.

For this scheme to work, you need the script to fail with a non-0 exit code if it wasnt succesful, else exit with 0
status

# Usage
## Job Configuration
INI based configuration as follows
```
[sync-mbld]
path: ~/usr/local/bin/sync-nas -mbld
frequency: daily

[sync-fd]
path: ~/usr/local/bin/sync-nas -fd
frequency: daily
```
## Adding Cron
Add the following to cron
```shell
$ crontab -e
*/5 * * * * cd ~/work/python/jobrunner && python -m jobrunner
```
