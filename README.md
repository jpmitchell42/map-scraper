### Map Scraper

I wrote this to build out a really specific Django/React thing I'm working on which relies on
images of maps being stored as well as their associated information.

To do this I scarped the website:https://www.raremaps.com

What this does, if its linked up to an AWS S3 and DynamoDB. This scrapes that page for the image and uploads it to S3 and the associated date to postgres. Not super complicated.

For testing purposes in app.py you can put the link to any map on the website and it will pull down the data. The plan is to run this on an AWS Lambda in the future, once everythings in place.

## Steps to run

1. Have Docker
2. If you want to run this actually it will require a DynamoDB table and an S3 bucket. Add the credentials to a user with proper permissions and names to a .env file

- SECRET_KEY=\<aws secret key>
- ACCESS_KEY=\<aws access key>
- S3_BUCKET=\<bucket name>
- TABLE_NAME=\<table name>

3. Run docker-compose up --build
