from fcmlib.interfaces import IFunction
from math import *

#list of safe functions
_safe_list_ = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh',
               'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp',
               'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow',
               'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
#filter of the namespace
_safe_dict_ = dict([ (k, globals().get(k, None)) for k in _safe_list_ ])
#add necessary builtins back in.
_safe_dict_['abs'] = abs


class Predefined(IFunction):
    """Function predefined by equation string.
    
    Attributes:
    - equation - function equation
    - derivative - function derivative
    """
    
    equation = None
    derivative = None
    
    def __init__(self):
        """Function instantiation operation (constructor).
        
        Returns:
        - new Predefined function object.
        """
        
        self.equation = "x"
        
    def __repr__(self):
        """Return repr(self)."""
        
        return '%s(%s)' % (type(self).__name__, "f(x)="+self.equation)
        
    def info(self):
        """Return basic information about function.
        
        Returns:
        - string containing basic information about function
        """
        
        return "Predefined function f(x)="+self.equation

    def get(self):
        """Return detailed information about function (aka serialization).
        
        Returns:
        - equation string
        """
        
        return self.equation
    
    def set(self, params):
        """Specify function via predefined equation string.
        
        Arguments:
        - params - string containing function equation
        Returns:
        - None or raises Exception.
        """
        
        #test evaluation for x=1
        self._safeeval_(params.replace("^","**"),1)
        #set equation string
        self.equation = params
        
    def setDerivative(self, params):
        """Specify function derivative via predefined equation string.
        
        Arguments:
        - params - string containing function equation
        Returns:
        - None or raises Exception.
        """
        
        #test evaluation for x=1
        self._safeeval_(params.replace("^","**"),1)
        #set equation string
        self.derivative = params

    def getDerivative(self):
        """Get function derivative.
        
        Returns:
        - Predefined function or raises Error
        """

        if self.derivative is None:
            raise ValueError('Derivative equation is not set. Try to call function.setDerivative(equation) beforehand.')
        derivative = Predefined()
        derivative.set(self.derivative)
        return derivative
    
    def evaluate(self, input):
        """Calculate function output as out=f(in).
        
        Arguments:
        - input - function input
        Returns:
        - function output
        """
        
        x=input
        return self._safeeval_(self.equation.replace("^","**"),x)
        
    def _safeeval_(self,user_func,x):
        """Safe evaluation of expressions"""
        return eval(user_func,{"__builtins__":_safe_dict_},{"x":x})

    