@echo off
REM GENERAL INSTRUCTIONS: This script is used to extract object DDL from your RedShift Cluster. Please adjust the variables with enclosed by <>
REM                       below to match your environment. Once completed, your extracted DDL code will be stored in the object_extracts folder.

REM ---- Variables to change ----

REM General Variables
REM SET OUTPUT_PATH="<output_path>"
SET OUTPUT_PATH="C:\work\06_redshift_extraction_scripts\SnowConvertDDLExportScripts\_rs_test"

REM AWS RedShift Variables
SET RS_CLUSTER="<redshift_cluster_identifier>"
SET RS_DATABASE="<redshift_database>"
SET RS_SECRET_ARN="<secret_arn>"
REM ---- END: Variables to change ----

mkdir %OUTPUT_PATH%
mkdir %OUTPUT_PATH%\log
REM mkdir %OUTPUT_PATH%/temp
mkdir %OUTPUT_PATH%\object_extracts
mkdir %OUTPUT_PATH%\object_extracts\DDL
REM mkdir %OUTPUT_PATH%\object_extracts\Reports
REM mkdir %OUTPUT_PATH%\object_extracts\Storage

python ../scripts/_ddl_extractor.py %RS_CLUSTER% %RS_DATABASE% %RS_SECRET_ARN%