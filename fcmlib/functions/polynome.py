from fcmlib.interfaces import IFunction

class Polynome(IFunction):
    """Simple polynomial function.
    
    Attributes:
    - coefficients - list of polynome coefficients
    """
    
    coefficients = None
    
    def __init__(self):
        """Function instantiation operation (constructor).
        
        Returns:
        - new Polynomial function object.
        """
        
        self.coefficients = [0]
        
    def __repr__(self):
        """Return repr(self)."""
        
        ret=str(self.coefficients[-1])+"x^0"
        power=1
        for c in self.coefficients[-2::-1]:
            ret=str(c)+"x^"+str(power)+"+"+ret
            power+=1
        return '%s(%s)' % (type(self).__name__, ret)
        
    def info(self):
        """Return basic information about function.
        
        Returns:
        - string containing basic information about function
        """
        
        return "Polynomial function"

    def get(self):
        """Return detailed information about function (aka serialization).
        
        Returns:
        - string containing coefficients of polynomial function separated by spaces
        """
        
        return " ".join(self.coefficients)
    
    def set(self, params):
        """Specify function via predefined set of parameters (aka deserialization).
        
        Arguments:
        - params - string containing coefficients of polynomial function separated by spaces
        Returns:
        - None or raises Exception.
        """
        
        new_coefficients = params.split(" ")
        self.coefficients = [float(c) for c in new_coefficients]

    def getDerivative(self):
        """Get function derivative.
        
        Returns:
        - Polynomial function
        """

        # declare function object
        derivative = Polynomial()
        # set derivative function
        derivative.set(" ".join(self.coefficients[:-1]))
        # return function derivative
        return derivative
    
    def evaluate(self, input):
        """Calculate function output as out=f(in).
        
        Arguments:
        - input - function input
        Returns:
        - function output
        """
        
        res=self.coefficients[-1]
        power=1
        for c in self.coefficients[-2::-1]:
            res+=c*(input**power)
            power+=1
        return res
    