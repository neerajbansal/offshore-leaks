terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "ap-southeast-1"
}

resource "aws_s3_bucket" "b" {
  bucket = "refinitiv-data"
  acl    = "private"
  tags = {
    Name = "refinitiv-data"
  }
}

resource "aws_neptune_cluster" "default" {
  cluster_identifier                  = "refinitiv-neptune-cluster"
  engine                              = "neptune"
  backup_retention_period             = 5
  preferred_backup_window             = "07:00-09:00"
  skip_final_snapshot                 = true
  iam_database_authentication_enabled = true
  apply_immediately                   = true
}

resource "aws_iam_policy" "ref-data-policy" {
  name        = "ref-data-policy"
  description = "Ref data policy"

  policy = <<EOT
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]

}
EOT
}

resource "aws_iam_role_policy_attachment" "test-attach" {
  role       = "neptune-s3-reader"
  policy_arn = aws_iam_policy.ref-data-policy.arn
}

resource "aws_neptune_cluster_instance" "example" {
  count              = 1
  cluster_identifier = aws_neptune_cluster.default.id
  engine             = "neptune"
  instance_class     = "db.r4.large"
  apply_immediately  = true
  port = 8182
}