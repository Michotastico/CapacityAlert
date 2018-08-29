## Capacity Alert

Command line interface to easily the checking of available ram and disk.

Is built thinking in integration with [Slack](https://slack.com/) using a webhook integration.

### Use
Help
```shell
$ python main.py --help
Usage: main.py [OPTIONS]

  Program to check the system capacity on RAM and DISK and send alert if is
  lower than certain threshold set by the user.

Options:
  -rp, --ram-percentage TEXT   Percent of total ram
  -rf, --ram-fixed TEXT        Fixed amount of ram
  -dp, --disk-percentage TEXT  Percent of total disk
  -df, --disk-fixed TEXT       Fixed amount of disk
  -sw, --slack-webhook TEXT    Slack webhook
  -sa, --slack-admins TEXT     Slack administrator ids
  --help   
```
Default behaviour sent an alert if the available resource is lower than 1GB
```shell
$ python main.py
[WARNING] LOW AVAILABLE RAM 0.763Gb/11.625Gb
[WARNING] LOW AVAILABLE DISK 0.962Gb/97.709Gb
```
Using a Slack webhook
```shell
$ python main.py -sw https://hooks.slack.com/services/.../.../...
```
Using a Slack webhook and tag multiple users
```shell
$ python main.py -sw https://hooks.slack.com/services/.../.../... -sa user1 -sa user2
```

### LICENSE
MIT