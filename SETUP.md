# Artale Market Discord Bot 設置指南

## 📋 環境需求

- Python 3.8 或更高版本
- 穩定的網路連接
- Discord 開發者帳號

## 🚀 快速開始

### 1. 創建 Discord 應用程式

1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 點擊 **"New Application"** 創建新應用程式
3. 輸入應用程式名稱（例如：Artale Market Bot）
4. 點擊 **"Create"**

### 2. 設置機器人

1. 在左側選單中點擊 **"Bot"**
2. 點擊 **"Add Bot"** 創建機器人
3. 自定義機器人設置：
   - **Username**: 設置機器人名稱
   - **Avatar**: 上傳機器人頭像（可選）
4. 在 **"Token"** 部分點擊 **"Copy"** 複製 Bot Token

⚠️ **重要**: Bot Token 是敏感信息，請妥善保管，不要分享給他人

### 3. 設置機器人權限

在 **"Bot"** 頁面中，確保以下設置：

- ✅ **Message Content Intent** - 開啟
- ✅ **Server Members Intent** - 開啟（可選）
- ✅ **Presence Intent** - 開啟（可選）

### 4. 邀請機器人到伺服器

1. 在左側選單中點擊 **"OAuth2"** > **"URL Generator"**
2. 在 **"Scopes"** 中勾選：
   - ✅ `bot`
   - ✅ `applications.commands`
3. 在 **"Bot Permissions"** 中勾選：
   - ✅ Send Messages
   - ✅ Embed Links
   - ✅ Read Message History
   - ✅ Use Slash Commands
4. 複製生成的 URL 並在瀏覽器中打開
5. 選擇要邀請機器人的伺服器
6. 點擊 **"Authorize"**

## 💻 本地設置

### 方法1：使用自動化腳本（推薦）

```bash
# 1. 下載專案
git clone <repository-url>
cd maple_story_robots

# 2. 創建 .env 文件
echo "DISCORD_BOT_TOKEN=your_bot_token_here" > .env

# 3. 運行啟動腳本
./start_bot.sh
```

### 方法2：手動設置

```bash
# 1. 創建虛擬環境
python3 -m venv venv

# 2. 激活虛擬環境
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 創建環境變數文件
cp .env.example .env
# 編輯 .env 文件，添加你的 Bot Token

# 5. 測試功能
python test_bot.py

# 6. 啟動機器人
python main.py
```

## 🔧 環境變數設置

創建 `.env` 文件並添加以下內容：

```env
# Discord Bot Token（必需）
DISCORD_BOT_TOKEN=your_discord_bot_token_here

# 可選設置
DEBUG=false
COMMAND_PREFIX=!
```

### 獲取 Discord Bot Token：

1. 在 [Discord Developer Portal](https://discord.com/developers/applications) 中選擇你的應用程式
2. 點擊左側的 **"Bot"**
3. 在 **"Token"** 部分點擊 **"Copy"**
4. 將 Token 貼到 `.env` 文件中

## 🧪 測試機器人

### 本地測試

```bash
# 激活虛擬環境
source venv/bin/activate

# 運行測試
python test_bot.py
```

### Discord 測試

1. 確保機器人已在你的伺服器中
2. 在 Discord 中嘗試以下指令：

```
# 標記機器人查詢價格
@機器人名稱 楓葉

# 使用指令查詢
!price 頭盔
!p 藥水

# 查看幫助
!help
```

## 📊 功能說明

### 價格查詢

- **標記機器人**: `@機器人名稱 道具名稱`
- **指令查詢**: `!price 道具名稱` 或 `!p 道具名稱`

### 支援的道具類型

- 🍁 材料：楓葉、礦石等
- ⚔️ 裝備：武器、頭盔、盔甲、飾品等
- 🧪 消耗品：藥水等
- 📜 道具：卷軸等
- 🐕 寵物
- 🐎 坐騎

### 其他指令

- `!help` - 顯示幫助信息
- `!幫助` - 顯示幫助信息（中文）

## 🔧 故障排除

### 常見問題

#### Q: 機器人無法啟動
- 檢查 Python 版本是否為 3.8+
- 確認已安裝所有依賴包
- 檢查 Bot Token 是否正確設置

#### Q: 機器人無法回應
- 確認機器人已被邀請到伺服器
- 檢查機器人權限設置
- 確認 Message Content Intent 已開啟

#### Q: 無法查詢價格
- 檢查網路連接
- 確認 Artale Market 網站是否正常
- 檢查道具名稱拼寫

#### Q: 權限錯誤
- 確認機器人有 "Send Messages" 權限
- 檢查頻道權限設置
- 重新邀請機器人並確認權限

### 日誌檢查

機器人運行時會在控制台顯示日誌信息：

```bash
# 正常啟動日誌
Bot_Username#1234 已成功連接到Discord!
機器人ID: 123456789012345678
機器人已準備就緒!
```

### 聯繫支援

如果遇到其他問題：

1. 檢查 [Discord.py 文檔](https://discordpy.readthedocs.io/)
2. 查看專案的 Issues 頁面
3. 提交新的 Issue 並描述問題

## 🛡️ 安全注意事項

1. **絕不分享 Bot Token**
2. **不要將 .env 文件提交到版本控制**
3. **定期更新依賴包**
4. **使用最小權限原則**

## 📝 授權條款

此專案採用 MIT 授權條款，詳見 LICENSE 文件。

## 🙏 免責聲明

- 此機器人僅供學習和個人使用
- 價格信息僅供參考，不保證準確性
- 作者不對任何交易損失負責
- 請遵守 Discord 和 Artale Market 的使用條款 