import numpy as np

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def __getitem__(self, key):
        return (self.x, self.y)[key]

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
    
# if __name__ == "__main__":
    # print(*Point(10, 20))