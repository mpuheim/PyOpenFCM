from abc import ABC, abstractmethod

class IFunction(ABC):
    """Interface for standard SISO function (single input, single output) in form out=f(in)."""
    
    @abstractmethod
    def __repr__(self):
        """Return repr(self)."""
        pass
        
    @abstractmethod
    def info(self):
        """Basic description of function.
        
        Returns:
        - string containing basic information about function.
        """
        pass

    @abstractmethod
    def get(self):
        """Detailed information about function (aka serialization).
        
        Returns:
        - string containing serialized function object.
        """
        pass

    @abstractmethod
    def set(self,params):
        """Specify function via predefined set of parameters (aka deserialization).
        
        Arguments:
        - params - List of parameters or formula specifiing the function.
        Returns:
        - None or raises Error.
        """
        pass
        
    @abstractmethod
    def getDerivative(self):
        """Get function derivative.
        
        Returns:
        - either IFunction object or None.
        """
        pass
    
    @abstractmethod
    def evaluate(self,input):
        """Calculate function output as out=f(in).
        
        Arguments:
        - input - real value used as input of the function.
        Returns:
        - output as output=f(input)
        """
        pass

class IRelation(ABC):
    """Interface for MISO relation (multiple input, single output) between preceding concepts and single following concept."""
    
    @abstractmethod
    def __repr__(self):
        """Return repr(self)."""
        pass
    
    @property
    @abstractmethod
    def previous(self):
        """Connected previous concepts."""
        pass
        
    @abstractmethod
    def info(self):
        """Return relation model information.
        
        Returns:
        - string containing relation model information.
        """
        pass

    @abstractmethod
    def get(self, params):
        """Get information about relation (optionaly specified by provided parameters).
        
        Arguments:
        - params - optional function parameters
        Returns:
        - relation information in string format
        """
        pass
        
    @abstractmethod
    def set(self, params):
        """Set relation using provided data.
        
        Arguments:
        - params - optional function parameters
        Returns:
        - None or raises Error.
        """
        pass
        
    @abstractmethod
    def attach(self, concept):
        """Attach new preceding concept to the relation.
        
        Arguments:
        - concept - specified preceding concept
        Returns:
        - None or raises Error.
        """
        pass
        
    @abstractmethod
    def detach(self, concept):
        """Detach preceding concept from the relation.
        
        Arguments:
        - concept - specified preceding concept
        Returns:
        - None or raises Error.
        """
        pass
        
    @abstractmethod
    def propagate(self):
        """Propagate inputs through relation and calculate new value for the following concept.
        
        Returns:
        - None or raises Error.
        """
        pass

    @abstractmethod
    def backprop(self, error):
        """Error backpropagation to all preceding concepts.
        
        Arguments:
        - error - error of relation.
        Returns:
        - None or raises Error.
        """
        pass
        
    @abstractmethod
    def adapt(self, error, gama):
        """Relation adaptation/learning via the "delta rule.
        
        Arguments:
        - error - error of relation.
        - gama - learning rate.
        Returns:
        - None or raises Error.
        """
        pass
