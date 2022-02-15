import requests
from loguru import logger
from core.utils import jsonFilter,regxFilter,containFilter
class HttpOper:
    def __init__(self):
        """session管理器, 后续引入登录或者token处理"""
        self.session = requests.session()
        self.res=None
    def call(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        self.res=self.session.request(method,url, params=params, data=data, json=json, headers=headers,**kwargs)
        return self
    def resCheck(self,flag="",pattern="",key=""):
        logger.info(f'oriStr is: {self.res.text}')
        if flag=='json':
            if not jsonFilter(self.res.text, flag, pattern, key)[0]:
                return False
            return True
        if flag=="regx":
            if not regxFilter(self.res.text, flag, pattern, key)[0]:
                return False
            return True
        if flag=="contain":
            if not containFilter(self.res.text, key)[0]:
                return False
            return True
    def getRes(self):
        return self.res
        
    def close_session(self):
        """关闭session"""
        self.session.close()

if __name__ == '__main__':

    url = 'http://192.168.xxx.xxx:9499/device/v1/api/devices/926499854176743469'
    header={"content-type":"application/json;charset=UTF-8"}
    req = HttpOper()
    # res = req.call("get", url, headers=header).resCheck(flag="json", pattern="data.id", key="926499854176743469")
    # print(res)
    res = req.call("get", url, headers=header).resCheck(flag="regx", pattern="classifyName\":\"(.*)\"", key="水冷主机")
    print(res)
    # res = req.call("get", url, headers=header).resCheck(flag="contain", key="926499854176743469")
    # print(res)