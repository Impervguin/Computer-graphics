import UI
import Point
import ObjectsUI as oui
import DrawObjects as do

UI.SHIFT_ACTION = oui.shift
UI.ROTATE_ACTION = oui.rotate
UI.SCALE_ACTION = oui.scale
UI.CLEAR_ACTION = oui.clear
UI.UNDO_ACTION = oui.undo

oui.ORIGINAL.append(do.DrawAstroid((500, 500), 150, with_center=True))
oui.ORIGINAL.append(do.DrawCircle((500, 500), 35))
oui.ORIGINAL.append(do.DrawObject((0, 0), Point.Point(350, 500), Point.Point(350, 700), Point.Point(650, 700), Point.Point(650, 500)))

UI.init_window()
UI.build_ui()

oui.draw_original(UI.ORIGINAL)
oui.draw_modified(UI.MODIFIED)

UI.start_ui()