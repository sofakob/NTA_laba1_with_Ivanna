from sympy import primerange, nextprime
import math
import numpy as np
import galois
from laba1 import *

def gcd (a,b):
    if a == 0 and b == 0:
        return
    elif b == 0:
        return a
    else:
        return gcd(b, a%b)


def legendre(n, p):

    n_mod_p = n%p

    if n_mod_p == 0:
        return 0

    l = pow(n_mod_p, (p-1)//2, p) #за Ойлером

    if l == 1:
        return 1
    else:
        return -1


def factor_B(n):

    big_l = math.exp(math.sqrt(math.log(n) * math.log(math.log(n))))
    a = 1/math.sqrt(2)

    big_l_a = int(big_l**a)

    list_of_prime = list(primerange(1, big_l_a)) #генерує список послідовних простих чисев в діапазоні 1<p<L^a

    factor_base = []

    for p in list_of_prime: #до факторної бази додаються всі прості, для яких символ Лежандра = 1
        if legendre(n, p) == 1:
            factor_base.append(p)

    return factor_base


def continued_fraction(n, chain_len): #ланцюговий дріб

    alpha = math.sqrt(n) #початкові значення
    a = int(alpha)
    u = a
    v = 1

    a_i = [a]

    for i in range(chain_len):

        v = (n - u**2)//v
        alpha = (math.sqrt(n) + u)/v
        a = int(alpha)
        u = a*v - u

        a_i.append(a)

    b_i = []
    b_2 = 0  
    b_1 = 1  

    for i in a_i:
        b = i * b_1 + b_2
        b_i.append(b)
        b_2, b_1 = b_1, b #зсуваємо

    return b_i



#Функція для перевірки на гладкість (b_i)^2modn
def B_candidate(candidate, f_base): 
    for p in f_base:
        while candidate % p == 0:
            candidate //= p
    return candidate == 1 


#для розкладу на вектор степенів
def s_vector(s, f_base):

    vector = [0]*len(f_base)
    for i, p in enumerate(f_base):
        while s % p == 0:
            s //= p
            vector[i] ^= 1 #одразу вектор з 0 та 1
    return vector



def solve_SLE(A):

    GF2 = galois.GF(2)
    A_gf2 = GF2(A)
    
    null_space = A_gf2.null_space() #множина всіх розв'зків (список векторів)

    #кожен вектор у звичайний список
    basis_solutions = []
    for v in null_space:
        basis_solutions.append([int(x) for x in v])# v типу GF2-array у звичайний список
    return basis_solutions

    

 
def Brillhart_Morrison(n):
    
    f_base = factor_B(n)
    b_values = continued_fraction(n, 1000)

    B_numbers = []
    b_for_x = [] #ті b_i з яких потім можливо буде X

    #шукаємо гладкі
    for b in b_values:
        b_sq = pow(b, 2, n)  
        if B_candidate(b_sq, f_base):
            B_numbers.append(b_sq)  
            b_for_x.append(b)
            
        if len(B_numbers) > len(f_base):  
            break

    A = [] #матриця для СЛР
    for b_sq in B_numbers:
        A.append(s_vector(b_sq, f_base))

    solutions = solve_SLE(A)
    divisors = set()

    #обчислюємо x та у
    for solution in solutions:
        x = 1
        y = 1
        p_counts = [0]*len(f_base) #список для зберігання відповідних степенів p

        for i, j in enumerate(solution):
            if j and i < len(b_for_x):
                b = b_for_x[i] #відповідно до розв'язку беремо b для х
                b_num = B_numbers[i]
                x *= b

                for k, p in enumerate(f_base): #збираємо всі степені простих з відповідних підходящих гладких
                    while b_num % p == 0:
                        b_num //= p
                        p_counts[k] += 1

        for count, p in zip(p_counts, f_base): 
            y *= p ** count
        y = math.isqrt(y)  

        candidate1 = gcd(x + y, n)
        candidate2 = gcd(x - y, n)

        if not test_soloveia_shtrasena(int(candidate1)) and candidate1 not in [1, n]:
            divisors.add(candidate1)
        if not test_soloveia_shtrasena(int(candidate2)) and candidate2 not in [1, n]:
            divisors.add(candidate2)

    if  divisors:
        for i in divisors:
            n/=i
            n=int(n)
        divisors.add(n)

    return divisors



n = 4301 

print(Brillhart_Morrison(n))

