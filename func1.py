# Các biến
x1 = 1
x2 = 2
x5 = 13

# Bảng chỉ số biến
lst_index = [1, 2, 5]

# In ra các biến với chỉ số tương ứng trong lst_index
for index in lst_index:
    print(globals()[f'x{index}'])


def list_to_latex_array(input_list):
    """
    Chuyển đổi list hai chiều thành chuỗi LaTeX cho mảng.

    Args:
    - input_list: List hai chiều chứa dữ liệu.

    Returns:
    - Chuỗi LaTeX tạo mảng tương ứng.
    """
    # Kiểm tra input_list không phải là rỗng
    if not input_list or not input_list[0]:
        return "Empty input list!"

    # Xác định số cột
    num_columns = len(input_list[0])
    
    # Tạo tiêu đề cho môi trường array
    latex_str = "\\begin{array}{" + "c" * num_columns + "}\n"

    # Thêm các hàng
    for row in input_list:
        row_str = " & ".join(map(str, row))  # Chuyển đổi mỗi phần tử thành chuỗi và nối chúng bằng &
        latex_str += row_str + " \\\\\n"  # Kết thúc hàng

    # Kết thúc môi trường array
    latex_str += "\\end{array}"

    return latex_str

# Ví dụ sử dụng,
my_list = [range(0,16),[1    ,  6     , 1    ,  -9    , 5      ,29   ,  -113,   261,    -467  , 695  ,  -899  , 1116  , -1686,  3651  , -9367 , 23326]]
# latex_code = list_to_latex_array(my_list)
# print(latex_code)

def list_to_latex_table(input_list):
    """
    Chuyển đổi list hai chiều thành chuỗi LaTeX cho bảng.

    Args:
    - input_list: List hai chiều chứa dữ liệu.

    Returns:
    - Chuỗi LaTeX tạo bảng tương ứng.
    """
    # Kiểm tra input_list không phải là rỗng
    if not input_list or not input_list[0]:
        return "Empty input list!"

    # Xác định số cột
    num_columns = len(input_list[0])
    
    # Tạo tiêu đề cho môi trường tabular
    latex_str = "\\begin{tabular}{" + "c" * num_columns + "}\n"

    # Thêm các hàng
    for row in input_list:
        row_str = " & ".join(map(str, row))  # Chuyển đổi mỗi phần tử thành chuỗi và nối chúng bằng &
        latex_str += row_str + " \\\\\n"  # Kết thúc hàng

    # Kết thúc môi trường tabular
    latex_str += "\\end{tabular}"

    return latex_str

# Ví dụ sử dụng

latex_code = list_to_latex_table(my_list)
print(latex_code)

def support_to_function(coefficient,degree):
    if coefficient == 0:
        return str(0)
    return f"{coefficient}x^{degree}"
    
coefficients = [3, -2, 5, 0, -1]

def latex_coefficients(coefficients):
    degree = len(coefficients) - 1
    #terms1 = [coefficients[0]]
    terms = map(lambda i, coeff: f"{coeff}x^{i}" if coeff != 0 else None, range(1,degree+1), coefficients[1:])
     # Loại bỏ các phần tử rỗng từ danh sách terms bằng hàm filter
    filtered_terms = filter(None, terms)
    latex_eqn = f"$f(x) = {coefficients[0]} " + " + ".join(filtered_terms)
    latex_eqn+="$"
    return latex_eqn

latex_function = latex_coefficients(coefficients)
print(latex_function)

