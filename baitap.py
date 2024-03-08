import numpy as np

def gcd(a, b):
    """
    This function returns the greatest common divisor (GCD) of two numbers a and b.
    """
    while b:
        a, b = b, a % b
    return a
def gcdChoNhieuSo(lst):
    res = lst[0]
    for elem in lst[1:]:
        res = gcd(res, elem)
    return res


def gcd_u_v(A, B):
    g = 1
    _A = A
    _B = B
    while _A % 2 == 0 and _B % 2 == 0:
        _A >>= 1
        _B >>= 1
        g <<= 1
    x, y, E, F, G, H = _A, _B, 1, 0, 0, 1
    while x != 0:
        while x % 2 == 0:
            x >>= 1
            if E % 2 == 0 and F % 2 == 0:
                F >>= 1
                E >>= 1
            else:
                E = (E + _B) >> 1
                F = (F - _A) >> 1
        while y % 2 == 0:
            y >>= 1
            if G % 2 == 0 and H % 2 == 0:
                G >>= 1
                H >>= 1
            else:
                G = (G + _B) >> 1
                H = (H - _A) >> 1
        if x >= y:
            x -= y
            E -= G
            F -= H
        else:
            y -= x
            G -= E
            H -= F

    # print(f"d = {g*y}")
    # print(f"u = {G}")
    # print(f"v = {H}")
    return g * y, G, H

def prime_factors(n):
    """
    This function returns the prime factors of the given number n.
    """
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

def timHeSoCuaC(lst,k):
    lst_res = []
    #tim he só cho 3 so
    a1 = lst[0]
    d1 = gcd(a1,k)
    d = 0
    a2 = 0
    a1_temp = 0
    c2 = 0
    i=0
    for idx in range(0,len(lst)-1):
        a2 = lst[idx+1]
        c2 = 1
        print(f"a1 = {a1},a2 = {a2}")
        if a1 != 0 and a2 != 0:
            d = gcdChoNhieuSo([a1,a2,k])
            a1_temp,k_temp = a1//d,k//d
            # tim he so
            i = 2
            while i * i <= k_temp:
                if k_temp % i:
                    i += 1
                else:
                    k_temp //= i
                    if a1_temp % i:
                        c2*=i
            if k_temp > 1 and a1_temp %k_temp:
                c2 *=k_temp
        elif a2==0:
            c2 = 0
        lst_res.append(c2)
        a1 += a2*c2
    lst_res.insert(0,1)
    lst_res =[t % k for t in lst_res]
    return lst_res,a1
    
def mainProcess(alpha,beta,k):
    # buoc 1 : check có cùng d không ?
    d1 = gcdChoNhieuSo(alpha)
    d2 = gcdChoNhieuSo(beta)
    if d1 != d2:
        print("2 bộ khác gcd : ", d1, d2)
    else:
        # tìm bộ c2,..,cn
        lst_c_alpha,a = timHeSoCuaC(alpha,k)
        lst_c_beta,b = timHeSoCuaC(beta,k)
        # tìm ma trận F
        #  # chỉ cần ghi nhớ hàng đầu của F là đủ
        F = [((beta[i]-alpha[i])//d1 ) % k for i in range(1,len(alpha))]
        F.insert(0,1)
        
        # tìm s1, (s1,k) = 1 và s1 * d1 = 1 (mod k)
        k_temp = k//d1
        a//=d1
        b//=d1
        b%=k_temp
        a%=k_temp
        _,u1,_ = gcd_u_v(a,k_temp)
        u1 %= k_temp
        lst_c_temp,s1 = timHeSoCuaC([u1,k_temp],k)
        s1%=k
        #s1 = (u1 + k_temp*lst_c_temp[1])%k
        # # tương tự cho d2  =  d1
        _,u1,_ = gcd_u_v(b,k_temp)
        u1 %= k_temp
        lst_c_temp,s2 = timHeSoCuaC([u1,k_temp],k)
        s2%=k
        _,s2,_ = gcd_u_v(s2,k)
        s2 %= k
        # k_temp = k//d1
        # _,u1,_ = gcd_u_v(d1,k_temp)
        # lst_c_temp = timHeSoCuaC([u1,k_temp],k)
        # s2 = u1 + k_temp*lst_c_temp[1]

        # Nhân ma trân A1 với s1
        # # chỉ cân nhân vào cột đầu là đủ
        # # tạo cột A1 và nhân với A2
        A1 = [(elem * s1) % k for elem in lst_c_alpha]
        
        # sau đó nhân với F
        
        Matrix_A = [A1.copy()]
        print(Matrix_A)
        
        
        A1_cp =[]
        for idx,elem2 in enumerate(F[1:]):
            A1_cp = [elem * elem2 for elem in A1]
            A1_cp[idx+1] +=1
            Matrix_A.append([elem % k for elem in A1_cp])
        Matrix_A = np.array(Matrix_A)
        Matrix_A=Matrix_A.transpose()
        print(Matrix_A)
        
        # sau đó nhân B2 invert
        for row in Matrix_A:
            row[0] = (row[0]*s2) % k
                
        print(Matrix_A)
        Matrix_A=Matrix_A.transpose()
        print(Matrix_A)
        # nhân với B1 invert lst_c_beta
        for idx in range(1,Matrix_A.shape[0]):
            Matrix_A[0] = Matrix_A[0] - (Matrix_A[idx] * lst_c_beta[idx])
            Matrix_A[0] = Matrix_A[0] % k
            print(Matrix_A)
        Matrix_A = Matrix_A.transpose()
        print("================================ result ===========================\n\n")
        print(Matrix_A)
        return Matrix_A
        # xây dựng ma trận A1,A2,B1,B2
        
############################################ Main #######################################

n = 4
p = 2
q = p**n - 1
