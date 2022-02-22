import boto3
import os
import re
import multiprocessing as mp
print("Number of processors: ", mp.cpu_count())

import time

'''
===========================
== Functions definitions ==
===========================
'''

def read_ddl_queries():
    queries_dict = {}
    for f in os.listdir('.'):
        if f.endswith(".sql"):
            object_type = re.search(r'^(.*)_ddl\.sql', f, )
            with open(f,'r') as file:
                queries_dict[object_type.group(1)] = file.read()
    return queries_dict


def execute_ddl_queries(object_type):
    resp = RS_CLIENT.execute_statement(
        ClusterIdentifier='redshift-cluster-1'
        , Database=RS_DATABASE
        , SecretArn=RS_SECRET_ARN
        , Sql=QUERIES[object_type]
        , StatementName=f'mobilize_ddl_extraction_{object_type}'
    )
    return resp['Id']


def is_query_valid(query_id):
    resp = RS_CLIENT.describe_statement(Id=query_id)
    return resp['ResultRows'] >= 0


def iterate_query_result(query_id):
    code = []
    if is_query_valid(query_id):
        resp = RS_CLIENT.get_statement_result(Id=query_id)
        for row in resp['Records']:
            code.append(row[0]['stringValue'] + '\n')
    return code


def save_results(object_type, code):
    with open(f'out/DDL_{object_type}.sql', 'w') as f:
        f.writelines(code)

'''
=================================
== Global variables definition ==
=================================
'''

QUERIES = read_ddl_queries()
RS_CLIENT = boto3.client('redshift-data')
RS_DATABASE = 'dev'
RS_SECRET_ARN = 'arn:aws:secretsmanager:us-east-2:049502660834:secret:dev/redsfhift-cluster-1-edSdeq'

query_id = execute_ddl_queries('table')
print(query_id)

i = 0

valid_query = False

while(i < 15):
    print(f'Validation number {i}')
    valid_query = is_query_valid(query_id)
    if valid_query:
        c = iterate_query_result(query_id)
        save_results('table', c)
        break
    time.sleep(1)
    i += 1

if __name__ == 'main':
    pass






