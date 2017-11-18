from lib.relations.simplesigmoid import RSimpleSigmoid
from lib.functions.piecewiselinear import PiecewiseLinear

_defaultRelation = RSimpleSigmoid
_defaultInputMF = PiecewiseLinear
_defaultOutputMF = PiecewiseLinear

class Config:
    """Configuration for FCM functions & relations
    
    Attributes:
    - relation  - default FCM relation
    - inputMF   - default fuzzification functions
    - outputMF  - default defuzzification functions
    """
    
    relation = _defaultRelation
    inputMF = _defaultInputMF
    outputMF = _defaultOutputMF
