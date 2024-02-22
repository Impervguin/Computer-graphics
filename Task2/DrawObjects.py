import Transform as tr
import dearpygui.dearpygui as dpg
import math as m
import numpy as np
from Point import Point

DEFAULT_STEP = m.pi / 30

class DrawObject:
    def __init__(self, start_shift : Point, *points) -> None:
        self.points = points
        for p in self.points:
            p.shift(*start_shift)
    
    def dpgdraw(self, screen_tag):
        dpg.draw_polygon([list(map(int, p.get_tuple())) for p in self.points], parent=screen_tag)

    def transform(self, matrix):
        for p in self.points:
            p.transform(matrix)
    
    def copy(self):
        return DrawObject(Point(0, 0), *[p.copy() for p in self.points])

class DrawCircle(DrawObject):
    def __init__(self, start_shift : Point, r, step=DEFAULT_STEP) -> None:
        points = []
        now_angle = 0
        while now_angle < m.pi * 2:
            x = r * m.cos(now_angle)
            y = r * m.sin(now_angle)
            points.append(Point(x, y))
            now_angle += step
        super().__init__(start_shift, *points)


class DrawAstroid(DrawObject):
    def __init__(self, start_shift, amplitude, step=DEFAULT_STEP) -> None:
        points = []
        now_angle = 0
        while now_angle < m.pi * 2:
            x = amplitude * m.cos(now_angle) ** 3
            y = amplitude * m.sin(now_angle) ** 3
            points.append(Point(x, y))
            now_angle += step
        super().__init__(start_shift, *points)


class DrawCollection:
    def __init__(self, *objs) -> None:
        self.objs = objs
    
    def dpgdraw(self, screen_tag):
        for obj in self.objs:
            obj.dpgdraw(screen_tag)
    
    def transform(self, action : tr.TransformAction):
        mat = action.get_matrix()
        for obj in self.objs:
            obj.transform(mat)
    
    def copy(self):
        return DrawCollection(*[obj.copy() for obj in self.objs])



if __name__ == "__main__":
    ast = DrawAstroid((500, 500), 100)

    circle = DrawCircle((500, 500), 30)
    polygon = DrawObject((400, 500), Point(0,0), Point(0, 200), Point(200, 200), Point(200, 0))
    col = DrawCollection(ast, circle, polygon)

    astc = col.copy()

    dpg.create_context()
    dpg.create_viewport(title='DRAW_TEST', width=1000, height=1000)
    dpg.add_window(pos=(0, 0), width=1000, height=1000, label="Draw", tag="draw")

    masch = tr.ScaleAction(2, 2, Point(500, 500))
    rotate = tr.RotateAction(45, Point(500, 500), True)
    acol = tr.ActionsCollection(masch, rotate)
    col.transform(acol)
    col.dpgdraw("draw")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

