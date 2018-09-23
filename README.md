## download and parse html pages from LUBW and City of Stuttgart

### run downloader

```
docker-compose run main download
```


### run parsers

```
docker-compose run main parse
```


### (my) crontab

```
17 * * * * ~/klima/cron_downloader.sh > /dev/null 2>&1
```


### development

#### run tests

```
docker-compose run main tests
```

