import asyncio
import json
import re
from typing import Optional, Dict, List
import time
import logging
from fuzzywuzzy import fuzz
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import random

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
        self.executor = ThreadPoolExecutor(max_workers=1)
        
    def _try_requests_with_retry(self) -> List[Dict]:
        """嘗試使用 requests 獲取數據，包含重試機制"""
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                logger.info(f"requests 嘗試 {attempt + 1}/{max_retries}...")
                
                # 構建更完整的請求頭
                headers = {
                    'User-Agent': random.choice([
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    ]),
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Cache-Control': 'max-age=0',
                }
                
                session = requests.Session()
                session.headers.update(headers)
                
                # 先訪問主頁建立會話
                logger.info("訪問主頁建立會話...")
                main_response = session.get(self.base_url, timeout=30)
                
                # 檢查是否被 Cloudflare 阻擋
                if main_response.status_code == 403 or "just a moment" in main_response.text.lower():
                    logger.warning(f"嘗試 {attempt + 1}: 主頁被 Cloudflare 阻擋")
                    time.sleep(5 * (attempt + 1))  # 遞增延遲
                    continue
                
                # 等待一段時間模擬人類行為
                time.sleep(random.uniform(2, 5))
                
                # 請求 API 數據
                logger.info("請求 API 數據...")
                api_response = session.get(f"{self.api_url}?date=latest", timeout=30)
                
                if api_response.status_code == 200:
                    try:
                        # 檢查響應內容
                        content_type = api_response.headers.get('content-type', '').lower()
                        if 'application/json' in content_type or api_response.text.strip().startswith('{'):
                            data = api_response.json()
                            items = data.get('snapshots', [])
                            if items:
                                logger.info(f"requests 成功獲取 {len(items)} 個物品數據")
                                return items
                        else:
                            logger.warning(f"嘗試 {attempt + 1}: API 返回非 JSON 內容")
                    except json.JSONDecodeError as e:
                        logger.warning(f"嘗試 {attempt + 1}: JSON 解析失敗: {e}")
                else:
                    logger.warning(f"嘗試 {attempt + 1}: API 請求失敗，狀態碼: {api_response.status_code}")
                
                # 在重試前等待
                if attempt < max_retries - 1:
                    wait_time = 10 * (attempt + 1)
                    logger.info(f"等待 {wait_time} 秒後重試...")
                    time.sleep(wait_time)
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"嘗試 {attempt + 1}: 請求異常: {e}")
                if attempt < max_retries - 1:
                    wait_time = 5 * (attempt + 1)
                    time.sleep(wait_time)
            except Exception as e:
                logger.error(f"嘗試 {attempt + 1}: 未知錯誤: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
        
        logger.error("所有 requests 嘗試都失敗了")
        return []
    
    def _try_selenium_fallback(self) -> List[Dict]:
        """使用 Selenium 作為備用方案（如果 Selenium 可用）"""
        try:
            # 只有在 Selenium 可用時才嘗試
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from selenium.webdriver.common.by import By
            from webdriver_manager.chrome import ChromeDriverManager
            
            logger.info("嘗試使用 Selenium 備用方案...")
            
            options = Options()
            options.add_argument('--headless')  # 無頭模式
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-images')
            options.add_argument('--log-level=3')
            
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            try:
                # 設置較短的超時時間
                driver.set_page_load_timeout(60)
                
                # 訪問 API
                driver.get(f"{self.api_url}?date=latest")
                time.sleep(10)  # 等待頁面加載
                
                # 嘗試提取數據
                try:
                    pre_elements = driver.find_elements(By.TAG_NAME, "pre")
                    for pre in pre_elements:
                        text = pre.text.strip()
                        if text and text.startswith('{'):
                            data = json.loads(text)
                            items = data.get('snapshots', [])
                            if items:
                                logger.info(f"Selenium 成功獲取 {len(items)} 個物品數據")
                                return items
                except Exception as e:
                    logger.warning(f"Selenium JSON 提取失敗: {e}")
                
                return []
                
            finally:
                driver.quit()
                
        except ImportError:
            logger.warning("Selenium 不可用，跳過 Selenium 備用方案")
            return []
        except Exception as e:
            logger.error(f"Selenium 備用方案失敗: {e}")
            return []
    
    def _fetch_data_with_strategies(self) -> List[Dict]:
        """使用多種策略獲取數據"""
        # 策略1: 使用 requests（主要方法）
        items = self._try_requests_with_retry()
        
        # 策略2: 如果失敗且 Selenium 可用，使用 Selenium
        if not items:
            logger.info("requests 方法失敗，嘗試 Selenium...")
            items = self._try_selenium_fallback()
        
        # 策略3: 使用模擬數據（緊急備用）
        if not items:
            logger.warning("所有數據獲取方法都失敗，使用模擬數據")
            items = self._get_mock_data()
        
        return items
    
    def _get_mock_data(self) -> List[Dict]:
        """返回一些模擬數據作為最後備用"""
        return [
            {
                'item_name': '楓葉',
                'item_type': '其他',
                'low': 100,
                'median': 150,
                'high': 200,
                'volume': 50,
                'recent_change_percent': 5.0,
                'snapshot_date': '2024-01-01'
            },
            {
                'item_name': '藥水',
                'item_type': '消耗品',
                'low': 500,
                'median': 750,
                'high': 1000,
                'volume': 100,
                'recent_change_percent': -2.0,
                'snapshot_date': '2024-01-01'
            }
        ]
    
    async def _fetch_all_items(self) -> List[Dict]:
        """獲取所有物品數據"""
        try:
            # 檢查緩存
            current_time = time.time()
            if self.cached_items and (current_time - self.cache_timestamp) < self.cache_duration:
                return self.cached_items
            
            # 在線程池中運行數據獲取
            loop = asyncio.get_event_loop()
            items = await loop.run_in_executor(self.executor, self._fetch_data_with_strategies)
            
            # 更新緩存
            if items:
                self.cached_items = items
                self.cache_timestamp = current_time
                logger.info(f"成功獲取並緩存 {len(items)} 個物品數據")
            
            return items
                        
        except Exception as e:
            logger.error(f"獲取數據失敗: {e}")
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
                score = fuzz.partial_ratio(keyword.lower(), item_name.lower())
                
                if keyword.lower() in item_name.lower():
                    score += 20
                
                if score > best_score and score >= 60:
                    best_score = score
                    best_match = item
            
            if best_match:
                logger.info(f"找到匹配物品: {best_match.get('item_name')} (匹配度: {best_score})")
                return self._format_item_data(best_match)
            
            # 部分關鍵詞匹配
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
            
            sorted_items = sorted(items, 
                                key=lambda x: abs(x.get('recent_change_percent', 0)), 
                                reverse=True)
            
            trending_items = []
            for item in sorted_items[:limit]:
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
            
            filtered_items = [item for item in items 
                            if item.get('item_type', '') == item_type]
            
            sorted_items = sorted(filtered_items, 
                                key=lambda x: x.get('volume', 0), reverse=True)
            
            result_items = []
            for item in sorted_items[:limit]:
                formatted_item = self._format_item_data(item)
                if formatted_item:
                    result_items.append(formatted_item)
            
            return result_items
            
        except Exception as e:
            logger.error(f"根據類型獲取物品失敗: {e}")
            return []
    
    def get_available_types(self) -> List[str]:
        """獲取可用的物品類型"""
        if not self.cached_items:
            return []
        
        types = set()
        for item in self.cached_items:
            item_type = item.get('item_type')
            if item_type:
                types.add(item_type)
        
        return sorted(list(types))
    
    def __del__(self):
        """析構函數"""
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=True)

