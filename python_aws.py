import boto3
import sys


class Bucket:

    def __init__(self):
        self.options = {'r': 'eu-west-1'}
        for index, arg in enumerate(sys.argv[1:]):
            if arg[0] == '-':
                current_options = []
                arg_found = False
                for option_index, option in enumerate(sys.argv[1:]):
                    if option_index > index and arg_found == False:
                        if option[0] == '-':
                            arg_found = True
                        else:
                            current_options.append(option)
                if len(current_options) == 1:
                    self.options[arg[1:]] = current_options[0]
                else:
                    self.options[arg[1:]] = current_options
        self.s3 = boto3.resource('s3')
        self.s3_client = boto3.client('s3', region_name=self.options['r'])

    def create_bucket(self):
        location = {'LocationConstraint': self.options['r']}
        if self.options['b'] not in list(bucket.name for bucket in self.s3.buckets.all()):
            self.s3_client.create_bucket(Bucket=self.options['b'], CreateBucketConfiguration=location)

    def delete_bucket(self):
        self.s3_client.delete_bucket(Bucket=self.options['b'])

    def upload(self):
        response = self.s3_client.upload_file(Filename=self.options['f'], Bucket=self.options['b'], Key=self.options['k'])

    def download(self):
        response = self.s3_client.download_file(Bucket=self.options['b'], Key=self.options['k'], Filename=self.options['f'])

    def delete(self):
        response = self.s3_client.delete_object(Bucket=self.options['b'], Key=self.options(['k']))


try:
    bucket = Bucket()
    if bucket.options['p'] == 'cb':
        bucket.create_bucket()
    elif bucket.options['p'] == 'db':
        bucket.delete_bucket()
    elif bucket.options['p'] == 'upload':
        bucket.upload()
    elif bucket.options['p'] == 'download':
        bucket.download()
    elif bucket.options['p'] == 'delete':
        bucket.delete()

    else:
        print('Invalid process!')
except Exception as e:
    print(e)
