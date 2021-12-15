import datetime
import json
import threading
from kafka import KafkaConsumer,KafkaProducer
from kafka.client_async import KafkaClient
import jmespath
import threading
from loguru import logger

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
    def doFileterFromComsumer(self,jmeshPath="",regMatchString="",matchStr="",keepListen=False,store=False):
        print('Start filter....')
        resStore=[]
        for one in self.kafkaConnection:
            # print(one.value.decode())
            businessData = json.loads(one.value.decode())
            if regMatchString!="" and jmeshPath!="":
                logger.error("can't using both jsonPath and regx filter in the same time")
                return False
            try:
                # print(flag)
                if jmeshPath!="":
                    flag=jmespath.search(jmeshPath,businessData)
                    if flag==matchStr:
                        logger.warning(f'Topic: {self.topic} 在时间：{datetime.datetime.now()}->结果匹配到: {matchStr}了')
                        logger.info(f'{one.value.decode()}')
                else:
                    logger.info(f'{one.value.decode()}')
            except Exception as e:
                logger.error('json 解析失败')
                logger.error(f'{one.value.decode()}')
    def doSendFromProducer(self,message,partition=None,key=None):
        self.kafkaConnection.send(self.topic,value=bytes(message,encoding='utf-8'),partition=partition,key=key)


def general_monitor(topic="",serverAndPort="localhost:9092",pattern="",key=""):
    kafkaOper(topic,serverAndPort).getConsumer().doFileterFromComsumer(pattern,key)

def multi_topic_listener(topicList=[],serverAndPortList=[],patternList=[],keyList=[]):
    threadList=[]
    for one in zip(topicList,serverAndPortList,patternList,keyList):
        (a,b,c,d)=one
        # print(f"{a},{b},{c},{d}")
        threadList.append(threading.Thread(target=general_monitor,args=(a,b,c,d)))
    for one in threadList:
        one.start()
        one.join()


if __name__ == '__main__':
    # multi_topic_listener(topicList=['topic','topic1','topic2'],serverAndPortList=["ip:port","ip:port","ip:port"]
    # ,patternList=["json.data.id","json.data.id","json.data.id"],keyList=["assertingData1","assertingData2","assertingData3"])


    multi_topic_listener(topicList=['topic',],serverAndPortList=["ip:port"],patternList=["json.data.id"],keyList=["assertingData"])