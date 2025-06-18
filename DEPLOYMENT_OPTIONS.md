# Discord Bot 部署選項

## 🚀 推薦部署平台

### 1. **Render** (最推薦)
**優點：**
- ✅ 完全免費
- ✅ 24/7運行，無sleep
- ✅ 自動部署
- ✅ 環境變數設定簡單
- ✅ 對Discord bot支援完美

**部署步驟：**
1. 前往 [render.com](https://render.com)
2. 連接GitHub帳號
3. 選擇 "New Worker Service"
4. 選擇你的repo: `artale_market_robot`
5. 設定：
   - **Name**: `artale-market-bot`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
6. 在Environment Variables添加：
   - `DISCORD_BOT_TOKEN` = `你的Discord token`
7. 點擊 "Create Worker Service"

---

### 2. **Fly.io** (技術派推薦)
**優點：**
- ✅ 全球CDN
- ✅ 每月免費額度充足
- ✅ 超快部署速度
- ✅ 支援多區域

**部署步驟：**
1. 安裝Fly CLI:
   ```bash
   # macOS
   brew install flyctl
   
   # 或直接下載
   curl -L https://fly.io/install.sh | sh
   ```

2. 登入並初始化：
   ```bash
   fly auth login
   cd /path/to/your/project
   fly launch
   ```

3. 設定環境變數：
   ```bash
   fly secrets set DISCORD_BOT_TOKEN="你的Discord token"
   ```

4. 部署：
   ```bash
   fly deploy
   ```

---

### 3. **Replit** (最簡單)
**優點：**
- ✅ 零配置
- ✅ 線上IDE
- ✅ 即時編輯
- ⚠️ 免費版會sleep

**部署步驟：**
1. 前往 [replit.com](https://replit.com)
2. 點擊 "Create Repl"
3. 選擇 "Import from GitHub"
4. 輸入你的repo URL
5. 在Secrets添加 `DISCORD_BOT_TOKEN`
6. 點擊Run按鈕

---

### 4. **Heroku** (經典選擇)
**優點：**
- ✅ 成熟穩定
- ✅ 豐富插件
- ⚠️ 免費版有限制

**部署步驟：**
1. 安裝Heroku CLI
2. 登入：`heroku login`
3. 創建應用：`heroku create artale-market-bot`
4. 設定環境變數：
   ```bash
   heroku config:set DISCORD_BOT_TOKEN="你的token"
   ```
5. 部署：
   ```bash
   git push heroku main
   ```

---

## 🏆 平台比較

| 平台 | 免費額度 | 24/7運行 | 自動部署 | 設定難度 | 推薦度 |
|------|----------|----------|----------|----------|---------|
| **Render** | ✅ 無限制 | ✅ 是 | ✅ 是 | ⭐ 簡單 | 🏆 最推薦 |
| **Fly.io** | ✅ 充足 | ✅ 是 | ✅ 是 | ⭐⭐ 中等 | 🥈 技術派 |
| **Railway** | ✅ 有限 | ✅ 是 | ✅ 是 | ⭐ 簡單 | ⚠️ 環境變數問題 |
| **Replit** | ⚠️ 會sleep | ❌ 否 | ✅ 是 | ⭐ 最簡單 | 🥉 入門用 |
| **Heroku** | ⚠️ 會sleep | ❌ 否 | ✅ 是 | ⭐⭐ 中等 | 📝 備選 |

---

## 🎯 我的建議

1. **新手 → Render**: 最簡單，完全免費，無限制
2. **進階 → Fly.io**: 更多控制權，全球部署
3. **測試 → Replit**: 快速測試，線上編輯
4. **備用 → Heroku**: 老牌穩定，但有限制

---

## 💡 小貼士

1. **環境變數問題**: 如果某平台的環境變數有問題，可以考慮直接把token加密後寫在代碼裡
2. **多平台部署**: 可以同時部署到多個平台作為備份
3. **監控**: 設定Discord webhook來監控bot狀態
4. **日誌**: 大部分平台都有日誌查看功能，方便debug

想要我幫你部署到哪個平台？我推薦先試試Render！ 