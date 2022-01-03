from pywebio.platform.flask import webio_view
from flask import Flask
from flask import redirect
from core.bladeTest.interactive  import myapp,kafkaListener,uploadXmind,oneCheck,onePageInput,jmeterScriptGen,myFackData
from core.kafkaUtil import kafkaFetchServer
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