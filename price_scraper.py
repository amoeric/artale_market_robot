import asyncio
import aiohttp
import json
import re
from typing import Optional, Dict, List
import time
import logging
from fuzzywuzzy import fuzz

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArtaleMarketScraper:
    def __init__(self):
        self.base_url = "https://artale-market.org"
        self.api_url = "https://artale-market.org/api/price-snapshots"
        self.cached_items = []
        self.cache_timestamp = 0
        self.cache_duration = 300  # 5分鐘緩存
        
    async def _fetch_all_items(self) -> List[Dict]:
        """從API獲取所有物品數據"""
        try:
            # 檢查緩存是否有效
            current_time = time.time()
            if self.cached_items and (current_time - self.cache_timestamp) < self.cache_duration:
                return self.cached_items
            
            async with aiohttp.ClientSession() as session:
                params = {'date': 'latest'}
                async with session.get(self.api_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        items = data.get('snapshots', [])
                        
                        # 更新緩存
                        self.cached_items = items
                        self.cache_timestamp = current_time
                        
                        logger.info(f"成功獲取 {len(items)} 個物品數據")
                        return items
                    else:
                        logger.error(f"API請求失敗，狀態碼: {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"獲取API數據失敗: {e}")
            return []
    
    def _format_price(self, price: int) -> str:
        """格式化價格顯示"""
        if price >= 1000000:
            return f"{price // 1000000}M{(price % 1000000) // 1000}K" if price % 1000000 >= 1000 else f"{price // 1000000}M"
        elif price >= 1000:
            return f"{price // 1000}K{price % 1000}" if price % 1000 != 0 else f"{price // 1000}K"
        else:
            return str(price)
    
    def _get_trend_text(self, percent: float) -> str:
        """根據價格變化百分比返回趨勢文字"""
        if percent > 5:
            return "大幅上漲 📈"
        elif percent > 0:
            return "上漲 📈"
        elif percent < -5:
            return "大幅下跌 📉"
        elif percent < 0:
            return "下跌 📉"
        else:
            return "穩定 ➡️"
    
    def _format_item_data(self, item: Dict) -> Dict:
        """格式化物品數據"""
        try:
            return {
                'name': item.get('item_name', '未知物品'),
                'type': item.get('item_type', '未知類型'),
                'price_low': self._format_price(item.get('low', 0)),
                'price_median': self._format_price(item.get('median', 0)),
                'price_high': self._format_price(item.get('high', 0)),
                'price_raw_median': item.get('median', 0),
                'volume': item.get('volume', 0),
                'trend': self._get_trend_text(item.get('recent_change_percent', 0)),
                'trend_percent': round(item.get('recent_change_percent', 0), 2),
                'last_updated': item.get('snapshot_date', '未知'),
                'source': 'artale-market.org'
            }
        except Exception as e:
            logger.error(f"格式化物品數據失敗: {e}")
            return None
    
    async def search_item_price(self, keyword: str) -> Optional[Dict]:
        """搜索道具價格信息"""
        try:
            items = await self._fetch_all_items()
            if not items:
                return None
            
            # 精確匹配
            for item in items:
                if keyword.lower() == item.get('item_name', '').lower():
                    return self._format_item_data(item)
            
            # 模糊匹配
            best_match = None
            best_score = 0
            
            for item in items:
                item_name = item.get('item_name', '')
                # 計算相似度
                score = fuzz.partial_ratio(keyword.lower(), item_name.lower())
                
                # 如果關鍵詞在物品名稱中，給予額外加分
                if keyword.lower() in item_name.lower():
                    score += 20
                
                if score > best_score and score >= 60:  # 設定最低匹配分數
                    best_score = score
                    best_match = item
            
            if best_match:
                logger.info(f"找到匹配物品: {best_match.get('item_name')} (匹配度: {best_score})")
                return self._format_item_data(best_match)
            
            # 嘗試部分關鍵詞匹配
            for item in items:
                item_name = item.get('item_name', '').lower()
                if any(word in item_name for word in keyword.lower().split()):
                    logger.info(f"找到部分匹配物品: {item.get('item_name')}")
                    return self._format_item_data(item)
            
            logger.info(f"未找到匹配的物品: {keyword}")
            return None
            
        except Exception as e:
            logger.error(f"搜索價格時發生錯誤: {e}")
            return None
    
    async def get_popular_items(self, limit: int = 10) -> List[Dict]:
        """獲取熱門物品（按交易量排序）"""
        try:
            items = await self._fetch_all_items()
            if not items:
                return []
            
            # 按交易量降序排序
            sorted_items = sorted(items, key=lambda x: x.get('volume', 0), reverse=True)
            
            popular_items = []
            for item in sorted_items[:limit]:
                formatted_item = self._format_item_data(item)
                if formatted_item:
                    popular_items.append(formatted_item)
            
            return popular_items
            
        except Exception as e:
            logger.error(f"獲取熱門物品失敗: {e}")
            return []
    
    async def get_trending_items(self, limit: int = 10) -> List[Dict]:
        """獲取趨勢物品（按價格變化排序）"""
        try:
            items = await self._fetch_all_items()
            if not items:
                return []
            
            # 按價格變化幅度降序排序
            sorted_items = sorted(items, 
                                key=lambda x: abs(x.get('recent_change_percent', 0)), 
                                reverse=True)
            
            trending_items = []
            for item in sorted_items[:limit]:
                # 只選擇變化幅度較大的物品
                if abs(item.get('recent_change_percent', 0)) >= 2:
                    formatted_item = self._format_item_data(item)
                    if formatted_item:
                        trending_items.append(formatted_item)
            
            return trending_items[:limit]
            
        except Exception as e:
            logger.error(f"獲取趨勢物品失敗: {e}")
            return []
    
    async def get_items_by_type(self, item_type: str, limit: int = 20) -> List[Dict]:
        """根據物品類型獲取物品"""
        try:
            items = await self._fetch_all_items()
            if not items:
                return []
            
            # 篩選指定類型的物品
            filtered_items = [item for item in items 
                            if item.get('item_type', '') == item_type]
            
            # 按交易量降序排序
            sorted_items = sorted(filtered_items, 
                                key=lambda x: x.get('volume', 0), 
                                reverse=True)
            
            type_items = []
            for item in sorted_items[:limit]:
                formatted_item = self._format_item_data(item)
                if formatted_item:
                    type_items.append(formatted_item)
            
            return type_items
            
        except Exception as e:
            logger.error(f"獲取{item_type}類物品失敗: {e}")
            return []
    
    def get_available_types(self) -> List[str]:
        """獲取所有可用的物品類型"""
        if not self.cached_items:
            return []
        
        types = set()
        for item in self.cached_items:
            item_type = item.get('item_type', '')
            if item_type:
                types.add(item_type)
        
        return sorted(list(types))

# 創建全局實例
scraper = ArtaleMarketScraper()

# 同步包裝函數，供Discord bot使用
def search_item_price(keyword: str) -> Optional[Dict]:
    """同步版本的搜索函數"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(scraper.search_item_price(keyword))
    finally:
        loop.close()

def get_popular_items(limit: int = 10) -> List[Dict]:
    """同步版本的熱門物品函數"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(scraper.get_popular_items(limit))
    finally:
        loop.close()

def get_trending_items(limit: int = 10) -> List[Dict]:
    """同步版本的趨勢物品函數"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(scraper.get_trending_items(limit))
    finally:
        loop.close()

async def test_scraper():
    """測試爬蟲功能"""
    print("=== 測試 Artale Market 爬蟲 ===")
    
    # 測試搜索
    test_keywords = ["手套攻擊", "披風幸運", "弓攻擊", "藥水"]
    
    for keyword in test_keywords:
        print(f"\n搜索: {keyword}")
        result = await scraper.search_item_price(keyword)
        if result:
            print(f"找到: {result['name']}")
            print(f"類型: {result['type']}")
            print(f"價格: {result['price_low']} - {result['price_median']} - {result['price_high']}")
            print(f"趨勢: {result['trend']} ({result['trend_percent']}%)")
            print(f"交易量: {result['volume']}")
        else:
            print("未找到匹配結果")
    
    # 測試熱門物品
    print("\n=== 熱門物品 ===")
    popular = await scraper.get_popular_items(5)
    for i, item in enumerate(popular, 1):
        print(f"{i}. {item['name']} - {item['price_median']} (交易量: {item['volume']})")
    
    # 測試趨勢物品
    print("\n=== 趨勢物品 ===")
    trending = await scraper.get_trending_items(5)
    for i, item in enumerate(trending, 1):
        print(f"{i}. {item['name']} - {item['trend']} ({item['trend_percent']}%)")

if __name__ == "__main__":
    asyncio.run(test_scraper()) 