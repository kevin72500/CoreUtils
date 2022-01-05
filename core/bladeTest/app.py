import sys,os
# print(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.extend(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from pywebio.platform.flask import webio_view
from flask import Flask,request
from flask import redirect
from interactive  import myapp



app = Flask(__name__,static_url_path="",static_folder=".",template_folder=".")


# `task_func` is PyWebIO task function
app.add_url_rule('/testTool', 'webio_view', webio_view(myapp),methods=['GET', 'POST', 'OPTIONS'])  # need GET,POST and OPTIONS methods

@app.route('/')
def testTool():
    return redirect('/testTool')


@app.route('/kafka')
def kafkaClient():
    portNum=request.args.get('portNum')
    return redirect('kafkaWebClient'+portNum+'.html')





if __name__=='__main__':
    app.run(host='0.0.0.0', port=8899)