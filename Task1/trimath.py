import math

EPS = 0.001

def vector_length(ab):
    return math.sqrt(ab[0] ** 2 + ab[1] ** 2)

def cos_of_vec(ab, ac):
    return (ab[0]*ac[0] + ab[1]*ac[1]) / (vector_length(ab)*vector_length(ac))

def sin_of_vec(ab, ac):
    return math.sqrt(1 - cos_of_vec(ab, ac) ** 2)

def vec_mult(ab, ac):
    return vector_length(ab) * vector_length(ac) * sin_of_vec(ab, ac)

def calculate_inscribed_circle(p1, p2, p3):
    p1p2 = [p2[i] - p1[i] for i in range(2)]
    p1p3 = [p3[i] - p1[i] for i in range(2)]
    p2p3 = [p3[i] - p2[i] for i in range(2)]

    R = vec_mult(p1p2, p1p3) / (vector_length(p1p2) + vector_length(p2p3) + vector_length(p1p3))

    # p1O = R / math.sin(math.asin(sin_of_vec(p1p2, p1p3)) / 2)
    p1O = R * math.sqrt(2) / math.sqrt(1 - cos_of_vec(p1p2, p1p3))

    l = [p1p2[i] / vector_length(p1p2) + p1p3[i] / vector_length(p1p3) for i in range(2)]
    l1 = [l[i] / vector_length(l) for i in range(2)]

    O = [p1[i] + l1[i] * p1O for i in range(2)]
    return O, R


def triangle_square(p1, p2, p3):
    p1p2 = [p2[i] - p1[i] for i in range(2)]
    p1p3 = [p3[i] - p1[i] for i in range(2)]
    return vec_mult(p1p2, p1p3) / 2

def circle_square(r):
    return math.pi * r ** 2

def inscribed_circle_square(p1, p2, p3):
    _, r = calculate_inscribed_circle(p1, p2, p3)
    return circle_square(r)

def diff_triange_inscribed_circle(p1, p2, p3):
    return triangle_square(p1, p2, p3) - inscribed_circle_square(p1, p2, p3)

def check_points(p1, p2):
    if (abs(p1[0] - p2[0]) < EPS and abs(p1[1] - p2[1]) < EPS):
        return True
    return False

def check_triangle_points(p1, p2, p3):
    if (check_points(p1, p2) or check_points(p1, p3) or check_points(p3, p2)):
        return False
    p1p2 = [p2[i] - p1[i] for i in range(2)]
    p1p3 = [p3[i] - p1[i] for i in range(2)]
    p2p3 = [p3[i] - p2[i] for i in range(2)]

    lenp1p2 = vector_length(p1p2)
    lenp2p3 = vector_length(p2p3)
    lenp1p3 = vector_length(p1p3)

    if abs(lenp1p2 + lenp2p3 - lenp1p3) < EPS or abs(lenp1p3 + lenp2p3 - lenp1p2) < EPS or abs(lenp1p2 + lenp1p3 - lenp2p3) < EPS:
        return False
    return True

def find_max_triangle(points, criteria):
    if len(points) < 3:
        return None
    max_triangle = None
    max_sum = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                now = (points[i], points[j], points[k])
                if (not check_triangle_points(*[i[1] for i in now])):
                    continue
                print(now)
                now_sum = criteria(*[i[1] for i in now])
                if (not max_triangle or now_sum > max_sum):
                    max_triangle = now
                    max_sum = now_sum
    return max_triangle

if __name__ == "__main__":
    print(calculate_inscribed_circle((10, -10), (-26.13, -10), (10, 26.13)))