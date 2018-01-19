from lib.fcm import FCM
import json

#initialize new FCM with two concepts
map=FCM(C1=0.6,C2=0.4)

#add third concept
map["C3"]=0.5

#add fourth concept and connect it to first
map.connect("C1","C4")

#make additional connections
map.connect("C2","C4")
map.connect("C3","C4")
map.connect("C4","C1")

#list concepts preceding C4
print(map.listPreceding("C4"))

#show relation of C4
print(map["C4"].relation.get())

#set relation of C4 and show the change
map["C4"].relation.set("C1",0.2)
print(map["C4"].relation.get())

#show FCM in action
print()
while True:
    #print current activation values of all concepts
    print("; ".join(str(k)+":"+str(v.value) for k, v in map.items()))
    #update FCM by propagating signals via relations
    map.update()
    #save FCM to file as JSON
    map.save("maps/example.json")
    #load FCM from file as JSON
    map=FCM("maps/example.json")
    #press enter to repeat (CTRL+C to exit)
    input()