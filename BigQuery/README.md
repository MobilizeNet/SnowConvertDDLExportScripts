# BigQuery DDL Export Scripts

These scripts can be used to perform a BigQuery Data Export.

## Version

Release 2021-12-02

## Usage

The following are the steps to execute the DDL Code Generation. They can be executed in Linux/Unix and Windows enviroments.

## How does this work?

The script `create_ddls.sh` will connect to your database and create a collection of SQL files.

## Prerequisits

1. Follow [these](https://cloud.google.com/sdk/docs/install#linux) instructions for installing Cloud SDK.
2. It is recommended to use a user  with **Admin** or **Owner** privileges
2. The user must be granted with a role with the `bigquery.datasets.get` permission. If there is no roles with it, you could create a custom role just for this.


## How are these scripts used ?

In order to use them.

1. Modify the `create_ddls.sh`

1.1 The region setting will be at the top of this file.

1.2 You must log in going to a link in your browser when you run `./google-cloud-sdk/bin/gcloud init`, and then select the cloud project to use.

2. Finally, run `create_ddls.sh` to extract the DDLs from BigQuery

After a successful run, remove region information from the top line of `create_ddls.sh`.

Compress the entire `Output` folder.