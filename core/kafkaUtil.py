import datetime
import json
import threading
from kafka import KafkaConsumer,KafkaProducer
from kafka.client_async import KafkaClient
import jmespath
import threading
from loguru import logger
import re
import websockets
import asyncio

logger.add('kafkaUtil_log.txt',encoding='utf-8')

class kafkaOper(object):
    def __init__(self,topic,bootstrapserver):
        self.topic=topic
        self.bootstrapserver=bootstrapserver
        self.kafkaConnection=None
    def getConsumer(self,clientid="kafkaOper",auto_offset_reset="latest",**args):
        self.kafkaConnection=KafkaConsumer(self.topic,bootstrap_servers=self.bootstrapserver,client_id=clientid,auto_offset_reset=auto_offset_reset)
        return self
    def getProducer(self,clientid="kafkaOper"):
        self.kafkaConnection=KafkaProducer(bootstrap_servers=self.bootstrapserver,client_id=clientid)
        return self
    def getSubscribe(self):
        self.kafkaConnection=KafkaConsumer(bootstrap_servers=self.bootstrapserver)
        return self
    def jsonFilter(self,allStr,pattern,key):
        try:
        # print(flag)
            allStr = json.loads(allStr.value.decode())
            flag=jmespath.search(pattern,allStr)
            if flag==key:
                logger.warning(f'Topic: {self.topic} 在时间：{datetime.datetime.now()}->结果匹配到: {key}了')
                logger.info(f'Total String is: {allStr}')
            # else:
            #     logger.info(f'{allStr}')
        except Exception as e:
            logger.error('json 解析失败')
            logger.error(f'{allStr}')
    def returnJsonFilter(self,allStr,pattern,key):
        try:
        # print(flag)
            allStr = json.loads(allStr.value.decode())
            flag=jmespath.search(pattern,allStr)
            if flag==key:
                return allStr
            # else:
            #     logger.info(f'{allStr}')
        except Exception as e:
            logger.error('json 解析失败')
            logger.error(f'{allStr}')

    def returnRegxFilter(self,allStr,pattern, key):
        try:
            allStr = allStr.value.decode()
            flag=re.compile(pattern)
            res=flag.findall(allStr)
            # print(res)
            if key in "".join(res):
                return allStr
            # else:
            #     logger.info(f'{allStr}')
        except Exception as e:
            logger.error('regx 解析失败')
            logger.error(f'{allStr}') 

    def regxFilter(self,allStr,pattern, key):
        try:
            allStr = allStr.value.decode()
            flag=re.compile(pattern)
            res=flag.findall(allStr)
            # print(res)
            if key in "".join(res):
                logger.warning(f'Topic: {self.topic} 在时间：{datetime.datetime.now()}->结果匹配到: {res}了')
                logger.info(f'Total String is: {allStr}')
            # else:
            #     logger.info(f'{allStr}')
        except Exception as e:
            logger.error('regx 解析失败')
            logger.error(f'{allStr}') 

    def doFileterFromComsumer(self,flag="",pattern="",matchStr="",keepListen=False,store=False):
        '''
            flag = "json"
            or
            flag ="regx"
        '''
        logger.info('Start filter....')
        resStore=[]
        for one in self.kafkaConnection:
            # print(one)
            # print(flag)
            if flag=="json":
                # logger.info(f"json {one}")
                self.jsonFilter(allStr=one,pattern=pattern,key=matchStr)
            elif flag=="regx":
                # logger.info(f"regx {one}")
                self.regxFilter(allStr=one,pattern=pattern,key=matchStr)
            elif flag=="":
                logger.warning(f'Topic: {self.topic} 在时间：{datetime.datetime.now()}->未加入匹配的消息是: {one}了')
                
    def doSendFromProducer(self,message,partition=None,key=None):
        self.kafkaConnection.send(self.topic,value=bytes(message,encoding='utf-8'),partition=partition,key=key)

    def retrivalFixedMsg(self,interval_ms,getNum):
        self.kafkaConnection.subscribe(self.topic)
        # print(self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=False).items())
        # return self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=False).items()
        resList=[]
        while len(resList)<getNum:
            for k,v in self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=True).items():
                # print(f"{k}--->{v}")
                for one in v:
                    # print(f"data is : {one}")
                    resList.append(one.value.decode())
            # print(len(resList))
        return resList

    def retrivalFixedMsgWithFilter(self,interval_ms,getNum,filterFlag,pattern,matchStr):
        self.kafkaConnection.subscribe(self.topic)
        # print(self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=False).items())
        # return self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=False).items()
        resList=[]
        while len(resList)<getNum:
            for k,v in self.kafkaConnection.poll(timeout_ms=interval_ms,max_records=getNum,update_offsets=True).items():
                # print(f"{k}--->{v}")
                for one in v:
                    print(f"data is : {one}")
                    if filterFlag=='json':
                        try:
                            print(filterFlag)
                            allStr = json.loads(one.value.decode())
                            flag=jmespath.search(pattern,allStr)
                            if flag==matchStr:
                                print(f'got json:::{allStr}')
                                resList.append(one.value.decode())
                        except Exception as e:
                            logger.error('json 解析失败')
                            logger.error(f'{allStr}')
                    elif filterFlag=='regx':
                        try:
                            allStr = one.value.decode()
                            flag=re.compile(pattern)
                            res=flag.findall(allStr)
                            if matchStr in "".join(res):
                                resList.append(one.value.decode())
                        except Exception as e:
                            logger.error('regx 解析失败')
                            logger.error(f'{allStr}') 
            # print(len(resList))
        return resList
    
    def retrivalFlowMsg(self,flag,pattern,key):
        self.kafkaConnection.subscribe(self.topic)
        while True:
        # now = datetime.datetime.utcnow().isoformat() + 'Z'
            msg=self.kafkaConnection.poll(timeout_ms=0,max_records=10)
            for k,v in msg.items():
                for one in v:
                    if flag=="json":
                        yield self.returnJsonFilter(one.value.decode(), pattern, key)
                    elif flag=="regx":
                        yield self.returnRegxFilter(one.value.decode(), pattern, key)
                    else:
                        yield one.value.decode()


