#!/usr/bin/env python3
import os

print("=== Railway 測試 ===")
print(f"Python 可以正常運行")
print(f"當前目錄: {os.getcwd()}")
print(f"環境變數數量: {len(os.environ)}")

# 檢查一些Railway特有的環境變數
railway_vars = [
    'RAILWAY_SERVICE_NAME',
    'RAILWAY_ENVIRONMENT',
    'RAILWAY_PROJECT_NAME'
]

print("\n=== Railway 環境變數 ===")
for var in railway_vars:
    value = os.getenv(var)
    if value:
        print(f"✓ {var} = {value}")
    else:
        print(f"✗ {var} = 未設置")

# 檢查DISCORD_BOT_TOKEN
discord_token = os.getenv('DISCORD_BOT_TOKEN')
print(f"\n=== Discord Token 檢查 ===")
print(f"DISCORD_BOT_TOKEN 存在: {discord_token is not None}")

if discord_token:
    print(f"Token 長度: {len(discord_token)}")
    print(f"Token 開頭: {discord_token[:15]}...")
    print("✅ Discord token 設置正確！")
else:
    print("❌ Discord token 未設置")
    print("請在Railway Variables中設置 DISCORD_BOT_TOKEN")

print("\n=== 測試完成 ===") 