from fcmlib.interfaces import IFunction

class PiecewiseLinear(IFunction):
    """Simple piecewise linear function.
    
    Attributes:
    - piece - list of connected linear functions
    """
    
    piece = None
    
    def __init__(self):
        """Function instantiation operation (constructor).
        
        Returns:
        - new piecewise linear function object.
        """
        
        self.piece = []
        
    def __repr__(self):
        """Return repr(self)."""
        r = self.get()
        return '%s(%s)' % (type(self).__name__, r)
        
    def info(self):
        """Return basic information about function.
        
        Returns:
        - string containing basic information about function
        """
        
        return "Simple piecewise linear function."

    def get(self):
        """Return detailed information about function (aka serialization).
        
        Returns:
        - string containing point coordinates (x:y) of linear breaks separated by spaces
        """
        
        if len(self.piece) < 1:
            return ""
        points = self.pieces2points(self.piece)
        return " ".join([str(p.x)+":"+str(p.y) for p in points])
    
    def set(self, params):
        """Specify function via predefined set of parameters (aka deserialization).
        
        Arguments:
        - params - string containing coordinates (x:y) {ordered by x} of piecewise linear function breakpoints separated by spaces
        Returns:
        - None or raises Error Exception.
        """
        
        # check if any points are provided
        if (not params) or (not isinstance(params,str)) or (params == ""):
            raise Exception("Error - params is not string or empty")
        # deserialize params string to points
        points = params.split(" ")
        # check if there are at least 2 points
        if len(points) < 2:
            raise Exception("Error - deserialization error, params contains less than 2 points")
        # generate point objects
        pointObjects = []
        for p in points:
            coords = p.split(":")
            #check coordinates
            if len(coords) != 2:
                raise Exception("Error - deserialization error, wrong format used for coordinates")
            #convert to the point object
            pointObjects.append(Point(float(coords[0]),float(coords[1])))
        # check point order                
        prev = pointObjects[0]
        for curr in pointObjects:
            if prev.x > curr.x:
                raise Exception("Error - deserialization error, wrong order of x-coordinate")
            prev = curr
        # remove duplicite or close points
        self.removeDuplicitPoints(pointObjects)
        # check if there are at least 2 remaining points
        if len(pointObjects) < 2:
            raise Exception("Error - deserialization error, less than 2 remaining points")
        # generate function pieces
        self.piece = self.points2pieces(pointObjects)
        # merge consequent pieces with same slope
        self.simplify()

    def getDerivative(self):
        """Get function derivative.
        
        Returns:
        - PiecewiseLinear function
        """

        # declare function object
        derivative = PiecewiseLinear()
        # return if this function is not set
        if len(self.piece) == 0:
            return derivative
        # calculate derivatives of individual pieces
        for p in self.piece:
            start = Point(p.start.x, p.a)
            end = Point(p.end.x, p.a)
            derivative.piece.append()
        # merge consequent pieces with same slope
        derivative.simplify()
        # return function derivative
        return derivative
    
    def evaluate(self, input):
        """Calculate function output as out=f(in).
        
        Arguments:
        - input - function input
        Returns:
        - function output
        """
        
        if input < self.piece[0].end.x:
            return self.piece[0].eval(input)
        for p in self.piece:
            if input >= p.start.x and input < p.end.x:
                return p.eval(input)
        return self.piece[-1].eval(input)
    
    def simplify(self):
        """Remove unnecessary breakpoints (if two consequent pieces have the same slope 'a', merge them into one piece)."""
    
        if len(self.piece) < 2:
            return
        curr = 0
        next = 1
        while next < len(self.piece):
            if self.piece[curr] == self.piece[next] and self.piece[curr].end.y == self.piece[next].start.y:
                piece[curr].end = piece[next].end;
                piece.pop(next)
            else:
                curr += 1
                next += 1

    def removeDuplicitPoints(self, points):
        """Remove duplicit & close points from provided List (in-place).
        
        Arguments:
        - points - List of Point objects sorted by 'x' attribute
        """
        
        i = 0
        j = 1
        while j<len(points):
            if points[i].x == points[j].x and points[i].y == points[j].y:
                points.pop(i)
            else:
                i += 1
                j += 1
    
    def points2pieces(self, points):
        """Convert list of points into list of function pieces.
        
        Arguments:
        - points - list of (at least two) Point objects sorted by 'x' attribute
        Returns:
        - list of linear function pieces
        """
        
        #new piece list
        piece = []
        #point count check
        if (len(points) < 2):
            raise Exception("Error - cannot convert points to pieces, less than 2 points were provided")
        #local variables
        i = 0;
        j = 1;
        c = len(points);
        #handle discontinued initial point
        if points[0].x == points[1].x:
            additionalStartPoint = Point(float("-inf"), points[0].y)
            piece.append(Piece(additionalStartPoint, points[0]))
        #create function pieces
        while j < c:
            #check for discontinuity
            if points[i].x < points[j].x:
                #add function piece
                piece.append(Piece(points[i], points[j]));
            #increase counters
            i += 1
            j += 1
        #handle discontinued end point
        if points[c-2].x == points[c-1].x:
            additionalEndPoint = Point(float("inf"), points[c - 1].y);
            piece.append(Piece(points[c - 1], additionalEndPoint));
        #return list of pieces
        return piece
        
    def pieces2points(self, piece):
        """Convert function pieces into list of points.
        
        Returns:
        - list of Point objects sorted by 'x' attribute
        """

        #points to return
        points = []
        #return no points if there are no function pieces
        if (len(piece) < 1):
            raise Exception("Error - cannot convert pieces to points, no pieces were provided")
        #always add initial point
        points.append(Point(piece[0].start));
        #add remaining points
        prev = None
        for curr in piece:
            #add start point only in case of discontinuity
            if prev != None and prev.end.y != curr.start.y:
                points.append(Point(curr.start));
            #add end point of each piece
            points.append(Point(curr.end));
            #store reference to this piece
            prev = curr;
        return points;
        
