import random




def test_soloveia_shtrasena(p):
    k=10
    for i in range(k):
         x=random.randint(2, p-1)
         gcd_p_x=evklid(p, x)
         if gcd_p_x==1:
             bool_function=check_psevdoprost_Euler(x, p)
             if bool_function:
                 k+=1
             else:
                 return "Число складене"
         else:
             return "Число складене"
         
    return "Число просте"
                 
             


    return 0
def evklid(a, b):
    while a!=b:
        if a<b:
            d=a
            b-=a
        else:
            d=b
            a-=b

    return d

def check_psevdoprost_Euler(a, p):
    a_p=jacobi(a, p)
    exponent=(p-1)/2
    a=pow(int(a), int(exponent), p)
    if a==a_p or a-p==a_p:
        return True
    else:
        return False
def jacobi(x, n):
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




a=5717


c=test_soloveia_shtrasena(a)
print(c)