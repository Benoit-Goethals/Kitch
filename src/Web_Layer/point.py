class Point:
    def __init__(self,*,x:float,y:float,description:str,summary:str):
        self.__x:float = x
        self.__y:float = y
        self.__description:str = description
        self.__summary:str = summary


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
        return [self.x,self.y]





