class Point:
    """
    Represents a point in a 2D coordinate system with additional descriptive attributes.

    This class encapsulates x and y coordinates, along with a description, summary,
    and an optional value for a radius or magnitude. It provides properties for
    managing these attributes and methods to convert point data into lists.

    :ivar __x: X-coordinate of the point.
    :type __x: float
    :ivar __y: Y-coordinate of the point.
    :type __y: float
    :ivar __description: Descriptive text about the point.
    :type __description: str
    :ivar __summary: Summary information related to the point.
    :type __summary: str
    :ivar __value_radius: Optional radius or magnitude value associated with the point.
    :type __value_radius: float
    """
    def __init__(self,*,x:float,y:float,description:str,summary:str,value:float=0):
        self.__x:float = x
        self.__y:float = y
        self.__description:str = description
        self.__summary:str = summary
        self.__value_radius:float = value


    @property
    def x(self)->float:
        return self.__x
    @property
    def y(self)->float:
        return self.__y
    @x.setter
    def x(self,value:float):
        self.__x = value
    @y.setter
    def y(self,value:float):
        self.__y = value


    @property
    def value_radius(self)->float:
        return self.__value_radius

    @value_radius.setter
    def value_radius(self,value:float):
        self.__value_radius = value

    @property
    def description(self)->str:
        return self.__description
    @description.setter
    def description(self,value:str):
        self.__description = value

    @property
    def summary(self)->str:
        return self.__summary
    @summary.setter
    def summary(self,value:str):
        self.__summary = value

    def point_to_lst(self)-> list[float]:
        return [self.x,self.y,self.value_radius]

    def to_points(self) -> list[float]:
        return [self.x, self.y]

    def __str__(self):
        return f"Point(x={self.x},y={self.y},description={self.description})"

    def __repr__(self):
        return self.__str__()





