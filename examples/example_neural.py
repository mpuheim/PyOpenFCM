from fcmlib.relations import RNeural
from fcmlib import Concept

print("\nCreating Neural Relation with 1 hidden layer consisting of 2 neurons.")
r=RNeural(2)
print(r)
input()

print("\nAttaching 2 concepts to the relation.")
r.attach(Concept("C2",1.0))
r.attach(Concept("C3",1.0))
print(r)
input()

print("\nSerialized weights:")
print(r.get())
input()

print("\nPropagate:")
print(r.propagate())
input()

print("\nSetting new weights to:")
print("0.9,1.0,1.0,1.0,1.0,1.0")
r.set("0.9,1.0,1.0,1.0,1.0,1.0")
print(r)
input()

print("\nSetting weights of C2 to:")
print("0.5,0.5")
r.set("C2","0.5,0.5")
print(r)
input()

print("\nDetaching concept C2")
r.detach(Concept("C2"))
print(r)
input()

while True:
    res=r.propagate()
    print(res)
    error=1.0-res
    r.backprop(error)
    learning_rate=1.0
    r.adapt(error,learning_rate)
    print(r)
    input()