import sys
import os
import requests
from io import BytesIO
from PIL import Image
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from image_types import ImageLink
from mock_data import mock_images_links


storage_path = sys.argv[1]

os.makedirs(storage_path, exist_ok=True)

service = build(
    "customsearch",
    "v1",
    developerKey="AIzaSyCPKV5KpQrEZaQBI6U2Vst8wlRkj0EuYGQ",
)


def load_images_links(query, max_links=200):
    links = []
    offset = 1
    res = dict()

    # return mock_images_links

    while True:
        try:
            res = (
                service.cse()
                .list(q=query, cx="40bfffb8f0aa742b4", searchType="image", start=offset)
                .execute()
            )
        except HttpError as http_err:
            if http_err.status_code != 400:
                print(http_err)
            break

        for item in res["items"]:
            links.append(ImageLink(item["link"], item["fileFormat"]))

        offset += 10
        if offset > max_links:
            break

    print(f"Loaded {(offset-1)} results")

    return links


def get_images_types(image_links):
    unique_types = list(set(item.type for item in image_links))
    return unique_types


def get_images_with_type(image_links, type):
    links_with_type = list(item.link for item in image_links if item.type == type)
    return links_with_type


def load_images(storage_path, links):
    counter = 1
    failed_images = 0
    for img_link in links:
        response = None
        try:
            response = requests.get(img_link.link)
        except Exception as e:
            print(
                f"Error occured during http connection, url - {img_link.link}, error - {e}"
            )
            failed_images += 1
            continue
        if response.status_code != 200:
            print(
                f"Failed to load image {img_link.link}, error code {response.status_code}"
            )
            failed_images += 1
            continue
        image = None
        try:
            image = Image.open(BytesIO(response.content))
        except (IOError, OSError) as e:
            print(f"Ivalid image {img_link.link}, error {e}")
            failed_images += 1
            continue
        if image.mode != "RGB":
            image = image.convert("RGB")

        image.save(os.path.join(storage_path, f"{counter}.jpg"), "JPEG")
        counter += 1

    print(f"Number of failed images - {failed_images}")


def load_seasons_images():
    seasons_queries = [
        ("summer", "summer landscape"),
        ("winter", "winter landscape"),
        ("autumn", "autumn landscape"),
        ("spring", "spring landscape"),
    ]

    for season_query in seasons_queries:
        links = load_images_links(season_query[1])
        season_storage_path = os.path.join(storage_path, season_query[0])
        os.makedirs(season_storage_path, exist_ok=True)

        load_images(season_storage_path, links)


load_seasons_images()
