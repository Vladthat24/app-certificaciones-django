def get_calculator_tem(tea):
    result = pow((1 + tea / 100), (1 / 12)) - 1
    return round(result * 100, 2)

def get_pay_month_by_tem(tem, p, n):
    i = (tem / 100)
    # i = round((tem / 100), 4)
    i_n = ((1 + i) ** n)
    # i_n = round(((1 + i) ** n), 2)
    ss = (i * i_n) / (i_n - 1)
    result = float(p) * float(ss)

    return result
