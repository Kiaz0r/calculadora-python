from decimal import Decimal, getcontext
from .engine import result_exceeds_limits, decimal_to_str, evaluate_decimal_expr, normalize_decimal_tokens

def _find_last_binary_op(expr: str):
    i = len(expr) - 1
    while i >= 0:
        ch = expr[i]
        if ch in '+*/':
            return i
        if ch == '-':
            if not (i == 0 or expr[i - 1] in '+-*/'):
                return i
        i -= 1
    return None

def backspace_expr(expr: str) -> str:
    return expr[:-1] if expr else ''

def clear_entry_expr(expr: str) -> str:
    if not expr:
        return ''
    last_op_idx = None
    i = len(expr) - 1
    while i >= 0:
        ch = expr[i]
        if ch in '+*/':
            last_op_idx = i
            break
        if ch == '-':
            if i > 0 and expr[i - 1].isdigit():
                last_op_idx = i
                break
        i -= 1
    if last_op_idx is None:
        return ''
    right = expr[last_op_idx + 1:]
    if right == '':
        return expr
    return expr[:last_op_idx + 1]

def toggle_sign_expr(expr: str) -> str:
    if not expr:
        return ''
    i = len(expr) - 1
    while i >= 0 and (not (expr[i].isdigit() or expr[i] == ',')):
        i -= 1
    if i < 0:
        return expr
    j = i
    while j >= 0 and (expr[j].isdigit() or expr[j] == ','):
        j -= 1
    start = j + 1
    has_sign = False
    sign_idx = None
    if start > 0 and expr[start - 1] == '-' and (start - 1 == 0 or expr[start - 2] in '+-*/'):
        has_sign = True
        sign_idx = start - 1
    if has_sign:
        return expr[:sign_idx] + expr[sign_idx + 1:]
    else:
        return expr[:start] + '-' + expr[start:]

def percent_expr(expr: str):
    if not expr:
        return (expr, False)
    last_op_idx = _find_last_binary_op(expr)
    if last_op_idx is None:
        try:
            b_str = normalize_decimal_tokens(expr).replace(',', '.')
            b = Decimal(b_str)
        except Exception:
            return (expr, True)
        percent_value = b / Decimal('100')
        if result_exceeds_limits(percent_value):
            return (expr, True)
        res_str = decimal_to_str(percent_value)
        return (res_str, False)
    left = expr[:last_op_idx]
    op = expr[last_op_idx]
    right = expr[last_op_idx + 1:]
    if right.strip() == '':
        return (expr, False)
    try:
        a = evaluate_decimal_expr(left)
    except Exception:
        return (expr, True)
    try:
        right_norm = right
        if right_norm.startswith(','):
            right_norm = '0' + right_norm
        elif right_norm.startswith('-,'):
            right_norm = '-0' + right_norm[1:]
        b = Decimal(right_norm.replace(',', '.'))
    except Exception:
        return (expr, True)
    if op in '+-':
        percent_value = a * (b / Decimal('100'))
    else:
        percent_value = b / Decimal('100')
    if result_exceeds_limits(percent_value):
        return (expr, True)
    new_right = decimal_to_str(percent_value)
    return (left + op + new_right, False)

def reciprocal_expr(expr: str):
    if not expr:
        return (expr, False)
    last_op_idx = _find_last_binary_op(expr)
    if last_op_idx is None:
        try:
            v_str = normalize_decimal_tokens(expr).replace(',', '.')
            v = Decimal(v_str)
        except Exception:
            return (expr, True)
        if v == Decimal('0'):
            return (expr, True)
        res = Decimal('1') / v
        if result_exceeds_limits(res):
            return (expr, True)
        return (decimal_to_str(res), False)
    right = expr[last_op_idx + 1:]
    if right.strip() == '':
        return (expr, False)
    try:
        right_norm = right
        if right_norm.startswith(','):
            right_norm = '0' + right_norm
        elif right_norm.startswith('-,'):
            right_norm = '-0' + right_norm[1:]
        v = Decimal(right_norm.replace(',', '.'))
    except Exception:
        return (expr, True)
    if v == Decimal('0'):
        return (expr, True)
    res = Decimal('1') / v
    if result_exceeds_limits(res):
        return (expr, True)
    new_right = decimal_to_str(res)
    return (expr[:last_op_idx + 1] + new_right, False)

def square_expr(expr: str):
    if not expr:
        return (expr, False)
    last_op_idx = _find_last_binary_op(expr)
    if last_op_idx is None:
        try:
            v = Decimal(normalize_decimal_tokens(expr).replace(',', '.'))
        except Exception:
            return (expr, True)
        res = v * v
        if result_exceeds_limits(res):
            return (expr, True)
        return (decimal_to_str(res), False)
    right = expr[last_op_idx + 1:]
    if right.strip() == '':
        return (expr, False)
    try:
        right_norm = right
        if right_norm.startswith(','):
            right_norm = '0' + right_norm
        elif right_norm.startswith('-,'):
            right_norm = '-0' + right_norm[1:]
        v = Decimal(right_norm.replace(',', '.'))
    except Exception:
        return (expr, True)
    res = v * v
    if result_exceeds_limits(res):
        return (expr, True)
    new_right = decimal_to_str(res)
    return (expr[:last_op_idx + 1] + new_right, False)

def sqrt_expr(expr: str):
    if not expr:
        return (expr, False)
    last_op_idx = _find_last_binary_op(expr)

    def sqrt_decimal(val: Decimal) -> Decimal:
        return getcontext().sqrt(val)
    if last_op_idx is None:
        try:
            v = Decimal(normalize_decimal_tokens(expr).replace(',', '.'))
        except Exception:
            return (expr, True)
        if v < Decimal('0'):
            return (expr, True)
        res = sqrt_decimal(v)
        if result_exceeds_limits(res):
            return (expr, True)
        return (decimal_to_str(res), False)
    right = expr[last_op_idx + 1:]
    if right.strip() == '':
        return (expr, False)
    try:
        right_norm = right
        if right_norm.startswith(','):
            right_norm = '0' + right_norm
        elif right_norm.startswith('-,'):
            right_norm = '-0' + right_norm[1:]
        v = Decimal(right_norm.replace(',', '.'))
    except Exception:
        return (expr, True)
    if v < Decimal('0'):
        return (expr, True)
    res = sqrt_decimal(v)
    if result_exceeds_limits(res):
        return (expr, True)
    new_right = decimal_to_str(res)
    return (expr[:last_op_idx + 1] + new_right, False)