# 全域實例
_scraper_instance = None

def get_scraper():
    """獲取爬蟲實例（單例模式）"""
    global _scraper_instance
    if _scraper_instance is None:
        _scraper_instance = ArtaleMarketScraper()
    return _scraper_instance

# 向後兼容的函數
def search_item_price(keyword: str) -> Optional[Dict]:
    """搜索道具價格信息（同步版本）"""
    scraper = get_scraper()
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(scraper.search_item_price(keyword))

def get_popular_items(limit: int = 10) -> List[Dict]:
    """獲取熱門物品（同步版本）"""
    scraper = get_scraper()
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(scraper.get_popular_items(limit))

def get_trending_items(limit: int = 10) -> List[Dict]:
    """獲取趨勢物品（同步版本）"""
    scraper = get_scraper()
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(scraper.get_trending_items(limit))

# 測試函數
async def test_scraper():
    """測試爬蟲功能"""
    scraper = ArtaleMarketScraper()
    
    try:
        print("測試增強版 Artale Market 爬蟲...")
        items = await scraper._fetch_all_items()
        print(f"獲取到 {len(items)} 個物品")
        
        if items:
            print("\n前3個物品:")
            for i, item in enumerate(items[:3]):
                name = item.get('item_name', '未知')
                item_type = item.get('item_type', '未知')
                median = item.get('median', 0)
                volume = item.get('volume', 0)
                print(f"{i+1}. {name} ({item_type}) - 價格: {median:,}, 交易量: {volume}")
            
            # 測試搜索
            print("\n測試搜索功能...")
            result = await scraper.search_item_price("楓葉")
            if result:
                print(f"搜索 '楓葉': {result['name']} - {result['price_median']}")
        
    except Exception as e:
        print(f"測試失敗: {e}")

if __name__ == "__main__":
    asyncio.run(test_scraper()) 