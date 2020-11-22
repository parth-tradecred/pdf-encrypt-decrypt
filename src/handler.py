from src.utils.download import download_from_url
from src.utils.saver import decrypt_pdfblob_save, pdf_to_img_save

import json
from datetime import datetime
import boto3


def bucketupload(pdf_file, img_file, file_format):
    try:
        # """Takes a pdf file blob and uploads to s3 storage."""

        init_time = datetime.now()
        print("Initiating s3 upload")

        bucket_name = 'tradecred-website-assets'
        pdfkey = 'decrypted-asset.pdf'
        imgkey = 'decrypted-asset.jpg'

        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)

        if file_format == 'pdf' or file_format is None:
            bucket.put_object(Key=pdfkey, Body=pdf_file.read(), ACL='public-read', ContentType='application/pdf',
                              ContentEncoding='ascii')
            current_time = datetime.now()
            print("pdf uploaded in {} seconds".format((current_time - init_time).microseconds / 1000000))
            return f'https://{bucket_name}.s3.amazonaws.com/{pdfkey}'

        if file_format == 'image':
            bucket.put_object(Key=imgkey, Body=img_file.read(), ACL='public-read', ContentType='image/jpg')
            # ,ContentEncoding='gzip')
            current_time = datetime.now()
            print("pdf uploaded in {} seconds".format((current_time - init_time).microseconds / 1000000))
            return f'https://{bucket_name}.s3.amazonaws.com/{imgkey}'

    except Exception as err:
        print(err, '\n s3 bucket initiation problem \n')
        return None


def process(file_url, password, file_format):
    return_msg = None
    return_flag = False
    return_service = None
    pdfpath = '/tmp/test-rotated-pdf'
    imgpath = '/tmp/test-rotated-img'

    with open(pdfpath, 'wb+') as pdf_file, open(imgpath, 'wb+') as img_file:

        print("\nCALLING>>>>>download_from_url()")
        file_blob, content_type = download_from_url(file_url)
        if content_type != 'application/pdf':
            return_msg = 'CONTENT-TYPE not application/pdf'
            return return_msg, return_flag, return_service

        print("\nCALLING>>>>>decrypt_blob_save()")
        decrypt_pdfblob_save(file_blob, password, pdf_file)

        # convert decrypted pdf to png
        print("\nCALLING>>>>>pdf_to_image_save")
        pdf_file.seek(0);
        img_file.seek(0)
        pdf_to_img_save(pdf_file, img_file)

        # Bucket upload honi hai acc. to file format
        print("\nCALLING>>>>>bucketupload()")
        pdf_file.seek(0);
        img_file.seek(0)
        return_msg = bucketupload(pdf_file, img_file, file_format)

        if return_msg is not None:
            return_flag = True
            return_service = 'DECRYPTION LIBRARY'

    return return_msg, return_flag, return_service


def extract(event, context):
    body = event.get("body")
    body = json.loads(body)
    file_url = body.get("file_url", None)
    password = body.get("password", None)
    file_format = body.get("format", None)

    if file_url:
        print("PROCESS INITIATED")
        return_msg, return_flag, return_service = process(file_url, password, file_format)
    else:
        return_msg = "No file passed"
        return_flag = False
        return_service = None

    body = {
        "message": return_msg,
        "flag": return_flag,
        "service_used": return_service
    }

    response = {
        "statusCode": 200 if return_flag else 404,
        "body": json.dumps(body)
    }
    return response
