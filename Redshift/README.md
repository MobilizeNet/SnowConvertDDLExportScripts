# Redshift Export Scripts

This repository provides some simple scripts to help exporting your Redshift Code so it can be migrated to [Snowflake](https://www.snowflake.com/) using [SnowConvert](https://www.mobilize.net/products/database-migrations/snowconvert).

## Version

Release 2021-03-24

## Usage

To start, please download this folder into your computer.

This solution provides 3 alternatives to extract the data: 

* Windows Script: A script written with PowerShell + AWS Cli
* Bash (Linux/macOS) Script: A script written with Bash + AWS Cli
* Manual: SQL Queries to execute on your preferred SQL Editor

### Prerequisites

Depending on the type of execution, the prerequisites are different, however these are shared across all types:
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

Specific requirements for each type are:

#### Script (Powershell or Bash)

This script uses Powershell (Windows) or Bash (Linux/macOS), and AWS Cli (both platforms) to connect and communicate with AWS services. In order for this to work you first need to:

* Install AWS Cli. Instructions on how to install [can be found here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
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
    
#### Manual

* Access to an SQL Editor with access to Redshift, such as SQL Workbench/J or the AWS Redshift Query Editor v1. v2 doesn't work properly since it only exports 100 rows at a time.

After completing these steps, you're now ready to execute the script.

### Usage

#### Script (Powershell or Bash)

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

* After modifying these variables, execute the scripts and your DDL Code should be extracted into the path you specified.

#### Manual

* Open the queries located in `Redshift/scripts` in your preferred SQL Editor and replace the `{schema_filter}` line  with the desired filter for your needs. If you need all schemas to be pulled, you could either input `lower(schemaname) like '%'` or remove the entire `WHERE`. 
* Execute the `.sql` queries. Make sure that there is no limit set on the amount of rows it can extract. After executing the queries, export each query result to either `.txt` or `.csv` and rename them to:

Script|Result Filename|
--- | --- |
function_ddl.sql|DDL_Function.sql
procedure_ddl.sql|DDL_Procedure.sql
table_ddl.sql|DDL_Table.sql
view_ddl.sql|DDL_View.sql

## Notes

* These queries to extract the code were based on the queries on [this repository](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/AdminViews) and they were modified slightly or not at all.
* Extracting the information from Redshift is performed asynchronously. This means that when a statement is sent to the database, the code will continue executing. For this there is a Timeout of 5 minutes to wait for a query to finish executing and it will check every 5 seconds if it's finished by default, but it can be modified with the MAX_ITERATIONS variable. 

## Reporting issues and feedback

If you encounter any bugs with the tool please file an issue in the
[Issues](https://github.com/MobilizeNet/SnowConvertDDLExportScripts/issues) section of our GitHub repo.

## Known issues

* There is a known issue when procedure code exceeds 65535 characters. `[22001] ERROR: value too long for type character varying(65535)`

To solve this issue, we've setup an alternative script, which uses Python 3 and boto3. This script will change the way in which the procedures are extracted. To do so, please follow these steps:

* Download Python for your OS [here](https://www.python.org/downloads/). There's an initialization script for both Windows or Unix-based environment.
* After installing Python, install the boto3 library by executing: `pip install boto3`
* Configure your AWS credentials into your computer. There are several ways to do this, the default and most recommended is creating a credentials file as shown [here](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).
> If your organization has more strict controls, you can also modify the `get_client` function in the `scripts/_boto_3_client.py` file to change parameters specifically for your organization's requirements. More details on the options can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).
* Open the script corresponding to your environment on the folder `Redshift/bin/python_alternative`.
* Change the variables as shown in the usage section. However, you will see some new variables:

Variable|Description|Must be modified|
--- | --- | ---
BATCH_WAIT|The only way provided by Redshift to get the code for procedures without losing parameters' precision is by executing `SHOW PROCEDURE <procedure>`. This means that we have to query each procedure one by one, which means that a lot of queries are sent to the database at the same time. If you're having issues with Maximum concurrent statements, you can increase this value to send the batches in a more controlled manner. This will increase extraction time considerably on databases with a big number of procedures. The default value is 0.2 seconds.|N
THREADS|Amount of threads to use to extract the code for procedures once their queries have been completed.|N

Once you've modified these, you will be able to execute the script and avoid the issue. This process, however will take several minutes to extract depending on the amount of the procedures.

## License

These export scripts are licensed under the [MIT license](https://github.com/MobilizeNet/SnowConvertDDLExportScripts/blob/main/Redshift/LICENSE.txt).
