#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
測試Artale Market Discord Bot的價格查詢功能
"""

from price_scraper import ArtaleMarketScraper
import asyncio

def test_price_scraper():
    """測試價格爬蟲功能"""
    print("🔍 開始測試 Artale Market 價格爬蟲...")
    
    scraper = ArtaleMarketScraper()
    
    # 測試關鍵字列表
    test_keywords = [
        '楓葉', '頭盔', '藥水', '武器', '盔甲',
        '卷軸', '礦石', '飾品', '寵物', '坐騎',
        '不存在的道具'
    ]
    
    print("\n📊 測試搜索功能:")
    print("-" * 50)
    
    for i, keyword in enumerate(test_keywords, 1):
        print(f"\n{i:2d}. 搜索關鍵字: '{keyword}'")
        
        try:
            result = scraper.search_item_price(keyword)
            
            if result:
                print(f"    ✅ 找到結果:")
                print(f"       名稱: {result['name']}")
                print(f"       價格: {result['price']}")
                print(f"       趨勢: {result['trend']}")
                if 'category' in result:
                    print(f"       類別: {result['category']}")
                print(f"       來源: {result.get('source', '未知')}")
            else:
                print(f"    ❌ 未找到相關道具")
                
        except Exception as e:
            print(f"    ⚠️  發生錯誤: {e}")
    
    print("\n" + "=" * 50)
    print("📈 測試熱門道具功能:")
    print("-" * 50)
    
    try:
        popular_items = scraper.get_popular_items()
        for i, item in enumerate(popular_items, 1):
            print(f"{i}. {item['name']} - {item['price']} ({item['trend']})")
    except Exception as e:
        print(f"獲取熱門道具時發生錯誤: {e}")
    
    print("\n" + "=" * 50)
    print("📊 測試趨勢道具功能:")
    print("-" * 50)
    
    try:
        trending_items = scraper.get_trending_items()
        for i, item in enumerate(trending_items, 1):
            print(f"{i}. {item['name']} - {item['price']} (🔥 {item['trend']})")
    except Exception as e:
        print(f"獲取趨勢道具時發生錯誤: {e}")
    
    print("\n" + "=" * 50)
    print("✅ 測試完成！")

def test_discord_message_format():
    """測試Discord訊息格式"""
    print("\n🤖 測試Discord訊息格式:")
    print("-" * 50)
    
    scraper = ArtaleMarketScraper()
    result = scraper.search_item_price('楓葉')
    
    if result:
        # 模擬Discord Embed格式
        print("Discord Embed 預覽:")
        print(f"標題: 💰 {result['name']} - 價格信息")
        print(f"💵 當前價格: {result['price']}")
        print(f"📈 價格趨勢: {result['trend']}")
        if 'category' in result:
            print(f"🏷️ 道具類別: {result['category']}")
        print(f"🕒 最後更新: {result.get('last_updated', '未知')}")
        print(f"🔗 查看更多: https://artale-market.org/price-trends")
        print(f"數據來源: Artale Market")

async def test_async_functionality():
    """測試異步功能"""
    print("\n⚡ 測試異步搜索:")
    print("-" * 50)
    
    scraper = ArtaleMarketScraper()
    keywords = ['楓葉', '頭盔', '藥水']
    
    # 模擬異步搜索（實際上這裡是同步的，但可以展示如何使用）
    for keyword in keywords:
        result = scraper.search_item_price(keyword)
        if result:
            print(f"✅ {keyword}: {result['price']}")
        await asyncio.sleep(0.1)  # 模擬異步延遲

def main():
    """主函數"""
    print("🎮 Artale Market Discord Bot 測試程式")
    print("=" * 50)
    
    # 測試價格爬蟲
    test_price_scraper()
    
    # 測試Discord訊息格式
    test_discord_message_format()
    
    # 測試異步功能
    print("\n⚡ 執行異步測試...")
    asyncio.run(test_async_functionality())
    
    print("\n" + "=" * 50)
    print("🎉 所有測試完成！")
    print("\n💡 提示:")
    print("   1. 確保已安裝所有必要的依賴: pip install -r requirements.txt")
    print("   2. 創建 .env 檔案並添加你的 Discord Bot Token")
    print("   3. 執行 python main.py 啟動機器人")

if __name__ == "__main__":
    main() 