## Analyse and make visualisations for offshore leaks database (paradise papers)
Unpack and upload data to graph database (AWS Neptune) &amp; create visualisations around offshore (Paradise papers) leaks database.

## Setup infra

--Install terraform locally using https://learn.hashicorp.com/tutorials/terraform/install-cli

--Confirm terraform installtion using
```
terraform --version
cd terraform
terraform init
terraform plan
terraform apply
```

There are 2 steps need to do manually for infra setup-

Make a role which have access to data s3 bucket.
Assign this role to Neptune cluster.
 https://docs.aws.amazon.com/neptune/latest/userguide/bulk-load-tutorial-IAM.html


## Check Data Analysis
On root path run command:
```
jupyter notebook
```
check data_analysis notebook


## Run code locally
Install requirements
```
pipx install poetry
poetry install
```
This will automatically setup python version and dependencies.

After this there are some manual things to add in `config.py`
```
(optional)
LOCAL_PATH = "data"
LOCAL_FILENAME = "paradise_papers"
PARADISE_S3_BUCKET = "refinitiv-data"
PARADISE_S3_RELATIVE_PATH = "paradise_papers"
NEPTUNE_CLUSTER_PORT = 8182
REGION = "ap-southeast-1"

(required)
NEPTUNE_CLUSTER_ID = "chcnyrk9qbkr"
NEPTUNE_CLUSTER_IAM_ROLE = "neptune-cluster-auth"
```

You'll find `NEPTUNE_CLUSTER_ID` from cluster's dynamic path.
`NEPTUNE_CLUSTER_IAM_ROLE` is the role having access to this cluster.