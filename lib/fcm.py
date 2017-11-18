from lib.config import Config

class Concept:
    """Represents single FCM concept.
    
    Attributes:
    - name      - The unique name of the concept.
    - value     - The activation value of the concept in time "t".
    - newValue  - The activation value of the concept in time "t+1".
    - delta     - The activation error in time "t".
    - newDelta  - The activation error in time "t+1".
    - relation  - The relation (class IRelation) with previous concepts.
    - inputMF   - The function (class IFunction) used for fuzzification
    - outputMF  - The function (class IFunction) used for defuzzification.
    """
    
    name = None
    value = None
    newValue = None
    delta = None
    newDelta = None
    relation = None
    inputMF = None
    outputMF = None
    
    def __init__(self, name):
        """Concept instantiation operation (constructor).
        
        Attributes:
        - name - concept name
        Returns:
        - new Concept object.
        """
        
        self.name = name;
        self.newValue = 0;
        self.value = 0;
        self.relation = Config.relation() # TODO - config default relation
        self.inputMF = Config.inputMF() # TODO - config default function
        self.outputMF = Config.outputMF() # TODO - config default function

class FCM:
    """Represents fuzzy cognitive map. Provides methods to add, connect and configure map concepts and to calculate map updates.
    
    Attributes:
    - concepts  - list of concepts
    - config    - current FCM configuration
    """
    
    concepts = []      # empty list of concepts
    config = Config()  # default config
    
    __c1 = None       # helper variable
    __c2 = None       # helper variable
    
    def add(self, name):
        """Add new concept to the FCM.
        
        Arguments:
        - name - unique name
        Returns:
        - None or raises Error Exception.
        """
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif any(x.name == name for x in self.concepts):
            raise Exception("Error - name is already used for another concept")
        else:
            self.concepts.append(Concept(name))
            
    def remove(self, name):
        """Remove concept from the FCM.
        
        Arguments:
        - name - concept name
        Returns:
        - None or raises Error Exception.
        """
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif not any(x.name == name for x in self.concepts):
            raise Exception("Error - there is no concept with name to be removed")
        else:
            self.concepts = [x for x in self.concepts if x.name != name]
            
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
        elif not any(x.name == currentname for x in self.concepts):
            raise Exception("Error - there is no concept with currentname to be removed")
        elif any(x.name == newname for x in self.concepts):
            raise Exception("Error - concept with newname already exists")
        else:
            for x in self.concepts:
                if x.name == currentname:
                    x.name = newname
                    break
                    
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
        elif not any(x.name == preceding for x in self.concepts):
            raise Exception("Error - there is no preceding concept with name " + preceding)
        elif not any(x.name == following for x in self.concepts):
            raise Exception("Error - there is no following concept with name " + following)
        c1 = [item for item in self.concepts if item.name == preceding][0]
        c2 = [item for item in self.concepts if item.name == following][0]
        c2.relation.attach(c1)
        
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
        elif not any(x.name == preceding for x in self.concepts):
            raise Exception("Error - there is no preceding concept with name " + preceding)
        elif not any(x.name == following for x in self.concepts):
            raise Exception("Error - there is no following concept with name " + following)
        c1 = [item for item in self.concepts if item.name == preceding][0]
        c2 = [item for item in self.concepts if item.name == following][0]
        c2.relation.dettach(c1)

    def get(self, name):
        """Get current activation value of the concept
        
        Arguments:
        - name - concept name
        Returns:
        - float value or raises Error Exception.
        """
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif not any(x.name == name for x in self.concepts):
            raise Exception("Error - there is no concept with name " + name)
        else:
            c = [item for item in self.concepts if item.name == name][0]
            return c.value
            
    def set(self, name, value):
        """Set current activation value of the concept
        
        Arguments:
        - name - concept name
        - value - new activation value of the concept
        Returns:
        - None or raises Error Exception.
        """
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif not any(x.name == name for x in self.concepts):
            raise Exception("Error - there is no concept with name " + name)
        elif not isinstance(value, (int,float)):
            raise Exception("Error - value is not of numeric data type")
        else:
            c = [item for item in self.concepts if item.name == name][0]
            c.value = float(value)
        
    def concept(self, name):
        """Getter for concept object
        
        Arguments:
        - name - concept name
        Returns:
        - Concept or raises Error Exception.
        """
        if (not name) or (not isinstance(name,str)) or (name == ""):
            raise Exception("Error - name is not string or empty")
        elif not any(x.name == name for x in self.concepts):
            raise Exception("Error - there is no concept with name " + name)
        else:
            c = [item for item in self.concepts if item.name == name][0]
            return c
    
    def update(self):
        """Update activation values of all concept within the map
        
        Returns:
        - None or raises Error Exception.
        """
        for c in self.concepts:
            c.newValue = c.relation.propagate()
        for c in self.concepts:
            c.value = c.newValue
    
    def list(self):
        """Return string containing names of all concepts within the map
        
        Returns:
        - string containing sorted names of all concepts separated by semicolons
        """
        if len(self.concepts) == 0:
            return ""
        else:
            l = [x.name for x in self.concepts]
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
        elif not any(x.name == name for x in self.concepts):
            raise Exception("Error - there is no concept with name " + name)
        c = [item for item in self.concepts if item.name == name][0]
        if len(c.relation.previous)==0:
            return ""
        else:
            l=[x.name for x in c.relation.previous]
            l.sort()
            return ";".join(l)
        