#!/anaconda3/envs/xxx/bin python3.7
# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @File: main.py
# @Author: oupeng
# @Time: 9月 23, 2021
# ---
import json
import time
from fabric import Connection,SerialGroup
from loguru import logger
from requests import session
from copy import deepcopy
import csv
class RemoteRunner(object):
    '''
    run command in remote host
    '''
    def __init__(self, host, port, user, passwd):
        '''
        :param host:
        :param port:
        :param user:
        :param passwd:
        result will be store in instance res variables
        '''
        self.host = host
        self.port = port
        self.user = user
        self.passwd = {"password": passwd}
        self.conn = Connection(host=self.host, user=self.user, port=self.port, connect_kwargs=self.passwd)
        self.res=""
        self.containerList=[]
        self.commandList=[]
    def __enter__(self):
        return self
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.conn.close()
    def upload_file(self, localFilePath, remoteFilePath):
        '''
        :param localFilePath:
        :param remoteFilePath:
        :return:
        '''
        # logger.info(f"localFilePath: {localFilePath}")
        # logger.info(f"remoteFilePath: {remoteFilePath}")
        self.conn.put(local=localFilePath, remote=remoteFilePath)
        return self
    def download_file(self, localFilePath, remoteFilePath):
        '''
        :param localFilePath:
        :param remoteFilePath:
        :return:
        '''
        # logger.info(f"localFilePath: {localFilePath}")
        # logger.info(f"remoteFilePath: {remoteFilePath}")
        self.conn.get(remote=remoteFilePath, local=localFilePath)
        return self
    def exec_cmd(self, cmd):
        '''
        :param cmd: command in running on the host
        :return:
        '''
        logger.info(f"cmd: {cmd}")
        res = self.conn.run(cmd)
        # logger.info(f'cmd stdout is: {res.stdout.strip()}')
        # logger.error(f'cmd stdout is: {res.stderr.strip()}')
        self.res=res
        return self
    def exec_on_multi(self,*hosts,cmd):
        '''
        :param hosts: host list,contain lots of host
        :param cmd: command in running on the host
        :return:
        '''
        logger.info(f"hosts: {hosts}")
        logger.info(f"cmd: {cmd}")
        res=SerialGroup(hosts).run(cmd)
        # logger.info(f'cmd stdout is: {res.stdout.strip()}')
        # logger.error(f'cmd stdout is: {res.stderr.strip()}')
        self.res=res
        return self
    def exec_check_by_cmd(self,cmd,expect):
        '''
        :param cmd: command
        :param expect: command expect str
        :return:
        '''
        self.exec_cmd(cmd)
        stdout = self.res.stdout.strip()
        logger.info(f"result is: {stdout}, expect is: {expect}")
        if expect in stdout:
            return True
        else:
            return False
    def exec_check_contain(self,expect):
        '''
        :param expect: expect str
        :return:
        '''
        stdout=self.res.stdout.strip()
        logger.info(f"result is: {stdout}, expect is: {expect}")
        if expect in stdout:
            # logger.info(f"expect: {expect}")
            # logger.info(f"stdout: {stdout}")
            return True
        return False
    def exec_check_equal(self,expect):
        '''
        :param expect: expect str, exactly same
        :return:
        '''
        stdout=self.res.stdout.strip()
        logger.info(f"result is: {stdout}, expect is: {expect}")
        if expect == stdout:
            # logger.info(f"expect: {expect}")
            # logger.info(f"stdout: {stdout}")
            return True
        return False
    def exec_check_request_alive(self,url,method,data="",json="",*kwargs):
        '''
        check service is available using return code 200
        :param url:
        :param method:
        :param data:
        :param json:
        :param kwargs:
        :return:
        '''
        resp=None
        if method.lower() == 'post':
            resp = session().post(url, data, json)
        elif method.lower() == 'get':
            resp = session().post(url, data, json)
        if resp.status_code==200:
            return True
        else:
            return False
    def exec_check_request_response(self,url,method,data="",json="",expect="",*kwargs):
        '''
        check service ok, using response code by contain
        :param url:
        :param method:
        :param data:
        :param json:
        :param expect:
        :param kwargs:
        :return:
        '''
        resp = None
        if method.lower() == 'post':
            resp = session().post(url, data, json)
        elif method.lower() == 'get':
            resp = session().post(url, data, json)
        if expect in resp.text:
            return True
        else:
            return False
    def prepare_blade(self):
        '''
        :return: blade binaries will be placed in /opt/chaos/chaosblade-1.2.0/, and add blade in path
        '''
        self.exec_cmd("cd /opt;rm -rf chaos*")
        self.upload_file("chaosblade.tar.gz", "/opt")
        self.exec_cmd('cd /opt; mkdir chaos;tar -xzvf chaosblade.tar.gz -C ./chaos;')
        self.exec_cmd('echo "export PATH=$PATH:/opt/chaos/chaosblade-1.2.0/">>~/.bashrc')
        return self
    def get_docker_id(self):
        res=self.conn.run("docker ps|awk '{if (NR>2) {print $1}}'")
        self.containerList=deepcopy(res.stdout.strip().split('\n'))
        return self

    def run_docker_cmd(self,cmd,uniq_docker_name):
        docker_id=self.conn.run(f"docker ps|grep {uniq_docker_name}|awk '{print $1}'").stdout.strip()
        self.conn.run(f"{cmd} --container-id {docker_id}")
        return self

        # print(type(self.containerList))
        # return self.containerList
    # def __getattribute__(self, *args, **kwargs):
    #     # print(self.__class__.__name__)
    #     # print(f'args: {args}')
    #     # print(f'kwargs: {kwargs}')
    #     if args[0] == 'executeCmd':
    #         print("#"*20)
    #     return object.__getattribute__(self, *args, **kwargs)
if __name__ == "__main__":
    f=open("cmdCase.csv")
    for one in csv.DictReader(f):
        time.sleep(5)
        if one['flag']=="true":
            if one['dockerCommand']!="":
                r=RemoteRunner(host=one['host'],port=int(one['port']),user=one['user'],passwd=one['passwd'])
                r.run_docker_cmd(one['dockerCommand']).exec_check_contain(one['execCommandExpect'])
                time.sleep(1)
                r.exec_check_by_cmd(one['checkCommand'],one['exepect'])
            else:
                r=RemoteRunner(host=one['host'],port=int(one['port']),user=one['user'],passwd=one['passwd'])
                r.exec_cmd(one['execCommand']).exec_check_contain(one['execCommandExpect'])
                time.sleep(1)
                r.exec_check_by_cmd(one['checkCommand'],one['exepect'])
    # r = RemoteRunner('192.168.118.178', 22, 'root', "")
#     # # print(r.exec_cmd('uname -a').exec_check_contain('Linux'))
#     # # r.upload_file("chaosblade.tar.gz","/opt")
#     # r.exec_cmd('cd /opt; mkdir chaos;tar -xzvf chaosblade.tar.gz -C ./chaos; cd ./chaos/chaos-1.2.0')
#     # r.prepare_blade()
#     print("*"*20)
#     r.get_docker_id()
#     print(r.containerList)
# res=Connection(host='192.168.118.178', port=22, user='root', connect_kwargs={"password":""}).run("docker ps|awk '{if (NR>2) {print $1}}'")
# print(res.ok)
# if '\n' in res.stdout.strip():
#     print('find return ')
# print(res.stdout.strip().split('\n'))
# print(res.stderr)
