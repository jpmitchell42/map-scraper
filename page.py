import requests
import re
import os
import json
from bs4 import BeautifulSoup
import shutil
from config import Config
from utils.bucket import Bucket
from datetime import datetime
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError


class MapDetails:
    def __init__(self, *args, **kwargs):
        self.page_link = kwargs["page_link"] if "page_link" in kwargs else None
        self.get_page_html()
        self.name = kwargs["name"] if "name" in kwargs else None
        self.price = kwargs["price"] if "price" in kwargs else None
        self.category = kwargs["category"] if "category" in kwargs else None
        self.content_id = kwargs["content_id"] if "content_id" in kwargs else None
        self.image_link = kwargs["image_link"] if "image_link" in kwargs else None
        self.cartographer = kwargs["cartographer"] if "cartographer" in kwargs else None
        self.description = kwargs["description"] if "description" in kwargs else None
        self.publish_date = kwargs["name"] if "name" in kwargs else None
        self.bucket = kwargs["bucket"] if "bucket" in kwargs else None
        self.run_on_init = kwargs["run_on_init"] if "run_on_init" in kwargs else False
        self.run_debug = kwargs["run_debug"] if "run_debug" in kwargs else False
        if self.html_text:
            self.soup = BeautifulSoup(self.html_text, features="html.parser")
            self.read_html()
        self.ddb = kwargs["ddb"] if "ddb" in kwargs else None
        self.table = kwargs["table"] if "table" in kwargs else None
        if self.run_on_init:
            self.full_run()
        if self.run_debug:
            # self.write_details_to_db()
            pass

    def __str__(self):
        s = f"Name:{self.name}\nPrice:{self.price}\nCategory:{self.category}\nLink:{self.image_link}\nid:{self.content_id}"
        return s

    def read_html(self):
        master_dictionary = {}
        head = self.soup.head.find_all("meta")

        self.read_head_tags(head)
        self.read_head_script()
        self.read_info_card()

    def read_head_tags(self, h):
        for i in h:
            content = i.get("content")
            prop = i.get("property")
            if prop == "og:image":
                self.image_link = content
            if prop == "og:title":
                self.name = content
            if prop == "og:description":
                self.description = content

    def read_head_script(self):
        script = self.soup.head.find_all("script")
        # print(script)
        for s in script:
            r = re.search(r"(?<=gtag\(\'event\',\'view_item\',).*(?=\))", s.get_text())
            f = re.search(r"(?<=fbq\(\'track\',\'ViewContent\',).*(?=\))", s.get_text())

            if r:
                try:
                    kv = json.loads(r.group())
                    d = kv["items"][0]
                    # print(d)
                    self.content_id = d["id"]
                    self.price = d["price"]
                except KeyError:
                    pass
            if f:
                try:
                    kv = json.loads(f.group())
                    d = kv["content_category"]
                    self.category = d

                except KeyError:
                    pass

    def read_info_card(self):
        info = self.soup.find_all("div", {"class": "info card"})

        creator = (
            info[0].find_all("div", {"class": "creator"})
            if info and len(info) > 0
            else None
        )
        cart = creator[0].find_all("a") if creator and len(creator) > 0 else None
        self.cartographer = cart[0].text if cart and len(cart) > 0 else None

        issue = (
            info[0].find_all("div", {"class": "issue-place"})
            if info and len(info) > 0
            else None
        )

        pub_info = (
            issue[0].find_all("div", {"class": "value"})
            if issue and len(issue) > 0
            else None
        )

        pub_string = pub_info[0].text.strip()

        self.pub_loc = pub_string.split("/")[0]
        self.publish_date = pub_string.split("/")[1]

    def write_details_to_db(self):
        entry = {
            "name": self.name,
            "cartographer": self.cartographer,
            "price": self.price,
            "image_link": self.image_link,
            "blr_id": self.content_id,
            "description": self.description,
            "publish_date": self.publish_date,
            "date_downloaded": str(datetime.utcnow()),
            "publish_location": self.pub_loc,
            "category": self.category,
        }
        self.entry = entry
        try:

            self.table.put_item(Item=entry)
        except ClientError as e:
            print(e)
            print(self.entry)

    def get_page_html(self):
        r = requests.get(self.page_link)
        s = r.status_code
        if s == 200:
            self.html_text = r.content

            return r.content

    def save_image_to_s3(self):
        r = requests.get(self.image_link, stream=True)
        s3_name = self.image_link.split("/")[-1]
        filetype = s3_name.split(".")[-1]

        with open(s3_name, "wb") as out_file:
            shutil.copyfileobj(r.raw, out_file)
        try:
            self.bucket.bucket.upload_file(s3_name, f"{s3_name}")
            os.remove(s3_name)
        except S3UploadFailedError as e:
            print(e)
            print(f"Saved file {s3_name} to folder")

        del r

    def full_run(self):
        self.write_details_to_db()
        self.save_image_to_s3()

