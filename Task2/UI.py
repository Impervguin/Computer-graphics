import dearpygui.dearpygui as dpg

# center_x, center_y, angle, screen
ROTATE_ACTION = None

# shift_x, shift_y
SHIFT_ACTION = None

# center_x, center_y, scale_x, scale_y
SCALE_ACTION = None


CLEAR_ACTION = None

UNDO_ACTION = None

def clean_item(item_tag):
    for num in dpg.get_item_children(item_tag):
        for el in dpg.get_item_children(item_tag)[num]:
            dpg.delete_item(el)

def shift_callback():
    shift_x = dpg.get_value("ShiftX")
    shift_y = dpg.get_value("ShiftY")
    if abs(shift_x) < 0.5 or abs(shift_y) < 0.5:
        dpg.draw_text((300, 700), "Сдвиг не может быть меньше 0.5.", parent=MODIFIED, size=25)
        return
    clean_item(MODIFIED)
    
    dpg.set_value(LOG_TEXT, SHIFT_ACTION(shift_x, shift_y, MODIFIED))

def scale_callback():
    center_x = dpg.get_value("ScaleCenterX")
    center_y = dpg.get_value("ScaleCenterY")
    scale_x = dpg.get_value("ScaleX")
    scale_y = dpg.get_value("ScaleY")
    if abs(scale_x) < 0.001 or abs(scale_y) < 0.001:
        dpg.draw_text((300, 700), "Масштаб не может нулевым.", parent=MODIFIED, size=25)
        return

    clean_item(MODIFIED)
    dpg.set_value(LOG_TEXT, SCALE_ACTION(center_x, center_y, scale_x, scale_y, MODIFIED))
    

def rotate_callback():
    center_x = dpg.get_value("RotateCenterX")
    center_y = dpg.get_value("RotateCenterY")
    angle = dpg.get_value("RotateAngle")

    if abs(angle) < 0.001:
        dpg.draw_text((300, 700), "Угол поворота не может быть нулевым.", parent=MODIFIED, size=25)
        return

    clean_item(MODIFIED)
    dpg.set_value(LOG_TEXT, ROTATE_ACTION(center_x, center_y, angle, MODIFIED))

def undo_callback():
    clean_item(MODIFIED)
    dpg.set_value(LOG_TEXT, UNDO_ACTION(MODIFIED))

def clear_callback():
    clean_item(MODIFIED)
    dpg.set_value(LOG_TEXT, CLEAR_ACTION(MODIFIED))

# Minimum sizes of blocks in window
MINDRAW_BLOCK = (2000, 1000)
MINSHIFT = (400, 500)
MINSCALE = (400, 500)
MINROTATE = (400, 500)
MINLOG = (800, 500)
MININPUT_BLOCK = (MINSHIFT[0] + MINLOG[0] + MINROTATE[0] + MINSCALE[0], max(MINLOG[1], MINROTATE[1], MINSCALE[1], MINSHIFT[1]))
MINWINDOW =(max(MININPUT_BLOCK[0], MINDRAW_BLOCK[0]),  MINDRAW_BLOCK[1]+ MININPUT_BLOCK[1])
MINDRAW_BLOCK_BUTTONS_OFFSET = 200

LOG = "Log"
LOG_TEXT = "log"
SCALE = "Scale"
SHIFT = "Shift"
ROTATE = "Rotate"
ORIGINAL = "Original"
MODIFIED = "Modified"

WINDOW = MINWINDOW
def resize_callback(_, app_data):
    wsize = (app_data[0], app_data[1])
    position_resize(wsize=wsize)

