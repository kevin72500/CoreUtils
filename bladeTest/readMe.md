#目的

主要减少上线 or UAT阶段的工作，将混沌测试检查工作提前并固化。达到一个项目使用，其他项目可复用的效果。
通常公司的业务部署仅包含了主机和docker内的容器，此工具也仅对此部分做了封装，并未包含k8s部分，如需扩展请参考chaosmesh
#用法

（使用前，需要参考创建chaose的命令，具体使用指令可以参考https://github.com/chaosblade-io/chaosblade）
主要用法步骤：
1. 新建chaose
2. 命令行输入
3. 检查命令行输入
4. 等待
5. 检查输出
6. 销毁chaos
本工具已经集成了这6个步骤不用手工输入
只需要在以下格式的文件中输入需要的检查项：
```
{
    "data":[
      {
        "description": "检查cpu利用率大于80%",  #你检查的目标是什么
        "flag":"false",   #是否运行
        "type": "host",   #执行类型，host主机， docker，k8s不支持
        "host":"192.168.xx.xxx", #主机IP
        "port": 22, #主机端口
        "user":"xxxx",  #主机用户名
        "passwd": "xxxxx",  #主机密码
        "execCommand":"blade create cpu load --cpu-percent 80",   #执行命令
        "execCommandExpect": "success",           #执行命令返回项检查，通常指定为success即可
        "dockerName": "",                     #执行类型为docker的时候，需要指定docker的名称，工具可以通过名称去获取docker id
        "checkCommand": "top -b -n 1|grep Cpu|awk '{print $2}'",  #执行chaos命令以后需要检查对应的信息，是否有效果
        "checkExpect": "70",   #效果检查值
        "httpCheckCommand": {                            #http请求检查服务是否可用或者返回是否正确
          "url":"http://192.168.xxxx.195:18086/query",
          "method":"POST",
          "header":{},
          "cookie":{},
          "params":{"q":"show databases"},
          "json":{}
        },
        "httpExpect": "results"                    #http检查期望返回值，包含认为为真
      },
    {
        "description": "检查docker中CPU大于80%",
        "flag":"false",
        "type": "docker",
        "host":"192.168.xxx.xxx",
        "port": 22,
        "user":"xx",
        "passwd": "xxx",
        "execCommand":"blade create docker cpu fullload --cpu-percent 80 --blade-tar-file /opt/chaosblade.tar.gz",
        "execCommandExpect": "success",
        "dockerName": "test_mysql",
        "checkCommand": "docker stats --no-stream",
        "checkExpect": "mysql",
        "httpCheckCommand": "",
        "httpExpect": ""
      },
      {
        "description": "检查进程被杀掉后，服务是否可用",
        "flag":"false",
        "type": "docker",
        "host":"192.168.xxx.xxx",
        "port": 22,
        "user":"xxx",
        "passwd": "xxx",
        "execCommand":"blade create docker process kill --process java --blade-tar-file /opt/chaosblade.tar.gz",
        "execCommandExpect": "success",
        "dockerName": "dubbo",
        "checkCommand": "",
        "checkExpect": "",
        "httpCheckCommand": "http://192.168.xxxx.xxxx:8080/api/dev/services~post~ ~ ~{\"Content-Type\": \"application/json;charset=UTF-8\"}",
        "httpExpect": " "
      },
       {
        "description": "检查进程被杀掉后，服务是否可用",
        "flag":"true",
        "type": "docker",
        "host":"192.168.xxxx.xxxx",
        "port": 22,
        "user":"root",
        "passwd": "xxx",
        "execCommand":"blade create docker process kill --process java --blade-tar-file /opt/chaosblade.tar.gz",
        "execCommandExpect": "success",
        "dockerName": "dubbo",
        "checkCommand": "",
        "checkExpect": "",
        "httpCheckCommand": "{"url":"http://www.baidu.com",
                              "method":"get",
                              "cookie":"{}",
                              "params":"{}",
                              "json":"{}"
                                }",
        "httpExpect": " "
      }
    ]
}
```
#F&Q
