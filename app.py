from config import Config
import boto3
import requests
from page import MapDetails
from utils.bucket import Bucket


def create_app():
    ddb = boto3.resource("dynamodb", region_name="us-east-1")
    table = ddb.Table(Config.TABLE_NAME)
    b = Bucket()
    m = MapDetails(
        table=table,
        # page_link="https://www.raremaps.com/gallery/detail/54058/angliae-scotiae-et-hiberniae-sive-britannicae-insularum-de-ortelius",
        page_link="https://www.raremaps.com/gallery/detail/51844/cestria-vulgo-chester-angliae-civitas-braun-hogenberg",
        bucket=b,
        run_on_init=False,
        run_debug=True,
    )
    # m.write_details_to_db()


if __name__ == "__main__":
    create_app()
