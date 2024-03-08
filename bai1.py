# F --> (F1,F2)
from sympy import factorint


def transformFunction(coefficients,module):
    # ex : transformFunction([7,5,11],12)  tuong ung voi 7 + 5x + 11x^2 , theo module 12 = 2^2 * 3
    # bước 1 : factor module
    factors = factorint(module)
    # bước 2 : moudle từng hệ số theo p^m
    result = []
    func = []
    p_temp = 0
    for primer,pow in factors.items():
        func = []
        p_temp = primer ** pow
        for c in coefficients:
            func.append(c % p_temp)
        result.append(func)
    return result



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
    



if __name__ == '__main__':
    # t = transformFunction([7,5,11],12)
    # print(t)
    createSupportTable(2,4)