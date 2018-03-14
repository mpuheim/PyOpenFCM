from fcmlib import relations as rlib
from fcmlib import functions as flib

_defaultRelation = rlib.RSimpleSigmoid
_defaultInputMF = flib.PiecewiseLinear
_defaultOutputMF = flib.PiecewiseLinear

class Config:
    """Configuration for FCM functions & relations
    
    Attributes:
    - default_relation - default FCM relation
    - default_inputMF  - default fuzzification function
    - default_outputMF - default defuzzification function
    
    - functions - library of available functions
    - relations - library of available relations
    """
    
    default_relation = _defaultRelation
    default_inputMF = _defaultInputMF
    default_outputMF = _defaultOutputMF
    
    relations = rlib
    functions = flib
    
    def __init__(self):
        """Config instantiation operation (constructor)."""
        
        self.default_relation = _defaultRelation
        self.default_inputMF = _defaultInputMF
        self.default_outputMF = _defaultOutputMF
    
        self.relations = rlib
        self.functions = flib
        