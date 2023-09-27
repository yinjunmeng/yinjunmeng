import random
import fractions
import copy
max_value = 10  # 这里设置合适的最大值
there = []
result_list = []  # Added global variable for result_list
type_list = []    # Added global variable for type_list
check = []        # Added global variable for check

"""
a + b
(a+b)+c
a+(b+c)  a b c称之为因子
"""


# 生成两位数的运算基础块，以后在此基础上生成多位数的运算
def operation_yunsuan(a, b, operation_symbol):
    P = "NOT"
    if operation_symbol == "+":
        result = a + b
        return result
    if operation_symbol == "-":
        if a >= b:
            result = a - b
            return result
        else:
            return  P
    if operation_symbol == "*":
        result = a * b
        return result
    if operation_symbol == "/":
        result = a / b
        return result


# 产生因子
def factor_yunsuan():
    # 随机生成 自然数、真分数
    global max_value
    while True:
        index = random.randint(1, 2)  # 随机生成1或者2  1就生成自然数因子，2就生成真分数因子
        if index == 1:
            # 自然数,先设置为1到10
            int_cwj = random.randint(1, max_value)
            int_cwj_0 = fractions.Fraction(int_cwj)
            return int_cwj_0
            break
        if index == 2:
            fenzi = random.randint(1, max_value)
            fenmu = random.randint(1, max_value)

            true_fraction = fractions.Fraction(fenzi, fenmu)
            if true_fraction < 1:
                return true_fraction
                break


# 调用operation_yunsuan,factor_yunsuan函数生成两位数的式子
def product():
    two_index = []
    a = factor_yunsuan()
    b = factor_yunsuan()
    while True:
        operation_symbol = random.choice('+-*/')
        # print(a, b, operation_symbol)
        result = operation_yunsuan(a, b, operation_symbol)
        # print(result)
        if result != "NOT":
            # print("可以")
            two_index.extend((a,b,operation_symbol))
            break

    return result,two_index


def start_yunsuan():
    # 主体函数，设置随机flag，flag = 0时调用product生成两位数的式子
    # flag为其他数时生成不同类型的多位数式子（有的有括号，有的没括号）
    flag = random.randint(0,2)
    # flag = 2
    if flag == 0:
        result,two_index = product()
        there.append(two_index)
        result_list.append(result)
        type_list.append(2)
        check.append(0)
        return result
    if flag == 1:
        unio,two_index = product()
        # 此时two_index = [1,2,"+"]
        # print("---------------------")
        c = factor_yunsuan()
        while True:
            operation_symbol = random.choice('+-*/')
            pos = random.randint(0, 1)  # 0代表是unio + c 1代表c + unio
            # print(unio, c, operation_symbol)
            if operation_symbol == "+":
                result = unio + c
                break
            if operation_symbol == "-":
                if pos == 0:
                    if unio >= c:
                        result = unio - c
                        break
                elif pos == 1:
                    if c >= unio:
                        result = c - unio
                        break
                else:
                    continue
            if operation_symbol == "*":
                result = unio * c
                break
            if operation_symbol == "/":
                if pos == 0 and c != 0:
                    result = unio / c
                    break
                if pos == 1 and unio != 0:
                    result = c / unio

                    break
        if pos == 0:                              # 括号在左边，即[2,1,3,"hav","left","-","/"]
            two_index.insert(2, c)
            two_index.insert(3, "hav")
            two_index.insert(4, "left")
            two_index.insert(6, operation_symbol)
            there.append(two_index)
        if pos == 1:                              # 括号在右边
            two_index.insert(0, c)
            two_index.insert(3, "hav")
            two_index.insert(4, "right")
            two_index.insert(5, operation_symbol)
            there.append(two_index)
        result_list.append(result)
        type_list.append(3)
        check.append(0)
        return result
    if flag == 2:
        a = factor_yunsuan()     # a+b*c先右后左，其他按顺序来
        b = factor_yunsuan()
        c = factor_yunsuan()
        there_index = []
        result = "NOT"
        while True:
            # [2,1,3,"nohav","none","-","/"]
            operation_symbol_1 = random.choice('+-*/')  # 第一次运算符
            operation_symbol_2 = random.choice('+-*/')  # 第二次运算符
            # print(a, b, c, operation_symbol_1, operation_symbol_2)
            if (operation_symbol_1 == "+" or operation_symbol_1 == '-') and (operation_symbol_2 == "*" or operation_symbol_2 == "/"):
                cwj = operation_yunsuan(b, c, operation_symbol_2)
                if cwj != "NOT":                      # 先右后左

                    result = operation_yunsuan(a, cwj, operation_symbol_1)
            else:
                cwj = operation_yunsuan(a, b, operation_symbol_1)
                if cwj != "NOT":
                    result = operation_yunsuan(cwj, c, operation_symbol_2)

            if result != "NOT":
                there_index.extend((a, b, c, "nohav", "none", operation_symbol_1, operation_symbol_2))
                there.append(there_index)
                break
        type_list.append(3)
        result_list.append(result)
        check.append(0)
        return result


