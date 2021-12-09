import time,datetime
import os,json
import logging
import threading
from kafka import KafkaConsumer,KafkaProducer
from kafka.client_async import KafkaClient
import jmespath


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
    def doFileterFromComsumer(self,jmeshPath,matchStr,store=False):
        '''
            :param keyStr: search patten
            :param businessData: total data
            :return: key or key list
        '''
        print('Start filter....')
        resStore=[]
        for one in self.kafkaConnection:
            # print(one.value.decode())
            businessData = json.loads(one.value.decode())
            flag=jmespath.search(jmeshPath,businessData)
            # print(flag)
            if flag==matchStr:
                # if store==True:
                #     resStore.append(one.value.decode())
                #     print(one.value.decode())
                print(f'结果匹配到了: {matchStr}')
                print(one.value.decode())
    def doSendFromProducer(self,message,partition=None,key=None):
        self.kafkaConnection.send(self.topic,value=bytes(message,encoding='utf-8'),partition=partition,key=key)

if __name__ == '__main__':
    # start_consumer("device_default_prop","192.168.125.149:9092")
    # start_consumer()
    # kafkaOper("iotHub","192.168.125.149:9092").getConsumer().doFileterFromComsumer("payload.name","status")
    msg='{"messageId":"18db3242-18ff-4c62-958a-321457ca9211","payload":{"name":"onff","timestamp":"1639017000529","alias":"在离线状态","items":[{"keyName":"onff","value":"Offline","alias":"在线"}],"virDevUid":"908287192640741398"},"timestamp":"1639017000529"}'
    kafkaOper("device_default_state","192.168.125.149:9092").getProducer().doSendFromProducer(msg)