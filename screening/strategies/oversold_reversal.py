# -*- coding: utf-8 -*-
"""
超跌反弹策略
寻找超跌后可能反弹的股票
"""


class OversoldReversalStrategy:
    """超跌反弹策略"""

    name = "超跌反弹"
    description = "寻找超跌后可能反弹的股票"

    def __init__(self, max_change=-5, min_turnover_rate=2, min_amount=50000000):
        self.max_change = max_change
        self.min_turnover_rate = min_turnover_rate
        self.min_amount = min_amount

    def filter(self, df):
        """筛选条件"""
        filtered = df[
            (df['涨跌幅'] < self.max_change) &
            (df['换手率'] > self.min_turnover_rate) &
            (df['成交额'] > self.min_amount)
        ].copy()
        return filtered

    def score(self, df):
        """计算得分"""
        # 跌幅越大，反弹潜力越大
        df['得分'] = abs(df['涨跌幅']) * 10 + df['换手率'] * 5
        df['策略'] = self.name
        return df
