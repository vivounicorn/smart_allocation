import math


class Customer:

    def __init__(self, identifier, m=0.0, w=36, t=0, rt=0, r=0.1188, pd=0.015, lgd=0.7, p_score=500, mr=0.2, hr=0):
        self.id = identifier  # 用户唯一标识
        self.m = m  # 融资额
        self.w = w  # 融资期限
        self.t = t  # 业务类型（新车0、二手车1、车主融2..）
        self.rt = rt  # 还款类型（等额本息0或等额本金1）
        self.r = r  # 融资利率
        self.pd = pd  # 违约概率率（pd）
        self.lgd = lgd  # 违约损失率（lgd）
        self.p_score = p_score  # 易鑫分
        self.mr = mr  # 首付比例
        self.hr = hr  # 已还款期数
        self.funders = []  # 匹配资方列表（资方结构体）

    def __str__(self):
        return "用户{0},融资额:{1},融资期限:{2},业务类型:{3},还款类型:{4},融资利率:{5},违约概率率:{6},违约损失率:{7},易鑫分:{8},首付比例:{9},已还款期数:{10}," \
               "匹配资方列表:{11}".format(
            self.id,
            self.m,
            self.w,
            self.t,
            self.rt,
            self.r,
            self.pd,
            self.lgd,
            self.p_score,
            self.mr,
            self.hr,
            [item.id for item in self.funders])

    def e(self):
        if self.rt == 0:
            return self.r / 12 * math.pow(self.r / 12 + 1, self.w) / (
                    math.pow(1 + self.r / 12, self.w) - 1) * self.w - 1
        else:
            return (self.w + 1) * 0.5 * self.r / 12
