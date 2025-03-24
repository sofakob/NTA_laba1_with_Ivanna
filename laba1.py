import random
from sympy import primerange, nextprime
import math
import numpy as np
import galois
from decimal import Decimal


def test_soloveia_shtrasena(p):             
    '''Основна функція її юзаємо, на вхід приймається р, k можна змінювати, як я читала в залежності 
    від довжини числа треба збільшувати k, але більше 40 не рекомендовано брати, загалом 10-20 ітерацій повинно вистачати
    Ця функція повертає булеве значення True, якщо число складене та False, якщо просте
    '''
    p_int=int(p)
    k=10
    if p<=2:
        return False
    for i in range(k):
         x=random.randint(2, p_int-1)
         x=Decimal(x)
        
         gcd_p_x=gcd(p, x)
         if gcd_p_x==1:
             bool_function=check_psevdoprost_Euler(x, p)
             if bool_function:
                 k+=1
             else:
                 return True# "Число складене"
         else:
             return True# "Число складене"
         
    return False# "Число просте"
                 

def ro_metod_Polarda(n):    # Теж основна функція

    ''' На вхід беремо тільки n, функція використовується як і методичці f(x)=x^2+1. 
    змінні x_start, y_start виведені саме так, щоби можна було їх змінити та запустити цей алгоритм з іншими значеннями, 
    на вихід ми подаємо дільник
'''
    arr=[]
    x_start=Decimal(2)
    y_start=Decimal(2)
    arr.append(0)
    while arr[0]!=1 and x_start<11:
        arr=algoritm_for_ro_metod_Polarda(x_start, y_start, n)
        x_start+=1
        y_start+=1


    return int(arr[1])

def algoritm_for_ro_metod_Polarda(x, y, n):
    '''
    Допоміжна функція, виведена окремо, щоби легко змінювати значення х та у, та не заплутатися в циклах, на вихід подаємо список
    два елементи якщо ми знайшли дільник, та один якщо дійшли до ситуації, коли х=у
    '''
    d=1
    arr=[]
    while d==1: 
        x=function_for_Polard(x, n)
        y=function_for_Polard(function_for_Polard(y, n), n)
        d=gcd(abs(x-y), n)
        if d>1:
            arr.append(1)
            arr.append(d)
        elif d==0:
            arr.append(0)
            arr.append(0)
            
    return arr
        
        
        

def function_for_Polard(x, n):
    '''
    Допоміжна функція щоби при необхідності швидко змінити f(x)=x^2+1
    '''
    t=(pow(x, 2)+1)%n
    
    return  t


def evklid(a, b):
    
    '''
    Допоміжна функція обрахунок gcd, так як це алгоритм Евкліда то і назва така, чому не gcd, бо в моменті Евклідом назвати було зручніше
    '''
    if a==0 or b==0:
        return 0
    while a!=b:
        if a<b:
            d=a
            b%=a
        else:
            d=b
            a%=b
    

    return d

def check_psevdoprost_Euler(a, p):

    '''Перевірка числа чи є воно псевдо простим зо Ойлером, вихід функції булевий
    '''
    a_p=jacobi(a, p)
    exponent=(p-1)/2
    a=pow(int(a), int(exponent), p)
    if a==a_p or a-p==a_p:
        return True
    else:
        return False



def jacobi(x, n):
    ''' 
    Символ Якобі, рекурсивний
    '''
    x=Decimal(x)
    if x==0 or x==1:
        return x
    elif x==2:
        exponent=(pow(n, 2)-1)/8
        j=pow(-1, exponent)
        return j
    elif x%2==0:
        k=0
        while x%2==0:
            k+=1
            x/=2
        if k%2==0:
            j=jacobi(x, n)
            return j
        else:
            exponent=(pow(n, 2)-1)/8
            j=pow(-1, exponent)*jacobi(x, n)
            return j
    else:
        exponent=(x-1)*(n-1)/4
        modul=n%x
        j=pow(-1, exponent)*jacobi(modul, x)          
        return j


def prime_factorization(n):
    cheking_number=test_soloveia_shtrasena(n)
    if cheking_number==True:
        print(f"Число: {n} є складеним")
        list_of_divisors=[]#список для дільників числа
        bool_function=True
        while bool_function:
            bool_function, d, n=trial_division(n)
            if d!=1:
                list_of_divisors.append(d)

        
                

        


        d=Decimal(ro_metod_Polarda(n))
       
        if d!=0:
            print(f"Дільник знайдено {d}")
            list_of_divisors.append(d)
            #print(list_of_divisors)
            n/=d
            cheking_number=test_soloveia_shtrasena(n)
            if cheking_number==False:
                list_of_divisors.append(n)
                return list_of_divisors
            divisori_BM=Brillhart_Morrison(n)
            if not divisori_BM:
                return "я не можу знайти канонiчний розклад числа :("
            else:
                list_of_divisors.extend(divisori_BM)
        return list_of_divisors
    else:
        return "Число просте"
            



            

def r_i_sequence(m, digits_num):

    b = 10
    r_i = []
    
    r =1
    for i in range(digits_num):
        r_i.append(r)
        r = (r * b) % m 

    return r_i 

    
exp = r_i_sequence(7, 8)



def trial_division(n):
    
    prime = [Decimal(2), Decimal(3), Decimal(5), Decimal(7), Decimal(11), Decimal(13), Decimal(17), Decimal(19), Decimal(23), Decimal(29), Decimal(31), Decimal(37), Decimal(41), Decimal(43), Decimal(47)]

    n_digits = [int(d) for d in str(n)]
    a_i = n_digits[::-1] #список з цифр n в оберненому порядку

    
    for p in prime:       
        r_i_p_seq = r_i_sequence(p, len(a_i)) #послідовність r_i для р

        sum_ = 0 #сума для а_i * r_i
         
        for i, a in enumerate(a_i):
            sum_ += a * r_i_p_seq[i]

        if sum_ % p == 0:
            print(f"Дільник знайдено {p}")
            #print(n/p)
            return True, p, n/p # на мою думку дивно, що дільники будуть плаваючими точками (Якщо проти видаляй)

    return False, 1, n


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
    n_sqrt=n.sqrt()

    alpha = n_sqrt#початкові значення
    a = Decimal(int(alpha))
    u = a
    v = Decimal(1)

    a_i = [a]

    for i in range(chain_len):

        v = (n - u**2)//v

        alpha = (n_sqrt + u)/v
        a = Decimal(int(alpha))
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

        candidate1 = Decimal(gcd(x + y, n))
        candidate2 = Decimal(gcd(x - y, n))
        

        if not test_soloveia_shtrasena(candidate1) and candidate1 not in [1, n]:
            divisors.add(candidate1)
        if not test_soloveia_shtrasena(candidate2) and candidate2 not in [1, n]:
            divisors.add(candidate2)

    if  divisors:
        for i in divisors:
            n/=i
            n=int(n)
        divisors.add(n)

    return divisors






print(prime_factorization(Decimal("303983")))

 
