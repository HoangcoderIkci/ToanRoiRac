from bai2 import *
SIZEPOLE = 16 # số lượng elem trong field 
CHAR = 2  # character
DEGREE = 4  # bậc đa thức f
LIMIT = 0  # dùng cho hàm dịch bit vòng ; với t = 4 tương ứng với 0b1111 = 0xF
hsPole = 19  # tương ứng với x^4 + x + 1
g_r = 1
#hsPole = 285; # x8 + x4 + x3 + x2 + 1


arrMultiple = [[0 for _ in range(SIZEPOLE)] for _ in range(SIZEPOLE)]
arrOppositeArray = [0] * SIZEPOLE  # tại vị trí x là nghịch đảo của x
ArrayPowerSupport = [0] * SIZEPOLE  # tại vị trí i là giá trị của x^i
ArrayPower = []   # tại vị trí[x][i]  là x^i

def multipleTwoElement(a, b):
    _a = a
    b_ = b
    c = 0
    gh = (1 << DEGREE)
    while  b_ != 0:
        if b_ & 0x1:
            c^=_a
        _a<<= 1
        b_ >>= 1
        if _a & gh:
            _a ^= hsPole
    return c
def createArrayMult():
    for i in range(SIZEPOLE):
        for j in range(i,SIZEPOLE):
            temp = multipleTwoElement(i, j)
            arrMultiple[i][j] = temp
            arrMultiple[j][i] = temp
            if temp == 1:
                arrOppositeArray[i] = j
                arrOppositeArray[j] = i
def createArrayPower():
    ArrayPowerSupport[0] = 1
    temp = 2
    for idx1 in range(1,SIZEPOLE):
        ArrayPowerSupport[idx1] = temp
        temp = arrMultiple[2][temp]                
    lst_temp = []
    ArrayPower.append([0] * SIZEPOLE)
    ArrayPower.append([1] * SIZEPOLE)
    ArrayPower.append(ArrayPowerSupport)
    for idx1 in range(3,SIZEPOLE):
        temp = idx1
        lst_temp = [1,temp]
        # tìm vị trí của temp trong arrSp
        index_temp = ArrayPowerSupport.index(temp)
        for idx2 in range(2,SIZEPOLE):
            temp = (idx2 * index_temp) % (SIZEPOLE - 1)
            lst_temp.append(ArrayPowerSupport[temp])
        ArrayPower.append(lst_temp.copy())           
    #return      
def __startCreateMatrices():
    createArrayMult()
    createArrayPower()
    ArrayPower[0][0] = 1
############## begin bit functions #################
def circleRegister(X,r):
    r %= DEGREE
    return (X >> DEGREE-r) ^ (X << r) & (LIMIT)
def changeLimit(t):
    global LIMIT
    LIMIT = (1 << t) - 1   
    
    
########### end  bit functions #################

########### begin handle functions #################

def F(x,b,r):
    return circleRegister((x+b)%SIZEPOLE,r)

def createTable(b):
    valFunc = 0
    #b = 11
    r = g_r
    lst_val_func = []
    binary_x = 0
    for idx1 in range(SIZEPOLE):
        valFunc = F(idx1,b,r)
        lst_val_func.append(valFunc)
        binary_x = bin(idx1)[2:]
        print(binary_x,end="  ")
        print(valFunc)
    return lst_val_func
def findCoefficientFunction(lst_val_func):
    coeff = 0
    lst_coeff_func = []
    temp1 = 0
    for deg in range(SIZEPOLE):
        coeff = 0
        for elem in range(SIZEPOLE):
            temp1 = arrMultiple[lst_val_func[elem]][ArrayPower[elem][SIZEPOLE-1-deg]]
            coeff ^= temp1
        lst_coeff_func.append(coeff)
    return lst_coeff_func
def findCoefficientFunctionVersion2(lst_val_func):
    coeff = 0
    lst_coeff_func = []
    temp1 = 0
    lst_coeff_func.append(lst_val_func[0])
    for deg in range(SIZEPOLE-1):
        coeff = 0
        for elem in range(SIZEPOLE):
            temp1 = arrMultiple[lst_val_func[elem]][ArrayPower[elem][SIZEPOLE-2-deg]]
            coeff ^= temp1
        lst_coeff_func.append(coeff)
    return lst_coeff_func
def F_at(lst_hs,a):
    res = 0
    temp = 1
    for idx in range(len(lst_hs)):
        res ^= arrMultiple[lst_hs[idx]][temp]
        temp = arrMultiple[temp][a]
    return res
########### end  handle functions #################
def change_r(r):
    global g_r 
    g_r = r
######  begin hàm tạo mảng
def printTables():
    # table 1:
    print("================================================================")
    print("================================================================")
    print("Table 1")
    for elem_r in arrMultiple:
        for elem_c in elem_r:
            #print(str(elem_c).center(3),end=" ")
            print(f"{elem_c:<{5}}",end=" ")
        print()
    # table 2:
    print("================================================================")
    print("================================================================")
    print("Table 2")
    for elem in ArrayPower:
        print(elem)
    print("================================================================")
    print("================================================================")
######  end hàm tạo mảng
__startCreateMatrices()  ## tạo ma trận nhân, ma trận nghịch đảo, ma trận mũ
changeLimit(DEGREE)  ## chỉnh sửa lại LIMIT = số lượng bit cần dùng
change_r(3)
# for b in range(9,10):
# for b in range(17):
b = 0
lst_val_func = createTable(11)
print(lst_val_func)

Phi = lst_val_func
res = (checkPoly(Phi))
if res!=False:
        print(res)
        for i in range(gSizeRing):
            print(f(i,res[::-1]) % gSizeRing,end=" ")