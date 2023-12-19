#coding: utf-8
#添加包的路径
import sys
sys.path.append('./src')
import os
import autoact
import time
import requests



#print("Received:", autoact.sendEvent_ping())
#print("Received:", autoact.sendEvent_isinprint())
print("Received:", autoact.sendEvent_print_waitEnd("介绍一下中国"))
print("done")