def position_resize(wsize):
    DRAW_X = wsize[0] // 2
    DRAW_Y = wsize[0] // 2 if wsize[1] - wsize[0] // 2 > MININPUT_BLOCK[1] else wsize[1] - MININPUT_BLOCK[1]

    dpg.configure_item(ORIGINAL, pos=(0, 0), width=DRAW_X, height=DRAW_Y)
    dpg.configure_item(MODIFIED, pos=(DRAW_X, 0), width=DRAW_X, height=DRAW_Y)


    LOG_X = MINROTATE[0] + MINSCALE[0] + MINSHIFT[0]
    LOG_HEIGHT = wsize[1] - DRAW_Y
    LOG_WIDTH = wsize[0] - LOG_X
    dpg.configure_item(LOG, pos=(LOG_X, DRAW_Y), width=LOG_WIDTH, height=LOG_HEIGHT)
    dpg.configure_item(SCALE, pos=(0, DRAW_Y), width=MINSCALE[0], height=LOG_HEIGHT)
    dpg.configure_item(SHIFT, pos=(MINSCALE[0], DRAW_Y), width=MINSHIFT[0], height=LOG_HEIGHT)
    dpg.configure_item(ROTATE, pos=(MINSCALE[0] + MINSHIFT[0], DRAW_Y), width=MINROTATE[0], height=LOG_HEIGHT)

    dpg.configure_item(LOG_TEXT, height=LOG_HEIGHT - 200, width=LOG_WIDTH - 200)
    dpg.configure_item("LogButtonGroup", pos=(100, LOG_HEIGHT - 75), horizontal_spacing=LOG_WIDTH - 200 - 300)
    for b in ["ScaleButton", "ShiftButton", "RotateButton"]:
        dpg.configure_item(b, pos=(50, LOG_HEIGHT - 75))


def init_window():
    dpg.create_context()

    with dpg.font_registry():
        with dpg.font("UbuntuMono-B.ttf", 30) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

    
    dpg.bind_font(font)

    dpg.create_viewport(title='DRAW_TEST', width=MINWINDOW[0], height=MINWINDOW[1])
    dpg.set_viewport_resize_callback(callback=resize_callback)
    dpg.set_viewport_min_height(MINWINDOW[1])
    dpg.set_viewport_min_width(MINWINDOW[0])

def build_ui():
    dpg.add_window(tag=ORIGINAL, label=ORIGINAL)
    dpg.add_window(tag=MODIFIED, label=MODIFIED)

    with dpg.window(tag=LOG, label=LOG):
        dpg.add_input_text(multiline=True, label=LOG_TEXT, tag=LOG_TEXT, readonly=True, pos=(100, 100), width=MINLOG[0] - 300, height=MINLOG[1] - 300)
        with dpg.group(tag="LogButtonGroup", horizontal=True, horizontal_spacing=(MINLOG[0] - dpg.get_item_height(LOG_TEXT) - 300), pos=(100, MINLOG[1] - 75)):
            dpg.add_button(tag="UndoLog", label="Отменить", height=50, width=150, callback=undo_callback)
            dpg.add_button(tag="ClearLog", label="Очистить", height=50, width=150, callback=clear_callback)
    with dpg.window(tag=SCALE, label=SCALE):
        with dpg.group(indent=50):
            with dpg.group():
                dpg.add_text("Центр по x:")
                dpg.add_input_double(tag="ScaleCenterX")
            with dpg.group():
                dpg.add_text("Центр по y:")
                dpg.add_input_double(tag="ScaleCenterY")
            with dpg.group():
                dpg.add_text("Масштаб по x:")
                dpg.add_input_double(tag="ScaleX")
            with dpg.group():
                dpg.add_text("Масштаб по y:")
                dpg.add_input_double(tag="ScaleY")
        dpg.add_button(tag="ScaleButton", label="Масштабировать", width=300, height=50, pos=(50, MINSCALE[1] - 100), callback=scale_callback)
            
    with dpg.window(tag=SHIFT, label=SHIFT):
        with dpg.group(indent=50):
            with dpg.group():
                dpg.add_text("Сдвиг по x:")
                dpg.add_input_double(tag="ShiftX")
            with dpg.group():
                dpg.add_text("Сдвиг по y:")
                dpg.add_input_double(tag="ShiftY")
        dpg.add_button(tag="ShiftButton", label="Сдвинуть", width=300, height=50, pos=(50, MINSHIFT[1] - 100), callback=shift_callback)
    
    with dpg.window(tag=ROTATE, label=ROTATE):
        with dpg.group(indent=50):
            with dpg.group():
                dpg.add_text("Центр поворота по x:")
                dpg.add_input_double(tag="RotateCenterX")
            with dpg.group():
                dpg.add_text("Центр поворота по y:")
                dpg.add_input_double(tag="RotateCenterY")
            with dpg.group():
                dpg.add_text("Угол поворота\nпо часовой стрелке:")
                dpg.add_input_double(tag="RotateAngle")
        dpg.add_button(tag="RotateButton", label="Повернуть", width=300, height=50, pos=(50, MINROTATE[1] - 100), callback=rotate_callback)
    position_resize(MINWINDOW)


def start_ui():
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    init_window()
    build_ui()
    start_ui()


    

    
    