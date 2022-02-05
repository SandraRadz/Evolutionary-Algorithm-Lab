def fh(seq):
    """
    FH(X)=l-H(X,X_opt), де H(X,X_opt) – відстань Геммінга до оптимального ланцюжка Xopt=«0...0»
    (фактично кількість «0» в ланцюжку);
    """
    res = 0
    for i in seq:
        if i == '0':
            res += 1
    return res


def fhd(seq):
    """
    FHD(X)=(l-k)+k*δ – відстань до оптимального ланцюжка Xopt=«0...0» з врахуванням селективної переваги
    на біт (параметр δ), де k – кількість «0» в ланцюжку; очевидно, FHD(«0...0»)=l*δ.
    Розглянути такі значення селективної переваги:  δ=10, δ=50, δ=150. ( δ=2, δ=4,  δ=10)

    # todo ask if k is number of 0 or 1
    """
    pass
