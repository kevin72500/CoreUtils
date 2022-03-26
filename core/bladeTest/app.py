import sys,os
sys.path.extend(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pywebio.platform.flask import webio_view
from flask import Flask,request,render_template,session
from flask import redirect
# from core.bladeTest.interactive import myapp


staticPath=os.path.abspath(os.path.expanduser('~'))
app = Flask(__name__)#,static_url_path="/static",static_folder="static",template_folder="templates")
g_res=None

# `task_func` is PyWebIO task function
# app.add_url_rule('/testTool', 'webio_view', webio_view(myapp),methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods

@app.route('/*')
def testTool():
    global g_res
    return g_res


# @app.route('/kafka')
# def kafkaClient():
#     portNum=request.args.get('portNum')
#     ip=request.args.get('ip')
#     print(session.get('host'))
#     # return redirect(f'/static/kafkaWebClient{portNum}.html')
#     return render_template('kafkaWebClient.html',ip=ip,portNum=portNum)

def run(port=8899,retStr="Not set when your start app"):
    global g_res=retStr
    app.run(host='0.0.0.0', port=port)


if __name__=='__main__':
    app.run(host='0.0.0.0', port=8899)