def sub_u16(a, b):
    if a < b:
        a += 2**16
    return a - b

