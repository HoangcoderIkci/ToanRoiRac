SIZEPOLE = 16 # количество элементов в поле
CHAR = 2  # символ
DEGREE = 4  # степень многочлена f
LIMIT = 0  # используется для функции циклического сдвига битов; для t = 4 соответствует 0b1111 = 0xF
hsPole = 19  # соответствует x^4 + x + 1
g_r = 1
#hsPole = 285; # x8 + x4 + x3 + x2 + 1


arrMultiple = [[0 for _ in range(SIZEPOLE)] for _ in range(SIZEPOLE)]
arrOppositeArray = [0] * SIZEPOLE  # на позиции x находится обратное к x
ArrayPowerSupport = [0] * SIZEPOLE  # на позиции i находится значение x^i
ArrayPower = []   # на позиции [x][i] находится x^i

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
        # ищем позицию temp в arrSp
        index_temp = ArrayPowerSupport.index(temp)
        for idx2 in range(2,SIZEPOLE):
            temp = (idx2 * index_temp) % (SIZEPOLE - 1)
            lst_temp.append(ArrayPowerSupport[temp])
        ArrayPower.append(lst_temp.copy())           
    #return      
def __startCreateMatrices():
    createArrayMult()
    createArrayPower()
    # вывод таблицы:
    
    ArrayPower[0][0] = 1
############## начало функций битов #################
def circleRegister(X,r):
    r %= DEGREE
    return (X >> DEGREE-r) ^ (X << r) & (LIMIT)
def changeLimit(t):
    global LIMIT
    LIMIT = (1 << t) - 1   
    
    
########### конец функций битов #################

########### начало функций обработки #################

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
########### конец функций обработки #################
def change_r(r):
    global g_r 
    g_r = r
######  начало функции создания массивов
def printTables():
    # таблица 1:
    print("================================================================")
    print("================================================================")
    print("Таблица 1\n  ",end="")
    for idx in range(SIZEPOLE):
        print(f"{hex(idx)[2:]:<{2}}",end="")
    print()
    idx = 0
    for elem_r in arrMultiple:
        print(f"{hex(idx)[2:]:<{2}}",end="")
        idx+=1
        for elem_c in elem_r:
            #print(str(elem_c).center(3),end=" ")
            print(f"{hex(elem_c)[2:]:<{2}}",end="")
        print()
    # таблица 2:
    print("================================================================")
    print("================================================================")
    print("Таблица 2\n  ",end="")
    for idx in range(SIZEPOLE-1,-1,-1):
        print(f"a^{idx:<{3}}",end="")
    print()
    idx = 0
    for elem_r in ArrayPower:
        print(f"{hex(idx)[2:]:<{3}}",end="")
        idx+=1
        for elem_c in elem_r[::-1]:
            #print(str(elem_c).center(3),end=" ")
            print(f"{hex(elem_c)[2:]:<{5}}",end="")
        print()
    print("================================================================")
    print("================================================================")
######  конец функции создания массивов
__startCreateMatrices()  ## создание матриц умножения, матриц обратных элементов, матриц ст
changeLimit(DEGREE)  ## изменить LIMIT на количество битов, которое нужно использовать
change_r(1)
#printTables()
# для b в диапазоне от 0 до 16:
lst_val_func = createTable(10)
print(lst_val_func)
#     если len(set(lst_val_func)) != 16:
#         print("ошибка")
lst_res = findCoefficientFunctionVersion2(lst_val_func)
#print(lst_res)
i = 0
t = 0
print("Коэффициенты функции f(X): ")
for elem in lst_res:
    print(f"{hex(elem)[2:]}x^{i}",end= " + ")
    i+=1
    t ^=elem
    
print()



# проверить правильность коэффициентов    
# print()


for idx in range(SIZEPOLE):
# print(F_at(lst_res,idx),end= "  ")
    t = F_at(lst_res,idx)
    if t != lst_val_func[idx]:
        print("???")
print("\nНайденная функция верна!!!!!!!!!!!!")
