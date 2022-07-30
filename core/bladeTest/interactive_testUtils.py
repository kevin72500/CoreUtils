import random,time
import os,sys
import platform as pf
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from time import sleep
import shutil

from loguru import logger
from pywebio.input import FLOAT,NUMBER,input_group,select, textarea,file_upload,checkbox,radio,actions
from pywebio.output import close_popup, output, put_file, put_html, put_image, put_markdown, put_text,popup,put_link,put_code,put_row,put_processbar,set_processbar,put_error,put_warning,toast,put_grid,put_button,put_table,use_scope,span,clear,remove
from pywebio import start_server,session,platform
from core.bladeTest.main import RemoteRunner,generateHtmlReport,running
from core.jmeterTool.swagger2jmeter import swagger2jmeter
from core.jmeterTool.har2jmeter import har2jmeter
from core.xmind2excel import makeCase
from core.utils import CFacker,getDateTime,parseJmeterXml
from core.mqttUtil import NormalMqttGetter,NormalMqttSender
from core.kafkaUtil import general_sender,continue_orderMsg,general_orderMsg,general_orderMsgWithFilter,kafkaFetchServerWithFilter,kafkaFetchServer
from functools import partial
from multiprocessing import Process
import decimal,websockets,asyncio
import json
from functools import partial

import pywebio.output as output
import pywebio.input as input
import pywebio.pin as pin
from pywebio.session import hold



def kafkaSender():
    output.put_markdown("## 请输入kafka连接信息")
    pin.put_input(name='host',label='主机：端口')
    pin.put_input(name='topic',label='主题')
    pin.put_textarea(name='msg',label='消息',rows=10)
    pin.put_input(name='interval',label='发送间隔',value=0)
    def getValueAndCall():
        host=pin.pin.host
        topic=pin.pin.topic
        msg=pin.pin.msg
        interval=int(pin.pin.interval)
        
        if interval==0:
            general_sender(topic=topic,serverAndPort=host,message=msg)
            output.toast(content=f"发送成功: {host} \n {topic} \n {msg}")
        elif interval>0:
            while True:
                general_sender(topic=topic,serverAndPort=host,message=msg)
                output.toast(content=f"发送成功: {host} \n {topic} \n {msg}")
                sleep(int(interval))

    output.put_button(label='提交', onclick=lambda :getValueAndCall())




class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(DecimalEncoder, self).default(o)


@use_scope('content',clear=True)
def kafkaListener():
    '''
    to send kafka message or listener the kafka topic
    :return:
    '''
    try:
        session.set_env(title='testTools')
        clear('content')
        select_type = select("选择kafka操作:",["kafka发送消息","kafka持续接收消息"])

        if select_type=="kafka发送消息":
            kafkaSender()
        
        elif select_type=="kafka持续接收消息":
            put_text(
                "json过滤如：data.deviceId")
            data = input_group("kafka连接配置", [
                input.input("kafka topic，必填", name="topic",value='iotHub'),
                input.input("kafka 地址，如ip:port，必填", name="address",value='192.168.xxx.xxx:9092'),
                input.input("过滤方式，仅支持填json或regx，非必填", name="filter",value='json'),
                input.input("过滤表达式，json使用jmeshpath方式，regx采用abc(.*)bbb的方式，非必填", name="pattern",value="payload.name"),
                input.input("过滤后比对关键字，过滤后的值是否等于输入的值，非必填", name="key",value="status"),
            ])
            
            for one in continue_orderMsg(data['topic'], data['address'], data['filter'], data['pattern'], data['key']):
                for a in one:
                    if a is not None:
                        put_text(f"{getDateTime()} : {data['topic']} --> {a}")

    except Exception as e:
        output.popup(title="error",content=put_text(e))
        clear('content')





if __name__ == '__main__':
    start_server(kafkaListener,port=8080,debug=True,cdn=False,auto_open_webbrowser=True)


