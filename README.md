# Artale Market Discord Bot

一個用於查詢楓之谷 Artale 道具價格的 Discord 機器人，數據來源於 [Artale Market](https://artale-market.org)。

## 功能特色

- 🔍 **快速查價**: 標記機器人並輸入道具名稱即可查詢價格
- 💰 **即時更新**: 從 Artale Market 獲取最新價格信息
- 📊 **價格趨勢**: 顯示道具價格變化趨勢
- 🎯 **智能搜尋**: 支援模糊搜尋和關鍵字匹配
- 🎨 **美觀界面**: 使用 Discord Embed 呈現資訊

## 使用方法

### 方法1：標記機器人
```
@機器人名稱 楓葉
@機器人名稱 頭盔
@機器人名稱 藥水
```

### 方法2：使用指令
```
!price 楓葉
!p 頭盔
!價格 藥水
```

### 其他指令
```
!help      - 顯示幫助信息
!幫助      - 顯示幫助信息
```

## 安裝和設置

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 創建 Discord 應用程式
1. 前往 [Discord Developer Portal](https://discord.com/developers/applications)
2. 點擊 "New Application" 創建新應用程式
3. 在左側選單選擇 "Bot"
4. 點擊 "Add Bot" 創建機器人
5. 複製 Bot Token

### 3. 設置環境變數
創建 `.env` 文件：
```env
DISCORD_BOT_TOKEN=your_discord_bot_token_here
```

### 4. 邀請機器人到伺服器
1. 在 Discord Developer Portal 中選擇 "OAuth2" > "URL Generator"
2. 勾選 "bot" 和 "applications.commands"
3. 在 Bot Permissions 中選擇以下權限：
   - Send Messages
   - Use Slash Commands
   - Embed Links
   - Read Message History
4. 複製生成的 URL 並在瀏覽器中打開
5. 選擇要邀請機器人的伺服器

### 5. 啟動機器人
```bash
python main.py
```

## 所需權限

機器人需要以下 Discord 權限：
- 發送訊息 (Send Messages)
- 嵌入連結 (Embed Links)
- 讀取訊息歷史 (Read Message History)
- 使用斜線指令 (Use Slash Commands)

## 技術架構

- **程式語言**: Python 3.8+
- **Discord API**: discord.py
- **網頁爬蟲**: requests + BeautifulSoup
- **數據來源**: Artale Market API/網站

## 項目結構

```
maple_story_robots/
├── main.py              # 主程式文件
├── requirements.txt     # Python 依賴包
├── README.md           # 說明文件
└── .env                # 環境變數 (需自行創建)
```

## 故障排除

### 常見問題

**Q: 機器人無法回應**
- 檢查 Bot Token 是否正確
- 確認機器人已被邀請到伺服器
- 檢查機器人是否有足夠的權限

**Q: 無法獲取價格信息**
- 檢查網路連接
- 確認 Artale Market 網站是否正常運行
- 檢查道具名稱拼寫是否正確

**Q: 機器人離線**
- 檢查程式是否正在運行
- 查看控制台錯誤訊息
- 確認 Token 沒有過期

## 開發說明

### 環境設置
```bash
# 克隆專案
git clone <repository-url>
cd maple_story_robots

# 安裝依賴
pip install -r requirements.txt

# 設置環境變數
cp .env.example .env
# 編輯 .env 文件並填入你的 Bot Token
```

### 自定義功能
你可以修改 `main.py` 中的 `ArtaleMarketBot` 類別來添加更多功能：
- 修改搜尋算法
- 添加價格提醒功能
- 支援更多道具類別
- 增加數據分析功能

## 注意事項

1. 請遵守 Discord 的服務條款和 API 使用政策
2. 不要濫用 Artale Market 的 API，避免過於頻繁的請求
3. 機器人 Token 是敏感信息，請妥善保管，不要公開分享
4. 定期更新依賴包以確保安全性

## 貢獻

歡迎提交 Issue 和 Pull Request 來改進這個專案！

## 授權

此專案採用 MIT 授權條款。

## 免責聲明

此機器人僅供學習和個人使用，價格信息僅供參考。作者不對任何交易損失負責。 