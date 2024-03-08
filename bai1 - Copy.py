from sympy import symbols, Or, And, Not
from math import log2
# Định nghĩa các biến
x1, x2, x3, x4, x5, x6 = symbols('x1 x2 x3 x4 x5 x6')
variables = [x1, x2, x3, x4, x5, x6]

def listToLogic(input_list):
    # Chuyển đổi mỗi list con thành một biểu thức And
    clauses = []
    for sub_list in input_list:
        clause = []
        for i, val in enumerate(sub_list):
            if val == 1:
                clause.append(variables[i])
            else:
                clause.append(Not(variables[i]))
        clauses.append(And(*clause))
    
    # Kết hợp tất cả các biểu thức And bằng Or
    return Or(*clauses)
# Hàm chuyển đổi binary:
def convertToBinary(num : int,lenBit):
    res =  [int(x) for x in bin(num)[2:]]
    temp = [0] * (lenBit - len(res))
    temp.extend(res)
    return temp

def check_columns_property(matrix):
    for col in zip(*matrix):
        unique_values = set(col)
        if len(unique_values) > 2:
            return False
    return True

def createTableAssignmentFunction(coefficients : list,num_variables : int,k : int):
    num_rows = 1 << (num_variables-k)
    num_cols = 1 << k
    f_x = listToLogic(coefficients)
    #g_x = (x3 +x1*x2+x1*x2*x3) * (x4+x4*x6 +x4*x5*x6) + x6 + x4 + x4*x5 + x4*x5*x6
    g_x = (x3 +x1*x2+x1*x2*x3) * (x6+x4*x6 +x4*x5) + x4+x4*x6 +x4*x5*x6
    # lst_variables_r = ['x' + str(num) for num in range(k+1,num_variables+1)]
    # lst_variables_c = ['x' + str(num) for num in range(1,k+1)]
    lst_variables_all = ['x' + str(num) for num in range(1,num_variables+1)]
    lst_value_of_func = []
    matrix = []
    for num_r in range(num_rows):
        bina_type_r = convertToBinary(num_r,num_variables-k)
        #bool_values = dict(zip(lst_variables_r, bina_type_r))
        #lst_value_of_func.append(f_x.subs(bool_values))
        for num_c in range(num_cols):
            bina_type_c = convertToBinary(num_c,k)
            bina_type_all = bina_type_c + bina_type_r
            bool_values = dict(zip(lst_variables_all, bina_type_all))
            value = f_x.subs(bool_values)
            # Thay đổi giá trị False thành 0 và True thành 1
            value = 1 if value else 0
            lst_value_of_func.append(value)
            print(value,end='  ')
        print()
    
        matrix.append(lst_value_of_func)
        lst_value_of_func = []
    # check 
    lst_value_of_func = []
    matrix2 = []
    print("################################")
    for num_r in range(num_rows):
        bina_type_r = convertToBinary(num_r,num_variables-k)
        #bool_values = dict(zip(lst_variables_r, bina_type_r))
        #lst_value_of_func.append(f_x.subs(bool_values))
        for num_c in range(num_cols):
            bina_type_c = convertToBinary(num_c,k)
            bina_type_all = bina_type_c + bina_type_r
            bool_values = dict(zip(lst_variables_all, bina_type_all))
            value = g_x.subs(bool_values) & 0b1
            # Thay đổi giá trị False thành 0 và True thành 1
            #value = 1 if value else 0
            lst_value_of_func.append(value)
            print(value,end='  ')
        print()
        
        matrix2.append(lst_value_of_func)
        lst_value_of_func = []
        
    if matrix == matrix2:
        print("bang nhau")
    return matrix
def IsDecomposition(matrix : list):
    return check_columns_property(matrix)

def decomposeBinaFunc(lst_coefficients : list,num_variables : int,k):
    # b1 tao mang gia tri 2 chieu
    table_values = createTableAssignmentFunction(lst_coefficients,num_variables,k)
    isDec = IsDecomposition(table_values)
    # b2 nếu có thể decompose :
    if isDec == False:
        print("function cannot compose")
        return False
    # b3 h(x) là hàng đầu tiên khác 0
    id_not_null = 0
    for row in table_values:
        if not all(item == 0 for item in row):
            trust_table_h_x = row
            break
        id_not_null +=1
    # tìm hệ số của h(x) БПФ
    lst_h_x = findCoefficients(trust_table_h_x)
    print("he so của h(x) :")
    print(lst_h_x)
    # tifm F0 F1
    for idx1 in range(len(trust_table_h_x)):
        if trust_table_h_x[idx1] == 0:
            idx_F_0 = idx1
            break
    for idx1 in range(len(trust_table_h_x)):
        if trust_table_h_x[idx1] != 0:
            idx_F_1 = idx1
            break
    col_idx_F_0 = []
    for row in table_values:
        col_idx_F_0.append(row[idx_F_0])
    col_idx_F_1 = []
    for row in table_values:
        col_idx_F_1.append(row[idx_F_1])
        
    lst_F_0 = findCoefficients(col_idx_F_0)
    print("he so của F0(x) :")
    print(lst_F_0)
    lst_F_1 = findCoefficients(col_idx_F_1)
    print("he so của F1(x) :")
    print(lst_F_1)
def findCoefficients(lst_coefficients : list):
    length = len(lst_coefficients)
    k = int(log2(length))
    res = [x for x in lst_coefficients]
    for idx1 in range(k):
        half_len = 1 << idx1
        full_len = half_len << 1
        num_turns = length // full_len
        for idx2 in range(num_turns):
            for idx3 in range(half_len):
                res[idx2 * full_len+half_len+idx3] ^= res[idx2 * full_len+idx3] 
    return res
        
# Đầu vào dưới dạng list 2 chiều
input_list = [[0,0,0,0,1,0],[0,0,0,0,1,1], [0,0,0,1,0,0],[0,0,1,0,0,1],[0,0,1,1,0,0],[0,0,1,1,0,1],[0,1,0,0,0,1],[0,1,0,1,1,0],[0,1,0,1,0,1],[0,1,1,0,0,1],[0,1,1,1,0,0]]
input_list = [[0,0,0,0,1,0],[0,0,0,0,1,1]]
input_list = [[0,0,0,1,0,0],[0,0,0,1,1,0],[0,0,0,1,1,1],[0,0,1,0,0,1],[0,0,1,0,1,1],[0,0,1,1,0,0],[0,1,0,1,0,0],[0,1,0,1,1,0],[0,1,0,1,1,1],[0,1,1,0,0,1],[0,1,1,0,1,1],[0,1,1,1,0,0],[1,0,0,1,0,0],[1,0,0,1,1,0],[1,0,0,1,1,1],[1,0,1,0,0,1],[1,0,1,0,1,1],[1,0,1,1,0,0],[1,1,0,0,0,1],[1,1,0,0,1,1],[1,1,0,1,0,0],[1,1,1,0,0,1],[1,1,1,0,1,1],[1,1,1,1,0,0]]
# Tạo biểu thức logic từ list
#f = listToLogic(input_list)
#createTableAssignmentFunction(input_list,6,3)

#decomposeBinaFunc(input_list,6,3)

lst = [1,1,0,0,0,0,1,0]

print(findCoefficients(lst))