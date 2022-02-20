import random,time
import os,sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from swaggerjmx.convert import conversion
from swaggerjmx.settings import Settings as ST
import traceback



def swagger2jmeter(url):

    #  swagger_url
    try:
        ST.swagger_url = url
        #  report_path
        ST.report_path = 'jmx'
        # 开始转换
        conversion()
        # print(os.path.abspath(os.path.dirname(__file__))+os.sep+'jmx'+os.sep)
        upperDir=os.path.abspath(os.path.dirname(__file__))+os.sep+'jmx'+os.sep
        for x,y,z in os.walk(os.path.abspath(os.path.dirname(__file__))+os.sep+'jmx'+os.sep):
            return upperDir+"".join(z)
    except Exception as e:
        print(traceback.format_exc())
        return "switch to jmeter script error"