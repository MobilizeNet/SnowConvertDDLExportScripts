# RedShift Export Scripts

This repository provides some simple scripts to help exporting your Redshift Code so it can be migrated to to [Snowflake](https://www.snowflake.com/) using [SnowConvert](https://www.mobilize.net/products/database-migrations/snowconvert).

## Version

Release 2021-02-25

## Usage

To start, please download this folder into your computer.

### Prerequisites

This script uses Python and boto3 library as the API to connect and communicate with AWS services. In order for this to work you would first need to:

* Download Python for your OS [here](https://www.python.org/downloads/). There's an initialization script for both Windows or Unix-based environment.
* After installing Python, install the boto3 library by executing: `pip install boto3`
* Create a Secret in the AWS Secrets Manager with the `username`, `password`, `engine`, `host`, `port` and `dbClusterIdentifier`. The keys must be named as mentioned.  
* Configure your AWS credentials into your computer. There are several ways to do this, the default and most recommended is creating a credentials file as shown [here](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html).
> If your organization has more strict controls, you can also modify the `get_client` function in the `scripts/_boto_3_client.py` file to change parameters specifically for your organization's requirements. More details on the options can be found [here](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html).

After completing these steps, you're now ready to execute the script.

### Usage

To use the script, follow these steps:

* Navigate to the bin folder, and open the `create_ddls.bat` or `create_ddls.sh`, depending on your environment in a text editor.
* In here, modify these variables:

Variable|Description|Must be modified|
--- | --- | ---
OUTPUT_PATH|Output folder where the results will be saved to.|Y
RS_CLUSTER|Your Redshift Cluster identifier.|Y
RS_DATABASE|The Redshift Database that you're interested in extracting.|Y
RS_SECRET_ARN|The Secret ARN with your credentials.|Y
SCHEMA_FILTER|SQL statement to filter the schemas you're interested in. By default the script ignores the `pg_catalog`, `pg_internal` and `information_schema` schemas.|N
BATCH_WAIT|The only way provided by Redshift to get the code for procedures without losing parameters' precision is by executing `SHOW PROCEDURE <procedure>`. This means that we have to query each procedure one by one, which means that a lot of queries are sent to the database at the same time. If you're having issues with Maximum concurrent statements, you can increase this value to send the batches in a more controlled manner. This will increase extraction time considerably on databases with a big number of procedures. The default value is 0.2 seconds.|N
THREADS|Amount of threads to use to extract the code for procedures once their queries have been completed.|N

* After modifying these variables, execute the scripts and your DDL Code should be extracted. 

## Notes

* Since the procedures extraction needs to be made individually, on big workloads the process might take more than 30 minutes. This was tested on a database with 10.000 procedures on a single-node dc2.large cluster and it took approximately 40 minutes. To tackle this issue, multithreading has been applied to speed up this process. The amount of threads to be used can be specified with the `THREADS` parameter.
* To avoid extracting a specific object, you can change the extension of the .sql file of the object you want to ignore. For example, if you want to avoid extracting procedures, rename the `procedure_ddl.sql` to `procedure_ddl.sql.ignore`.
* These queries to extract the code were based on the queries on [this repository](https://github.com/awslabs/amazon-redshift-utils/tree/master/src/AdminViews) and they were modified slightly or not at all.
* Extracting the information from Redshift is performed asynchronously. This means that when an statement is sent to the database, the code will continue executing. For this there is a Timeout of 5 minutes to wait for a query to finish executing and it will check every 5 seconds if it's finished.

## Reporting issues and feedback

If you encounter any bugs with the tool please file an issue in the
[Issues](https://github.com/MobilizeNet/SnowConvertDDLExportScripts/issues) section of our GitHub repo.

## License

These export scripts are licensed under the [MIT license](https://github.com/MobilizeNet/SnowConvertDDLExportScripts/blob/main/Redshift/LICENSE.txt).
