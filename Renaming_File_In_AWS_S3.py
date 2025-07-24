import boto3

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY'
)

bucket_name = 'BUCKET_NAME' 
old_key = 'oldfilename.csv' 
new_key = 'newfilename.csv'


# Copy the object to the new key
s3.Object(bucket_name, new_key).copy({'Bucket': bucket_name, 'Key': old_key})

# Delete the old object
s3.Object(bucket_name, old_key).delete()

print(f"Renamed {old_key} to {new_key} in bucket {bucket_name}")


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