# SQL Server Export Scripts

This repository provides some simple scripts to help exporting your SQLServer code so it can be migrated to [Snowflake](https://www.snowflake.com/) using [SnowConvert](https://www.mobilize.net/products/database-migrations/snowconvert)

## Version

Version 1.7
Release 2021-12-10

## Usage

The `extract-sql-server-ddl.ps1` script attempts to connect to an instance of SQL Server and, for each database/schema that survives inclusion/exclusion filters, retrieves object Data Definition Language (DDL) to files in a specified directory.

**SQL Server tested versions**: `SQL Server 2019`, `Azure SQLDatabase`

The script use the following parameters:

* **ServerInstance**: Specifies the instance to use.  Format is [[\<server>]\[\<named_instance>]] (i.e., \\\<named_instance>, \<server>, \<server>\\\<named_instance>, or not specified).  If not specified, use the default instance on the local server.
* **Port**: Specifies the port to use when connecting to <server>.  Overrides a <named_instance> if specified in -ServerInstance and forces -UseTcp.  Default is none.
* **UseTcp**: Specify whether to use the TCP format when connecting to -ServerInstance. Default is to not use TCP format.
* **UserName**: Specifies the user name to use with SQL Authentication.  If not specified, use the current user with Windows Authentication.
* **Password**: Specifies the password associated with -UserName (otherwise prompted interactively if -UserName is specified).
* **ScriptDirectory**: Specifies the root directory under which server-, instance-, database-, and object-related files are stored.  Default is 'C:\MyScriptsDirectory'.
* **IncludeDatabases**: Specifies which database(s) to include via a comma-delimited list of patterns (using PowerShell -match syntax).  Default is to include all databases other than SQL Server system databases.
* **ExcludeDatabases**: Specifies which database(s) to exclude via a comma-delimited list of patterns (using PowerShell -match syntax).  Default is to exclude none.
* **IncludeSchemas**: Specifies which schema(s) to include via a comma-delimited list of patterns (using PowerShell -match syntax).  Default is to include all.
* **ExcludeSchemas**: Specifies which schema(s) to exclude via a comma-delimited list of patterns (using PowerShell -match syntax).  Default is to exclude none.
* **IncludeSystemDatabases**: Specify whether to include SQL Server system databases prior to applying inclusion/exclusion filters.  Default is false.
* **ExistingDirectoryAction**: Specify whether to (non-interactively) 'delete' or 'keep' existing directories where encountered.  Default is to prompt interactively.
* **NoSysAdminAction**: Specify whether to (non-interactively) 'stop' or 'continue' when the -UserName does not have the sysadmin role on -ServerInstance.  Default is to prompt interactively.


**INPUTS**: None.  You cannot pipe objects to extract-sql-server-ddl.ps1.

**OUTPUTS**: System.String.

## Here some examples of how use the script:

Example 1: connect to the default instance on the local server using Windows Authentication

```ps
PS> .\extract-sql-server-ddl.ps1
```

Example 2: connect to the instance listening on port 1500 on server foo.mydomain.com

```ps
PS> .\extract-sql-server-ddl.ps1 -ServerInstance foo.mydomain.com -Port 1500
```

Example 3: connect as juser using SQL Authentication to the default instance on foo.database.windows.net

```ps
PS> .\extract-sql-server-ddl.ps1 -UserName juser -ServerInstance foo.database.windows.net 
```

## Reporting issues and feedback

If you encounter any bugs with the tool please file an issue in the
[Issues](https://github.com/MobilizeNet/SnowConvertDDLExportScripts/issues) section of our GitHub repo.

## License

These scripts are licensed under the [MIT license](https://github.com/MobilizeNet/SnowConvertDDLExportScripts/blob/main/SQLServer/LICENSE.txt).
