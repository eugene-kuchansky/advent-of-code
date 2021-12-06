with open('input_data/22.txt') as f:
    shuffles = f.read().strip().split('\n')

D = 119315717514047  # deck size


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def reverse_deal(i):
    return D-1-i
    
def reverse_cut(i, N):
    return (i+N+D) % D

def reverse_increment(i, N):
    return modinv(N, D) * i % D  # modinv is modular inverse

def f(x, shuffles):
    for line in reversed(shuffles):
        if line.endswith("stack"):
            x = reverse_deal(x)
            continue
        N = int(line.split()[-1])
        if line.startswith('cut'):
            x = reverse_cut(x, N)
        else:
            x = reverse_increment(x, N)
    return x
X = 2020
Y = f(X, shuffles)
Z = f(Y, shuffles)
A = (Y-Z) * modinv(X-Y+D, D) % D
B = (Y-A*X) % D
print(A, B)

n = 101741582076661
# = A^n*x + (A^n-1) / (A-1) * B
print((pow(A, n, D)*X + (pow(A, n, D) - 1) * modinv(A-1, D) * B) % D)
print((pow(A, n, D)*X + (pow(A, n, D)-1) * modinv(A-1, D) * B) % D)
