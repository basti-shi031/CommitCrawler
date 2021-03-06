import json

import requests
from requests_toolbelt.multipart import encoder

from Query import Query

divider = '----'


# 生成参数
def initData(file_list, meta):
    multiple_files = []
    for file in file_list:
        multiple_files.append((file.url + '/' + file.name, file.raw))
        size = len(file.parent_urls)
        for index in range(size):
            parent_url = file.parent_urls[index]
            parent_raw = file.parent_raws[index]
            multiple_files.append((parent_url + '/' + str(file.name) + divider + 'parent' + str(index), parent_raw))
    multiple_files.append(('meta', json.dumps(meta.__dict__)))
    print(json.dumps(meta.__dict__))
    multipart_encoder = encoder.MultipartEncoder(
        fields=multiple_files,
        boundary="xxx---------------xxx",
    )

    return multipart_encoder


# query = Query('https://github.com/CleWang/ThirdPartyLibraryAnalysis/commit/220a1865d80f5bd46cd378d060dfd0ba276b8c57')
# # query = Query('https://github.com/basti-shi031/StatusBarActivity/commit/19e9eb0581e3b467acac34334b60210a12be02c3')
# # query = Query('https://github.com/ReactiveX/RxJava/commit/2edea6b8c8349dc06355d9c0182ba537978d6191')
# file_list, meta = query.query()
# print(file_list)
# multipart_encoder = initData(file_list, meta)
# print(multipart_encoder)
# r = requests.post('http://localhost:12007/DiffMiner/main', data=multipart_encoder,
#                   headers={'Content-Type': multipart_encoder.content_type})
#
# print(r.text)
# print(r.request.body)
# print(r.content)
# print(r.status_code)
# commit_hash = '12312314'
# a = {'commit_hash': commit_hash}
# r = requests.post('http://localhost:12007/DiffMiner/main/fetchMetaCache', json=a)
author = ''
commit_hash = '220a1865d80f5bd46cd378d060dfd0ba276b8c57'
parent_commit_hash = 'd055523c185381f084496d74730988fcd6d4e9f5'
project_name = 'ThirdPartyLibraryAnalysis'
prev_file_path = 'prev/d055523c185381f084496d74730988fcd6d4e9f5/src/main/java/cn/edu/fudan/se/api/FileDbDataFlow.java'
curr_file_path = 'curr/d055523c185381f084496d74730988fcd6d4e9f5/src/main/java/cn/edu/fudan/se/api/FileDbDataFlow.java'
a = {'commit_hash': commit_hash, 'parent_commit_hash': commit_hash, 'project_name': project_name,
     'prev_file_path': prev_file_path, 'curr_file_path': curr_file_path};
r = requests.post("http://localhost:12007/DiffMiner/main/fetchContent", json=a)
content = r.content
print(content)