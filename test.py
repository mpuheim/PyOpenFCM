from lib.fcm import FCM

map=FCM()

map.add("C1")
map.add("C2")
map.add("C3")
map.add("C4")

map.set("C1",0.5)
map.set("C2",0.5)
map.set("C3",0.5)
map.set("C4",0.5)

map.connect("C1","C4")
map.connect("C2","C4")
map.connect("C3","C4")
map.connect("C4","C1")

print(map.listPreceding("C4"))
print(map.concept("C4").relation.get())
map.concept("C4").relation.set("C1",0.2)
print(map.concept("C4").relation.get())

while True:
    map.update()
    print(map.get("C1"),map.get("C2"),map.get("C3"),map.get("C4"),end="")
    input()