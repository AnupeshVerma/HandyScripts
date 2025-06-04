import boto3

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

source_bucket_name = 'source_bucket_name'
source_key = 'source_filename.csv'
destination_bucket_name = 'destination_bucket_name'
destination_key = 'destination_filename.csv'

copy_source = {
    'Bucket': source_bucket_name,
    'Key': source_key
}

# Copy file from source bucket to destination bucket with a new name
s3.Bucket(destination_bucket_name).copy(copy_source, destination_key)
#s3.Object(destination_bucket_name, destination_key).copy(copy_source)

# You can delete the source file after copying
s3.Object(source_bucket_name, source_key).delete()


print(f"Moved {source_key} from {source_bucket_name} to {destination_key} in {destination_bucket_name}")


"""
You can use any one of the following method to copy the file:
    -> s3.Bucket(destination_bucket_name).copy(copy_source, destination_key)

    -> s3.Object(destination_bucket_name, destination_key).copy(copy_source)
"""




"""
copy only accepts dictionary as source

copy_source = {
    'Bucket': bucket_name,
    'Key': old_key
}
s3.Object(bucket_name, new_key).copy(copy_source)   
 or
 s3.Object(bucket_name, new_key).copy({'Bucket': bucket_name, 'Key': old_key})
 """