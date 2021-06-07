import requests
from requests.exceptions import ConnectionError
from loguru import logger


def upload_data_to_aws_neptune(
    cluster_id: str,
    s3_path: str,
    region: str,
    iam_role: str,
    cluster_port: int = 8182,
) -> str:
    """
    Download data from local system
    :param cluster_id: Neptune cluster Id.
    :param s3_path: S3 path contains data to upload.
    :param region: Region.
    :param iam_role: Iam role have access to neptune cluster.
    :param cluster_port: Neptune cluster port.
    :return: Load id of task.
    """
    try:
        res = requests.post(
            f"https://refinitiv-neptune-cluster.cluster-{cluster_id}.ap-southeast-1.neptune.amazonaws.com:{cluster_port}"
            f"/loader",
            json={
                "source": s3_path,
                "format": "csv",
                "iamRoleArn": iam_role,
                "region": region,
                "mode": "AUTO",
            },
        )
        """
        Neptune tasks return job id like:
        
        Example:-
        {
            "status" : "200 OK",
            "payload" : {
                "loadId" : "ef478d76-d9da-4d94-8ff1-08d9d4863aa5"
            }
        }
        """
        if res.status_code == 200:
            return res["payload"]["loadId"]
        else:
            logger.error(f"Error occurred while loading data: {res=}")
    except ConnectionError as e:
        logger.error(f"Connection failed: {e}")
