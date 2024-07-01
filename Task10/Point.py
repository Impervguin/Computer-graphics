import numpy as np

class Point:
    def __init__(self, x, y, intensity=1) -> None:
        self.x = x
        self.y = y
        self.intensity = intensity
    
    def __getitem__(self, key):
        return (self.x, self.y)[key]
    
    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise Exception("Wrong key")

    def __len__(self):
        return 2

    def shift(self, x_shift, y_shift):
        self.x += x_shift
        self.y += y_shift
    
    def get_tuple(self):
        return (self.x, self.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def transform(self, matrix):
        c = [self.x, self.y, 1]
        res = np.matmul(c, matrix)
        self.x = res[0] / res[2]
        self.y = res[1] / res[2] 
    
    def copy(self):
        return Point(self.x, self.y)
    
    def __eq__(self, value: object) -> bool:
        if value[0] == self.x and value[1] == self.y:
            return True
        return False
    
    def scalar(self, other) -> float:
        return self[0] * other[0] + self[1] * other[1]
    
    def vector(self, other) -> float:
        return self[0] * other[1] - self[1] * other[0]
    
    def vectorLength(self) -> float:
        return (self[0] ** 2 + self[1] ** 2) ** 0.5

    