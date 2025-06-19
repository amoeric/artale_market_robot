#!/usr/bin/env python3
"""
測試 Selenium 爬取 Artale Market 數據的腳本
"""

import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

def get_chrome_options():
    """設置 Chrome 選項以避免被檢測"""
    options = Options()
    
    # 基本隱身設置
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')  # 禁用圖片加載以提高速度
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    
    # 用戶代理隨機化
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    # 其他反檢測設置
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 設置頁面加載策略
    options.page_load_strategy = 'eager'
    
    # 禁用日誌
    options.add_argument('--log-level=3')
    options.add_argument('--silent')
    
    return options

def human_like_delay(min_delay=1, max_delay=3):
    """模擬人類的隨機延遲"""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def test_artale_market_scraping():
    """測試 Artale Market 爬取"""
    driver = None
    
    try:
        print("正在初始化 Chrome 瀏覽器...")
        
        # 使用 webdriver-manager 自動管理 ChromeDriver
        service = Service(ChromeDriverManager().install())
        options = get_chrome_options()
        driver = webdriver.Chrome(service=service, options=options)
        
        # 執行反檢測腳本
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                window.chrome = {
                    runtime: {},
                };
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-TW', 'zh', 'en'],
                });
            '''
        })
        
        print("瀏覽器初始化完成")
        
        base_url = "https://artale-market.org"
        api_url = "https://artale-market.org/api/price-snapshots"
        
        print(f"正在訪問網站: {base_url}")
        
        # 先訪問主頁，建立會話
        driver.get(base_url)
        human_like_delay(3, 5)
        
        # 等待頁面加載完成
        try:
            WebDriverWait(driver, 30).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            print("主頁加載完成")
        except TimeoutException:
            print("⚠️ 主頁加載超時，但繼續執行...")
        
        # 模擬人類行為：滾動頁面
        print("正在模擬人類瀏覽行為...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        human_like_delay(1, 2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        human_like_delay(1, 2)
        driver.execute_script("window.scrollTo(0, 0);")
        human_like_delay(1, 2)
        
        # 嘗試獲取 API 數據
        api_url_with_params = f"{api_url}?date=latest"
        print(f"正在請求 API: {api_url_with_params}")
        
        # 在同一個會話中請求 API
        driver.get(api_url_with_params)
        human_like_delay(5, 8)  # 給更多時間處理 Cloudflare
        
        # 檢查是否有 Cloudflare 挑戰頁面
        page_source = driver.page_source
        if "Just a moment" in page_source or "Checking your browser" in page_source:
            print("檢測到 Cloudflare 挑戰，等待自動處理...")
            try:
                WebDriverWait(driver, 60).until(
                    lambda driver: "Just a moment" not in driver.page_source and 
                                 "Checking your browser" not in driver.page_source
                )
                print("✅ Cloudflare 挑戰已通過")
                page_source = driver.page_source
            except TimeoutException:
                print("❌ Cloudflare 挑戰處理超時")
                return False
        
        print(f"響應長度: {len(page_source)} 字符")
        print(f"響應開頭: {page_source[:200]}")
        
        # 檢查是否是 JSON 響應
        if page_source.strip().startswith('{') or page_source.strip().startswith('['):
            try:
                # 從 <pre> 標籤中提取 JSON（Chrome 會自動格式化 JSON）
                try:
                    pre_element = driver.find_element(By.TAG_NAME, "pre")
                    json_text = pre_element.text
                    print("從 <pre> 標籤提取 JSON")
                except:
                    # 如果沒有 <pre> 標籤，直接使用頁面源碼
                    json_text = page_source.strip()
                    # 移除 HTML 標籤
                    if json_text.startswith('<html>'):
                        start = json_text.find('{')
                        end = json_text.rfind('}') + 1
                        if start != -1 and end != 0:
                            json_text = json_text[start:end]
                    print("從頁面源碼提取 JSON")
                
                # 解析 JSON
                data = json.loads(json_text)
                items = data.get('snapshots', []) if isinstance(data, dict) else data
                
                if items:
                    print(f"✅ 成功獲取 {len(items)} 個物品數據")
                    
                    # 顯示前幾個物品信息
                    print("\n前5個物品:")
                    for i, item in enumerate(items[:5]):
                        name = item.get('item_name', '未知')
                        item_type = item.get('item_type', '未知')
                        median = item.get('median', 0)
                        volume = item.get('volume', 0)
                        print(f"{i+1}. {name} ({item_type}) - 中位價: {median}, 交易量: {volume}")
                    
                    return True
                else:
                    print("❌ API 返回空數據")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON 解析失敗: {e}")
                print(f"響應內容: {page_source[:1000]}")
                return False
                
        else:
            print("❌ 響應不是有效的 JSON 格式")
            print(f"響應內容前 500 字符: {page_source[:500]}")
            return False
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print("正在關閉瀏覽器...")
            driver.quit()

if __name__ == "__main__":
    print("=== Artale Market Selenium 爬取測試 ===")
    success = test_artale_market_scraping()
    
    if success:
        print("\n🎉 測試成功！Selenium 能夠成功繞過 Cloudflare 保護並獲取數據")
    else:
        print("\n❌ 測試失敗！需要進一步調整策略") 