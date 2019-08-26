### Map Scraper

I wrote this to build out a really specific Django/React thing I'm working on which relies on
images of maps being stored as well as their associated information.

To do this I scarped the website:https://www.raremaps.com

What this does, if its linked up to an AWS S3 and DynamoDB. This scrapes that page for the image and uploads it to S3 and the associated date to postgres. Not super complicated.

For testing purposes in app.py you can put the link to any map on the website and it will pull down the data. The plan is to run this on an AWS Lambda in the future, once everythings in place.

## Steps to run

1. Have Python 3.6 or greater (f strings)
2.
