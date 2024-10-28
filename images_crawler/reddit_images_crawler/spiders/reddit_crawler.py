import scrapy
from reddit_images_crawler.items import ImageItem


class RedditSpider(scrapy.Spider):
    name = "old.reddit.com"
    # allowed_domains = ["old.reddit.com"]

    def start_requests(self):
        subreddits = self.settings.getdict("SUBREDDITS")
        for key in subreddits.keys():
            for subreddit in subreddits[key]:
                yield scrapy.Request(
                    url=f"https://old.reddit.com/r/{subreddit}/new/",
                    callback=self.parse,
                    cb_kwargs={"tag": key},
                )

    def parse(self, response, tag):
        for url in response.css("a.thumbnail::attr(href)").getall():
            image = ImageItem(url=url, tag=tag)
            yield image

        next_url = response.css("span.next-button a::attr(href)").get()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse, cb_kwargs={"tag": tag})
