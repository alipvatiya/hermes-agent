# Telegram Bot - Quick Deploy Guide untuk Hermes Agent

## 📋 Panduan Cepat

Hermes Agent sudah memiliki support lengkap untuk Telegram! Berikut cara setup-nya:

### 1️⃣ **Dapatkan Bot Token dari BotFather**

1. Buka Telegram dan cari **@BotFather**
2. Kirim pesan `/newbot`
3. Ikuti instruksi untuk membuat bot baru
4. Copy token yang diberikan (format: `123456:ABCxyz...`)

### 2️⃣ **Setup Bot - Pilih Salah Satu:**

#### **Option A: Menggunakan Script Python (Recommended)**
```bash
python3 setup-telegram.py YOUR_BOT_TOKEN

# Dengan home channel (optional)
python3 setup-telegram.py YOUR_BOT_TOKEN --home-chat-id YOUR_CHAT_ID

# Setup dan langsung start
python3 setup-telegram.py YOUR_BOT_TOKEN --start
```

#### **Option B: Menggunakan Bash Script**
```bash
chmod +x deploy-telegram.sh
./deploy-telegram.sh YOUR_BOT_TOKEN

# Dengan home channel
./deploy-telegram.sh YOUR_BOT_TOKEN -1001234567890
```

#### **Option C: Manual Setup via .env**
```bash
# Copy template
cp .env.telegram .env

# Edit .env dan update:
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_HOME_CHANNEL=your_chat_id  # optional
```

### 3️⃣ **Mulai Gateway**

```bash
# Menggunakan Docker
docker-compose up -d
docker-compose logs -f

# Atau local Python
python3 -m gateway.run

# Atau menggunakan CLI
hermes gateway run
```

---

## 🎯 Konfigurasi Lanjutan

### Setup dengan Docker

```bash
# Create .env file
export TELEGRAM_BOT_TOKEN="your_token_here"

# Start with docker-compose
docker-compose up -d

# View logs
docker-compose logs -f telegram
```

### Setup di VPS/Cloud

```bash
# 1. SSH ke server
ssh user@your-vps.com

# 2. Clone repository
git clone https://github.com/yourusername/hermes-agent.git
cd hermes-agent

# 3. Setup environment
python3 setup-telegram.py YOUR_BOT_TOKEN --start

# 4. Keep running (gunakan tmux atau screen)
tmux new -s hermes python3 -m gateway.run
```

### Advanced Configuration

Edit `.env` untuk opsi lebih lanjut:

```env
# Bot Token (wajib)
TELEGRAM_BOT_TOKEN=123456:ABCxyz...

# Home Channel untuk /sethome command
TELEGRAM_HOME_CHANNEL=-1001234567890
TELEGRAM_HOME_CHANNEL_NAME=My Home

# Authorization
TELEGRAM_ALLOWED_USERS=12345,67890  # Hanya user ini bisa akses
TELEGRAM_REQUIRE_MENTION=false

# Group Settings  
TELEGRAM_REQUIRE_MENTION=true       # Require mention di groups
TELEGRAM_GROUP_ALLOWED_USERS=12345  # Specific users di groups

# Threading
TELEGRAM_REPLY_TO_MODE=first        # off/first/all

# Proxy (jika diperlukan)
TELEGRAM_PROXY=http://proxy:8080
```

---

## 📊 Status & Monitoring

```bash
# Check if bot is connected
hermes gateway status

# View real-time logs
docker-compose logs -f

# Send test message (dari Python)
python3 << 'EOF'
import os
from gateway.platforms.telegram import TelegramAdapter

token = os.getenv("TELEGRAM_BOT_TOKEN")
chat_id = os.getenv("TELEGRAM_HOME_CHANNEL")

if token and chat_id:
    # Bisa test message di sini
    print(f"Bot token: {token[:20]}...")
    print(f"Chat ID: {chat_id}")
EOF
```

---

## 🐛 Troubleshooting

### Bot tidak connect
```bash
# Test token validity
python3 setup-telegram.py YOUR_TOKEN --test-only

# Check logs
docker-compose logs | grep -i telegram
```

### "Invalid token"
- Pastikan token benar dari @BotFather
- Jangan ada spasi tambahan
- Buka @BotFather lagi jika lupa tokennya

### Bot tidak merespons di chat
1. Pastikan bot sudah di-add ke grup
2. Check TELEGRAM_REQUIRED_MENTION setting
3. Verify user ID di TELEGRAM_ALLOWED_USERS jika menggunakan whitelist
4. Lihat logs: `docker-compose logs -f`

### Connection timeout
```bash
# Jika punya proxy
export TELEGRAM_PROXY=http://your-proxy:port

# Atau gunakan fallback IPs
export TELEGRAM_FALLBACK_IPS=149.154.167.198,149.154.167.199
```

---

## 📱 Commands

Setelah bot aktif, user bisa gunakan:

```
/start - Info bot
/reset - Reset conversation
/new - New session  
/sethome - Set default delivery channel
/help - List commands
```

---

## 🔗 Links

- 📖 [Telegram Bot API Docs](https://core.telegram.org/bots)
- 🤖 [@BotFather](https://t.me/botfather) - Create bot
- 💬 [Hermes Docs](https://hermes-agent.nousresearch.com)

---

## ✅ Verifikasi Setup

Setelah deploy, test dengan:

1. **Text message**
   ```
   Hey @bot_name test
   ```

2. **Check response**
   - Bot seharusnya merespons

3. **Check logs**
   ```bash
   docker-compose logs --tail=50 | grep -i telegram
   ```

4. **Test dengan Python**
   ```python
   python3 setup-telegram.py YOUR_TOKEN --test-only
   ```

---

Semoga berhasil! 🚀 Jika ada masalah, buka issue di GitHub.
