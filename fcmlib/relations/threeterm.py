from math import exp
from fcmlib.interfaces import IRelation

class R3Term(IRelation):
    """Represents MISO relations between preceding concepts and single following concept. (MISO - multiple input, single output)
       This class implements three-term weighted FCM connection with sigmoid thresholding function.
       
    Attributes:
    - previous  - list of connected preceding concepts
    - weights   - list of (P,D,A) weight tuples
    - p_weights - list of proportional   (P) weights 
    - d_weights - list of differential   (D) weights
    - a_weights - list of moving-average (A) weights
    - p_values  - list of current activation values of preceding concepts
    - d_values  - list of difference of activation values of preceding concepts
    - a_values  - list of moving-average values of preceding concepts
    - a_window  - time window used to calculate moving average
    """
    
    previous = None
    weights = None
    p_weights = None
    d_weights = None
    a_weights = None
    p_values = None
    d_values = None
    a_values = None
    a_window = None

    def __init__(self,window=10):
        """Function instantiation operation (constructor).
        
        Returns:
        - new R3Term relation object.
        """
        
        self.previous  = []
        self.weights   = []
        self.p_weights = []
        self.d_weights = []
        self.a_weights = []
        self.p_values  = []
        self.d_values  = []
        self.a_values  = []
        self.a_window = window
        
    def __repr__(self):
        """Return repr(self)."""
        
        r = str(dict([(x[0].name,(x[1],x[2],x[3])) for x in zip(self.previous,self.p_weights,self.d_weights,self.a_weights)]))
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
            self.p_weights.append(1.0)
            self.d_weights.append(1.0)
            self.a_weights.append(1.0)
            self.p_values.append(concept.value)
            self.d_values.append(0.0)
            self.a_values.append(concept.value)

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
                    self.p_weights.pop(i)
                    self.d_weights.pop(i)
                    self.a_weights.pop(i)
                    self.p_values.pop(i)
                    self.d_values.pop(i)
                    self.a_values.pop(i)
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
        if len(self.p_weights) == 0:
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
        return str(self.p_weights[s])+','+str(self.d_weights[s])+','+str(self.a_weights[s])

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
                    self.p_weights[i] = float(values[0])
                    self.d_weights[i] = float(values[1])
                    self.a_weights[i] = float(values[2])
                    self.weights[i] = [float(values[0]),float(values[1]),float(values[2])]
                    break
        #set all weights
        elif selection and not value:
            tterms = selection.split(";");
            if len(tterms) != len(self.p_weights):
                raise Exception("Error - wrong number of values to be assigned as weights")
            self.weights = [list(map(float(tt.split(",")))) for tt in tterms]
            self.p_weights = [tt[0] for tt in self.weights]
            self.d_weights = [tt[1] for tt in self.weights]
            self.a_weights = [tt[2] for tt in self.weights]
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
            self.d_values[i] = self.previous[i].value - self.p_values[i]
            # P = proportional component as current activation value
            self.p_values[i] = self.previous[i].value
            # A = averaging component as moving average of historical values
            self.a_values[i] = ((self.a_values[i]*self.a_window)+self.p_values[i])/(1+self.a_window)
            # sum += w_p*P + w_d*D + w_a*A
            sum += self.p_weights[i] * self.p_values[i]
            sum += self.d_weights[i] * self.d_values[i]
            sum += self.a_weights[i] * self.a_values[i]
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
            self.previous[i].newError += error * self.p_weights[i]
            self.previous[i].newError += error * self.d_weights[i]
            self.previous[i].newError += error * self.a_weights[i]

    def adapt(self, error, gama):
        """Relation adaptation/learning via the "delta rule"
        
        Arguments:
        - error - error signal of relation
        - gama  - learning rate
        """
        
        for i in range(len(self.previous)):
            p_delta = error * self.__sigmoid_derivative(self.p_values[i])
            d_delta = error * self.__sigmoid_derivative(self.d_values[i])
            a_delta = error * self.__sigmoid_derivative(self.d_values[i])
            self.p_weights[i] += gama * p_delta * self.p_values[i]
            self.d_weights[i] += gama * d_delta * self.d_values[i]
            self.a_weights[i] += gama * a_delta * self.a_values[i]


