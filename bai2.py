import math
import random as rd
from itertools import combinations
import numpy as np
# tìm hệ số trên Ring

# Global variables
p = 2
n = 4
gSizeRing = p **n
# Function :
def UCLN_u_v_in_MOD(A, B, MOD):
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
    return (g * y) % MOD, G % MOD, H % MOD
def FindV(r):
    # tìm Nguy
    t = 0
    r_factor = math.factorial(r)
    while r_factor%(p**t)  == 0:
        t += 1
    t-=1
    # tìm V
    return min(t,n)

# tạo bảng hỗ trợ tính   max{t : p^t | r!}
def createSupportTable(p,n):
    cardinalityOfRing = p**n
    supTab = []
    result = [0]
    count = 0
    s = 0
    for r in range(1,cardinalityOfRing):
        count = 0
        while r % p == 0:
            count += 1
            r //= p
        supTab.append(count)
        s = sum(supTab)
        if s >= n:
            break
        result.append(s)
    # thêm phần còn lại của bảng sẽ là n
    result.extend([n] * (cardinalityOfRing-len(result)))
    # print(supTab)
    # print(result)
    return result
def DentaPhi(Phi,r,c=0):
    t1= t2 = 0
    for s in range(0,r+1,2):
        t1 += math.comb(r,s) * Phi[(c+s)%gSizeRing]
    for s in range(1,r+1,2):
        t2 += math.comb(r,s) * Phi[(c+s)%gSizeRing]
    if r &0b1:
        return (t2 - t1) #% gSizeRing
    return (t1 - t2) #% gSizeRing
def printTablePhi(phi):
    denta = 0
    arrDenta = []
    for j in range(gSizeRing):
        denta = DentaPhi(phi,j)
        arrDenta.append(denta)
    for id in range(len(arrDenta)):
        print(id,end=" & ")
    print("\\")
    for id in arrDenta:
        print(id,end=" & ")
    print("\\")     
def printTablePhi2(phi):
    denta = 0
    arrDenta = []
    for j in range(gSizeRing):
        denta = DentaPhi(phi,j)
        arrDenta.append(denta)
    for id in range(len(arrDenta)):
        print(f"{id:<{7}}",end="")
    print("")
    for id in arrDenta:
        print(f"{id:<{7}}",end="")
    print("") 
def checkPoly(phi):
    denta = 0
    v_temp = 0
    lstC = []
    lstCoeffs = [0] * gSizeRing
    Aj = Bj = Cj = A_inv = Pj = 0
    tableV = createSupportTable(p,n)
    #arrDenta = []
    for j in range(gSizeRing):
        denta = DentaPhi(phi,j)
        #arrDenta.append(denta)
        #v_temp = FindV(j)
        v_temp = tableV[j]
        if denta % p**v_temp !=0 :
                print(f"Not Polinomial at index r = {j}")
                return False
            
        if denta == 0 or v_temp == n: # th1 v_temp = n
            lstC.append(0)
        else: # th2 v_temp !=n 
            #print(f"{j} : {denta}")
            # Giải hệ so sánh:
            Aj = math.factorial(j) // (p**v_temp)
            Bj = denta // (p**v_temp)
            Pj = p**(n-v_temp)
            # giải hệ Ax = B (mod p^ (n - v_temp))
            # tìm Aj ^(-1)
            _,A_inv,_ = UCLN_u_v_in_MOD(Aj,Pj,gSizeRing)
            Cj =A_inv * Bj % gSizeRing
            #print(Cj)
            lstC.append(Cj)
    
    lstCoeffs[0] = lstC[0]       
    # tính hệ số 
    for n_temp in range(1,gSizeRing):
    # b1 sinh tất cả hệ số của hàm số x(x-1)...(x-(n-1))
        lstFuncTemp = [1]
        all_combinations = 0
        nums = list(range(1,n_temp))  # Tạo một danh sách từ 1 đến n - 1
        if n_temp > 1:
            lstFuncTemp.append((- sum(range(n_temp))) % gSizeRing)
        #t1= t2 = 0
        for j in range(2,n_temp,2):
            Cj = 0
            all_combinations = list(combinations(nums, j))
            for combo in all_combinations:
                Aj = 1
                for c in combo:
                    Aj *= c
                Cj += Aj
            lstFuncTemp.append(Cj % gSizeRing)   
        for j in range(3,n_temp,2):
            Cj = 0
            all_combinations = list(combinations(nums, j))
            for combo in all_combinations:
                Aj = 1
                for c in combo:
                    Aj *= c
                Cj -= Aj
            lstFuncTemp.append(Cj % gSizeRing)
            
        for deg in range(n_temp):
            lstCoeffs[deg+1] += lstFuncTemp[-1-deg] * lstC[n_temp]
            lstCoeffs[deg+1] %= gSizeRing
    return lstCoeffs


def f(x,coeffs):
    return np.polyval(coeffs,x)
# Main function 

def tt():
    for x in range(16):
        print((2*x + 3) % 16,end="  ")
    print()
if __name__ == '__main__':
    tt()
    Phi = [12, 5, 13, 6, 14, 7, 15, 0, 8, 1, 9, 2, 10, 3, 11, 4]
    print(Phi)
    printTablePhi2(Phi)
    # for j in range(gSizeRing):
    #     print(f"{j} : {DentaPhi(phi,j)}")
    res = (checkPoly(Phi))
    if res!=False:
        print(res)
        for i in range(gSizeRing):
            print(f(i,res[::-1]) % gSizeRing,end=" ")   
