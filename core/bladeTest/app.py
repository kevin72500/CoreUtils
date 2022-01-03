import sys,os
# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.extend(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pywebio.platform.flask import webio_view
from flask import Flask
from flask import redirect
from interactive  import myapp,kafkaListener,uploadXmind,oneCheck,onePageInput,jmeterScriptGen,myFackData
from ..kafkaUtil import kafkaFetchServer
from multiprocessing import Process


app = Flask(__name__,static_url_path="",static_folder=".",template_folder=".")


# `task_func` is PyWebIO task function
app.add_url_rule('/testTool', 'webio_view', webio_view(myapp),
            methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods


@app.route('/kafka')
def kafkaClient():
    return redirect('kafkaWebClient.html')



Process(target=kafkaFetchServer).start()

app.run(host='localhost', port=8899)