class Point:
    def __init__(self,*,x:float,y:float,description:str,summary:str):
        self.__x = x
        self.__y = y
        self.__description = description
        self.__summary = summary


    @property
    def x(self):
        return self.__x
    @property
    def y(self):
        return self.__y
    @x.setter
    def x(self,value):
        self.__x = value
    @y.setter
    def y(self,value):
        self.__y = value

    @property
    def description(self):
        return self.__description
    @description.setter
    def description(self,value):
        self.__description = value

    @property
    def summary(self):
        return self.__summary
    @summary.setter
    def summary(self,value):
        self.__summary = value

    def point_to_lst(self):
        return [self.x,self.y]





