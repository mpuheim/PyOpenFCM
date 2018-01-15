from lib.fcm import FCM
import json

map=FCM()

map["C1"]=0.5
map["C2"]=0.5
map["C3"]=0.5
map["C4"]=0.5

map.connect("C1","C4")
map.connect("C2","C4")
map.connect("C3","C4")
map.connect("C4","C1")

print(map.listPreceding("C4"))
print(map["C4"].relation.get())
map["C4"].relation.set("C1",0.2)
print(map["C4"].relation.get())

while True:
    map.update()
    print(map["C1"],map["C2"],map.get("C3"),map.get("C4"),end="")
    #print(json.dumps(map.__dict__))#TODO
    input()