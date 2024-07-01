from Point import Point
import math as m
import numpy as np
from copy import deepcopy

class TransformAction:
    def __init__(self, matrix : list[list[float]]) -> None:
        self.matrix = matrix
    
    def get_matrix(self):
        return self.matrix
    
    def __add__(self, other):
        return TransformAction([list(row) for row in np.matmul(self.get_matrix(), other.get_matrix())])

    def do_action(self, point):
        homo_point = [point.x, point.y, 1]
        res = list(np.matmul(homo_point, self.get_matrix()))
        return Point(res[0] / res[2], res[1] / res[2])


class RotateAction(TransformAction):
    def __init__(self, angle, center : Point, indegrees=False) -> None:
        self.center = center
        self.angle = angle if not indegrees else m.radians(angle)
        shift = ShiftAction(Point(-center.x, -center.y))
        rotate = TransformAction([[m.cos(self.angle), -m.sin(self.angle), 0], 
                                  [m.sin(self.angle), m.cos(self.angle), 0],
                                  [0, 0, 1]
                                   ])
        shiftback = ShiftAction(center)
        matrix = (shift + rotate + shiftback).get_matrix()
        super().__init__(matrix)
    
    def __str__(self):
        return f"Поворот на {self.angle:.3g} радиан вокруг ({self.center.x:.3g}, {self.center.y:.3g})"
    
class ShiftAction(TransformAction):
    def __init__(self, shift : Point) -> None:
        self.shift = shift
        matrix = [[1, 0, 0], 
                  [0, 1, 0], 
                  [shift.x, shift.y, 1]
                  ]
        super().__init__(matrix)
    
    def __str__(self):
        return f"Сдвиг на {self.shift.x:.3g} по x и {self.shift.y:.3g} по y"


class ScaleAction(TransformAction):
    def __init__(self, scalex, scaley, center : Point) -> None:
        self.scale = Point(scalex, scaley)
        self.center = center
        shift = ShiftAction(Point(-center.x, -center.y))
        scale = TransformAction([[scalex, 0, 0], 
                                 [0, scaley, 0], 
                                 [0, 0, 1]
                                 ])
        shiftback = ShiftAction(center)
        matrix = (shift + scale + shiftback).get_matrix()
        super().__init__(matrix)
    
    def __str__(self):
        return f"Масшатбирование с коэффициентами ({self.scale.x:.3g}, {self.scale.y:.3g}) от точки ({self.center.x:.3g}, {self.center.y:.3g})"

class ActionsCollection(TransformAction):
    def __init__(self, *actions : TransformAction) -> None:
        self.actions = list(actions)
        self.matrix = None

    def __str__(self):
        return "\n".join(map(str, self.actions))

    def get_matrix(self):
        if (not self.matrix):
            self.matrix = sum(self.actions, start=TransformAction([[1, 0, 0], [0, 1, 0], [0, 0, 1]])).get_matrix()
        return self.matrix

    def __add__(self, other):
        if (isinstance(other, ActionsCollection)):
            return ActionsCollection(self.actions + other.actions)
        elif (isinstance(other, TransformAction)):
            return ActionsCollection(self.actions + [other])
        raise TypeError("Can only be ActionsCollection or TransformAction children.")

        # return TransformAction(self.actions + other.actions)
    
    def append(self, action):
        if (not isinstance(action, TransformAction)):
            raise TypeError("Can only be TransformAction children")
        self.actions.append(action)
        self.matrix = None
    
    def pop(self, ind = -1):
        self.actions.pop(ind)
        self.matrix = None
    
    def clear(self):
        self.actions.clear()
        self.matrix = None

E = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
class TransformAction3:
    def __init__(self, matrix : list[list[float]] = deepcopy(E)) -> None:
        self.matrix = matrix
    
    def get_matrix(self):
        return self.matrix
    
    def __add__(self, other):
        return TransformAction3([list(row) for row in np.matmul(self.get_matrix(), other.get_matrix())])

    def do_action(self, x, y, z):
        homo_point = [x, y, z, 1]
        res = list(np.matmul(homo_point, self.get_matrix()))
        return res[0] / res[3], res[1] / res[3], res[2] / res[3]
    
class RotateAction3ox(TransformAction3):
    def __init__(self, angle, x, y, z, indegrees=False) -> None:
        self.angle = angle if not indegrees else m.radians(angle)
        shift = ShiftAction3(-x, -y, -z)
        rotate = TransformAction([[1, 0, 0, 0], 
                                 [0, np.cos(angle), np.sin(angle), 0],
                                 [0, -np.sin(angle), np.cos(angle), 0],
                                 [0, 0, 0, 1]
                                 ])
        shiftback = ShiftAction3(x, y, z)
        matrix = (shift + rotate + shiftback).get_matrix()
        super().__init__(matrix)
    
    def __str__(self):
        return f"Поворот на {self.angle:.3g} радиан вокруг ({self.center.x:.3g}, {self.center.y:.3g})"
    
class RotateAction3oz(TransformAction3):
    def __init__(self, angle, x, y, z, indegrees=False) -> None:
        self.angle = angle if not indegrees else m.radians(angle)
        shift = ShiftAction3(-x, -y, -z)
        rotate = TransformAction([[np.cos(angle), -np.sin(angle), 0, 0], 
                                 [np.sin(angle), np.cos(angle), 0, 0],
                                 [0, 0, 1 , 0],
                                 [0, 0, 0, 1]
                                 ])
        shiftback = ShiftAction3(x, y, z)
        matrix = (shift + rotate + shiftback).get_matrix()
        super().__init__(matrix)
    
    def __str__(self):
        return f"Поворот на {self.angle:.3g} радиан вокруг ({self.center.x:.3g}, {self.center.y:.3g})"
    
class RotateAction3oy(TransformAction3):
    def __init__(self, angle, x, y, z, indegrees=False) -> None:
        self.angle = angle if not indegrees else m.radians(angle)
        shift = ShiftAction3(-x, -y, -z)
        rotate = TransformAction([[np.cos(angle), 0, np.sin(angle), 0], 
                                 [0, 1, 0, 0],
                                 [-np.sin(angle), 0, np.cos(angle), 0],
                                 [0, 0, 0, 1]
                                 ])
        shiftback = ShiftAction3(x, y, z)
        matrix = (shift + rotate + shiftback).get_matrix()
        super().__init__(matrix)
    
    def __str__(self):
        return f"Поворот на {self.angle:.3g} радиан вокруг ({self.center.x:.3g}, {self.center.y:.3g})"
    
class ShiftAction3(TransformAction3):
    def __init__(self, x, y, z) -> None:
        matrix = [[1, 0, 0, 0], 
                  [0, 1, 0, 0], 
                  [0, 0, 1, 0],
                  [x, y, z,  1]
                  ]
        super().__init__(matrix)
    
    def __str__(self):
        return f"Сдвиг на {self.shift.x:.3g} по x и {self.shift.y:.3g} по y"


class ScaleAction3(TransformAction3):
    def __init__(self, scalex, scaley, scalez, x, y, z) -> None:
        shift = ShiftAction3(-x, -y, -z)
        scale = TransformAction([[scalex, 0, 0, 0], 
                                 [0, scaley, 0, 0],
                                 [0, 0, scalez, 0],
                                 [0, 0, 0, 1]
                                 ])
        shiftback = ShiftAction3(x, y, z)
        matrix = (shift + scale + shiftback).get_matrix()
        super().__init__(matrix)
    
    def __str__(self):
        return f"Масшатбирование с коэффициентами ({self.scale.x:.3g}, {self.scale.y:.3g}) от точки ({self.center.x:.3g}, {self.center.y:.3g})"

