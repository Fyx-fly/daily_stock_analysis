# -*- coding: utf-8 -*-
"""
多市场数据获取
支持A股和美股
"""

import os
import pandas as pd
from datetime import datetime


class DataFetcher:
    """数据获取器"""

    def __init__(self):
        self.a_share_data = None
        self.us_stock_data = None

    def get_a_share_list(self):
        """获取A股股票列表"""
        try:
            import akshare as ak
            print("📊 正在获取A股股票列表...")
            df = ak.stock_zh_a_spot_em()
            print(f"✅ 获取到 {len(df)} 只A股股票")
            return df
        except Exception as e:
            print(f"❌ 获取A股数据失败: {e}")
            return pd.DataFrame()

    def get_us_stock_list(self):
        """获取美股股票列表"""
        try:
            import yfinance as yf
            print("📊 正在获取美股股票列表...")

            # 常见的美股股票代码
            us_tickers = [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA',
                'BRK.B', 'JPM', 'V', 'UNH', 'MA', 'JNJ', 'WMT', 'PG',
                'HD', 'DIS', 'BAC', 'XOM', 'CVX', 'ABBV', 'MRK', 'KO',
                'PEP', 'COST', 'AVGO', 'LLY', 'TMO', 'ADBE', 'CRM',
                'NFLX', 'AMD', 'INTC', 'QCOM', 'TXN', 'PYPL', 'BA',
                'GS', 'MS', 'CAT', 'HON', 'UNP', 'RTX', 'DE', 'LMT',
                'NEE', 'DUK', 'SO', 'D', 'AEP', 'SRE', 'EXC', 'XEL',
            ]

            # 获取实时数据
            data = []
            for ticker in us_tickers:
                try:
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    data.append({
                        '代码': ticker,
                        '名称': info.get('shortName', ticker),
                        '最新价': info.get('currentPrice', 0),
                        '涨跌幅': info.get('regularMarketChangePercent', 0),
                        '市盈率-动态': info.get('trailingPE', 0),
                        '市净率': info.get('priceToBook', 0),
                        '成交额': info.get('regularMarketVolume', 0) * info.get('currentPrice', 0),
                        '总市值': info.get('marketCap', 0),
                    })
                except:
                    continue

            df = pd.DataFrame(data)
            print(f"✅ 获取到 {len(df)} 只美股股票")
            return df

        except Exception as e:
            print(f"❌ 获取美股数据失败: {e}")
            return pd.DataFrame()

    def get_all_stocks(self):
        """获取所有股票"""
        a_share = self.get_a_share_list()
        us_stock = self.get_us_stock_list()

        # 合并数据
        if not a_share.empty and not us_stock.empty:
            # 添加市场标签
            a_share['市场'] = 'A股'
            us_stock['市场'] = '美股'

            # 合并
            all_stocks = pd.concat([a_share, us_stock], ignore_index=True)
            print(f"\n✅ 共获取 {len(all_stocks)} 只股票（A股: {len(a_share)}, 美股: {len(us_stock)}）")
            return all_stocks
        elif not a_share.empty:
            a_share['市场'] = 'A股'
            return a_share
        elif not us_stock.empty:
            us_stock['市场'] = '美股'
            return us_stock
        else:
            return pd.DataFrame()
