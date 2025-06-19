#!/usr/bin/env python3
"""
修正版 Selenium 爬取測試腳本
"""

import json
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_options():
    """設置 Chrome 選項"""
    options = Options()
    
    # 基本設置
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-images')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 隨機用戶代理
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--log-level=3')
    
    return options

def setup_driver():
    """初始化 webdriver"""
    try:
        print("正在初始化 Chrome 瀏覽器...")
        service = Service(ChromeDriverManager().install())
        options = get_chrome_options()
        driver = webdriver.Chrome(service=service, options=options)
        
        # 反檢測腳本
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                window.chrome = { runtime: {} };
            '''
        })
        
        print("瀏覽器初始化完成")
        return driver
        
    except Exception as e:
        print(f"初始化瀏覽器失敗: {e}")
        raise

def wait_and_simulate(driver, min_seconds=2, max_seconds=5):
    """等待並模擬人類行為"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)
    
    try:
        # 簡單的滾動模擬
        for _ in range(2):
            scroll_y = random.randint(100, 400)
            driver.execute_script(f"window.scrollTo(0, {scroll_y});")
            time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
    except Exception:
        pass

def check_cloudflare(driver):
    """檢查是否有 Cloudflare 保護"""
    page_source = driver.page_source.lower()
    cf_indicators = [
        "just a moment", "checking your browser", "請稍候",
        "cloudflare", "security check"
    ]
    return any(indicator in page_source for indicator in cf_indicators)

def wait_for_bypass(driver, timeout=90):
    """等待 Cloudflare 繞過"""
    if not check_cloudflare(driver):
        print("✅ 未檢測到 Cloudflare 保護")
        return True
    
    print("檢測到 Cloudflare 保護，等待繞過...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if not check_cloudflare(driver):
            print("✅ Cloudflare 保護已繞過")
            time.sleep(2)  # 額外等待
            return True
        
        wait_and_simulate(driver, 3, 6)
    
    print("❌ Cloudflare 保護繞過超時")
    return False

def extract_json(driver):
    """提取 JSON 數據"""
    try:
        # 方法1: 從 <pre> 標籤提取
        try:
            pre_elements = driver.find_elements(By.TAG_NAME, "pre")
            for pre in pre_elements:
                text = pre.text.strip()
                if text and (text.startswith('{') or text.startswith('[')):
                    return json.loads(text)
        except Exception:
            pass
        
        # 方法2: 從頁面源碼提取
        page_source = driver.page_source
        
        # 尋找 JSON 模式
        patterns = [r'{"snapshots":\s*\[', r'\[{"item_name"']
        
        for pattern in patterns:
            match = re.search(pattern, page_source)
            if match:
                start_pos = match.start()
                
                # 找 JSON 結束位置
                bracket_count = 0
                json_start = -1
                
                for i in range(start_pos, len(page_source)):
                    char = page_source[i]
                    if char in ['{', '[']:
                        if json_start == -1:
                            json_start = i
                        bracket_count += 1
                    elif char in ['}', ']']:
                        bracket_count -= 1
                        if json_start != -1 and bracket_count == 0:
                            json_text = page_source[json_start:i+1]
                            try:
                                return json.loads(json_text)
                            except json.JSONDecodeError:
                                break
        
        return None
        
    except Exception as e:
        print(f"提取 JSON 失敗: {e}")
        return None

def test_scraping():
    """測試爬取功能"""
    driver = None
    
    try:
        driver = setup_driver()
        
        base_url = "https://artale-market.org"
        api_url = "https://artale-market.org/api/price-snapshots?date=latest"
        
        print(f"階段1: 訪問主頁 {base_url}")
        driver.get(base_url)
        wait_and_simulate(driver, 3, 6)
        
        if not wait_for_bypass(driver, 60):
            print("主頁 Cloudflare 繞過失敗")
            return False
        
        print(f"階段2: 請求 API {api_url}")
        driver.get(api_url)
        wait_and_simulate(driver, 4, 8)
        
        if not wait_for_bypass(driver, 90):
            print("API 頁面 Cloudflare 繞過失敗")
            return False
        
        # 提取數據
        data = extract_json(driver)
        
        if data:
            items = data.get('snapshots', []) if isinstance(data, dict) else data
            
            if items and len(items) > 0:
                print(f"🎉 成功獲取 {len(items)} 個物品數據！")
                
                # 顯示樣本數據
                print("\n📦 物品樣本:")
                for i, item in enumerate(items[:3]):
                    name = item.get('item_name', '未知')
                    item_type = item.get('item_type', '未知')
                    median = item.get('median', 0)
                    volume = item.get('volume', 0)
                    print(f"{i+1}. {name} ({item_type}) - 價格: {median:,}, 交易量: {volume}")
                
                return True
            else:
                print("❌ 數據為空")
                return False
        else:
            print("❌ 無法提取數據")
            page_preview = driver.page_source[:500]
            print(f"頁面預覽: {page_preview}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print("關閉瀏覽器...")
            try:
                driver.quit()
            except Exception:
                pass

if __name__ == "__main__":
    print("=== Artale Market 爬取測試 ===")
    
    success = test_scraping()
    
    if success:
        print("\n🎉 測試成功！可以繼續集成到主要系統")
    else:
        print("\n❌ 測試失敗，可能需要調整策略") 