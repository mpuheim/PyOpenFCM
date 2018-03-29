from fcmlib import relations as rlib
from fcmlib import functions as flib

_defaultRelation = rlib.RSimpleSigmoid
_defaultInputMF = flib.PiecewiseLinear
_defaultOutputMF = flib.PiecewiseLinear

class Config:
    """Configuration for FCM functions & relations
    
    Attributes:
    - defaultRelation - default FCM relation
    - defaultInputMF  - default fuzzification function
    - defaultOutputMF - default defuzzification function
    
    - functions - library of available functions
    - relations - library of available relations
    """
    
    defaultRelation = _defaultRelation
    defaultInputMF = _defaultInputMF
    defaultOutputMF = _defaultOutputMF
    
    relations = rlib
    functions = flib
    
    def __init__(self):
        """Config instantiation operation (constructor)."""
        
        self.defaultRelation = _defaultRelation
        self.defaultInputMF = _defaultInputMF
        self.defaultOutputMF = _defaultOutputMF
    
        self.relations = rlib
        self.functions = flib
        