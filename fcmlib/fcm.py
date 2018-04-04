from fcmlib.config import Config
import json, jsonpickle

import jsonpickle.ext.numpy as jsonpickle_numpy
jsonpickle_numpy.register_handlers() #numpy support for object serialization

class Concept:
    """Represents single FCM concept.
    
    Attributes:
    - name      - The unique name of the concept.
    - value     - The activation value of the concept in time "t".
    - newValue  - The activation value of the concept in time "t+1".
    - error     - The activation error in time "t".
    - newError  - The activation error in time "t+1".
    - relation  - The relation (class IRelation) with previous concepts.
    - inputMF   - The function (class IFunction) used for fuzzification
    - outputMF  - The function (class IFunction) used for defuzzification.
    """
    
    name = None
    value = None
    newValue = None
    error = None
    newError = None
    relation = None
    inputMF = None
    outputMF = None
    
    def __init__(self, name, value=0, conf=Config):
        """Concept instantiation operation (constructor).
        
        Attributes:
        - name - concept name
        - value - initial concept value (optional)
        - conf - initial functions & relations configuration (optional)
        Returns:
        - new Concept object.
        """
        
        self.name = name;
        self.newValue = value;
        self.value = value;
        self.error = 0
        self.newError = 0
        self.relation = conf.defaultRelation()
        self.inputMF = conf.defaultInputMF()
        self.outputMF = conf.defaultOutputMF()
    
    def __repr__(self):
        """Return repr(self)."""        
        return str(self.value)
        

