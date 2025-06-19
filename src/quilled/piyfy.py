def piyfy(x):
    pi = 3.14159265358979323
    frac = x / pi * 8
    if abs(frac - round(frac)) > 1e-9:
        return None
    frac = round(frac)
    denom = 8
    if frac % 2 == 0:
        denom = 4
        frac //= 2
    if frac % 2 == 0:
        denom = 2
        frac //= 2
    if frac % 2 == 0:
        denom = 1
        frac //= 2

    return (frac, denom)
