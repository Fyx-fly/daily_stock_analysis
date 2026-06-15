# -*- coding: utf-8 -*-
"""
优质价值策略
寻找基本面优秀的股票
"""


class QualityValueStrategy:
    """优质价值策略"""

    name = "优质价值"
    description = "寻找基本面优秀、估值合理的股票"

    def __init__(self, max_pe=30, max_pb=5, min_amount=100000000, min_market_cap=20000000000):
        self.max_pe = max_pe
        self.max_pb = max_pb
        self.min_amount = min_amount
        self.min_market_cap = min_market_cap

    def filter(self, df):
        """筛选条件"""
        filtered = df[
            (df['市盈率-动态'] > 0) &
            (df['市盈率-动态'] < self.max_pe) &
            (df['市净率'] > 0) &
            (df['市净率'] < self.max_pb) &
            (df['成交额'] > self.min_amount) &
            (df['总市值'] > self.min_market_cap)
        ].copy()
        return filtered

    def score(self, df):
        """计算得分"""
        # 综合考虑PE、PB、市值
        df['得分'] = 100 - (df['市盈率-动态'] * 1.5 + df['市净率'] * 5) + (df['总市值'] / 1000000000)
        df['策略'] = self.name
        return df
