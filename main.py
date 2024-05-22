from random import randint
from tools import scalar_multiply_vector, sum_points


def main():
    #curve_params, P, Q, q = get_input()
    curve_params = (1, 11, 307)
    p = curve_params[2]
    P = (306, 304)
    Q = (146, 65)
    q = 167

    print(f"\nCurve: y^2 = x^3 + {curve_params[0]}x + {curve_params[1]} (mod {curve_params[2]})")
    print(f"Point P: {P}")
    print(f"Point Q: {Q}")
    #L = randint(1, 10)
    L = 4
    aj = [71, 71, 93, 156]
    bj = [62, 157, 50, 76]
    Rj = []
    for j in range(1, L+1):
        #aj.append(randint(0, q - 1))
        #bj.append(randint(0, q - 1))
        tmp_aj = scalar_multiply_vector(aj[j-1], P, p, curve_params[0])
        tmp_bj = scalar_multiply_vector(bj[j-1], Q, p, curve_params[0])
        Rj.append(sum_points(tmp_aj, tmp_bj, p, curve_params[0]))
    print(aj)
    print(bj)
    print(Rj)


def H(P, L):
    x, y = P
    return (x + y) % L + 1

def get_input():
    print("Enter elliptic curve params:")
    a = int(input("a: "))
    b = int(input("b: "))
    p = int(input("p: "))

    print("\nEnter the coordinates of point P:")
    Px = int(input("Px: "))
    Py = int(input("Py: "))

    print("\nEnter the coordinates of point Q:")
    Qx = int(input("Qx: "))
    Qy = int(input("Qy: "))

    q = int(input("\nEnter group order q: "))

    return (a, b, p), (Px, Py), (Qx, Qy), q



if __name__ == '__main__':
    main()
