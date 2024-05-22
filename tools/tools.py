from Crypto.Util.number import inverse


def scalar_multiply(k, P, a, p):
    R = None
    Q = P

    while k > 0:
        if k % 2 == 1:
            if R is None:
                R = Q
            else:
                R = algebraic_add(R, Q, a, p)
        Q = algebraic_add(Q, Q, a, p)
        k //= 2
    return R


def algebraic_add(P, Q, a, p):
    if P != Q:
        m = ((P[1] - Q[1]) * inverse(P[0] - Q[0], p)) % p
    else:
        m = ((3 * P[0]**2 + a) * inverse(2 * P[1], p)) % p

    x_R = (m ** 2 - P[0] - Q[0]) % p
    y_R = (P[1] + m * (x_R - P[0])) % p
    return x_R, -y_R % p

