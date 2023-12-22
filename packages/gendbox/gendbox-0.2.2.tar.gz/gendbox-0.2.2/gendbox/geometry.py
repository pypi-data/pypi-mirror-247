class Circle:
    __pi = 3.1415926535
    def __init__(self, radius:float=None, circum:float=None, area:float=None, location:tuple=None, size:tuple=None):
        self.radius = None
        self.circum = None
        self.area = None
        self.location = None
        if radius == None and circum == None and area == None:
            raise ValueError("At least one of the parameters (radius, circum, area) must be specified.")
        else:
            if radius != None:
                self.radius = radius
                self.area = Circle.calculate_area(radius=radius)
                self.circum = Circle.calculate_circum(radius=radius)
            if circum != None:
                self.circum = circum
                self.radius = Circle.calculate_radius(circum=circum)
                self.area = Circle.calculate_area(circum=circum)
            if area != None:
                self.area = area
                self.radius = Circle.calculate_radius(area=area)
                self.circum = Circle.calculate_circum(area=area)
            
            
        
        
    def calculate_area(radius=None, circum=None):
        _radius = None
        if radius != None and circum == None:
            _radius = radius
        elif radius == None and circum != None:
            _radius = Circle.calculate_radius(circum=circum)
        area = Circle.__pi * (_radius ** 2)
        return area
    
    
    def calculate_circum(radius=None, area=None):
        _radius = None
        if radius != None and area == None:
            _radius = radius
        elif radius == None and area != None:
            _radius = Circle.calculate_radius(area=area)
        circum = 2 * Circle.__pi * _radius
        return circum
    
    
    def calculate_radius(circum=None, area=None):
        _circum = None
        if circum != None and area == None:
            _circum = circum
        elif circum == None and area != None:
            _circum = Circle.calculate_circum(area=area)
        radius = _circum/(2 * Circle.__pi)
        return radius
    

class Square:
    
    def __init__(self, side:float=None):
        if side is not None:
            self.side = side
            self.area = Square.calculate_area(side)
            self.diagonal = Square.calculate_diagonal(side)
            self.perimeter = Square.calculate_perimeter(side) 
           
    
    def calculate_area(side:float)->float:
        area = side**2
        return area
        
    def calculate_perimeter(side:float)->float:
        perimeter = side*4
        return perimeter

    def calculate_diagonal(side:float)->float:
        diagonal = side * (2**0.5)
        return diagonal
    
    @staticmethod
    def calculate_side(value:float, metric:str)->float:
        if metric == 'area':
            side = value**0.5
        elif metric == 'perimeter':
            side = value/4
        elif metric == 'diagonal':
            side = value/(2**0.5)
        else:
            raise ValueError("Please enter 'area', 'perimeter' or 'diagonal' in metric.")
        return side

    
class Rectangle:
    
    def __init__(self, x_side:float, y_side:float):
        self.x_side = x_side
        self.y_side = y_side
        self.area = Rectangle.calculate_area(x_side, y_side)
        self.diagonal = Rectangle.calculate_diagonal(x_side, y_side)
        self.perimeter = Rectangle.calculate_perimeter(x_side, y_side)    
    
    def calculate_area(x_side:float, y_side:float)->float:
        area = x_side * y_side
        return area
        
    def calculate_perimeter(x_side:float, y_side:float)->float:
        perimeter = x_side*2 + y_side*2
        return perimeter

    def calculate_diagonal(x_side:float, y_side:float)->float:
        diagonal = (x_side**2 + y_side**2)**0.5
        return diagonal

