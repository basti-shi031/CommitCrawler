import requests

import Api
import Message
import U
from CommitCache import CommitCache
from Net.DataNet import DataNet
from Query import Query
from Result import Result
from util.UrlUtils import UrlUtils


def checkFileRaw(file_list):
    success = True
    for file in file_list:
        if not hasattr(file, 'raw'):
            success = False
            break
    return success


class MetaNet(object):
    @staticmethod
    def fetchMetaFromMiner(commit_hash, project_name, self2):
        a = {'commit_name': commit_hash, 'project_name': project_name}
        #U.p(commit_hash, project_name)
        r = requests.post(Api.FETCH_META, json=a)
        if r.status_code == 200:
            return True,r.content
            # self2.send_response(200)
            # self2.end_headers()
            # self2.wfile.write(r.content)
        else:
            return False,"error fecth meta file from cldiff"

    @staticmethod
    def fetchMetaFromGithub(commit_hash, project_name, self2, url):
        # 没有缓存，向github请求meta信息
        query = Query(url)
        status_code, message, content = query.query()
        resultContent = None
        if status_code == -1:
            #     无效url，不访问服务器
            # self2.send_response(200)
            # self2.end_headers()
            # result = Result(True, "please enter correct commit url")
            # self2.wfile.write(result.__dict__.__str__().encode())
            resultContent = "invalid github commit url"
            return False, resultContent

        elif status_code == 200:
            if message is not Message.success:
                # self2.send_response(200)
                # self2.end_headers()
                # result = Result(True, message)
                # self2.wfile.write(result.__dict__.__str__().encode())
                return False, message
            else:
                file_list = content[0]
                meta = content[1]
                if not checkFileRaw(file_list):
                    # self2.send_response(200)
                    # self2.end_headers()
                    # result = Result(True, Message.internet_error)
                    # self2.wfile.write(result.__dict__.__str__().encode())
                    return False, "message internet error with github"
                self2.send_response(200)
                self2.end_headers()
                result = Result(True, Message.success)
                # self.wfile.write(result.__dict__.__str__().encode())
                # 访问服务器
                # 此时已经获得所有文件，生成一个
                multipart_encoder = DataNet.initData(file_list, meta)
                # print(multipart_encoder)
                r = requests.post(Api.GENERATE_META, data=multipart_encoder,
                                headers={'Content-Type': multipart_encoder.content_type})
                if r.status_code == 200:
                    # self2.wfile.write(r.content)
                    cache = CommitCache()
                    cache.add_commit_hash(commit_hash, project_name)
                    return True, r.content
                else:
                    return False, "connection error with cldiff"
            #    请求结束
        # 写入数据库
        else:
            if message == Message.internet_error:
                resultContent = "internet error with github"
                return False, resultContent
            # self2.send_response(200)
            # self2.end_headers()
            # result = Result(True, "internet error")
            # self2.wfile.write(result.__dict__.__str__().encode())

    # 请求meta信息
    @staticmethod
    def fetchMeta(form, self2):
        url = UrlUtils.getUrl(form)
        if url == None:
            return False
        # https://github.com/basti-shi031/CommitClawerSever/commit/ad34ef79b84c8ec3a3f71608051c638510ccd330
        # 根据commitUrl生成commitHash 和 projectName
        commit_hash, project_name = UrlUtils.genCommitHashAndProjectName(url)
        # 查找是否存在缓存
        cache = CommitCache()
        isExist = cache.find(commit_hash)
        if isExist:
            # 如果存在缓存，向服务器请求缓存
            flag,content = MetaNet.fetchMetaFromMiner(commit_hash, project_name, self2)
            if flag:
                return flag,content
            else:
                # 向服务器请求缓存程序错误，向GitHub请求Meta
                return MetaNet.fetchMetaFromGithub(commit_hash, project_name, self2, url)
        else:
            return MetaNet.fetchMetaFromGithub(commit_hash, project_name, self2, url)
