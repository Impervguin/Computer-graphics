import Point
import DrawObjects as do
import Transform as tr

ORIGINAL = do.DrawCollection()
MODIFIED = ORIGINAL.copy()
ACTIONS = tr.ActionsCollection()

def shift(shift_x, shift_y, screen):
    action = tr.ShiftAction(Point.Point(shift_x, shift_y))
    ACTIONS.append(action)
    draw_modified(screen)
    return str(ACTIONS)

def scale(center_x, center_y, scale_x, scale_y, screen):
    action = tr.ScaleAction(scale_x, scale_y, Point.Point(center_x, center_y))
    ACTIONS.append(action)
    draw_modified(screen)
    return str(ACTIONS)

def rotate(center_x, center_y, angle, screen):
    action = tr.RotateAction(angle, Point.Point(center_x, center_y), indegrees=True)
    ACTIONS.append(action)
    draw_modified(screen)
    return str(ACTIONS)

def clear(screen):
    ACTIONS.clear()
    draw_modified(screen)
    return str(ACTIONS)

def undo(screen):
    try:
        ACTIONS.pop()
    except IndexError:
        pass
    draw_modified(screen)
    return str(ACTIONS)

def draw_modified(screen):
    MODIFIED = ORIGINAL.copy()
    MODIFIED.transform(ACTIONS)
    MODIFIED.dpgdraw(screen)

def draw_original(screen):
    ORIGINAL.dpgdraw(screen)
