#!/usr/bin/env python
# coding: utf-8

# Converts Hive DDL to Snowflake DDL. Please note: Date columns still need to be reassigned manually.
# 2021-07-15  Skip Reagor initial coding
# 2021-11-12 Minor updates plus some comments added by Brandon Carver

# 0. Import Needed Packages

import os
from itertools import islice
import snowflake.connector

# 1. Create all user defined variables.

# Grab all Hive DDL and place it in a directory. List the folder name below.
hive_directory = 'Hive_DDL'

# Define the output directory for the Snowflake DDL.
snowflake_directory = 'Snowflake_DDL'

# Input the values for your Snowflake account as strings in the variables below.
accountname = 'accountname'
username = 'username'
user_password = 'user_password'
dbname = 'dbname'
schemaname = 'schemaname'
rolename = 'rolename'
warehousename = 'warehousename'
       

# 2. Go through each DDL in Hive Directory and create the Snowflake DDL, then store this is separate Snowflake directory.

print("Getting files from Hive directory and creating Snowflake DDL...")

for filename in os.listdir(hive_directory):

    if filename[0] == '.':
        continue
    
    File_object = open(os.path.join(hive_directory, filename),"r")
    file_text = File_object.read()
    file_text = file_text.replace('(34,8)', '')

    ddl_parts = file_text.split('(\n')

    table_name = file_text.split('`')[1]

    column_info = ddl_parts[1].split(')')[0]

    ##print(column_info)

    column_info_lines = iter(column_info.splitlines())

    column_dict = {}

    for x in islice(column_info_lines,0,None):
        column_dict[x.split(' ')[2].split('`')[1]] = x.split(' ')[3].split(',')[0]


    for x in column_dict:
        if column_dict[x].startswith('map<'):
            column_dict[x] = 'variant'
        elif column_dict[x] == 'bigint':  
            column_dict[x] = 'integer'

    ##Create Table Statement
    Snowflake_DDL = 'Create or replace table ' + str(table_name) + '\n( \n'

    ##Column list
    for x in column_dict:
        Snowflake_DDL += str(x) + ' ' + str(column_dict[x]) + ',\n'

    ##Insert command

    Snowflake_DDL += '); \n \n insert into ' + str(table_name) + '\n( \n \nSelect \n'

    ## Select statement
    for x in column_dict:
        ##Snowflake_DDL += '$1:' + str(x) + '::' + str(column_dict[x]) + ' as ' + str(x) + ',\n'
        Snowflake_DDL += '$1'+":" + str(x) +'::' + str(column_dict[x]) + ' as ' + str(x) + ',\n'

    ##finish ddl
    Snowflake_DDL += 'from @my_s3_stage (file_format => parquet_ff) \n \n);'
    Snowflake_DDL=Snowflake_DDL.replace('decimal','decimal(34,8)')
    new_file_object = open(os.path.join(snowflake_directory, filename),"w+")
    new_file_object.write(Snowflake_DDL) 
    new_file_object.flush()
    print(filename + " is finished. Moving to next file.")
    
print("All Done!")


# 3. Connect to Snowflake and loop through each create ddl statement

# Setup the connection for the Snowflake Connector.  
  
con = snowflake.connector.connect(
        user= username,
        password= user_password,
        account=accountname,
        warehouse=warehousename,
        database=dbname,
        schema=schemaname,
        role = rolename
    )

print("Looping through each create ddl statement...")

for filename in os.listdir(snowflake_directory):
    File_object = open(os.path.join(snowflake_directory, filename),"r")
    file_text = File_object.read()
    command_list = file_text.split(';')
    con.cursor().execute(command_list[0])
    print(filename + " is finished. Moving to new file.")

print("All Done!")


# 4. Loop through the Snowflake DDL folder and run each insert statement

print("Running insert statements for the Snowflake DDL..."

for filename in os.listdir(snowflake_directory):
    File_object = open(os.path.join(snowflake_directory, filename),"r")
    file_text = File_object.read()
    command_list = file_text.split(';')
    con.cursor().execute(command_list[1])
    print(filename + " is finished. Moving to new file.")

print("All Done!")
