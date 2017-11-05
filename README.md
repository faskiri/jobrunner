Overview
--------
Simple cron based scheduler that can be used to ensure that an external program can be run per the specified frequency

Usage
-----
Add the following to cron
*/5 * * * * cd ~/work/python/scheduler && python -m jobrunner
