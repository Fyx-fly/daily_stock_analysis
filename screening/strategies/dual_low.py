# -*- coding: utf-8 -*-
"""
双低策略：低PE + 低PB
适合价值投资者
"""


class DualLowStrategy:
    """双低策略"""

    name = "双低策略"
    description = "低PE + 低PB，寻找被低估的股票"

    def __init__(self, max_pe=25, max_pb=3, min_turnover=50000000):
        self.max_pe = max_pe
        self.max_pb = max_pb
        self.min_turnover = min_turnover

    def filter(self, df):
        """筛选条件"""
        filtered = df[
            (df['市盈率-动态'] > 0) &
            (df['市盈率-动态'] < self.max_pe) &
            (df['市净率'] > 0) &
            (df['市净率'] < self.max_pb) &
            (df['成交额'] > self.min_turnover)
        ].copy()
        return filtered

    def score(self, df):
        """计算得分"""
        df['得分'] = 100 - (df['市盈率-动态'] * 2 + df['市净率'] * 10)
        df['策略'] = self.name
        return df
