import dearpygui.dearpygui as dpg
import trimath as tm


TEXT_SIZE = 25

def put_triangle_on_screen(points, screen_sizes, margins):
    xny = [el[1] for el in points]
    xs = [point[0] for point in xny]
    ys = [point[1] for point in xny]

    max_x = max(xs)
    min_x = min(xs)

    max_y = max(ys)
    min_y = min(ys)

    dx = max_x - min_x
    dy = max_y - min_y

    k = min((screen_sizes[0] - margins[0] * 2) / dx, (screen_sizes[1] - margins[1] * 2) / dy)

    screen_points = [(int((point[0] - min_x) * k) + margins[0], int(screen_sizes[1] - margins[1] * 2 - (point[1] - min_y) * k + margins[1])) for point in xny]
    print(screen_points)

    return list(zip([el[0] for el in points], screen_points)), k, (min_x, min_y)

def put_inscribed_circle_on_screen(points, coef, shift, screen_sizes, margins):
    center, r = tm.calculate_inscribed_circle(*[el[1] for el in points])
    screen_center = [
        int((center[0] - shift[0]) * coef) + margins[0],
        int(screen_sizes[1] - margins[1] * 2 - (center[1] - shift[1]) * coef + margins[1])
    ]
    screen_r = int(r * coef)
    return screen_center, screen_r

def draw_trianle_info(src_points, screen_coords, screen_sizes, margins, screen_tag):
    xny = [el[1] for el in src_points]

    draw_trianle_point_info(xny[0], xny[1], xny[2], screen_coords[0][1], f"N:{src_points[0][0]:.3f}\n({xny[0][0]:.3f}, {xny[0][1]:.3f})", screen_tag)
    draw_trianle_point_info(xny[1], xny[0], xny[2], screen_coords[1][1], f"N:{src_points[1][0]:.3f}\n({xny[1][0]:.3f}, {xny[1][1]:.3f})", screen_tag)
    draw_trianle_point_info(xny[2], xny[1], xny[0], screen_coords[2][1], f"N:{src_points[2][0]:.3f}\n({xny[2][0]:.3f}, {xny[2][1]:.3f})", screen_tag)


def draw_trianle_point_info(p1, p2, p3, screen_p1, mess, screen_tag):
    if p1[0] > p2[0] and p1[1] > p3[1] or p1[0] > p3[0] and p1[1] > p2[1]:
        dpg.draw_text((screen_p1[0] + TEXT_SIZE * 2, screen_p1[1] - TEXT_SIZE * 2), mess, parent=screen_tag, size=TEXT_SIZE)
    elif p1[0] < p2[0] and p1[1] > p3[1] or p1[0] < p3[0] and p1[1] > p2[1]:
        dpg.draw_text((screen_p1[0] - TEXT_SIZE * 2, screen_p1[1] - TEXT_SIZE * 2), mess, parent=screen_tag, size=TEXT_SIZE)
    elif p1[0] < p2[0] and p1[1] < p3[1] or p1[0] < p3[0] and p1[1] < p2[1]:
        dpg.draw_text((screen_p1[0] - TEXT_SIZE * 2, screen_p1[1] + TEXT_SIZE * 2), mess, parent=screen_tag, size=TEXT_SIZE)
    elif p1[0] > p2[0] and p1[1] < p3[1] or p1[0] > p3[0] and p1[1] < p2[1]:
        dpg.draw_text((screen_p1[0] + TEXT_SIZE * 2, screen_p1[1] + TEXT_SIZE * 2), mess, parent=screen_tag, size=TEXT_SIZE)


def draw_inscribed_circle_on_screen(points, screen_sizes, margins, screen_tag):
    _, k, shift = put_triangle_on_screen(points, screen_sizes, margins)

    precenter, prer = tm.calculate_inscribed_circle(*[el[1]for el in points])
    center, r = put_inscribed_circle_on_screen(points, k, shift, screen_sizes, margins)

    dpg.draw_circle(center, r, parent=screen_tag, thickness=5)
    dpg.draw_circle(center, 7, fill=(255, 255, 255), parent=screen_tag)
    dpg.draw_text(center, f"Center\n({precenter[0]:.3f}, {precenter[1]:.3f})\nR={prer:.3f}", parent=screen_tag, size=TEXT_SIZE)

def draw_triangle_on_screen(points, screen_sizes, margins, screen_tag):
    coords, *_ = put_triangle_on_screen(points, screen_sizes, margins)
    xny = [el[1] for el in coords]
    dpg.draw_triangle(*xny, parent=screen_tag, thickness=5)
    for point in xny:
        dpg.draw_circle(point, 7, parent=screen_tag, fill=(255, 255, 255))
    draw_trianle_info(points, coords,screen_sizes, margins, screen_tag)
