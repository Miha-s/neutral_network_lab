# Running a crawler
To run a crawler use command
```
scrapy crawl old.reddit.com
```

You can set storage directory via IMAGES_STORE parameter, or change it in settings.py
```
scrapy crawl old.reddit.com -s IMAGES_STORE=./storage
```

To be able to save and later continue scrolls, you need to tell teh directory, where the crawler will save its state
```
scrapy crawl old.reddit.com -s JOBDIR=crawls/reddit_spider
```