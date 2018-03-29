from fcmlib import FCM

print("initialize new FCM with two concepts")
map=FCM(C1=0.6,C2=0.4)
print(map)
input()

print("add third concept")
map["C3"]=0.5
print(map)
input()

print("add fourth concept and connect it to the first")
map.connect("C1","C4")
print(map)
input()

print("make additional connections")
map.connect("C2","C4")
map.connect("C3","C4")
map.connect("C4","C1")
print(map)
input()

print("list concepts preceding C4")
print(map.listPreceding("C4"))
input()

print("show relations of C4")
print(map["C4"].relation.get())
input()

print("set relation of C1->C4 and show the change")
map["C4"].relation.set("C1",0.2)
print(map["C4"].relation.get("C1"))
input()

print("FCM in action:")
print()
while True:
    print(map)
    #update FCM by propagating signals via relations
    map.update()
    #save FCM to file as JSON
    map.save("../maps/example.json")
    #load FCM from file as JSON
    map=FCM("../maps/example.json")
    #press enter to repeat (CTRL+C to exit)
    input()