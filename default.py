import os
from source.manage_raw_csv_files import download_zip_file, upload_data_to_s3
from source.upload_data_to_aws_neptune import upload_data_to_aws_neptune
from config import *
from loguru import logger


# Download data to local path as well as upload it to s3.
download_zip_file(
    url="https://offshoreleaks-data.icij.org/offshoreleaks/csv/csv_paradise_papers.2018-02-14.zip",
    local_path=LOCAL_PATH,
    updated_name=f"{LOCAL_FILENAME}.zip",
)

upload_data_to_s3(
    local_path=os.path.join(LOCAL_PATH, LOCAL_FILENAME),
    s3_bucket=PARADISE_S3_BUCKET,
    s3_path=PARADISE_S3_RELATIVE_PATH,
)

# Load data to neptune cluster
loading_task_id = upload_data_to_aws_neptune(
    cluster_id=NEPTUNE_CLUSTER_ID,
    s3_path=os.path.join(PARADISE_S3_BUCKET, PARADISE_S3_RELATIVE_PATH),
    cluster_port=NEPTUNE_CLUSTER_PORT,
    region=REGION,
    iam_role=NEPTUNE_CLUSTER_IAM_ROLE,
)

logger.info(f"Loading task id: {loading_task_id=}")
