# import dearpygui.dearpygui as dpg

# N = 1

# def add_num():
#     x = dpg.get_value("x_input")
#     y = dpg.get_value("y_input")
#     with dpg.table_row(parent="table"):
#         dpg.add_text(str(N))
#         dpg.add_text(str(x))
#         dpg.add_text(str(y))

# dpg.create_context()

import Interface

Interface.build_ui()
Interface.show()



