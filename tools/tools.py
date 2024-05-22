def scalar_multiply_vector(k, point, p, a):
    tmp_point = point
    for i in range(k % p):
        tmp_point = sum_points(tmp_point, point, p, a)


def sum_points(point1, point2, p, a):
    result = []
    if point1 != point2:
        alpha = (point1[1] - point2[1]) // (point1[0] - point2[0]) % p
    else:
        alpha = (3 * (point1[0] ** 2) + a) * (2 * point1[1])
    result.append((alpha ** 2 - point1[0] - point2[0]) % p)
    result.append((point1[1] + alpha * (result[0] - point1[0])) % p)
    return result

