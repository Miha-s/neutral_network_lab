# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
from scrapy.exceptions import DropItem
from PIL import Image
from io import BytesIO
import os
import scrapy
from scrapy.pipelines.files import FileException
from scrapy.pipelines.images import ImagesPipeline


class InternalImagePipeline(ImagesPipeline):
    headers = {
        # "Host": "i.redd.it",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
    }

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        url = adapter.get("url")
        if not url:
            raise DropItem("Failed to retrieve image url")
        if not url.endswith((".jpg", ".png", ".jpeg")):
            raise DropItem("Not image format")

        yield scrapy.Request(url, headers=self.headers)

    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        url = adapter.get("url")
        tag = adapter.get("tag")
        if not url:
            raise DropItem("Failed to retrieve image url")
        if not tag:
            raise DropItem(f"Failed to retrieve image tag {url}")

        filename = url.split("/")[-1].split(".")[0]
        path = os.path.join(tag, filename + ".jpg")
        return path

    def item_completed(self, results, item, info):
        image_paths = [x["path"] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
