import boto3
import os
class S3_Wrapper:
    def __init__(self):
        self.s3_client = boto3.client(
            's3'
        )

    def upload_file(self, file_name, bucket_name, object_name=None):
        if object_name is None:
            object_name = file_name
        try:
            self.s3_client.upload_file(file_name, bucket_name, object_name)
            print(f"File {file_name} uploaded to {bucket_name}/{object_name}")
        except Exception as e:
            print(f"Error uploading file: {e}")

    def download_file(self, bucket_name, object_name, file_name):
        try:
            self.s3_client.download_file(bucket_name, object_name, file_name)
            print(f"File {object_name} downloaded from {bucket_name} to {file_name}")
        except Exception as e:
            print(f"Error downloading file: {e}")

    def list_objects(self, bucket_name):
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                for obj in response['Contents']:
                    print(obj['Key'])
            else:
                print("No objects found in the bucket.")
        except Exception as e:
            print(f"Error listing objects: {e}")

s3_wrapper = S3_Wrapper()
bucket_name = 'demo-s3-prakash-v1'
local_file = '/Users/prakashtiwari/Downloads/vscode/de_projects/theory/aws/s3_demo.json'
object_name = 'vscode/demo_files/s3_demo.json'
#s3_wrapper.upload_file(local_file, bucket_name, object_name)
#s3_wrapper.list_objects(bucket_name)

##Using CLI to list objects in the bucket
os.system(f"aws s3 ls s3://{bucket_name} --recursive --human-readable --summarize")
