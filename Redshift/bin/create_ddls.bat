@echo off
REM GENERAL INSTRUCTIONS: This script is used to extract object DDL from your RedShift Cluster. Please adjust the variables with enclosed by <>
REM                       below to match your environment. Once completed, your extracted DDL code will be stored in the object_extracts folder.

REM ---- Variables to change ----

REM General Variables
SET OUTPUT_PATH="C:\_rs_out"

REM AWS RedShift Variables
SET RS_CLUSTER="redshift-cluster-1"
SET RS_DATABASE="dev"
SET RS_SECRET_ARN="arn:aws:secretsmanager:us-east-2:049502660834:secret:dev/redsfhift-cluster-1-edSdeq"

REM Script Variables
SET SCHEMA_FILTER="lower(schemaname) LIKE '%%'"
REM ---- END: Variables to change ----

mkdir %OUTPUT_PATH%
mkdir %OUTPUT_PATH%\log
REM mkdir %OUTPUT_PATH%/temp
mkdir %OUTPUT_PATH%\object_extracts
mkdir %OUTPUT_PATH%\object_extracts\DDL
REM mkdir %OUTPUT_PATH%\object_extracts\Reports
REM mkdir %OUTPUT_PATH%\object_extracts\Storage

python ../scripts/_ddl_extractor.py --rs-cluster %RS_CLUSTER% --rs-database %RS_DATABASE% --rs-secret-arn %RS_SECRET_ARN% --output-path %OUTPUT_PATH% --schema-filter %SCHEMA_FILTER%