# 查询重复率
def repeat_yunsuan(m):
    there_copy = []
    there_copy = copy.deepcopy(there)
    repeat = []
    repeat_index = []
    length = len(result_list)
    for u in range(length):

        if len(there_copy[u]) == 7:
            del there_copy[u][4]
            del there_copy[u][3]

        len1 = len(there_copy[u])
        for t in range(len1):
            there_copy[u][t] = str(there_copy[u][t])
    # print(there_copy)
    for j in range(length):
        # print(j,there_copy[j])
        repeat_j = []
        repeat_j.append(j)
        if check[j] == 0:

            for k in range(0,length):

                d1 = sorted(there_copy[j])
                d2 = sorted(there_copy[k])

                if result_list[j] == result_list[k] and type_list[j] == type_list[k] and j!=k:
                    # print(j,k)
                    if d1 == d2:                       # 结果相同且位数相同
                        repeat_j.append(k)
                        # there_copy[k] = "nothing"
                        check[k] = 1
            check[j] = 1

        repeat.append(repeat_j)

    for q in range(length):
        if len(repeat[q]) > 1:
            # print(q)
            len_o = len(repeat[q])
            for y in range(1,len_o):
                index_o = repeat[q][y]
                # print(index_o)
                repeat[index_o] = str(0)
                repeat_index.append(index_o)
    repeat_index.sort(reverse=True)
    for jj in range(len(repeat_index)):
        del there[repeat_index[jj]]
        del result_list[repeat_index[jj]]
        del type_list[repeat_index[jj]]
        del check[jj]
        m = m-1
    return m


# 结果进行转化（假分数转化成真分数，并存储结果）
def reset_result():
    global incorrect_answers, incorrect_expressions, incorrect_answers_list
    incorrect_answers = 0
    incorrect_expressions = []
    incorrect_answers_list = []

    with open('Answers.txt', 'w', encoding='utf-8') as a0:
        a0.write('答案如下\n')
        for i, result in enumerate(result_list):
            i_1 = i + 1
            if result >= 1:
                result_int = result // 1
                result_frac = result - result_int
                correct_answer = f"{result_int}'{fractions.Fraction(result_frac).limit_denominator()}"
            else:
                correct_answer = f"{fractions.Fraction(result).limit_denominator()}"

            user_answer = input(f"请计算第{i_1}题: {generate_expression(there[i])} = ")

            if str(result) != user_answer:
                incorrect_answers += 1
                incorrect_expressions.append(generate_expression(there[i]))
                incorrect_answers_list.append(f"第{i_1}题: {generate_expression(there[i])} = {user_answer} (正确答案: {correct_answer})")

            a0.write(f"第{i_1}题答案是    {correct_answer}\n")

    with open('check.txt', 'w', encoding='utf-8') as check_file:
        check_file.write(f'错误答案个数: {incorrect_answers}\n')
        for incorrect_expression in incorrect_answers_list:
            check_file.write(incorrect_expression + '\n')



