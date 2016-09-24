import numpy as np


def reading(n):
    n1 = n
    while n1 & (n1 - 1):
        n1 += 1

    a = np.zeros((n1, n1), np.int64)
    for i in range(len(a)):
        for g in range(len(a)):
            if g >= n or i >= n:
                a[i][g] = 0
            else:
                a[i][g] = np.int64(input())
    return a


def m_parsing(a, n):
    middle = n // 2
    a11 = a[:middle, :middle]
    a12 = a[:middle, middle:]
    a21 = a[middle:, :middle]
    a22 = a[middle:, middle:]
    return (a11, a12, a21, a22)


def m_mul(a, b):
    n = len(a)

    if n == 1:
        return a * b

    a11, a12, a21, a22 = m_parsing(a, n)
    b11, b12, b21, b22 = m_parsing(b, n)

    p1 = m_mul(a11 + a22, b11 + b22)
    p2 = m_mul(a21 + a22, b11)
    p3 = m_mul(a11, b12 - b22)
    p4 = m_mul(a22, b21 - b11)
    p5 = m_mul(a11 + a12, b22)
    p6 = m_mul(a21 - a11, b11 + b12)
    p7 = m_mul(a12 - a22, b21 + b22)

    c = np.zeros((n, n), np.int64)
    middle = n // 2
    c[:middle, :middle] = p1 + p4 - p5 + p7
    c[:middle, middle:] = p3 + p5
    c[middle:, :middle] = p2 + p4
    c[middle:, middle:] = p1 - p2 + p3 + p6

    return c


def strassen():
    n1 = int(input())
    a = reading(n1)
    b = reading(n1)
    n = len(a)

    c = m_mul(a, b)

    for i in range(n1):
        for g in range(n1):
            if (g < n1 - 1):
                print(c[i][g], end=' ')
            else:
                print(c[i][g])

if __name__ == "__main__":
    strassen()
