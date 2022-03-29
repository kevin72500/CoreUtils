import setuptools
import platform

win_requires=['fabric==2.6.0','pytest==6.2.5','pywebio==1.4.0','requests==2.26.0','loguru==0.5.3','jinja2==3.0.2','openpyxl==3.0.9','xmindparser==1.0.9','jmespath==0.10.0','pymysql==1.0.2','swaggerjmx==1.0.9','faker==8.12.1','websockets==10.1','pywebio==1.4.0','kafka-python==2.0.2','flask==2.0.2','Werkzeug==2.0.2','paho-mqtt==1.5.1','pycryptodome==3.12.0','msgpack==1.0.3','redis==4.1.3','python-dotenv==0.19.2','jsonschema']
linux_requires=['fabric==2.6.0','pytest==6.2.5','pywebio==1.4.0','requests==2.26.0','loguru==0.5.3','jinja2==3.0.2','openpyxl==3.0.9','xmindparser==1.0.9','jmespath==0.10.0','pymysql==1.0.2','swaggerjmx==1.0.9','faker==8.12.1','websockets==10.1','pywebio==1.4.0','kafka-python==2.0.2','flask==2.0.2','Werkzeug==2.0.2','paho-mqtt==1.5.1','pycrypto==2.6.1','msgpack==1.0.3','redis==4.1.3','python-dotenv==0.19.2','jsonschema']

if platform.system()=='Windows':
    cur_requires=win_requires
elif platform.system()=='Linux':
    cur_requires=linux_requires
elif platform.system()=='Darwin':
    cur_requires=linux_requires


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="khandytool",
    version="0.2.47",
    author="Ou Peng",
    author_email="kevin72500@qq.com",
    description="khandytool, handy core in testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kevin72500/khandytool",
    packages=setuptools.find_packages(),
    package_data={'core.jmeterTool.har2jmeter_utils': ['templates/*'],'core.bladeTest': ['jmx/*'],'core.bladeTest': ['xmindStructure.jpg']},
    install_requires=cur_requires,
    entry_points={
        'console_scripts': [
            'khandytool=khandytool:core'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
