import requests
import os
import zipfile
import boto3

s3_client = boto3.client("s3")


def download_zip_file(url: str, local_path: str, updated_name: str):
    """
    Download data from local system
    :param url: URL of resource to download.
    :param local_path: Local path to save.
    :param updated_name: Name of file to update.
    :return:
    """
    response = requests.get(url)

    # Assure data folder exists
    os.makedirs(local_path, exist_ok=True)

    local_file = os.path.join(local_path, updated_name)
    # Download file locally
    with open(local_file, "wb") as f:
        f.write(response.content)

    with zipfile.ZipFile(local_file, "r") as zip_ref:
        zip_ref.extractall(local_file.replace(".zip", ""))


def upload_data_to_s3(local_path: str, s3_bucket: str, s3_path: str):
    """
    Upload local data to s3.
    :param local_path: Local path of file or folder to upload.
    :param s3_bucket:
    :param s3_path:
    :return:
    """
    files = os.listdir(local_path) if os.path.isdir(local_path) else [local_path]
    for file in files:
        file_path = (
            os.path.join(local_path, file) if os.path.isdir(local_path) else file
        )
        s3_client.upload_file(
            file_path,
            s3_bucket,
            s3_path,
        )
