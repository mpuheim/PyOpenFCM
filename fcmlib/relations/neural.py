from fcmlib.interfaces import IRelation
import numpy as np

class RNeural(IRelation):
    """Represents MISO relations between preceding concepts and single following concept. (MISO - multiple input, single output)
       This class implements multilayer perceptron artifficial neural network.
       
    Attributes:
    - previous  - list of connected preceding concepts
    - weights   - list of weights - [[layer_1],...,[output_layer]]
    """
    
    previous = None
    weights = None
    activations = None
    errors = None
    deltas = None
    

    def __init__(self,*size):
        """Function instantiation operation (constructor).
        
        Returns:
        - new RNeural relation object.
        """
        
        if not size: size = [4,4]
        else: size=list(size)
        
        self.previous = []
        self.weights = [np.random.random((neurons, inputs_per_neuron))*2-1 for inputs_per_neuron, neurons in zip([0]+size,size+[1])]
        self.activations = [np.array([0 for neuron in range(layer)]) for layer in [0]+size+[1]]
        self.errors = [np.array([0 for neuron in range(layer)]) for layer in [0]+size+[1]]
        self.deltas = [np.array([0 for neuron in range(layer)]) for layer in [0]+size+[1]]
        
    def __repr__(self):
        """Return repr(self)."""
        
        r ="\nRNeural - Advanced FCM Relation based on Multilayer Perceptron Neural Network\n"
        r+="-----------------------------------------------------------------------------\n"
        for layer in range(len(self.weights)-1):
            r+="Weights preceding "+str(layer+1)+". hidden layer ("+str(self.weights[layer].shape[0])+" neurons, each with "+str(self.weights[layer].shape[1])+" inputs):\n"
            for neuron in range(len(self.weights[layer])):
                r+=" "+str(self.weights[layer][neuron])+"\n"
        r+="Weights preceding output (1 neuron with "+str(self.weights[-1].shape[1])+" inputs):\n"
        for neuron in range(len(self.weights[-1])):
            r+=" "+str(self.weights[-1][neuron])+"\n"
        r+="-----------------------------------------------------------------------------"
        return r
        
    def __sigmoid(self, x):
        """The Sigmoid function, which normalise input x between 0 and 1."""
        return 1 / (1 + np.exp(-x))

    def __sigmoid_derivative(self, x):
        """The derivative of the Sigmoid function."""
        return x * (1 - x)
        
    def info(self):
        """Relation model information.
        
        Returns:
        - Return relation model information.
        """
        
        return "Simple FCM relation between previous concepts and folowing concept implemented as multilayer perceptron artifficial neural network"
        
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
            self.weights[0] = np.hstack((self.weights[0],np.random.random((self.weights[0].shape[0],1))*2-1))

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
                    self.weights[0] = np.delete(self.weights[0],i,axis=1)
                    break
        else:
            raise Exception("Error - concept with name was not found in the relation")

    def get(self, selection=None):
        """Get string containing relations weights.
        
        Attributes:
        - selection - optional selected preceding concept name
        Returns:
        - string containing relation weights separated by semicolons
        """
        
        toReturn=[]
        #return all weights if no concepts are specified
        if not selection:
            for layer in self.weights:
                for neuron in layer:
                    for weight in neuron:
                        toReturn.append(str(weight))
            return ",".join(toReturn)
        #return weights of only specified concept
        s = -1
        for i in range(len(self.previous)):
            if self.previous[i].name == selection:
                s=i
                break
        if s == -1:
            raise Exception("Error - no such concept: "+str(selection))
        for neuron in self.weights[0]:
            toReturn.append(str(neuron[s]))
        return ",".join(toReturn)

    def set(self, selection, value=None):
        """Set relation using provided data.
        
        Attributes:
        - selection - string containing (comma separated) weights of whole neural network or single name of preceding concept
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
                    for neuron in range(len(self.weights[0])):
                        self.weights[0][neuron][i]=float(values[neuron])
                    break
        #set all weights
        elif selection and not value:
            values = selection.split(",");
            for layer in self.weights:
                for neuron in layer:
                    for weight in range(len(neuron)):
                        neuron[weight] = float(values.pop(0))
        else:
            raise Exception("Error - wrong parameters - weights are unchanged")

    def propagate(self):
        """Propagate inputs through relation and calculate new value for the following concept.
        
        Returns:
        - new value for the following concept
        """

        #reset activations
        self.activations=[]
        #set input layer activations as current values of attached concepts
        self.activations.append(np.array([[concept.value for concept in self.previous]]))
        #calculate activations through each layer of the network
        for layer in range(len(self.weights)):
            self.activations.append(self.__sigmoid(np.dot(self.activations[-1], self.weights[layer].T)))
        #return activation of the output neuron
        return float(self.activations[-1][0])
        
    def backprop(self, error):
        """Error backpropagation.
        
        Arguments:
        - error - error signal for relation
        Returns:
        - None or raises Error exception
        """
        
        #set error of the output neuron
        self.errors[-1] = np.array([error])
        self.deltas[-1] = self.errors[-1] * self.__sigmoid_derivative(self.activations[-1])
        #calculate errors through each layer of the network
        for layer in range(len(self.errors)-2,-1,-1):
            self.errors[layer] = np.dot(self.deltas[layer+1], self.weights[layer])
            self.deltas[layer] = self.errors[layer] * self.__sigmoid_derivative(self.activations[layer])
        #add errors to preceding concepts
        for i in range(len(self.previous)):
            self.previous[i].newError += self.errors[0][0][i]
        
        #print("DEBUG - Errors:",self.errors)
        #print("DEBUG - Deltas:",self.deltas)

    def adapt(self, error, gama):
        """Relation adaptation/learning via the "delta rule"
        
        Arguments:
        - error - error signal for relation
        - gama  - learning rate
        """
        
        #backprop if not already
        if error != self.errors[-1][0]:
            self.backprop(error) #;print("DEBUG - additional backprop")
        #adjust weights through the network
        for layer in range(len(self.weights)):
            self.weights[layer] += (gama * np.dot(self.activations[layer].T, self.deltas[layer+1])).T
            
            #print("DEBUG:")
            #print(self.weights[layer],"___weights")
            #print(self.activations[layer].T,"___activations")
            #print(self.deltas[layer+1],"___deltas")
            #print((gama * np.dot(self.activations[layer].T, self.deltas[layer+1])).T,"___adjustment")

