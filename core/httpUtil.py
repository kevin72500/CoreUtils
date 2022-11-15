import requests,os
from loguru import logger
from core.utils import jsonFilter,regxFilter,containFilter,findBy,getTimeStamp,timestampsCompare
from dotenv import load_dotenv, find_dotenv
from core.utils import addException,singleton,getTimeStamp
from abc import ABCMeta, abstractmethod

load_dotenv(verbose=True)


callLog=[]

g_exportParam={}


class baseCounter():
    def __init__(self):
        self.status=None
        self.name=None
        self.result=None
        self.callTime=None



class HttpOper():
    def __init__(self):
        """session管理器, 后续引入登录或者token处理"""
        self.session = requests.session()
        self.res=None
        self.exportParam={}
        self.counter=None

    def call(self, method, url, params=None, data=None, json=None, headers=None, name=None,**kwargs):
        logger.debug(f'url : {url}, parma: {params}, data: {data}, json: {json}, headers: {headers}')
        self.counter=baseCounter()

        if name!=None:
            self.counter.name=name
        else:
            self.counter.name=f"{url}"


        startTime=getTimeStamp()
        self.res=self.session.request(method, url, params=params, data=data, json=json, headers=headers,**kwargs)
        endTime=getTimeStamp()
        self.counter.callTime=timestampsCompare(endTime, startTime)

        if self.res.status_code==200:
            self.counter.status='Success'
        else:
            self.counter.status='Failed'

        self.counter.result=self.res.text

        callLog.append(self.counter)
        
        return self

    def resCheck(self,flag="",pattern="",key=""):
        logger.debug(f'oriStr : {self.res.text}')
        if self.res:
            if flag=='json':
                if not jsonFilter(self.res.text, flag, pattern, key)[0]:
                    self.failed=self.failed+1
                    self.counter.status='Failed'
                    return False
                self.counter.status='Success'
                return True
            if flag=="regx":
                if not regxFilter(self.res.text, flag, pattern, key)[0]:
                    self.failed=self.failed+1
                    self.counter.status='Failed'
                    return False
                self.counter.status='Success'
                return True
            if flag=="contain":
                if not containFilter(self.res.text, key)[0]:
                    self.failed=self.failed+1
                    self.counter.status='Failed'
                    return False
                self.counter.status='Success'
                return True
            callLog.append(self.counter)
        else:
            logger.error('please run call() first')

    def resGet(self,flag="",pattern="",key=""):
        logger.debug(f'oriStr : {self.res.text}')
        if self.res:
            if flag=='json':
                if not jsonFilter(self.res.text, flag, pattern, key)[0]:
                    return False
                return jsonFilter(self.res.text, flag, pattern, key)[1]
            if flag=="regx":
                if not regxFilter(self.res.text, flag, pattern, key)[0]:
                    return False
                return regxFilter(self.res.text, flag, pattern, key)[1]
            if flag=="contain":
                if not containFilter(self.res.text, key)[0]:
                    return False
                return containFilter(self.res.text, key)[1]
        else:
            logger.error('please run call() first')

    def setExportParam(self,paramName,flag="",pattern=""):
        logger.debug(f'oriStr is: {self.res.text}')
        temp=findBy(self.res.text,flag=flag,pattern=pattern)
        if temp!=False:
            self.exportParam[paramName]=temp
        else:
            logger.warning(f'can not set exportParm by pattern {pattern}')
        return self

    def getAllRes(self):
        return self.res

    def getResContent(self):
        return self.res.text
    
    def getResCode(self):
        return self.res.status_code
    
    def getExportParam(self,key):
        return self.exportParam[key]

    def updateExportParam(self,key,value):
        self.exportParam[key]=value

    def close_session(self):
        """关闭session"""
        self.session.close()

if __name__ == '__main__':
    host=os.getenv("test_ip1")

    url = 'http://'+host+':9499/device/v1/api/devices/926499854176743469'
    header={"content-type":"application/json;charset=UTF-8"}
    req = HttpOper()

    res = req.call("get", url, headers=header).resCheck(flag="json", pattern="data.id", key="926499854176743469")
    print(res)
    res = req.call("get", url, headers=header).resCheck(flag="regx", pattern="classifyName\":\"(.*)\"", key="水冷主机")
    print(res)
    res = req.call("get", url, headers=header).resCheck(flag="contain", key="926499854176743469")
    print(res)

    res = req.call("get", url, headers=header).setExportParam('p_name','json','data.productName')
    print(res.getExportParam('p_name'))