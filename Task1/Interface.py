import dearpygui.dearpygui as dpg
import dpg_draw as dpgdraw
import trimath as tm

WINDOW_SIZES = (2400, 1400)
INPUT_SIZES = (1000, WINDOW_SIZES[1]/2)
DRAW_SIZES = (WINDOW_SIZES[0] - INPUT_SIZES[0], WINDOW_SIZES[1])
TABLEW_SIZES = (INPUT_SIZES[0], WINDOW_SIZES[1]/2)
LOG_SIZES = (INPUT_SIZES[0] - 200, INPUT_SIZES[1] - 400)
INFO_SIZES = (600, 350)
MARGINS = (300, 300)
POPUP_TEXT="""
Программа для нахождения
треугольника среди заданных точек
с максимальной разницей между
площадью треугольника и вписанной
в него окружностью.
"""


POINTS_LIST = [(10, -10), (0, 17.3), (-17.3, -10)]
LINE = 1

def log(mess):
    global LINE
    text = dpg.get_value("log")
    dpg.set_value("log", text + str(LINE) + ") " + mess + '\n')
    LINE += 1

def clean_item(item_tag):
    for num in dpg.get_item_children(item_tag):
        for el in dpg.get_item_children(item_tag)[num]:
            dpg.delete_item(el)

def do_business():
    if len(POINTS_LIST) < 3:
        log("Недостаточно точек.")
        return
    triangle = tm.find_max_triangle(list(zip(range(1, len(POINTS_LIST) + 1), POINTS_LIST)), tm.diff_triange_inscribed_circle)
    if (not triangle):
        log("Не построить треугольник по заданным точкам.")
        return

    
    log("Треугольник с максимальной разницей:")
    print(triangle)
    for p in triangle:
        log(f"{p[0]}:({p[1][0]:.3f}, {p[1][1]:.3f})")
    log(f"Площадь треугольника: {tm.triangle_square(*[i[1] for i in triangle]):.3f}")
    log(f"Площадь вписанной окружностью: {tm.inscribed_circle_square(*[i[1] for i in triangle]):.3f}")
    
    clean_item("draww")
    print(triangle)
    dpgdraw.draw_triangle_on_screen(triangle, DRAW_SIZES, MARGINS, "draww")
    dpgdraw.draw_inscribed_circle_on_screen(triangle, DRAW_SIZES, MARGINS, "draww")
    

def add_point():
    x = dpg.get_value("x_input")
    y = dpg.get_value("y_input")
    POINTS_LIST.append((x, y))
    redraw_table(len(POINTS_LIST) - 1)

def delete_point():
    n = dpg.get_value("n_input")
    if len(POINTS_LIST) < n or n <= 0:
        log("Invalid point number.")
        return
    
    POINTS_LIST.pop(n - 1)
    redraw_table(len(POINTS_LIST) + 1)


def modify_point():
    n = dpg.get_value("n_input")
    if len(POINTS_LIST) < n or n <= 0:
        log("Invalid point number.")
        return
    x = dpg.get_value("x_input")
    y = dpg.get_value("y_input")

    POINTS_LIST[n - 1] = (x, y)
    redraw_table(len(POINTS_LIST))

def clear_points():
    n = len(POINTS_LIST)
    POINTS_LIST.clear()
    redraw_table(n)

def redraw_table(now):
    for i in range(now):
        dpg.delete_item(f"trow{i}")
    for i in range(len(POINTS_LIST)):
        with dpg.table_row(parent="table", tag=f"trow{i}"):
            dpg.add_text(str(i + 1))
            dpg.add_text(str(POINTS_LIST[i][0]))
            dpg.add_text(str(POINTS_LIST[i][1]))
    

def build_ui():
    dpg.create_context()

    with dpg.font_registry():
        with dpg.font("UbuntuMono-B.ttf", 30) as font:
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)


    dpg.bind_font(font)


    with dpg.window(pos=(0, 0), width=INPUT_SIZES[0], height=INPUT_SIZES[1], label="Ввод", tag="inputw"):
        dpg.add_input_double(label="X", tag="x_input", width=260, pos=(55, 100), min_value=-3000, max_value=3000)
        dpg.add_input_double(label="Y", tag="y_input", width=260, pos=(370, 100), min_value=-3000, max_value=3000)
        dpg.add_input_int(label="N", tag="n_input", width=260, pos=(685, 100), min_value=-3000, max_value=3000)
        # dpg.draw_text(pos=(450, 0), text="Point Info",size=30)
        dpg.add_button(label="Добавить", tag="add_button", pos=(40, 200), callback=add_point, width=200)
        dpg.add_button(label="Удалить", tag="delete_button", pos=(280, 200), callback=delete_point, width=200)
        dpg.add_button(label="Редактировать", tag="mod_button", pos=(520, 200), callback=modify_point, width=200)
        dpg.add_button(label="Очистить", tag="clear_button", pos=(760, 200), callback=clear_points, width=200)
        dpg.add_button(label="Вычислить", callback=do_business, tag="do_button", pos=(300, 250), width=400)
        dpg.add_input_text(label="Лог", pos=(100, 300), width=LOG_SIZES[0], height=LOG_SIZES[1], multiline=True, tag="log", readonly=True)
        dpg.add_button(label="Инфо", pos=(100, 325 + LOG_SIZES[1]), width=200, tag="infobutton", callback=lambda: (dpg.configure_item("infopopup", show=True), dpg.set_primary_window("infopopup", True),dpg.set_primary_window("infopopup", False)))
        
        
        # dpg.add_text(label="Log", pos=(100, 300), width=800, height=400)

    dpg.add_window(pos=(0, INPUT_SIZES[1]), width=TABLEW_SIZES[0], height=TABLEW_SIZES[1], label="Таблица", tag="tablew")
    dpg.add_window(pos=(INPUT_SIZES[0], 0), width=DRAW_SIZES[0], height=DRAW_SIZES[1], label="Рисовалка", tag="draww")


    with dpg.window(pos=(WINDOW_SIZES[0] // 2 - INFO_SIZES[0] // 2, WINDOW_SIZES[1] // 2 - INFO_SIZES[1] // 2), width=INFO_SIZES[0], height=INFO_SIZES[1], label="Инфо", tag ="infopopup"):
        dpg.add_text(POPUP_TEXT)
        dpg.add_button(label="Закрыть", callback=lambda: dpg.configure_item("infopopup", show=False), width=200, height=50, pos=(INFO_SIZES[0] // 2 - 100, INFO_SIZES[1] - 75))

    # dpgdraw.draw_triangle_on_screen([(1, (10, -10)), (2, (10, 17.3)),(3, (-37.3, -10))], (1400, 1400), (200, 200), "draww")
    # dpgdraw.draw_inscribed_circle_on_screen([(1, (10, -10)), (2, (10, 17.3)),(3, (-37.3, -10))], (1400, 1400), (200, 200), "draww")

    dpg.add_table(parent="tablew", tag="table", label="table")
    dpg.add_table_column(parent="table", label="Num")
    dpg.add_table_column(parent="table", label="X")
    dpg.add_table_column(parent="table", label="Y")
    redraw_table(len(POINTS_LIST))

    dpg.create_viewport(title='Lab 1', width=WINDOW_SIZES[0], height=WINDOW_SIZES[1])
    dpg.setup_dearpygui()

def show():
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()