
import requests
import time

g_url = 'http://127.0.0.1:9560'  


def postEvent(url, data):
    return requests.post(url, data).text

def sendEvent(url):
    return requests.get(url).text

def sendEvent_ping():
    url = g_url + '/ping'  
    return sendEvent(url)

def sendEvent_hide():
    url = g_url + '/hide'  
    return sendEvent(url)

def sendEvent_show():
    url = g_url + '/show'  
    return sendEvent(url)

def sendEvent_print(ques):
    url = g_url + '/print'
    return postEvent(url, ques.encode('utf-8'))

def sendEvent_print_waitEnd(ques):
    sendEvent_print(ques)
    time.sleep(1)
    for i in range(0, 500):
        res = sendEvent_isAsking()
        if(res == '1'):
            time.sleep(0.2)
        else:
            break

#是否在打印中,返回字符串0或1
def sendEvent_isAsking():
    url = g_url + '/isasking'
    return sendEvent(url)
