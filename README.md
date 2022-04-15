# Khandytool
## How to use it
- pip install khandytool
- from core.bladeTest import interactive
- interactive.run(8899), you can change the port if you like

## Purpose 
This core mainly to personal use, and it just wraped some other packages. the perpose that is make some functions are easy to use quickly.
## Main utils
### 1. blade chaose executer(may have problem by install by pip and run; but ok in deply by source)
which have two models to execute ChaoseBlade command in the remote server
### 2. transfer xmind testcase to excel testcase(some formated restrict xmind)
### 3. transfer swagger url to jmeter scripts
using some opensource packge to complish this
### 4. transfer har file to jmeter scripts
### 5. others code snips, can add into automation testing:
- get data from jmesh
- get fack data
- generate test case from xmind
- get sha1 password
- http request send and validate
- time counter wraper
- multi list to single list
- mysql operations to quick execute sql 
- redis operations to quick read or write data to it
- kafka operations to send or get data from target topic
- mqtt operations to send to receive data from server
- fake data generation base on faker
  
### 6. next step plan to add har2locust or other protocol sender... 
### or add some general validate function in the automation testing,like datatype validate,response validate,callback function ...
### or add some wrapped function about auto test framework, like pytest or behave 
### or deploy jmeter agent to distribute server or docker warapped agent
### or retry function in the auto test framework
