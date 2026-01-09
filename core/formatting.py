from decimal import Decimal

def _group_thousands(int_part: str) -> str:
    if not int_part:
        return ''
    n = len(int_part)
    if n <= 3:
        return int_part
    parts = []
    while n > 3:
        parts.append(int_part[n - 3:n])
        n -= 3
    parts.append(int_part[:n])
    return '.'.join(reversed(parts))

def _format_number_token(token: str) -> str:
    if not token:
        return ''
    sign = ''
    if token[0] == '-':
        sign = '-'
        token = token[1:]
    parts = token.split(',')
    int_part = parts[0]
    frac_part = parts[1] if len(parts) > 1 else None
    digits_len = sum((1 for c in token if c.isdigit()))
    if digits_len > 16:
        try:
            d = Decimal((sign + token).replace(',', '.'))
        except Exception:
            pass
        else:
            s = format(d.normalize(), 'e')
            m, e = s.split('e')
            md = m.replace('.', '')
            if len(md) > 16:
                md = md[:16]
            mantissa = md if len(md) <= 1 else md[0] + ',' + md[1:]
            pref = '-' if d.is_signed() else ''
            return pref + mantissa + 'e' + e
    if int_part == '':
        grouped = '0' if frac_part is not None and frac_part != '' else ''
    else:
        int_part = int_part.lstrip('0') or '0'
        grouped = _group_thousands(int_part)
    return sign + (grouped + (',' + (frac_part if frac_part is not None else '')) if frac_part is not None else grouped)

def format_display(expr: str) -> str:
    if not expr:
        return '0'
    out = []
    i = 0
    n = len(expr)
    while i < n:
        ch = expr[i]
        unary_ctx = i == 0 or expr[i - 1] in '+-*/'
        if unary_ctx and ch in '+-':
            j = i
            minus_count = 0
            plus_present = False
            while j < n and expr[j] in '+-':
                if expr[j] == '-':
                    minus_count += 1
                else:
                    plus_present = True
                j += 1
            if j < n and (expr[j].isdigit() or expr[j] == ','):
                if minus_count % 2 == 1:
                    out.append('−')
                elif i == 0 and plus_present:
                    out.append('+')
                i = j
                continue
        if ch.isdigit() or ch == ',':
            start = i
            while i < n and (expr[i].isdigit() or expr[i] == ','):
                i += 1
            out.append(_format_number_token(expr[start:i]))
            continue
        if ch in '+-*/':
            out.append({'*': '×', '/': '÷'}.get(ch, ch))
            i += 1
            continue
        out.append(ch)
        i += 1
    return ''.join(out)
