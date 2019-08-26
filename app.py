from config import Config
import boto3
import requests
from page import MapDetails
from utils.bucket import Bucket
import sys
from botocore.exceptions import NoCredentialsError


def create_app_test():

    ddb = boto3.resource("dynamodb", region_name="us-east-1",
                         aws_secret_access_key=Config.SECRET_KEY, aws_access_key_id=Config.ACCESS_KEY)
    # except NoCredentialsError as e:
    # print('No credentials but continuing for proof of concept')
    table = ddb.Table(Config.TABLE_NAME)
    b = Bucket()

    if len(sys.argv) > 1:
        URL_TO_SCRAPE = sys.argv[1]
    else:
        URL_TO_SCRAPE = "https://www.raremaps.com/gallery/detail/56844hs/carte-generale-de-la-terre-appliquee-a-lastronomie-pour-le-flecheux"

    m = MapDetails(
        table=table, page_link=URL_TO_SCRAPE, bucket=b, run_on_init=True, run_debug=True
    )


if __name__ == "__main__":
    create_app_test()
