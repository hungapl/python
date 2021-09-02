
import os, uuid, logging
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import pandas as pd
connect_str = 'DefaultEndpointsProtocol=https;AccountName=cluster00mlstore;AccountKey=tnfInFZysfJ2nPMPTGbhX8i3gy3rFaRj/56LIQVf6/reBfv5QFGXK+Vmvh18egrEjhriMS3NqIBk5XucYnhClA==;EndpointSuffix=core.windows.net'


def list_files(connection_string:str, container:str, file_dir: str):
    container = ContainerClient.from_connection_string(conn_str=connection_string, container_name=container)

    blob_list = []
    for blob in container.list_blobs(name_starts_with=file_dir):
            blob_list.append(blob)

    print('Found the {} files: {}'.format(len(blob_list), blob_list.join('\n')))


def download_blob_as_csv(connection_string:str, container:str, file_dir:str, blob_name:str):
    blob_path = file_dir + blob_name
    print('Downloading {}...'.format(blob_path))
    blob = BlobClient.from_connection_string(conn_str=connection_string, container_name=container,
                                             blob_name=blob_path)
    stream = blob.download_blob()
    data = stream.readall()
    return pd.read_csv(data)


def get_matching_files(connection_string:str, container:str, file_dir: str, text:str=None):
    container:ContainerClient = ContainerClient.from_connection_string(conn_str=connection_string, container_name=container)
    print('Finding files matching {}...'.format(file_dir))
    blob_list = []
    for blob in container.list_blobs(name_starts_with=file_dir):
        if blob.name.find(text) != -1:
            blob_list.append(blob.name.replace(file_dir, ''))

    print('Found {} matching files: {}'.format(len(blob_list), blob_list))
    return blob_list

cluster06file = "DefaultEndpointsProtocol=https;AccountName=cluster06file;AccountKey=lVPYRpAkPll" \
              "/2E1xJwCSg4D8qVTGFeUuMxxb3LknNZ5vRXSyXsWTEDr+p4jZiIrs9J5RDWp9Ht7ICeK7BCGsnw==;EndpointSuffix" \
              "=core.windows.net"
container = 'gm-dev'
file_dir = 'rasvalleyclone/loading_exchanges/'

cluster30mlstore = 'DefaultEndpointsProtocol=https;AccountName=cluster30mlstore;AccountKey=5vZ5TWUWenPbcy8LrC7a/o9gMT5p4wQHdUU9VVOE1BIo36feDWwuIfPON4g8Blgl9C02xn8GqPAIhtyc2fzuvA==;EndpointSuffix=core.windows.net'
cluster00mlstore = 'DefaultEndpointsProtocol=https;AccountName=cluster00mlstore;AccountKey=s2twJjN9eUMkstgrMrf1GqSPgo1mF+xFQVyIzu0TcECBl7mJVag+LWX7YOwrkhxu/8tU7W71QV7AjTOpRrfPeJaw==;EndpointSuffix=core.windows.net'
lhd_container = 'edgelhd'
lhd_file_dir ='{}/data/{}/{}'
ceourwharf_527 = 'd5cd5a93-e868-4f7d-b0da-dd09c2f1395e'
#matching_blobs = get_matching_files(cluster00mlstore, lhd_container, lhd_file_dir.format('fmg_cloudbreak', '2020-11-24'), 'TruckActivities-2020-10-19')
file_dir = lhd_file_dir.format('coeurwharf',  '2020-12-02', ceourwharf_527)
matching_blobs = get_matching_files(cluster30mlstore, lhd_container, file_dir, '2020-12-02')
for b in matching_blobs:
    df = download_blob_as_csv(cluster30mlstore, lhd_container, file_dir, b)
    df.to_csv('/data/model/edgelhd/input/coeurwharf_20201203/' + b, index=False)