import random




def test_soloveia_shtrasena(p):             
    '''Основна функція її юзаємо, на вхід приймається р, k можна змінювати, як я читала в залежності 
    від довжини числа треба збільшувати k, але більше 40 не рекомендовано брати, загалом 10-20 ітерацій повинно вистачати
    Ця функція повертає булеве значення True, якщо число складене та False, якщо просте
    '''
    k=10
    for i in range(k):
         x=random.randint(2, p-1)
         gcd_p_x=evklid(p, x)
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
    x_start=2
    y_start=2
    arr.append(0)
    while arr[0]!=1:
        arr=algoritm_for_ro_metod_Polarda(x_start, y_start, n)
        x_start+=1
        y_start+=1


    return arr[1] 

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
        d=evklid(abs(x-y), n)
        if d>1:
            arr.append(1)
            arr.append(d)
        elif d==0:
            arr.append(0)
            
    return arr
        
        
        

def function_for_Polard(x:int, n:int):
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
            b-=a
        else:
            d=b
            a-=b
    

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




a=527


c=ro_metod_Polarda(a)
print(c)