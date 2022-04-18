# Redshift Export Scripts

This repository provides some simple scripts to help exporting your Redshift Code so it can be migrated to [Snowflake](https://www.snowflake.com/) using [SnowConvert](https://www.mobilize.net/products/database-migrations/snowconvert). This is an alternative to the main script using Python and boto3, used when the user prefers Python or when the original scripts return the following error: `[22001] ERROR: value too long for type character varying(65535)`.

## Prerequisites

* Database user must have access to the following tables:
  * pg_namespace
  * pg_class
  * pg_attribute
  * pg_attrdef
  * pg_constraint
  * pg_class
  * pg_description
  * pg_proc
  * pg_proc_info
  * pg_language
  * information_schema.columns
* Create a Secret in the AWS Secrets Manager with the `username`, `password`, `engine`, `host`, `port` and `dbClusterIdentifier`. The keys must be named as mentioned.  
* Configure your AWS credentials into your computer. There are several ways to do this, the default and most recommended is creating a credentials file as shown [here](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).
* The AWS user must have the following permissions:
  * IAM Access to Redshift Data API:
    * DescribeStatement
    * GetStatementResult
    * ExecuteStatement
    * BatchExecuteStatement
  * IAM Access to SecretsManager:
    * GetSecretValue
* Download Python for your OS [here](https://www.python.org/downloads/). There's an initialization script for both Windows or Unix-based environment.
* After installing Python, install the boto3 library by executing: `pip install boto3`
* Configure your AWS credentials into your computer. There are several ways to do this, the default and most recommended is creating a credentials file as shown [here](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).
> If your organization has more strict controls, you can also modify the `get_client` function in the `scripts/_boto_3_client.py` file to change parameters specifically for your organization's requirements. More details on the options can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).

## Usage

To use the script, follow these steps:

* Navigate to the bin folder, and open the `create_ddls.ps1` or `create_ddls.sh`, depending on your environment, in a text editor.
* In here, modify these variables:

Variable|Description|Must be modified|
--- | --- | ---
OUTPUT_PATH|Output folder where the results will be saved to.|Y
RS_CLUSTER|Your Redshift Cluster identifier.|Y
RS_DATABASE|The Redshift Database that you're interested in extracting.|Y
RS_SECRET_ARN|The Secret ARN with your credentials.|Y
SCHEMA_FILTER|SQL statement to filter the schemas you're interested in. By default the script ignores the `information_schema`, `pg_catalog` and `pg_internal` schemas.|N
MAX_ITERATIONS|AWS handles requests asynchronously, therefore we need to perform constant checks on the query for completion. This value sets the max iterations allowed before finishing the script. Every iteration waits 5 seconds.|N
BATCH_WAIT|The only way provided by Redshift to get the code for procedures without losing parameters' precision is by executing `SHOW PROCEDURE <procedure>`. This means that we have to query each procedure one by one, which means that a lot of queries are sent to the database at the same time. If you're having issues with Maximum concurrent statements, you can increase this value to send the batches in a more controlled manner. This will increase extraction time considerably on databases with a big number of procedures. The default value is 0.2 seconds.|N
THREADS|Amount of threads to use to extract the code for procedures once their queries have been completed.|N

Once you've modified these, you will be able to execute the script and the error should not get this error `[22001] ERROR: value too long for type character varying(65535)` anymore. 

This process could take several minutes to extract when extracting a large number of procedures.
