from core.httpUtil import HttpOper
sender=HttpOper()
res=sender.call(method='get',url='http://www.baidu.com')
print(res.getResContent())