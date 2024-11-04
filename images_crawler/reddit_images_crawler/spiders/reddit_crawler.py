import scrapy
from reddit_images_crawler.items import ImageItem


class RedditSpider(scrapy.Spider):
    name = "old.reddit.com"
    # allowed_domains = ["old.reddit.com"]

    def start_requests(self):
        subreddits = self.settings.getdict("SUBREDDITS")
        for key in subreddits.keys():
            for subreddit in subreddits[key]:
                print(subreddit)
                if isinstance(subreddit, str):
                    yield scrapy.Request(
                        url=f"https://old.reddit.com/r/{subreddit}/new/",
                        callback=self.parse,
                        cb_kwargs={"tag": key},
                    )
                else:
                    only_key = list(subreddit.keys())[0]
                    yield scrapy.Request(
                        url=f"https://old.reddit.com/r/{only_key}/search?q={subreddit[only_key]}&restrict_sr=on",
                        callback=self.parse,
                        cb_kwargs={"tag": key},
                    )

    def parse(self, response, tag):
        load_only_thumbnail = self.settings.get("LOAD_ONLY_THUMBNAIL")
        query = ""
        if load_only_thumbnail:
            query = "a.thumbnail img::attr(src)"
        else:
            query = "a.thumbnail::attr(href)"

        for url in response.css(query).getall():
            if not url.startswith("https:"):
                url = "https:" + url
            image = ImageItem(url=url, tag=tag)
            yield image

        next_url = response.css("a[rel='nofollow next']::attr(href)").get()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse, cb_kwargs={"tag": tag})
