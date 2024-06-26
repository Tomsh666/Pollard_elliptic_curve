from multiprocessing import Process, Manager
from random import randint
import pandas as pd

from Crypto.Util.number import inverse

from tools import algebraic_add, scalar_multiply


def pollard_parallel(curve_params, P, Q, q, result_dict, proc_id, data_dict):
    p = curve_params[2]
    data_list = []

    while True:
        L = randint(1, 50)
        aj = []
        bj = []
        Rj = []
        for j in range(1, L+1):
            aj.append(randint(0, q - 1))
            bj.append(randint(0, q - 1))
            tmp_aj = scalar_multiply(aj[j-1], P, curve_params[0], p)
            tmp_bj = scalar_multiply(bj[j-1], Q, curve_params[0], p)
            Rj.append(algebraic_add(tmp_aj, tmp_bj, curve_params[0], p))
        print("a_j =", aj)
        print("b_j =", bj)
        print("R_j =", Rj)

        alpha_1 = randint(0, q - 1)
        betta_1 = randint(0, q - 1)
        tmp_alpha_1 = scalar_multiply(alpha_1, P, curve_params[0], p)
        tmp_betta_1 = scalar_multiply(betta_1, Q, curve_params[0], p)
        T_1 = algebraic_add(tmp_alpha_1, tmp_betta_1, curve_params[0], p)
        T_2 = T_1
        alpha_2 = alpha_1
        betta_2 = betta_1
        print("alpha' =", alpha_1)
        print("betta' =", betta_1)
        print("T' =", T_1)

        while True:
            # func misc
            j = H(T_1, L)
            T_1 = algebraic_add(T_1, Rj[j], curve_params[0], p)
            alpha_1 = (alpha_1 + aj[j]) % q
            betta_1 = (betta_1 + bj[j]) % q

            j = H(T_2, L)
            T_2 = algebraic_add(T_2, Rj[j], curve_params[0], p)
            alpha_2 = (alpha_2 + aj[j]) % q
            betta_2 = (betta_2 + bj[j]) % q

            j = H(T_2, L)
            T_2 = algebraic_add(T_2, Rj[j], curve_params[0], p)
            alpha_2 = (alpha_2 + aj[j]) % q
            betta_2 = (betta_2 + bj[j]) % q
            data_list.append((j, alpha_1, betta_1, T_1, alpha_2, betta_2, T_2))

            if T_1 == T_2:
                break

        if alpha_1 != alpha_2 and betta_1 != betta_2:
            d = (alpha_1 - alpha_2) * inverse(betta_2 - betta_1, q) % q
            result_dict[proc_id] = d
            data_dict[proc_id] = data_list
            break


def H(P, L):
    x, y = P
    return (x + y) % L


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


def main():
    # curve_params, P, Q, q = get_input()
    curve_params = (1, 11, 307)
    P = (306, 304)
    Q = (146, 65)
    q = 167

    print(f"\nCurve: y^2 = x^3 + {curve_params[0]}x + {curve_params[1]} (mod {curve_params[2]})")
    print(f"Point P: {P}")
    print(f"Point Q: {Q}")

    manager = Manager()
    result_dict = manager.dict()
    data_dict = manager.dict()
    processes = []

    for i in range(16):
        p = Process(target=pollard_parallel, args=(curve_params, P, Q, q, result_dict, i, data_dict))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    for key, value in result_dict.items():
        print(f"Process {key}: d = {value} (mod {q})")

    for key, data_list in data_dict.items():
        columns = ['j', 'alpha_1', 'betta_1', 'T_1', 'alpha_2', 'betta_2', 'T_2']
        df = pd.DataFrame(data_list, columns=columns)
        print(f"\nData for process {key}:")
        print(df)

if __name__ == '__main__':
    main()
