from math import exp
from fcmlib.interfaces import IRelation

class R3Term(IRelation):
    """Represents MISO relations between preceding concepts and single following concept. (MISO - multiple input, single output)
       This class implements three-term weighted FCM connection with sigmoid thresholding function.
       
    Attributes:
    - previous  - list of connected preceding concepts
    - weights   - list of (P,D,A) weight tuples
    - pweights  - list of proportional   (P) weights 
    - dweights  - list of differential   (D) weights
    - aweights  - list of moving-average (A) weights
    - pvalues   - list of current activation values of preceding concepts
    - dvalues   - list of difference of activation values of preceding concepts
    - avalues   - list of moving-average values of preceding concepts
    - awindow   - time window used to calculate moving average
    """
    
    previous = None
    weights = None
    pweights = None
    dweights = None
    aweights = None
    pvalues = None
    dvalues = None
    avalues = None
    awindow = None

    def __init__(self,window=10):
        """Function instantiation operation (constructor).
        
        Returns:
        - new R3Term relation object.
        """
        
        self.previous  = []
        self.weights   = []
        self.pweights = []
        self.dweights = []
        self.aweights = []
        self.pvalues  = []
        self.dvalues  = []
        self.avalues  = []
        self.awindow = window
        
    def __repr__(self):
        """Return repr(self)."""
        
        r = str(dict([(x[0].name,(x[1],x[2],x[3])) for x in zip(self.previous,self.pweights,self.dweights,self.aweights)]))
        return '%s(%s)' % (type(self).__name__, r)

    def __sigmoid(self, x):
        """The Sigmoid function, which normalise input x between 0 and 1."""
        return 1 / (1 + exp(-x))

    def __sigmoid_derivative(self, x):
        """The derivative of the Sigmoid function."""
        return x * (1 - x)
        
    def info(self):
        """Relation model information.
        
        Returns:
        - Return relation model information.
        """
        
        return "FCM relation defined by list of three-term weights (proportional, differential & averaged) between previous concepts and folowing concept"
        
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
            self.weights.append([1.0,1.0,1.0])
            self.pweights.append(1.0)
            self.dweights.append(1.0)
            self.aweights.append(1.0)
            self.pvalues.append(concept.value)
            self.dvalues.append(0.0)
            self.avalues.append(concept.value)

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
                    self.pweights.pop(i)
                    self.dweights.pop(i)
                    self.aweights.pop(i)
                    self.pvalues.pop(i)
                    self.dvalues.pop(i)
                    self.avalues.pop(i)
                    break
        else:
            raise Exception("Error - concept with name was not found in the relation")

    def get(self, selection=None):
        """Get string containing relational weights.
        
        Attributes:
        - selection - optional selected preceding concept name
        Returns:
        - string containing relation weights separated by commas (3 terms) and semicolons
        """

        #return empty string if there are no weights
        if len(self.pweights) == 0:
            return ""
        #return all weights if no concepts are specified
        if not selection:
            return ";".join([str(w[0])+","+str(w[1])+","+str(w[2]) for w in self.weights])
        #return weights of only specified concept
        s = -1
        for i in range(len(self.previous)):
            if self.previous[i].name == selection:
                s=i
                break
        if s == -1:
            raise Exception("Error - no such concept: "+str(selection))
        return str(self.pweights[s])+','+str(self.dweights[s])+','+str(self.aweights[s])

    def set(self, selection, value=None):
        """Set relation using provided data.
        
        Attributes:
        - selection - string containing (comma separated three-term) weights of all preceding concepts (separated by semicolons) or single name of preceding concept
        - value     - string containing (comma separated) values of weights related to selected concept
        Returns:
        - None or raises Error exception
        """
    
        #set specific single concept weights
        if selection and value:
            if not any(x.name == selection for x in self.previous):
                raise Exception("Error - concept with name "+str(selection)+" was not found in the relation")
            for i in range(len(self.previous)):
                if self.previous[i].name == selection:
                    values=value.split(',')
                    self.pweights[i] = float(values[0])
                    self.dweights[i] = float(values[1])
                    self.aweights[i] = float(values[2])
                    self.weights[i] = [float(values[0]),float(values[1]),float(values[2])]
                    break
        #set all weights
        elif selection and not value:
            tterms = selection.split(";");
            if len(tterms) != len(self.pweights):
                raise Exception("Error - wrong number of values to be assigned as weights")
            self.weights = [list(map(float(tt.split(",")))) for tt in tterms]
            self.pweights = [tt[0] for tt in self.weights]
            self.dweights = [tt[1] for tt in self.weights]
            self.aweights = [tt[2] for tt in self.weights]
        else:
            raise Exception("Error - wrong parameters - weights are unchanged")

    def propagate(self):
        """Propagate inputs through relation and calculate new value for the following concept.
        
        Returns:
        - new value for the following concept
        """
        
        sum = 0
        # Propagate through three-term relation (PDA)
        for i in range(len(self.previous)):
            # D = differential component as difference betwen current and last activation value
            self.dvalues[i] = self.previous[i].value - self.pvalues[i]
            # P = proportional component as current activation value
            self.pvalues[i] = self.previous[i].value
            # A = averaging component as moving average of historical values
            self.avalues[i] = ((self.avalues[i]*self.awindow)+self.pvalues[i])/(1+self.awindow)
            # sum += w_p*P + w_d*D + w_a*A
            sum += self.pweights[i] * self.pvalues[i]
            sum += self.dweights[i] * self.dvalues[i]
            sum += self.aweights[i] * self.avalues[i]
        # Return thresholded value using sigmoid function
        return self.__sigmoid(sum)
        
    def backprop(self, error):
        """Error backpropagation.
        
        Arguments:
        - error - error signal of relation
        Returns:
        - None or raises Error exception
        """
        
        for i in range(len(self.previous)):
            self.previous[i].newError += error * self.pweights[i]
            self.previous[i].newError += error * self.dweights[i]
            self.previous[i].newError += error * self.aweights[i]

    def adapt(self, error, gama):
        """Relation adaptation/learning via the "delta rule"
        
        Arguments:
        - error - error signal of relation
        - gama  - learning rate
        """
        
        for i in range(len(self.previous)):
            p_delta = error * self.__sigmoid_derivative(self.pvalues[i])
            d_delta = error * self.__sigmoid_derivative(self.dvalues[i])
            a_delta = error * self.__sigmoid_derivative(self.dvalues[i])
            self.pweights[i] += gama * p_delta * self.pvalues[i]
            self.dweights[i] += gama * d_delta * self.dvalues[i]
            self.aweights[i] += gama * a_delta * self.avalues[i]


