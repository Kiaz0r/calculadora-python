from decimal import Decimal, getcontext, DivisionByZero
from .constants import MAX_INTEGER_DIGITS, MAX_TOTAL_SIGNIFICANT, RESULT_MAX_FRACTION_DIGITS
getcontext().prec = 28

def strip_trailing_ops(expr: str) -> str:
    while expr and expr[-1] in '+-*/':
        expr = expr[:-1]
    return expr

def normalize_decimal_tokens(expr: str) -> str:
    if not expr:
        return ''
    out = []
    i = 0
    while i < len(expr):
        ch = expr[i]
        if ch.isdigit() or ch == ',' or (ch == '-' and (i == 0 or expr[i - 1] in '+-*/')):
            start = i
            i += 1
            while i < len(expr) and (expr[i].isdigit() or expr[i] == ','):
                i += 1
            tok = expr[start:i]
            if tok.startswith(','):
                tok = '0' + tok
            elif tok.startswith('-,'):
                tok = '-0' + tok[1:]
            out.append(tok)
        else:
            out.append(ch)
            i += 1
    return ''.join(out)

def _tokenize_numbers_and_ops(expr: str):
    tokens = []
    i = 0
    prev_type = None
    while i < len(expr):
        ch = expr[i]
        if ch in '+-*/':
            if ch in '+-' and prev_type in (None, 'op'):
                j = i
                sign = 1
                while j < len(expr) and expr[j] in '+-':
                    if expr[j] == '-':
                        sign *= -1
                    j += 1
                if j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                    k = j
                    while k < len(expr) and (expr[k].isdigit() or expr[k] == '.'):
                        k += 1
                    num = expr[j:k]
                    if sign == -1:
                        num = '-' + num
                    tokens.append(('num', num))
                    prev_type = 'num'
                    i = k
                    continue
                op = '-' if sign == -1 else '+'
                tokens.append(('op', op))
                prev_type = 'op'
                i = j
            else:
                tokens.append(('op', ch))
                prev_type = 'op'
                i += 1
        elif ch.isdigit() or ch == '.':
            j = i + 1
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(('num', expr[i:j]))
            prev_type = 'num'
            i = j
        else:
            i += 1
    while tokens and tokens[-1][0] == 'op':
        tokens.pop()
    return tokens

def _apply_op(op: str, a: Decimal, b: Decimal) -> Decimal:
    if op == '+':
        return a + b
    elif op == '-':
        return a - b
    elif op == '*':
        return a * b
    elif op == '/':
        if b == Decimal('0'):
            raise DivisionByZero
        return a / b
    else:
        raise ValueError('Operador inválido')

def evaluate_decimal_expr(expr: str) -> Decimal:
    expr2 = strip_trailing_ops(normalize_decimal_tokens(expr)).replace(',', '.')
    tokens = _tokenize_numbers_and_ops(expr2)
    if not tokens:
        return Decimal('0')
    out = []
    ops = []
    prec = {'+': 1, '-': 1, '*': 2, '/': 2}
    for typ, val in tokens:
        if typ == 'num':
            out.append(Decimal(val))
        else:
            while ops and prec[ops[-1]] >= prec[val]:
                out.append(ops.pop())
            ops.append(val)
    while ops:
        out.append(ops.pop())
    stack = []
    for item in out:
        if isinstance(item, Decimal):
            stack.append(item)
        else:
            b = stack.pop()
            a = stack.pop() if stack else Decimal('0')
            stack.append(_apply_op(item, a, b))
    return stack[-1] if stack else Decimal('0')

def _result_exceeds_limits(d: Decimal) -> bool:
    try:
        if d == Decimal('0'):
            int_digits = 1
        else:
            int_digits = d.copy_abs().adjusted() + 1
    except Exception:
        int_digits = 0
    try:
        digits_len = len(d.normalize().as_tuple().digits)
    except Exception:
        digits_len = 0
    if int_digits > MAX_INTEGER_DIGITS:
        return True
    if digits_len > MAX_TOTAL_SIGNIFICANT:
        return True
    return False

def _decimal_to_str(d: Decimal) -> str:
    s = format(d.normalize(), 'f')
    if '.' in s:
        int_part, frac = s.split('.', 1)
        if len(frac) > RESULT_MAX_FRACTION_DIGITS:
            frac = frac[:RESULT_MAX_FRACTION_DIGITS]
        s = int_part + '.' + frac
        s = s.rstrip('0').rstrip('.')
    if s == '':
        s = '0'
    return s.replace('.', ',')

def tokenize(expr: str):
    return _tokenize_numbers_and_ops(expr)

def apply_op(op: str, a: Decimal, b: Decimal) -> Decimal:
    return _apply_op(op, a, b)

def result_exceeds_limits(d: Decimal) -> bool:
    return _result_exceeds_limits(d)

def decimal_to_str(d: Decimal) -> str:
    return _decimal_to_str(d)
