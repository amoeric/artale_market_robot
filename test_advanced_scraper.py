#!/usr/bin/env python3
"""
進階 Selenium 爬取 Artale Market 數據的腳本
使用多種策略繞過 Cloudflare 保護
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
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def get_advanced_chrome_options():
    """設置進階 Chrome 選項以避免被檢測"""
    options = Options()
    
    # 基本隱身設置
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--disable-features=VizDisplayCompositor')
    
    # 進階反檢測設置
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # 隨機用戶代理
    user_agents = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    # 窗口設置
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--start-maximized')
    
    # 性能優化
    options.page_load_strategy = 'eager'
    options.add_argument('--log-level=3')
    options.add_argument('--silent')
    
    return options

def setup_stealth_driver():
    """設置隱蔽的 webdriver"""
    try:
        print("正在初始化隱蔽的 Chrome 瀏覽器...")
        
        service = Service(ChromeDriverManager().install())
        options = get_advanced_chrome_options()
        driver = webdriver.Chrome(service=service, options=options)
        
        # 執行更完整的反檢測腳本
        stealth_script = """
        // Remove webdriver property
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined,
        });
        
        // Mock plugins
        Object.defineProperty(navigator, 'plugins', {
            get: () => [1, 2, 3, 4, 5],
        });
        
        // Mock languages
        Object.defineProperty(navigator, 'languages', {
            get: () => ['zh-TW', 'zh', 'en-US', 'en'],
        });
        
        // Mock permissions
        const originalQuery = window.navigator.permissions.query;
        window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
        
        // Override chrome object
        window.chrome = {
            runtime: {},
        };
        
        // Additional webdriver masking
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
        });
        
        // Remove automation indicator
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
        """
        
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': stealth_script
        })
        
        print("隱蔽瀏覽器初始化完成")
        return driver
        
    except Exception as e:
        print(f"初始化瀏覽器失敗: {e}")
        raise

def human_delay(min_seconds=2, max_seconds=5):
    """模擬人類延遲"""
    delay = random.uniform(min_seconds, max_seconds)
    time.sleep(delay)

def simulate_human_browsing(driver):
    """模擬人類瀏覽行為"""
    try:
        print("正在模擬人類瀏覽行為...")
        
        # 隨機滾動多次
        for _ in range(random.randint(2, 4)):
                         scroll_position = random.randint(100, 800)
             driver.execute_script(f"window.scrollTo(0, {scroll_position});")
             human_delay(1, 2)
        
        # 回到頂部
        driver.execute_script("window.scrollTo(0, 0);")
        human_delay(1, 2)
        
        # 模擬鼠標移動和點擊
        driver.execute_script("""
            // 模擬鼠標移動
            const moveEvent = new MouseEvent('mousemove', {
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: Math.random() * window.innerWidth,
                clientY: Math.random() * window.innerHeight
            });
            document.dispatchEvent(moveEvent);
            
            // 模擬隨機點擊（但不實際觸發）
            const clickEvent = new MouseEvent('mousedown', {
                view: window,
                bubbles: true,
                cancelable: true,
                clientX: Math.random() * window.innerWidth / 2,
                clientY: Math.random() * window.innerHeight / 2
            });
            document.dispatchEvent(clickEvent);
        """)
        
        human_delay(1, 2)
        
    except Exception as e:
        print(f"模擬人類行為時發生錯誤: {e}")

def wait_for_cloudflare_bypass(driver, timeout=120):
    """等待 Cloudflare 保護繞過"""
    try:
        print("檢查 Cloudflare 保護狀態...")
        
        # 檢查頁面是否包含 Cloudflare 挑戰
        cloudflare_indicators = [
            "just a moment", "checking your browser", "please wait",
            "請稍候", "正在檢查您的瀏覽器", "驗證中", "cloudflare",
            "ray id", "security check", "browser check"
        ]
        
        page_source = driver.page_source.lower()
        has_cloudflare = any(indicator in page_source for indicator in cloudflare_indicators)
        
        if has_cloudflare:
            print("檢測到 Cloudflare 保護，等待自動繞過...")
            
            # 在等待期間繼續模擬人類行為
            start_time = time.time()
            while time.time() - start_time < timeout:
                current_source = driver.page_source.lower()
                
                # 檢查是否已經繞過
                if not any(indicator in current_source for indicator in cloudflare_indicators):
                    print("✅ Cloudflare 保護已繞過")
                    human_delay(2, 4)  # 額外等待確保頁面穩定
                    return True
                
                # 模擬人類行為
                try:
                    simulate_human_browsing(driver)
                except:
                    pass
                
                human_delay(3, 6)
            
            print("❌ Cloudflare 保護繞過超時")
            return False
        else:
            print("✅ 未檢測到 Cloudflare 保護")
            return True
            
    except Exception as e:
        print(f"等待 Cloudflare 繞過時發生錯誤: {e}")
        return False

def extract_json_data(driver):
    """從頁面中提取 JSON 數據"""
    try:
        print("正在提取 JSON 數據...")
        
        # 方法1: 從 <pre> 標籤提取
        try:
            pre_elements = driver.find_elements(By.TAG_NAME, "pre")
            for pre in pre_elements:
                text = pre.text.strip()
                if text and (text.startswith('{') or text.startswith('[')):
                    try:
                        data = json.loads(text)
                        print("從 <pre> 標籤成功提取 JSON")
                        return data
                    except json.JSONDecodeError:
                        continue
        except Exception:
            pass
        
        # 方法2: 從頁面源碼中搜尋 JSON
        page_source = driver.page_source
        
        # 尋找可能的 JSON 開始位置
        json_patterns = [
            r'{"snapshots":\s*\[',
            r'\[{"item_name"',
            r'{"success":\s*true',
        ]
        
        import re
        for pattern in json_patterns:
            match = re.search(pattern, page_source)
            if match:
                start_pos = match.start()
                
                # 從找到的位置開始提取完整 JSON
                bracket_count = 0
                json_start = -1
                json_end = -1
                
                for i in range(start_pos, len(page_source)):
                    char = page_source[i]
                    if char in ['{', '[']:
                        if json_start == -1:
                            json_start = i
                        bracket_count += 1
                    elif char in ['}', ']']:
                        bracket_count -= 1
                        if json_start != -1 and bracket_count == 0:
                            json_end = i + 1
                            break
                
                if json_start != -1 and json_end != -1:
                    json_text = page_source[json_start:json_end]
                    try:
                        data = json.loads(json_text)
                        print("從頁面源碼成功提取 JSON")
                        return data
                    except json.JSONDecodeError:
                        continue
        
        print("❌ 無法從頁面中提取有效的 JSON 數據")
        return None
        
    except Exception as e:
        print(f"提取 JSON 數據時發生錯誤: {e}")
        return None

def test_advanced_scraping():
    """測試進階爬取策略"""
    driver = None
    
    try:
        # 初始化隱蔽瀏覽器
        driver = setup_stealth_driver()
        
        base_url = "https://artale-market.org"
        api_url = "https://artale-market.org/api/price-snapshots?date=latest"
        
        print(f"第一階段：訪問主頁 {base_url}")
        
        # 階段1：訪問主頁建立可信會話
        driver.get(base_url)
        human_delay(4, 7)
        
        # 等待並繞過可能的 Cloudflare 保護
        if not wait_for_cloudflare_bypass(driver, 90):
            print("主頁 Cloudflare 繞過失敗")
            return False
        
        # 在主頁進行人類行為模擬
        simulate_human_browsing(driver)
        human_delay(3, 5)
        
        print(f"第二階段：請求 API {api_url}")
        
        # 階段2：請求 API 數據
        driver.get(api_url)
        human_delay(5, 8)
        
        # 等待 API 頁面的 Cloudflare 保護
        if not wait_for_cloudflare_bypass(driver, 120):
            print("API 頁面 Cloudflare 繞過失敗")
            return False
        
        # 提取數據
        data = extract_json_data(driver)
        
        if data:
            items = data.get('snapshots', []) if isinstance(data, dict) else data
            
            if items and len(items) > 0:
                print(f"🎉 成功獲取 {len(items)} 個物品數據！")
                
                # 顯示前幾個物品
                print("\n📦 物品樣本:")
                for i, item in enumerate(items[:5]):
                    name = item.get('item_name', '未知')
                    item_type = item.get('item_type', '未知')
                    median = item.get('median', 0)
                    volume = item.get('volume', 0)
                    print(f"{i+1}. {name} ({item_type}) - 中位價: {median:,}, 交易量: {volume}")
                
                return True
            else:
                print("❌ 獲取的數據為空")
                return False
        else:
            print("❌ 無法提取數據")
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        if driver:
            print("正在關閉瀏覽器...")
            try:
                driver.quit()
            except Exception:
                pass

if __name__ == "__main__":
    print("=== 進階 Artale Market 爬取測試 ===")
    print("使用多重策略繞過 Cloudflare 保護\n")
    
    success = test_advanced_scraping()
    
    if success:
        print("\n🎉 測試成功！成功繞過 Cloudflare 保護並獲取數據")
        print("現在可以將這些技術集成到主要的爬蟲中")
    else:
        print("\n❌ 測試失敗！可能需要調整策略或檢查網站狀態")
        print("建議：")
        print("1. 檢查網路連接")
        print("2. 嘗試使用不同的用戶代理")
        print("3. 增加等待時間")
        print("4. 檢查 Chrome 瀏覽器版本") 