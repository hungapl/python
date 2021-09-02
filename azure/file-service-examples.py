import logging
import os
from azure.storage.fileshare import ShareClient


def match_by_name(filename, file_name_to_match):
    return filename.find(file_name_to_match) != -1

# Reference:
# https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/storage/azure-storage-file-share/samples/file_samples_share.py#L87
def download_matching_files(connection_string:str, file_share_name:str, file_dir: str, file_name:str,
                            dest_dir: str, match_function=match_by_name):
    share: ShareClient = ShareClient.from_connection_string(connection_string, file_share_name)
    file_list = list(share.list_directories_and_files(directory_name=file_dir))
    logging.info('Found {} files in {}'.format(len(file_list), file_dir))

    if not os.path.isdir(dest_dir):
        os.makedirs(dest_dir)

    matching_files = list()
    for d in file_list:
        if d['is_directory']:
            continue
        if match_function(d['name'], file_name):
            matching_files.append({'file_dir':file_dir, 'file_name':d['name']})
    logging.info('Found {} matching files in {}'.format(len(matching_files), file_dir))
    i = 0
    for m in matching_files:
        file_name = m['file_name']
        file_path = m['file_dir'] + file_name
        my_file = share.get_file_client(file_path)
        logging.info('Download {} to {}'.format(file_name, dest_dir))
        with open(dest_dir + file_name, "wb") as data:
            stream = my_file.download_file()
            data.write(stream.readall())
        i = i + 1
    logging.info('Downloaded {} files to {}'.format(len(matching_files), dest_dir))

logging.basicConfig(level=logging.INFO)
cluster06file = 'DefaultEndpointsProtocol=https;AccountName=cluster06file;AccountKey=lVPYRpAkPll/2E1xJwCSg4D8qVTGFeUuMxxb3LknNZ5vRXSyXsWTEDr+p4jZiIrs9J5RDWp9Ht7ICeK7BCGsnw==;EndpointSuffix=core.windows.net'
cluster30mlstore = 'DefaultEndpointsProtocol=https;AccountName=cluster30mlstore;AccountKey=5vZ5TWUWenPbcy8LrC7a/o9gMT5p4wQHdUU9VVOE1BIo36feDWwuIfPON4g8Blgl9C02xn8GqPAIhtyc2fzuvA==;EndpointSuffix=core.windows.net'
cluster23file = 'DefaultEndpointsProtocol=https;AccountName=cluster23file;AccountKey=wZQO5w+QO2C2kGbjq7KqdLZhBrguxWai+6Zkohy7KI6TFCZPrqjRlY0UjnClZMkgitGwPhRYEutw7uVjxxHOYg==;EndpointSuffix=core.windows.net'
cluster00mlstore = 'DefaultEndpointsProtocol=https;AccountName=cluster00mlstore;AccountKey=s2twJjN9eUMkgrMrf1GqSPgo1mF+xFQVyIzu0TcECBl7mJVag+LWX7YOwrkhxu/8tU7W71QV7AjTOpRrfPeJaw==;EndpointSuffix=core.windows.net'
file_dir = 'support/nutrienaurorapracestripclone/mstarFiles/nodes/default/temp/tae/20201010/'
tae_file_dir = 'support/{}/mstarFiles/nodes/default/temp/tae/{}/'
lhd_file_dir = 'support/{}/mstarFiles/nodes/default/temp/tae/{}/'
log_dir = 'support/{}/mstarFiles/nodes/default/logs/'
f = 'nutrienauroraprestripclone_508_20201010180151_20201010220000'
dest_dir = '/home/alice/temp/'
match_function = lambda x: x.find(f) != -1
#download_matching_files(cluster06file, file_dir, f, dest_dir, match_function)
# download_matching_files(connection_string=cluster23file,
#                         file_share_name='app-services',
#                         file_dir=file_dir0.format('rasvalleyclone', '20201115'),
#                         file_name='rasvalleyclone_C-19-138_20201113191326_20201114152231',
#                         dest_dir='/data/model/edgetruckactivity/input/rasvalleyclone-20201115/')

# download_matching_files(connection_string=cluster06file,
#                         file_share_name='app-services',
#                         file_dir=file_dir0.format('nutrienauroragypstackclone', '20201118'),
#                         file_name='nutrienauroragypstackclone_BM0355_20201118192309_20201119013000',
#                         dest_dir='/data/model/edgetruckactivity/input/nutrienauroragypstackclone-20201119/')

# download_matching_files(connection_string=cluster23file,
#                         file_share_name='app-services',
#                         file_dir=log_dir.format('rasvalleyclone'),
#                         file_name='minestar-site.log',
#                         dest_dir='/home/alice/temp/')

# download_matching_files(connection_string=cluster06file,
#                         file_share_name='app-services',
#                         file_dir=file_dir0.format('plsmplsbhqclone', '20201025'),
#                         file_name='20201021',
#                         dest_dir='/data/model/edgetruckactivity/input/plsmplsbhqclone-20201026/')

# download_matching_files(connection_string=cluster00mlstore,
#                         file_share_name='app-services',
#                         file_dir=tae_file_dir.format('fmgcloudbreak', '20201122'),
#                         file_name='fmgcloudbreak_WL016_20201116',
#                         dest_dir='/data/model/edgelhd/input/fmgcloudbreak-20201123/')

def input_files_only(filename, file_name_to_match):
    return match_by_name(filename, file_name_to_match) and filename.endswith('input.csv')

cluster30file='DefaultEndpointsProtocol=https;AccountName=cluster30file;AccountKey=MHhFfLu7tNAiJq/OLidRDioEXltejGgiSUaMqq3qxEBf+H6GPDHqZifFk7uEvZRZT8fkHNSLaMkCTS7s0RDfPg==;EndpointSuffix=core.windows.net'

for e in ['682', '683', '681', '710', '291']:
    for d in range(15, 29):
        date_folder = '202102{}'.format(d)
        download_matching_files(connection_string=cluster30file,
                                file_share_name='app-services',
                                file_dir=tae_file_dir.format('longviewquarry', date_folder),
                                file_name='longviewquarry_' + e,
                                dest_dir='/data/model/edgetruckactivity/input/longviewquarry-20210225/',
                                match_function=input_files_only)