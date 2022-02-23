from _boto3_client import get_client
import os
import re
import sys
import time

'''
===========================
== Functions definitions ==
===========================
'''

class Query:

    object_type = None
    query_text = None
    query_id = None
    query_response = None

    def __init__(self, object_type, query_text):

        self.object_type = object_type
        self.query_text = query_text

    def is_query_valid(self, client):
        resp = client.describe_statement(Id=self.query_id)
        return resp['ResultRows'] >= 0

    def save_code(self, client):
        if self.is_query_valid(client):
            resp = client.get_statement_result(Id=self.query_id)
            code = []
            for row in resp['Records']:
                code.append(row[0]['stringValue'] + '\n')
            with open(f'out/DDL_{self.object_type}.sql', 'w') as f:
                f.writelines(code)
            return True
        else:
            return False


def read_ddl_queries():
    queries = []
    for f in os.listdir('.'):
        if f.endswith(".sql"):
            object_type = re.search(r'^(.*)_ddl\.sql', f, )
            with open(f, 'r') as file:
                queries.append(Query(object_type.group(1), file.read()))
                #queries_dict[object_type.group(1)] = file.read()
    return queries


def execute_ddl_queries():
    for q in QUERIES:
        resp = RS_CLIENT.execute_statement(
            ClusterIdentifier=RS_CLUSTER
            , Database=RS_DATABASE
            , SecretArn=RS_SECRET_ARN
            , Sql=q.query_text
            , StatementName=f'mobilize_ddl_extraction_{q.object_type}'
        )
        q.query_id = resp['Id']

'''
=================================
== Global variables definition ==
=================================
'''

args = sys.argv

QUERIES = read_ddl_queries()
RS_CLIENT = get_client()
'''
RS_CLUSTER = args[1]
RS_DATABASE = args[2]
RS_SECRET_ARN = args[3]
'''

RS_CLUSTER = 'redshift-cluster-1'
RS_DATABASE = 'dev'
RS_SECRET_ARN = 'arn:aws:secretsmanager:us-east-2:049502660834:secret:dev/redsfhift-cluster-1-edSdeq'

execute_ddl_queries()

for q in QUERIES:
    i = 0
    while i < 15:
        print(f'Validation number {i}')
        if q.save_code(RS_CLIENT):
            break
        time.sleep(1)
        i += 1

if __name__ == 'main':
    pass
