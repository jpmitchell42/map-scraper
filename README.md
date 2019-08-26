# Map Scraper

I wrote this to build out a really specific Django/React thing I'm working on which relies on
images of maps being stored as well as their associated information.

To do this I scarped the website:https://www.raremaps.com

What this does, if its linked up to an AWS S3 and DynamoDB. This scrapes that page for the image and uploads it to S3 and the associated date to postgres. Not super complicated.

For testing purposes in app.py you can put the link to any map on the website and it will pull down the data. The plan is to run this on an AWS Lambda in the future, once everythings in place.

## Steps to run

1. Have Docker
2. a. (easiest) If you just want to run without connection run `touch .env`
3. b. (harder) If you want to run this actually it will require a DynamoDB table and an S3 bucket. Add the credentials to a user with proper permissions and names to a .env file

```
SECRET_KEY=<aws secret key>
ACCESS_KEY=<aws access key>
S3_BUCKET=<bucket name>
TABLE_NAME=<table name>
```

4. Run `docker-compose up --build`

5. You can change the line 6 in the docker-compose.yml file. It can take one argument that is a new url:

```
   command: python3 app.py https://www.raremaps.com/gallery/detail/55035/an-exact-mapp-of-china-being-faithfully-copied-from-one-bro-de-smedo-webb

```

will get that new url. Alternatively you can change it in app.py
