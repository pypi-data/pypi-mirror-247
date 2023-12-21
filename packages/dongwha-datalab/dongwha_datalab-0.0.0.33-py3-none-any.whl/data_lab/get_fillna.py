# -*- coding: utf-8 -*-

import boto3
import io
import pandas as pd


# athena ������ ������ ó�� ���δ�.
def athena_excute_query( database, sql, save_path,  AWS_ACCESS_KEY_ID=None, AWS_SECRET_ACCESS_KEY=None, AWS_DEFAULT_REGION=None, athena_bucket='test-uram-athena' ):
    
    ### athena buck �� ã�� �ش� ����� �����ϴ� �����̴�. 
    athena_bucket = create_bucket_path(athena_bucket, save_path)

    ### athena�� �ҷ��´�. 
    if AWS_ACCESS_KEY_ID != None or AWS_SECRET_ACCESS_KEY != None : 
        client = boto3.client('athena',
                              region_name=AWS_DEFAULT_REGION,
                              aws_access_key_id=AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                           )
    else : 
        client = boto3.client('athena',
                          region_name=AWS_DEFAULT_REGION
                       )
        
    
    ### ���׳����� ������ ������. 
    responseE = client.start_query_execution(
        QueryString = sql,
        QueryExecutionContext={ 'Database': database, 'Catalog': 'AwsDataCatalog' },
        ResultConfiguration={'OutputLocation': athena_bucket }
    )
    
    ### �����͸� ������ �ö� ���� ��ٸ���. 
    while (True):
        responseC = client.get_query_execution( QueryExecutionId=responseE['QueryExecutionId'] )
        stateL = responseC['QueryExecution']['Status']['State']
        if (stateL != 'QUEUED' and stateL != 'RUNNING'):
            break
            
    ### ���� �� ������ �並 ���ؼ� ������ �´�. 
    res = client.get_paginator('get_query_results')
    response_iterator = res.paginate(
        QueryExecutionId=responseE['QueryExecutionId'],
        PaginationConfig={
        'MaxItems': 1000,
        'PageSize': 1000,
        'StartingToken': None
        }
    )

    ### ��Ÿ�����͸� �о�´�. 
    meta_json = {}
    for row in response_iterator:
        #print( row['ResultSet']['ResultSetMetadata']['ColumnInfo'] )
        col_info = row['ResultSet']['ResultSetMetadata']['ColumnInfo']
        for row_1 in col_info : 
            meta_json[row_1['Name']] = row_1['Type']
            
    ### Ÿ���� pandas Ÿ������ �����Ѵ�.  
    dataframe_schema = {}
    for column_name, column_type in meta_json.items() :
        if column_type == "varchar":
            column_type = str
        elif column_type == "double" or column_type ==  "decimal":
            column_type = float
        elif column_type == "integer":
            column_type = float
        elif column_type == "boolean":
            column_type = bool

        dataframe_schema[column_name] = column_type
        
    # file name �� ����� �ش�. 
    file_name = responseE['QueryExecutionId']
    file_path = "{0}{1}.csv".format( athena_bucket, file_name  )
    
    
    
    return file_path, dataframe_schema


# In[4]:


def create_bucket_path(athena_bucket, save_path):
    temp_file_path = '/{0}/{1}/'.format( athena_bucket, save_path )
    file_path = temp_file_path.replace("///", '/').replace("//", '/')
    s3_path = "s3:/{0}".format( file_path )
    print("---->",  s3_path ) 
    
    
    return s3_path





def get_s3(file_name, AWS_DEFAULT_REGION, bucket_name = "test-uram-athena"):

    # AWS ���� ���� ����
    file_name = file_name.replace('s3://{0}/'.format(bucket_name), '')


    # S3�� ����
    s3 = boto3.client('s3',  region_name=AWS_DEFAULT_REGION)

    # S3���� ������ �о��
    s3_object = s3.get_object(Bucket=bucket_name, Key=file_name)
    csv_content = s3_object['Body'].read().decode('utf-8')

    # CSV ���ڿ��� Pandas DataFrame���� ��ȯ
    df = pd.read_csv(StringIO(csv_content))

    
    return df 


# In[6]:


def get_athena( database, sql, save_path,  AWS_ACCESS_KEY_ID=None, AWS_SECRET_ACCESS_KEY=None, AWS_DEFAULT_REGION="ap-northeast-2", athena_bucket='test-uram-athena' ):
    file_path, meta = athena_excute_query(   database, sql, save_path,  AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, athena_bucket )
    
    
    print( 'file_path : ', file_path)
    
    df = get_s3( file_path , AWS_DEFAULT_REGION )  
#     print( file_csv ) 
#     print( meta ) 
#     df = pd.DataFrame(file_csv[1:], columns = file_csv[0]).replace('', None).astype(meta)
    return df 
    
    
def fillna_by_method(df, method, group_columns=None):
    
    
    if method not in ['���', '�߾Ӱ�', '������', '���İ�'] or type(method) != str: 
        return "[ERROR] method ���� STRING Ÿ������ '���', '�߾Ӱ�', '������', '���İ�' �� �� �� �ֽ��ϴ�."
        
    
    if  group_columns==None : 
        if method == '���':
            df = df.fillna(df.mean())
            return df 
        
        elif  method == '�߾Ӱ�':
            df = df.fillna(df.median())
            return df
        
        elif  method == '������':
            df = df.fillna(method='ffill')
            return df
        
        elif  method == '���İ�':
            df = df.fillna(method='bfill')
            return df
            
        
    
    else : 
        value_columns = df.columns.difference(group_columns).tolist()
        
        if method == '���':
            group_means = df.groupby(group_columns)[value_columns].mean().reset_index()
            df = df.merge(group_means, on=group_columns, suffixes=('', '_���'), how='left')
            for col in value_columns:
                df[col] = df[col].combine_first(df[col+'_���'])
            df = df.drop(columns=[col+'_���' for col in value_columns])


        elif method == '�߾Ӱ�':
            group_medians = df.groupby(group_columns)[value_columns].median().reset_index()
            df = df.merge(group_medians, on=group_columns, suffixes=('', '_�߾Ӱ�'), how='left')
            for col in value_columns:
                df[col] = df[col].combine_first(df[col+'_�߾Ӱ�'])
            df = df.drop(columns=[col+'_�߾Ӱ�' for col in value_columns])


        elif method == '������':
            grouped = df.groupby(group_columns)
            df[value_columns] = grouped[value_columns].transform(lambda x: x.ffill())


        elif method == '���İ�':
            grouped = df.groupby(group_columns)
            df[value_columns] = grouped[value_columns].transform(lambda x: x.bfill())

    return df
    
    

    
def get_fillna(database, sql, save_path, method, group_columns=None, AWS_ACCESS_KEY_ID=None, AWS_SECRET_ACCESS_KEY=None, AWS_DEFAULT_REGION="ap-northeast-2", athena_bucket='test-uram-athena' ):
    if AWS_ACCESS_KEY_ID != None or AWS_SECRET_ACCESS_KEY != None : 
        df = get_athena( database, sql, save_path, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, athena_bucket='test-uram-athena' )
        df = fillna_by_method( df, method, group_columns )
    else : 
        df = get_athena( database, sql, save_path, athena_bucket='test-uram-athena' )
        df = fillna_by_method( df, method, group_columns )
    return df
    
    