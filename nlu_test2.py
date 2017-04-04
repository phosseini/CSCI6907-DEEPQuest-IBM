import sys
import os
import httplib2
import urllib3
import time


sys.path.append(os.path.join(os.getcwd(),'..'))
import watson_developer_cloud
import watson_developer_cloud.natural_language_understanding.features.v1 as features
nlu = watson_developer_cloud.NaturalLanguageUnderstandingV1(version='2017-04-04',
                                                            url='https://gateway.watsonplatform.net/natural-language-understanding/api',
                                                            username='bd0895eb-eb88-4789-b3a6-5f178fa7ba5e',
                                                            password='DaLAH8nwYaUR')
f = open('/Users/vincent/Downloads/ner/data/esp.testa','r',encoding='ISO-8859-1')
output = open('/Users/vincent/Desktop/ner-esp/esp5','w+',encoding='UTF-8')

# speed=1000
# while speed>100:
#     r = h1.request("GET", "http://gimmeproxy.com/api/getProxy")
#     data = eval(r.data.decode("UTF-8").replace("true", "True").replace("false", "False"))
#     speed = int(data['speed'])
# print(speed)
# print(data)


line = f.readline()
count = 0
res = []
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
            res.append(label[2:])
        else:
            ori_results.append(label)
            res.append(label)
        line = f.readline()
    dict = nlu.analyze(text=sentence,language='es',features=[features.Entities()])
    print(dict)
    print(count)
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