### Helper classes ###

class Piece:
    """Piece helper class.
    
    Attributes:
    - start - starting Point object
    - end   - ending Point object
    - a     - piece slope
    - b     - piece shift
    """
    
    start = None
    end = None
    a = None
    b = None
    
    def __init__(self, start, end):
        """Function instantiation operation (constructor).
        
        Returns:
        - new Piece object.
        """
        
        self.start = Point(start)
        self.end = Point(end)
        if abs(self.start.x) == float("inf") and abs(self.end.x) == float("inf"):
            self.a = 0
            self.b = (self.start.y + self.end.y) / 2
        elif self.start.x == float("-inf"):
            self.a = 0
            self.b = self.end.y
        elif self.end.x == float("inf"):
            self.a = 0
            self.b = self.start.y
        elif self.start.x == self.end.x:
            self.a = 0
            self.b = (self.start.y+self.end.y)/2
        else:
            self.a = (self.start.y - self.end.y) / (self.start.x - self.end.x)
            self.b = self.start.y - self.a * self.start.x
            
    def eval(self, x):
        return self.a*x+self.b;

class Point:
    """Point helper class.
    
    Attributes:
    - x - x-coordinate
    - y - y-coordinate
    """
    
    x = None
    y = None
    
    def __init__(self, x=None, y=None):
        """Function instantiation operation (constructor).
        
        Arguments:
        - x - float value or Point object
        - y - float value or None
        Returns:
        - new Point object.
        """
        
        if type(x) is Point and y is None:
            self.x = x.x
            self.y = x.y
        elif x is None and y is None:
            self.x = 0
            self.y = 0
        elif (type(x) is float or type(x) is int) and (type(y) is float or type(y) is int):
            self.x = float(x)
            self.y = float(y)
        else:
            raise Exception("Error - wrong parameters: "+str(x)+" of type "+str(type(x))+", "+str(y)+" of type "+str(type(y)))
    