import sys
import os
import httplib2
import urllib3
import time


sys.path.append(os.path.join(os.getcwd(),'..'))
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features
nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-02-27',
                                                            url='https://natural-language-understanding-demo.mybluemix.net/api/analyze',
                                                            username='af822163-4503-4453-9cf9-2b09be493a97',
                                                            password='Yb5Kz6dkKA1M')
f = open('/Users/vincent/Desktop/ner-esp/esp.testa_b','r',encoding='UTF-8')
output = open('/Users/vincent/Desktop/ner-esp/esp4','w+',encoding='UTF-8')
proxy_list = open('proxy.txt','r',encoding='UTF-8')
h1 = urllib3.PoolManager()

# speed=1000
# while speed>100:
#     r = h1.request("GET", "http://gimmeproxy.com/api/getProxy")
#     data = eval(r.data.decode("UTF-8").replace("true", "True").replace("false", "False"))
#     speed = int(data['speed'])
# print(speed)
# print(data)

success = False
while not success:
    try:
        proxy = proxy_list.readline().split(" ")[0]
        h2 = urllib3.ProxyManager("http://"+proxy)
        success = True
    except:
        continue

headers = {'Content-Type': 'application/json'}
line = f.readline()
count = 0
while line:
    count+=1
    sentence = ""
    ori_words = []
    ori_results = []
    while len(line) > 1:
        items = line.split(" ")
        sentence+= str(items[0])+" "
        ori_words.append(items[0])
        label = items[1][0:-1]
        if label!="O":
            ori_results.append(label[2:])
        else:
            ori_results.append(label)
        line = f.readline()
    fields = {"language":"es","fallback_to_raw":True,"clean":True,"return_analyzed_text":False,"features":{"entities":{}},"text":"' + sentence + '"}
    uri = "https://natural-language-understanding-demo.mybluemix.net/api/analyze"
    content = h2.request("POST",uri, fields=fields, headers=headers)
    content = eval(content.decode("utf-8"))
    print(content)
    print(count)
    dict = content['results']
    words = []
    for entity in dict['entities']:
        for word in entity['text'].split(" "):
            words.append({"word":word,"type":entity['type']})
    res = ["O"]*len(ori_words)
    i = 0
    for word in words:
        try:
            i = ori_words.index(word["word"], i)
            if word['type'] == "Person":
                res[i] = "PER"
            elif word['type'] == "Organization":
                res[i] = "ORG"
            elif word['type'] == "Location":
                res[i] = "LOC"
            else:
                res[i] = "MISC"
        except:
            continue

    for idx, word in enumerate(ori_words):
        output.write(word+" "+ori_results[idx]+" "+res[idx]+"\n")
    line = f.readline()

    if count%10 == 0:
        success = False
        while not success:
            try:
                proxy = proxy_list.readline().split(" ")[0]
                h2 = urllib3.ProxyManager("http://" + proxy)
                success = True
            except:
                continue


