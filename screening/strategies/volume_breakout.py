# -*- coding: utf-8 -*-
"""
放量突破策略
适合趋势投资者
"""


class VolumeBreakoutStrategy:
    """放量突破策略"""

    name = "放量突破"
    description = "成交量放大 + 价格突破，追踪强势股"

    def __init__(self, min_change=2, max_change=9.5, min_turnover_rate=3, min_amount=100000000):
        self.min_change = min_change
        self.max_change = max_change
        self.min_turnover_rate = min_turnover_rate
        self.min_amount = min_amount

    def filter(self, df):
        """筛选条件"""
        filtered = df[
            (df['涨跌幅'] > self.min_change) &
            (df['涨跌幅'] < self.max_change) &
            (df['换手率'] > self.min_turnover_rate) &
            (df['成交额'] > self.min_amount)
        ].copy()
        return filtered

    def score(self, df):
        """计算得分"""
        df['得分'] = df['涨跌幅'] * 10 + df['换手率'] * 5
        df['策略'] = self.name
        return df
