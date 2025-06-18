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

# 檢查所有可能的Discord token變數
possible_discord_vars = [
    'DISCORD_BOT_TOKEN',
    'DISCORD_TOKEN',
    'BOT_TOKEN', 
    'TOKEN'
]

print(f"\n=== Discord Token 檢查 ===")
found_token = False

for var_name in possible_discord_vars:
    token_value = os.getenv(var_name)
    if token_value:
        print(f"✅ 找到 {var_name}")
        print(f"   長度: {len(token_value)}")
        print(f"   開頭: {token_value[:15]}...")
        found_token = True
    else:
        print(f"❌ {var_name}: 未設置")

if found_token:
    print("✅ 至少找到一個Discord token！")
else:
    print("❌ 沒有找到任何Discord token變數")
    print("請檢查Railway Variables設置")

# 列出所有包含 'DISCORD' 或 'TOKEN' 的環境變數
print(f"\n=== 所有相關環境變數 ===")
relevant_vars = {}
for key, value in os.environ.items():
    if 'DISCORD' in key.upper() or 'TOKEN' in key.upper() or 'BOT' in key.upper():
        relevant_vars[key] = value

if relevant_vars:
    for key, value in relevant_vars.items():
        print(f"🔍 {key} = {value[:20]}...")
else:
    print("❌ 沒有找到任何相關的環境變數")

print("\n=== 測試完成 ===") 