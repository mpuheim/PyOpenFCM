from math import exp
from fcmlib.interfaces import IRelation

class RSimpleSigmoid(IRelation):
    """Represents MISO relations between preceding concepts and single following concept. (MISO - multiple input, single output)
       This class implements standard linear weighted FCM connection with sigmoid thresholding function.
       
    Attributes:
    - previous  - list of connected preceding concepts
    - weights   - list of linear weights    
    """
    
    previous = None
    weights = None

    def __init__(self):
        """Function instantiation operation (constructor).
        
        Returns:
        - new RSimpleSigmoid relation object.
        """
        
        self.previous = []
        self.weights = []
        
    def info(self):
        """Relation model information.
        
        Returns:
        - Return relation model information.
        """
        
        return "Simple FCM relation defined by list of weights between previous concepts and folowing concept"
        
    def attach(self, concept):
        """Attach new preceding concept to the relation.
        
        Attributes:
        - concept - new concept to be attached to the relation
        Returns:
        - None or raises Error exception
        """
        
        if any(x.name == concept.name for x in self.previous):
            raise Exception("Error - concept with name is already connected to the relation")
        else:
            self.previous.append(concept)
            self.weights.append(1)

    def detach(self, concept):
        """Detach existing preceding concept from the relation.
        
        Attributes:
        - concept - concept to be detached from the relation
        Returns:
        - None or raises Error exception
        """
        
        if any(x.name == concept.name for x in self.previous):
            for i in range(len(self.previous)):
                if self.previous[i].name == concept.name:
                    self.previous.pop(i)
                    self.weights.pop(i)
                    break
        else:
            raise Exception("Error - concept with name was not found in the relation")

    def get(self, selection=None):
        """Get string containing relations weights.
        
        Attributes:
        - selection - optional list of selected preceding concept names
        Returns:
        - string containing relation weights separated by semicolons
        """

        #return empty string if there are no weights
        if len(self.weights) == 0:
            return ""
        #return all weights if no concepts are specified
        if not selection:
            return ";".join([str(s) for s in self.weights])
        #return weights of only specified concepts
        toReturn = []
        for s in selection:
            weight = [self.weights[self.previous.index(c)] for c in self.previous if c.name==s.name]
            if weight == []:
                raise Exception("Error - concept with name "+str(s.name)+" was not found in the relation")
            toReturn += weight
        return ";".join(toReturn)

    def set(self, selection, value=None):
        """Set relation using provided data.
        
        Attributes:
        - selection - string containing weights separated by semicolons or name of preceding concept
        - value     - value of related weight
        Returns:
        - None or raises Error exception
        """
    
        #set specific single weight
        if selection and value:
            #print("S:",selection,"val",value)
            if not any(x.name == selection for x in self.previous):
                raise Exception("Error - concept with name "+str(selection)+" was not found in the relation")
            for i in range(len(self.previous)):
                if self.previous[i].name == selection:
                    self.weights[i] = float(value)
        #set all weights
        elif selection and not value:
            delimiterChars = [' ',':',';','\t']
            newStrings = selection.split(delimiterChars);
            if len(newStrings) != len(self.weights):
                raise Exception("Error - wrong number of values to be assigned as weights")
            self.weights = [float(s) for s in newStrings]
        else:
            raise Exception("Error - wrong parameters - weights are unchanged")

    def propagate(self):
        """Propagate inputs through relation and calculate new value for the following concept.
        
        Returns:
        - new value for the following concept
        """
        
        sum = 0
        for i in range(len(self.previous)):
            sum += self.previous[i].value * self.weights[i]
        return 1/(1+exp(-sum))
        
    def backprop(self, delta):
        """Error backpropagation.
        
        Arguments:
        - delta - error signal delta
        Returns:
        - None or raises Error exception
        """
        
        for i in range(len(self.previous)):
            self.previous[i].newDelta += delta * self.weights[i]

    def adapt(self, delta, gama):
        """Relation adaptation/learning via the "delta rule"
        
        Arguments:
        - delta - error delta
        - gama  - learning rate
        """
        
        for i in range(len(self.previous)):
            self.weights[i] += gama * delta * previous[i].value