class FCM(dict):
    """Represents fuzzy cognitive map. Provides methods to add, connect and configure map concepts and to calculate map updates.
    
    Attributes:
    - config    - current FCM configuration
    - name      - FCM identification name
    """
    
    config = None
    name = None
    
    #TODO - add name initialization
    def __init__(self, *args, **kwargs):
        """Initialize self."""
        
        # default config
        self.config = Config()
        # load from JSON string
        if len(args)==1 and isinstance(args[0],str) and args[0][0]=="{":
            self.deserialize(args[0])
        # load from file path or file object
        elif len(args)==1:
            self.load(args[0])
        #initialize FCM from args
        elif len(args)!=1:
            for k, v in dict(*args, **kwargs).items():
                vu=float(v) if isinstance(v,(int,float)) else v
                dict.__setitem__(self, k, Concept(k,vu,self.config))

    def __getitem__(self, key):
        """x.__getitem__(y) <==> x[y]"""
        
        val = dict.__getitem__(self, key)
        return val

    def __setitem__(self, key, val):
        """Set self[key] to value."""

        if isinstance(val,Concept):
            dict.__setitem__(self, key, val)
        elif key in self:
            self[key].value=float(val)
            self[key].newValue=float(val)
        elif isinstance(val,int):
            dict.__setitem__(self, key, Concept(key,float(val),self.config))
        elif isinstance(val,float):
            dict.__setitem__(self, key, Concept(key,val,self.config))
        else:
            raise Exception("Error - unsupported value type of",type(val))

    def __repr__(self):
        """Return repr(self)."""
        
        dictrepr = dict.__repr__(self)
        return '%s(%s)' % (type(self).__name__, dictrepr)
    
    def add(self, name, value=0):
        """Add new concept to the FCM.
        
        Arguments:
        - name - unique name
        Returns:
        - None or raises Error Exception.
        """
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif name in self:
            raise Exception("Error - name is already used for another concept")
        else:
            dict.__setitem__(self, name, Concept(name,value,self.config))
            
    def remove(self, name):
        """Remove concept from the FCM.
        
        Arguments:
        - name - concept name
        Returns:
        - None or raises Error Exception.
        """
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif not name in self:
            raise Exception("Error - there is no concept with name to be removed")
        else:
            for concept in self:
                if name in [x.name for x in self[concept].relation.previous]:
                    self[concept].relation.detach(self[name])
            del self[name]
            
    def rename(self, currentname, newname):
        """Rename concept within the FCM.
        
        Arguments:
        - currentname - currnet name of the concept
        - newname - new name of the concept
        Returns:
        - None or raises Error Exception.
        """
        if (not currentname) or (not isinstance(currentname,str)) or (currentname == ""):
            raise Exception("Error - currentname is not string or empty")
        elif (not newname) or (not isinstance(currentname,str)) or (newname == ""):
            raise Exception("Error - newname is not string or empty")
        elif not currentname in self:
            raise Exception("Error - there is no concept with currentname to be removed")
        elif newname in self:
            raise Exception("Error - concept with newname already exists")
        else:
            self[newname]=self.pop(currentname)

    def connect(self, preceding, following):
        """Connects two concepts within the FCM.
        
        Arguments:
        - preceding - name of the preceding concept
        - following - name of the following concept
        Returns:
        - None or raises Error Exception.
        """
        if (not preceding) or (not isinstance(preceding,str)) or (preceding == ""):
            raise Exception("Error - preceding is not string or empty")
        elif (not following) or (not isinstance(following,str)) or (following == ""):
            raise Exception("Error - following is not string or empty")
        else:
            if not preceding in self:
                self[preceding]=0
            if not following in self:
                self[following]=0
            self[following].relation.attach(self[preceding])
        
    def disconnect(self, preceding, following):
        """Disconnects two concepts within the FCM.
        
        Arguments:
        - preceding - name of the preceding concept
        - following - name of the following concept
        Returns:
        - None or raises Error Exception.
        """
        if (not preceding) or (not isinstance(preceding,str)) or (preceding == ""):
            raise Exception("Error - preceding is not string or empty")
        elif (not following) or (not isinstance(following,str)) or (following == ""):
            raise Exception("Error - following is not string or empty")
        elif not preceding in self:
            raise Exception("Error - there is no preceding concept with name " + preceding)
        elif not following in self:
            raise Exception("Error - there is no following concept with name " + following)
        else:
            self[following].relation.detach(self[preceding])

    def get(self, name):
        """Get concept reference by name
        
        Arguments:
        - name - concept name
        Returns:
        - Concept object instance
        """
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif not name in self:
            raise Exception("Error - there is no concept with name " + name)
        else:
            return self[name]
            
    def set(self, name, value):
        """Set concept to specific activation value or Concept object instance
        
        Arguments:
        - name - concept name
        - value - new activation value of the concept or Concept instance
        Returns:
        - None or raises Error Exception.
        """
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif not isinstance(value, (int,float,Concept)):
            raise Exception("Error - value is neither numeric type nor Concept instance")
        elif isinstance(value, Concept):
            if name in self:
                del self[name]
            self[name]=value
        elif isinstance(value, (int,float)):
            self[name]=float(value)
        else:
            raise Exception("Error - cannot set value")
    
    def update(self):
        """Update activation values of all concept within the map
        
        Returns:
        - None or raises Error Exception.
        """
        for name, concept in self.items():
            if len(concept.relation.previous)>0:
                concept.newValue = concept.relation.propagate()
        for name, concept in self.items():
            concept.value = concept.newValue
    
    def list(self):
        """Return string containing names of all concepts within the map
        
        Returns:
        - string containing sorted names of all concepts separated by semicolons
        """
        if len(self) == 0:
            return ""
        else:
            l = [x for x in self]
            l.sort()
            return ";".join(l)

    def listPreceding(self,name):
        """Return string containing names of all concepts preceding single concept specified by name
        
        Arguments:
        - name - concept name
        Returns:
        - string containing sorted names of all preceding concepts separated by semicolons
        """
        
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif not name in self:
            raise Exception("Error - there is no concept with name " + name)
        if len(self[name].relation.previous)==0:
            return ""
        else:
            l=[x.name for x in self[name].relation.previous]
            l.sort()
            return ";".join(l)
            
    def serialize(self,indent=4):
        """Return JSON representation of FCM
        
        Arguments:
        - indent - optional integer value used to set output indentation
        Returns:
        - string containing JSON encoded fuzzy cognitive map
        """
        
        #preparation (separate relations to force flat pickle of concepts)
        self.relations=dict()
        for name, concept in self.items():
            p=self.relations[name]=concept.relation
            p.previousnames=[]
            for prev in p.previous:
                p.previousnames.append(prev.name)
            #del concept.relation
            concept.relation = None
        #encode concepts & relations
        line = jsonpickle.encode(self)
        if indent<=0:
            result = line
        else:
            obj = json.loads(line)
            result = json.dumps(obj, indent=indent)
        #restore former fcm (merge concepts & relations)
        for name, concept in self.items():
            concept.relation = self.relations[name]
        del self.relations
        #return JSON string
        return result
        
    def deserialize(self,string):
        """Initialize FCM from JSON representation
        
        Arguments:
        - string - JSON representation of FCM
        Returns:
        - string containing JSON encoded fuzzy cognitive map
        """
        
        #deserialize
        new = jsonpickle.decode(string)
        for name, value in new.relations.items():
            del value.previousnames
            new[name].relation=value
        del new.relations
        #copy to this object
        self.clear()
        for name, concept in new.items():
            self[name]=concept
        self.config=new.config
        self.name=new.name
    
    def save(self,file,indent=4):
        """Save JSON representation of FCM to file
        
        Arguments:
        - file - writeable file object or string containing file path
        Returns:
        - None or raises Error Exception.
        """
        
        if isinstance(file,str):
            with open(file,"w") as f:
                f.write(self.serialize(indent))
        else:
            file.write(self.serialize(indent))

    def load(self,file):
        """Load JSON representation of FCM from file
        
        Arguments:
        - file - readable file object or string containing file path
        Returns:
        - None or raises Error Exception.
        """
        
        if isinstance(file,str):
            with open(file,"r") as f:
                self.deserialize(f.read())
        else:
            self.deserialize(file.read())
