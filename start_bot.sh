#!/bin/bash

# Artale Market Discord Bot 啟動腳本

echo "🎮 Artale Market Discord Bot 啟動程式"
echo "======================================"

# 檢查虛擬環境是否存在
if [ ! -d "venv" ]; then
    echo "⚠️  未找到虛擬環境，正在創建..."
    python3 -m venv venv
    echo "✅ 虛擬環境創建完成"
fi

# 激活虛擬環境
echo "🔧 激活虛擬環境..."
source venv/bin/activate

# 檢查並安裝依賴
echo "📦 檢查依賴套件..."
pip install -r requirements.txt

# 檢查.env文件是否存在
if [ ! -f ".env" ]; then
    echo "⚠️  未找到 .env 文件"
    echo "請創建 .env 文件並添加您的 Discord Bot Token:"
    echo ""
    echo "DISCORD_BOT_TOKEN=your_discord_bot_token_here"
    echo ""
    echo "如何獲取 Discord Bot Token:"
    echo "1. 前往 https://discord.com/developers/applications"
    echo "2. 創建新應用程式或選擇現有應用程式"
    echo "3. 在左側選單中選擇 'Bot'"
    echo "4. 點擊 'Add Bot' 創建機器人"
    echo "5. 複製 Bot Token 並貼到 .env 文件中"
    echo ""
    exit 1
fi

# 運行測試
echo "🧪 運行功能測試..."
python test_bot.py

echo ""
echo "🚀 啟動 Discord 機器人..."
echo "按 Ctrl+C 停止機器人"
echo ""

# 啟動機器人
python main.py 