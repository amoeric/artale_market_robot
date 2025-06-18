#!/usr/bin/env python3
import os
import sys

print("=== Railway 環境變數檢查 ===")
print(f"Python版本: {sys.version}")
print(f"當前工作目錄: {os.getcwd()}")
print(f"環境變數總數: {len(os.environ)}")

print("\n=== 所有環境變數 ===")
for key, value in sorted(os.environ.items()):
    if 'TOKEN' in key.upper() or 'DISCORD' in key.upper():
        print(f"{key} = {value[:10]}..." if len(value) > 10 else f"{key} = {value}")
    else:
        print(f"{key} = {value[:50]}..." if len(value) > 50 else f"{key} = {value}")

print("\n=== Discord 相關變數 ===")
discord_found = False
for key, value in os.environ.items():
    if 'DISCORD' in key.upper() or 'BOT' in key.upper() or 'TOKEN' in key.upper():
        print(f"✓ {key} = {value[:15]}...")
        discord_found = True

if not discord_found:
    print("❌ 未找到任何Discord相關的環境變數")

print("\n=== 檢查完成 ===") 