def general_orderMsg(topic,serverAndPort,interval_ms,getNum,callbackFlag=False,callbackFuc=None):
    if callbackFlag==False:
        return kafkaOper(topic,serverAndPort).getSubscribe().retrivalFixedMsg(interval_ms,getNum)
    else:
        callbackFuc(kafkaOper(topic,serverAndPort).getSubscribe().retrivalFixedMsg(interval_ms,getNum))


def general_orderMsgWithFilter(topic,serverAndPort,interval_ms,getNum,filterFlag,pattern,matchStr,callbackFlag=False,callbackFuc=None):
    if callbackFlag==False:
        return kafkaOper(topic,serverAndPort).getSubscribe().retrivalFixedMsgWithFilter(interval_ms,getNum,filterFlag,pattern,matchStr)
    else:
        callbackFuc(kafkaOper(topic,serverAndPort).getSubscribe().retrivalFixedMsgWithFilter(interval_ms,getNum,filterFlag,pattern,matchStr))

def continue_orderMsg(topic,serverAndPort,flag,pattern,key):
    yield kafkaOper(topic,serverAndPort).getSubscribe().retrivalFlowMsg(flag,pattern,key)

def general_sender(topic="",serverAndPort="localhost:9092",message=""):
    kafkaOper(topic,serverAndPort).getProducer().doSendFromProducer(message)

def general_listener(topic="",serverAndPort="localhost:9092",flag="",pattern="",key=""):
    kafkaOper(topic,serverAndPort).getConsumer().doFileterFromComsumer(flag,pattern,key)

def multi_topic_listener(topicList=[],serverAndPortList=[],flagList=[],patternList=[],keyList=[]):
    threadList=[]
    for one in zip(topicList,serverAndPortList,flagList,patternList,keyList):
        (a,b,c,d,e)=one
        # print(f"{a},{b},{c},{d}")
        temp=threading.Thread(target=general_listener,args=(a,b,c,d,e))
        temp.start()
        threadList.append(temp)
    for one in threadList:
        one.join()




import asyncio
import websockets
import kafka
import random
from functools import partial

async def kafkaMsgRecv(websocket=None, serverPath='0.0.0.0:9092',topic="testTopic",interval=0,nums=None):
    k_conn=kafka.KafkaConsumer(bootstrap_servers=serverPath)
    k_conn.subscribe(topic)
    while True:
        # now = datetime.datetime.utcnow().isoformat() + 'Z'
        msg=k_conn.poll(timeout_ms=interval,max_records=nums)
        for k,v in msg.items():
            for one in v:
                print(one.value.decode())
                await websocket.send(one.value.decode())
                await asyncio.sleep(random.random() * 3)


async def kafkaMsgRecvWithFilter(websocket=None, serverPath='0.0.0.0:9092', topic="testTopic", interval=0, nums=None):
    k_conn = kafka.KafkaConsumer(bootstrap_servers=serverPath)
    k_conn.subscribe(topic)
    while True:
        # now = datetime.datetime.utcnow().isoformat() + 'Z'
        msg = k_conn.poll(timeout_ms=interval, max_records=nums)
        for k, v in msg.items():
            for one in v:
                print(one.value.decode())
                await websocket.send(one.value.decode())
                await asyncio.sleep(random.random() * 3)



def kafkaFetchServer(interval=0,nums=None,serverPath='0.0.0.0:9092',topic="testTopic",local='127.0.0.1',port=8765):
    start_server = websockets.serve(partial(kafkaMsgRecv,serverPath=serverPath,topic=topic), local, port)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    # multi_topic_listener(topicList=['topic','topic1','topic2'],serverAndPortList=["ip:port","ip:port","ip:port"]
    # ,patternList=["json.data.id","json.data.id","json.data.id"],keyList=["assertingData1","assertingData2","assertingData3"])


    # multi_topic_listener(topicList=['testTopic'],
    # serverAndPortList=["192.168.125.145:9092"],
    # flagList=["regx"],
    # partternList=["abb(.*)bba"],
    # keyList=["555"])


    # multi_topic_listener(topicList=['iotHub','device_default_prop','device_default_state'],
    # serverAndPortList=["192.168.125.145:9092","192.168.125.145:9092","192.168.125.145:9092"],
    # flagList=["json","json","json"],
    # patternList=["payload.virDevUid","payload.virDevUid","payload.deviceId"],
    # keyList=["914959009603264531","914959009603264531","914959009603264536"])

    
    # general_listener(topic="testTopic",serverAndPort="0.0.0.0:9092",flag="",pattern="",key="")


    # kafkaFetchServer()

    for one in continue_orderMsg('testTopic','localhost:9092','regx',"message (\d{4})\-",'2022'):
        for a in one:
            print(a)

    # general_listener(topic="testTopic",serverAndPort="192.168.125.145:9092",flag="regx",pattern=r"abb(.*)bba",key="555")
    # general_sender(topic="testTopic",serverAndPort="192.168.125.145:9092",message='{"abc":{"bcd":"555"}}')

    # k=kafkaOper(topic='ab',bootstrapserver='ab')
    # k.regxFilter("abb555bbc","abb(.*)bbc","555")