from config import Config
import boto3


class Bucket:
    """Class to wrap AWS S3 bucket instance

    Attributes:
        bucketName: url/name of S3 bucket
        session: boto3 session object with AWS credentials
        s3: s3 resource maped to boto3 session
        bucket: bucket associated with the s3 resource and bucketName

    Methods:
        writeImage: add image to s3 bucket
        doesKeyExist: checks to see if key already exists in s3 bucket
    """

    def __init__(self):
        self.bucketName = Config.S3_BUCKET
        self.session = boto3.Session(
            aws_access_key_id=Config.ACCESS_KEY,
            aws_secret_access_key=Config.SECRET_KEY,
        )
        self.s3 = self.session.resource("s3")
        self.bucket = self.s3.Bucket(self.bucketName)

    def writeImage(self, image_data, bucket_key):
        self.doesKeyExist(bucket_key)
        if self.doesKeyExist(bucket_key):
            # f"key: {bucket_key} - exists already. passing."
            pass
        else:
            o = self.bucket.Object(bucket_key)
            o.put(Body=image_data)
            print(f"key:{bucket_key} - written to S3")

    def doesKeyExist(self, b_key):
        objs = list(self.bucket.objects.filter(Prefix=b_key))
        if len(objs) > 0 and objs[0].key == b_key:
            return True
        else:
            # print(f"key:{b_key} - not found in S3")
            return False