def start(n):          # 启动函数，开始生成式子和查重
    for i in range(n):
        a = start_yunsuan()
    n_0 = repeat_yunsuan(n)
    while True:
        if n_0 == n:
            break
        else:
            for oo in range(n-n_0):
                start_yunsuan()

            n_0 = repeat_yunsuan(n)


# 生成相应的表达式字符串
def generate_expression(there_kid):
    there_kid_len = len(there_kid)

    if there_kid_len == 7:
        a = there_kid[0]
        b = there_kid[1]
        c = there_kid[2]
        operation1 = there_kid[5]
        operation2 = there_kid[6]

        if operation1 == "/":
            operation1 = "÷"
        if operation1 == "*":
            operation1 = "×"
        if operation2 == "/":
            operation2 = "÷"
        if operation2 == "*":
            operation2 = "×"

        if there_kid[3] == "hav":
            if there_kid[4] == "left":
                expression = f"({a}{operation1}{b}){operation2}{c}"
            else:
                expression = f"{a}{operation1}({b}{operation2}{c})"
        else:
            expression = f"{a}{operation1}{b}{operation2}{c}"
    elif there_kid_len == 3:
        a = there_kid[0]
        b = there_kid[1]
        operation = there_kid[2]
        expression = f"{a}{operation}{b}"
    else:
        expression = ""

    return expression


def reset_result_and_check():
    global incorrect_answers, incorrect_expressions, incorrect_answers_list
    incorrect_answers = 0
    incorrect_expressions = []
    incorrect_answers_list = []

    with open('Answers.txt', 'w', encoding='utf-8') as a0:
        a0.write('答案如下\n')
        for i, result in enumerate(result_list):
            i_1 = i + 1
            if result >= 1:
                result_int = result // 1
                result_frac = result - result_int
                correct_answer = f"{result_int}'{fractions.Fraction(result_frac).limit_denominator()}"
            else:
                correct_answer = f"{fractions.Fraction(result).limit_denominator()}"

            user_answer = input(f"请计算第{i_1}题: {generate_expression(there[i])} = ")

            if str(result) != user_answer:
                incorrect_answers += 1
                incorrect_expressions.append(generate_expression(there[i]))
                incorrect_answers_list.append(f"第{i_1}题: {generate_expression(there[i])} = {user_answer} (正确答案: {correct_answer})")

            a0.write(f"第{i_1}题答案是    {correct_answer}\n")

    with open('check.txt', 'w', encoding='utf-8') as check_file:
        check_file.write(f'错误答案个数: {incorrect_answers}\n')
        for incorrect_expression in incorrect_answers_list:
            check_file.write(incorrect_expression + '\n')



if __name__ == '__main__':
    n = int(input("生成题目的个数:"))
    max_value = int(input("请输入题目中数值的范围:"))

    there = []  # 式子的具体信息
    result_list = []  # 结果的信息，但没经过转化，包含假分数
    type_list = []  # 式子的项数
    result_list_new = []  # 最终结果，此时元素全是str类型（为了拼接最终表达式）
    there_kid_str = [None] * n  # 最终式子，此时元素全是str类型（为了拼接最终表达式）
    check = []  # 查询标志，0是表示没被查过，1代表已经查询过，避免重复查询
    start(n)

    b0 = open('Exercises.txt', 'w', encoding='utf-8')
    b0.write('题目如下，一共%d道题目' % n + '\n')
    b0.close()

    for index, there_kid in enumerate(there):
        index_1 = index + 1
        index_pro = "第%d题:      " % index_1
        expression = generate_expression(there_kid)

        if expression:
            there_kid_str[index] = index_pro + expression + " = "
            b0 = open('Exercises.txt', 'a', encoding='utf-8')
            b0.write(there_kid_str[index] + '\n')
            print(there_kid_str[index])

    reset_result_and_check()

