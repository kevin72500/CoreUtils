from core.httpUtil import HttpOper,callLog
sender=HttpOper()
res=sender.call(name='百度',method='get',url='http://www.baidu.com')
res.setExportParam(paramName)
print(res.resCheck(flag='contain',pattern="baidu"))
for one in callLog:
    print(one.name)
    print(one.status)
    print(one.callTime)
    print(one.result)