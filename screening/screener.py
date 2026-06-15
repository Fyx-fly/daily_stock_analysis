#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高级选股引擎
集成AlphaSift优点，支持A股和美股
"""

import os
import sys
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入策略
from strategies import (
    DualLowStrategy,
    VolumeBreakoutStrategy,
    MomentumStrategy,
    OversoldReversalStrategy,
    QualityValueStrategy,
)

# 导入数据获取器
from data_fetcher import DataFetcher


class AdvancedScreener:
    """高级选股器"""

    def __init__(self):
        self.top_n = int(os.environ.get('SCREENING_TOP_N', '10'))
        self.strategy = os.environ.get('SCREENING_STRATEGY', 'all')
        self.market = os.environ.get('STOCK_UNIVERSE', 'all')  # all, a_share, us
        self.results = []
        self.data_fetcher = DataFetcher()

        # 初始化策略
        self.strategies = {
            'dual_low': DualLowStrategy(),
            'volume_breakout': VolumeBreakoutStrategy(),
            'momentum': MomentumStrategy(),
            'oversold_reversal': OversoldReversalStrategy(),
            'quality_value': QualityValueStrategy(),
        }

    def get_stock_data(self) -> pd.DataFrame:
        """获取股票数据"""
        if self.market == 'a_share':
            return self.data_fetcher.get_a_share_list()
        elif self.market == 'us':
            return self.data_fetcher.get_us_stock_list()
        else:
            return self.data_fetcher.get_all_stocks()

    def run_strategy(self, strategy_name: str, df: pd.DataFrame) -> pd.DataFrame:
        """执行单个策略"""
        if strategy_name not in self.strategies:
            print(f"❌ 未知策略: {strategy_name}")
            return pd.DataFrame()

        strategy = self.strategies[strategy_name]
        print(f"\n🔍 执行{strategy.name}选股...")

        # 筛选
        filtered = strategy.filter(df)
        print(f"  ✅ 筛选出 {len(filtered)} 只股票")

        if filtered.empty:
            return filtered

        # 评分
        scored = strategy.score(filtered)

        # 取前N只
        result = scored.nlargest(self.top_n, '得分')
        print(f"  ✅ 最终选出 {len(result)} 只股票")

        return result

    def run_screening(self) -> List[Dict[str, Any]]:
        """执行选股"""
        print("=" * 60)
        print("🚀 开始执行高级选股系统")
        print(f"   市场: {self.market}")
        print(f"   策略: {self.strategy}")
        print(f"   数量: TOP {self.top_n}")
        print("=" * 60)

        # 获取股票数据
        df = self.get_stock_data()

        if df.empty:
            print("❌ 无法获取股票数据")
            return []

        all_picks = []

        # 执行策略
        if self.strategy == 'all':
            # 执行所有策略
            for strategy_name in self.strategies.keys():
                result = self.run_strategy(strategy_name, df)
                if not result.empty:
                    all_picks.extend(result.to_dict('records'))
        else:
            # 执行指定策略
            result = self.run_strategy(self.strategy, df)
            if not result.empty:
                all_picks.extend(result.to_dict('records'))

        # 去重（按代码）
        seen_codes = set()
        unique_picks = []
        for pick in all_picks:
            code = pick.get('代码', '')
            if code not in seen_codes:
                seen_codes.add(code)
                unique_picks.append(pick)

        # 按得分排序
        unique_picks.sort(key=lambda x: x.get('得分', 0), reverse=True)

        # 取前N只
        self.results = unique_picks[:self.top_n]

        print(f"\n✅ 选股完成，共选出 {len(self.results)} 只股票")
        return self.results

    def save_results(self):
        """保存选股结果"""
        # 创建目录
        os.makedirs('results', exist_ok=True)

        # 保存带时间戳的文件
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"results/screening_{timestamp}.json"

        # 转换为可序列化格式
        serializable_results = []
        for pick in self.results:
            serializable_pick = {}
            for key, value in pick.items():
                if isinstance(value, (int, float, str, bool, type(None))):
                    serializable_pick[key] = value
                else:
                    serializable_pick[key] = str(value)
            serializable_results.append(serializable_pick)

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, ensure_ascii=False, indent=2)

        # 同时保存为latest.json供后续步骤使用
        with open('results/latest.json', 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, ensure_ascii=False, indent=2)

        print(f"✅ 结果已保存到: {filename}")
        return filename

    def get_stock_codes(self) -> List[str]:
        """获取股票代码列表"""
        codes = []
        for pick in self.results:
            code = pick.get('代码', '')
            # 根据市场添加前缀
            market = pick.get('市场', '')
            if market == '美股':
                codes.append(code)  # 美股直接用代码
            else:
                codes.append(code)  # A股直接用代码
        return codes


def main():
    """主函数"""
    screener = AdvancedScreener()
    results = screener.run_screening()

    if results:
        screener.save_results()

        # 打印结果摘要
        print("\n" + "=" * 60)
        print("📋 选股结果摘要")
        print("=" * 60)

        # 按市场分组
        a_shares = [r for r in results if r.get('市场') == 'A股']
        us_stocks = [r for r in results if r.get('市场') == '美股']

        if a_shares:
            print(f"\n🇨🇳 A股推荐（{len(a_shares)}只）：")
            for i, pick in enumerate(a_shares[:5], 1):
                print(f"  {i}. {pick.get('名称', 'N/A')}({pick.get('代码', 'N/A')}) - "
                      f"得分: {pick.get('得分', 0):.1f} | "
                      f"策略: {pick.get('策略', 'N/A')}")

        if us_stocks:
            print(f"\n🇺🇸 美股推荐（{len(us_stocks)}只）：")
            for i, pick in enumerate(us_stocks[:5], 1):
                print(f"  {i}. {pick.get('名称', 'N/A')}({pick.get('代码', 'N/A')}) - "
                      f"得分: {pick.get('得分', 0):.1f} | "
                      f"策略: {pick.get('策略', 'N/A')}")

        # 输出股票代码列表
        codes = screener.get_stock_codes()
        print(f"\n📊 股票代码列表: {','.join(codes)}")
    else:
        print("❌ 无选股结果")


if __name__ == "__main__":
    main()
