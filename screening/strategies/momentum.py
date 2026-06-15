# -*- coding: utf-8 -*-
"""
动量策略
追踪近期表现强势的股票
"""


class MomentumStrategy:
    """动量策略"""

    name = "动量策略"
    description = "追踪近期涨幅强、资金流入的股票"

    def __init__(self, min_change=0, min_turnover_rate=2, min_amount=100000000, min_market_cap=10000000000):
        self.min_change = min_change
        self.min_turnover_rate = min_turnover_rate
        self.min_amount = min_amount
        self.min_market_cap = min_market_cap

    def filter(self, df):
        """筛选条件"""
        filtered = df[
            (df['涨跌幅'] > self.min_change) &
            (df['换手率'] > self.min_turnover_rate) &
            (df['成交额'] > self.min_amount) &
            (df['总市值'] > self.min_market_cap)
        ].copy()
        return filtered

    def score(self, df):
        """计算得分"""
        df['得分'] = df['涨跌幅'] * 15 + df['换手率'] * 3
        df['策略'] = self.name
        return df
