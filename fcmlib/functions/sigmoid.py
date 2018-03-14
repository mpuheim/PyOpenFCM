from fcmlib.interfaces import IFunction
from fcmlib.functions.predefined import Predefined
from math import exp

class Sigmoid(IFunction):
    """Simple sigmoid function.
    
    Attributes:
    - slope - sigmoid slope
    - center - sigmoid center on x-axis
    - maximum - maximum y value
    """
    
    slope = None
    center = None
    maximum = None
    
    def __init__(self):
        """Function instantiation operation (constructor).
        
        Returns:
        - new Sigmoid function object.
        """
        
        self.slope = 1
        self.center = 0
        self.maximum = 1
        
    def __repr__(self):
        """Return repr(self)."""
        
        L=str(self.maximum)
        k=str(self.slope)
        x_0=str(self.center)
        return '%s(%s)' % (type(self).__name__, "f(x)="+L+"/(1+e^(-"+k+"(x-"+x_0+")))")
        
    def info(self):
        """Return basic information about function.
        
        Returns:
        - string containing basic information about function
        """
        
        return "Sigmoid function f(x)=L/(1+e^(-k(x-x_0)))"

    def get(self):
        """Return detailed information about function (aka serialization).
        
        Returns:
        - string containing parameters of sigmoid function (maximum, slope, center) separated by spaces
        """
        
        return str(self.maximum)+" "+str(self.slope)+" "+str(self.center)
    
    def set(self, params):
        """Specify function via predefined set of parameters (aka deserialization).
        
        Arguments:
        - params - string containing parameters of sigmoid function (maximum, slope, center) separated by spaces
        Returns:
        - None or raises Exception.
        """
        
        self.maximum, self.slope, self.center = [float(c) for c in params.split(" ")]

    def getDerivative(self):
        """Get function derivative.
        
        Returns:
        - Predefined function f(x)=((Lk)e^(-k(x-x_0)))/(1+e^(-k(x-x_0)))^2
        """

        # declare function object
        derivative = Predefined()
        # set derivative function
        L=str(self.maximum)
        k=str(self.slope)
        x_0=str(self.center)
        #f(x)=((L*k)*exp(-k*(x-x_0)))/(1+exp(-k*(x-x_0)))**2
        equation="(("+L+"*"+k+")*exp(-"+k+"*(x-"+x_0+")))/(1+exp(-"+k+"*(x-"+x_0+")))**2"
        derivative.set(equation)
        # return function derivative
        return derivative
    
    def evaluate(self, input):
        """Calculate function output as out=f(x)=L/(1+e^(-k(x-x_0))).
        
        Arguments:
        - input - function input (x)
        Returns:
        - function output
        """
        
        return self.maximum/(1+exp(-self.slope*(input-self.center)))
    