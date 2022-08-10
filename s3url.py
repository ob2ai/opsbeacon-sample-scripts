
#    _|_
#   /@-@\ Copyright © OpsBeacon, Inc.
#   \ - /    All rights reserved.
#    };{
 
from awslib import *

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket", help="S3 bucket name")
    parser.add_argument("--path", help="file path name in s3 bucket")
    parser.add_argument("--expiration", type=int, default=3600, help="expiration seconds of the url")
    parser.add_argument("--region", help="S3 region")


    args = parser.parse_args()

    url = create_presigned_url(args.bucket, args.path, args.expiration, args.region)

    print(url)

if __name__ == "__main__":
    main()
