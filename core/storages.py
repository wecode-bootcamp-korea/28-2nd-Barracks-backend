import boto3
import uuid

from barracks.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        s3_client = boto3.client(
            's3',
            aws_access_key_id     = access_key,
            aws_secret_access_key = secret_key
        )
        self.s3_client   = s3_client
        self.bucket_name = bucket_name

    def upload(self, image):
        try:
            key  = 'projects/'+str(uuid.uuid4())

            self.s3_client.upload_fileobj(
                image,
                AWS_STORAGE_BUCKET_NAME,
                key,
                ExtraArgs = {
                    "ContentType" : image.content_type
                }
            )
            image_url = "https://wecode-barracks.s3.ap-northeast-2.amazonaws.com/"+key

            return image_url
        except:
            return None

    def delete(self, image_url):
        return self.s3_client.delete_object(bucket=self.bucket_name, Key=image_url)

s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)

class FileUpload:
    def __init__(self, client):
        self.client = client

    def upload(self, image_urls):
        return self.client.upload(image_urls)