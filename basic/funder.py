class Founder:
    def __init__(self, identifier, s=0.0, v=0, is_rc=True, is_base=False, d_score=500, dr=0.015, d=0.1, p=0.9, c=0.06,
                 alpha=0,
                 beta=1):
        self.id = identifier  # 资方唯一标示
        self.s = s  # 授信额度
        self.v = v  # 授信有效期
        self.is_rc = is_rc  # 是否为循环额度
        self.is_base = is_base  # 是否为托底资方
        self.d_score = d_score  # 资方接受易鑫分下限
        self.dr = dr  # 资方接受逾期率
        self.d = d  # 预期资方单量占比
        self.p = p  # 资方通过率
        self.c = c  # 资金成本
        self.alpha = alpha
        self.beta = beta  # 资方$\alpha、\beta$值

    def __str__(self):
        return "资方{0},授信额度:{1},授信有效期:{2},是否为循环额度:{3},是否为托底资方:{4},资方接受易鑫分下限:{5},资方接受逾期率:{6},预期资方单量占比:{7},资方通过率:{8}," \
               "资金成本:{9},alpha:{10},beta:{11}".format(
            self.id,
            self.s,
            self.v,
            self.is_rc,
            self.is_base,
            self.d_score,
            self.dr,
            self.d,
            self.p,
            self.c,
            self.alpha,
            self.beta)

