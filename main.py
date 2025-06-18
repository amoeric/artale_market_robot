import discord
from discord.ext import commands
import asyncio
import os
import re
import threading
from typing import Optional, List, Dict
from price_scraper import ArtaleMarketScraper
# 載入.env文件（本地開發用）
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ .env文件已載入")
except ImportError:
    print("⚠️ python-dotenv未安裝，跳過.env文件載入")

# 機器人設定
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# 創建價格查詢實例
scraper = ArtaleMarketScraper()

@bot.event
async def on_ready():
    print(f'{bot.user} 已成功連接到Discord!')
    print(f'機器人ID: {bot.user.id}')
    print('機器人已準備就緒!')

@bot.event
async def on_message(message):
    # 防止機器人回應自己的訊息
    if message.author == bot.user:
        return
    
    # 檢查是否有標記機器人
    if bot.user.mentioned_in(message):
        # 提取關鍵字（去除標記部分）
        content = message.content
        # 移除機器人標記
        content = re.sub(r'<@!?\d+>', '', content).strip()
        
        if content:
            # 搜索道具價格
            await search_and_reply(message, content)
        else:
            embed = discord.Embed(
                title="🤖 Artale Market 機器人",
                description="請在標記我的時候輸入您想查詢的道具名稱！\n\n**使用方法：**\n`@機器人名稱 道具名稱`\n\n**範例：**\n`@機器人名稱 楓葉`\n`@機器人名稱 頭盔`",
                color=0x00ff00
            )
            await message.channel.send(embed=embed)
    
    # 處理其他指令
    await bot.process_commands(message)

async def search_and_reply(message, keyword):
    """搜索並回覆價格信息"""
    # 發送搜索中的訊息
    searching_embed = discord.Embed(
        title="🔍 搜索中...",
        description=f"正在查詢「{keyword}」的價格信息，請稍候...",
        color=0xffff00
    )
    temp_message = await message.channel.send(embed=searching_embed)
    
    # 搜索價格
    result = await scraper.search_item_price(keyword)
    
    if result:
        # 創建結果嵌入訊息
        embed = discord.Embed(
            title=f"💰 {result['name']} - 價格信息",
            color=0x00ff00
        )
        
        embed.add_field(
            name="📦 物品類型",
            value=result['type'],
            inline=True
        )
        
        embed.add_field(
            name="💵 價格區間",
            value=f"**最低:** {result['price_low']}\n**中位:** {result['price_median']}\n**最高:** {result['price_high']}",
            inline=True
        )
        
        embed.add_field(
            name="📈 價格趨勢",
            value=f"{result['trend']}\n({result['trend_percent']}%)",
            inline=True
        )
        
        embed.add_field(
            name="📊 交易量",
            value=f"{result['volume']} 筆",
            inline=True
        )
        
        embed.add_field(
            name="🕒 最後更新",
            value=result['last_updated'],
            inline=True
        )
        
        embed.add_field(
            name="🔗 查看更多",
            value=f"[點擊查看詳細信息]({scraper.base_url}/price-trends)",
            inline=False
        )
        
        embed.set_footer(text=f"數據來源: {result['source']}")
        
    else:
        # 搜索失敗
        embed = discord.Embed(
            title="❌ 搜索失敗",
            description=f"很抱歉，無法找到「{keyword}」的價格信息。\n\n可能的原因：\n• 道具名稱拼寫錯誤\n• 該道具尚未有交易記錄\n• 網站暫時無法訪問",
            color=0xff0000
        )
        
        embed.add_field(
            name="💡 建議",
            value="• 檢查道具名稱拼寫\n• 嘗試使用道具的簡稱\n• 稍後再試",
            inline=False
        )
    
    # 更新訊息
    await temp_message.edit(embed=embed)

@bot.command(name='price', aliases=['p', '價格'])
async def price_command(ctx, *, keyword):
    """使用指令查詢價格"""
    await search_and_reply(ctx.message, keyword)

@bot.command(name='help', aliases=['幫助'])
async def help_command(ctx):
    """顯示幫助信息"""
    embed = discord.Embed(
        title="🤖 Artale Market 機器人使用說明",
        description="這個機器人可以幫你查詢楓之谷 Artale 的道具價格信息！",
        color=0x0099ff
    )
    
    embed.add_field(
        name="📋 使用方法",
        value="**方法1：標記機器人**\n`@機器人名稱 道具名稱`\n\n**方法2：使用指令**\n`!price 道具名稱`\n`!p 道具名稱`",
        inline=False
    )
    
    embed.add_field(
        name="💡 範例",
        value="`@機器人名稱 楓葉`\n`!price 頭盔`\n`!p 藥水`",
        inline=False
    )
    
    embed.add_field(
        name="🔗 相關連結",
        value=f"[Artale Market 官網]({scraper.base_url})",
        inline=False
    )
    
    embed.set_footer(text="如有問題或建議，請聯繫管理員")
    
    await ctx.send(embed=embed)

def run_bot():
    """啟動Discord bot"""
    # 嘗試多種環境變數名稱
    possible_names = [
        'DISCORD_BOT_TOKEN',
        'DISCORD_TOKEN', 
        'BOT_TOKEN',
        'TOKEN'
    ]
    
    token = None
    found_var = None
    
    print("環境變數檢查:")
    for name in possible_names:
        test_token = os.getenv(name)
        if test_token:
            token = test_token
            found_var = name
            print(f"✅ 找到環境變數: {name}")
            print(f"Token長度: {len(token)}")
            print(f"Token開頭: {token[:10]}...")
            break
        else:
            print(f"❌ {name}: 未找到")
    
    if not token:
        print("請設置 DISCORD_BOT_TOKEN 環境變量")
        print("你可以創建一個 .env 檔案並添加：")
        print("DISCORD_BOT_TOKEN=your_bot_token_here")
        return
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("機器人Token無效，請檢查DISCORD_BOT_TOKEN環境變量")
    except Exception as e:
        print(f"啟動機器人時發生錯誤: {e}")

def start_http_server():
    """啟動簡單的HTTP服務器供Render使用"""
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
        import json
        
        class HealthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == '/':
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    response = {
                        "status": "running",
                        "service": "Artale Market Discord Bot",
                        "bot_user": str(bot.user) if bot.user else "Connecting..."
                    }
                    self.wfile.write(json.dumps(response).encode())
                elif self.path == '/health':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/plain')
                    self.end_headers()
                    self.wfile.write(b'OK')
                else:
                    self.send_response(404)
                    self.end_headers()
            
            def log_message(self, format, *args):
                # 靜默HTTP日誌
                pass
        
        port = int(os.environ.get('PORT', 10000))
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        print(f"🌐 HTTP服務器啟動在端口 {port}")
        server.serve_forever()
    except Exception as e:
        print(f"❌ HTTP服務器錯誤: {e}")

if __name__ == "__main__":
    # 檢查是否在Render環境中
    if os.getenv('RENDER'):
        print("🚀 檢測到Render環境，啟動HTTP服務器...")
        # 在背景執行Discord bot
        bot_thread = threading.Thread(target=run_bot, daemon=True)
        bot_thread.start()
        # 主線程運行HTTP服務器
        start_http_server()
    else:
        # 本地開發環境，直接運行bot
        run_bot() 