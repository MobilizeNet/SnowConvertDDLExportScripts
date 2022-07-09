# SQL Server Export Scripts

This repository provides some simple scripts to help exporting your SQLServer code so it can be migrated to [Snowflake](https://www.snowflake.com/) using [SnowConvert](https://www.mobilize.net/products/database-migrations/snowconvert).

## Version

Version 2.5
Release 2022-07-08

## Usage

The `extract-sql-server-ddl.ps1` script attempts to connect to an instance of SQL Server using either Windows or SQL authentication and, for each database that survives inclusion/exclusion filters, retrieves certain object definitions as individual DDL files to a local directory. 

**SQL Server tested versions**: `SQL Server 2019`, `Azure SQLDatabase`

The script uses the following parameters.  The script will prompt the user for any parameter not specified on the command line.

* **ServerName**: Specifies the SQL Server database server to use
* **InstanceName**: Specifies the SQL Server database instance to use (default is the default instance)
* **PortNumber**: Specifies the port to use (default is 1433)
* **UserName**: Specifies the user name to use with SQL Authentication (default is the logged-in user)
* **Password**: Specifies the password to use for **UserName** (if SQL authentication preferred)
* **ScriptDirectory**: Specifies the root directory in which the extracted files are to be stored (default is .\MyScriptsDirectory)
* **IncludeDatabases**: Specifies databases that match the listed pattern(s) be included in the extraction (default is all)
* **ExcludeDatabases**: Specifies databases that match the listed pattern(s) be excluded from the extraction (default is none)
* **IncludeSchemas**: Specifies schemas (in any database) that match the listed pattern(s) be included in the extraction (default is all)
* **ExcludeSchemas**: Specifies schemas (in any database) that match the listed pattern(s) be excluded from the extraction (default is none)
* **IncludeSystemDatabases**: Specifies whether to include databases, schemas, and tables tagged as SQL Server system objects (default is false)
* **ExistingDirectoryAction**: Specifies whether to delete or keep the existing **ScriptDirectory** (default is to prompt interactively)
* **NoSysAdminAction**: Specifies whether to stop or continue should the authenticated **UserName** not have the sysadmin role on **ServerName**\\**InstanceName** (default is to prompt interactively)

## Additional Help

For more information on using the script, execute the following:
```ps
PS> Get-Help -full .\extract-sql-server-ddl.ps1
```

## Reporting issues and feedback

If you encounter any bugs with the tool please file an issue in the
