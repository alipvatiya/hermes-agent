#!/bin/bash

# Telegram Bot Deployment Script for Hermes Agent
# Usage: ./deploy-telegram.sh TOKEN [CHAT_ID]

set -e

BOT_TOKEN="${1}"
HOME_CHAT="${2}"
ENV_FILE=".env"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# Validate token
if [ -z "$BOT_TOKEN" ]; then
    print_header "Telegram Bot Deployment for Hermes Agent"
    print_error "Bot token is required!"
    echo ""
    echo "Usage:"
    echo "  ./deploy-telegram.sh YOUR_BOT_TOKEN [HOME_CHAT_ID]"
    echo ""
    echo "Example:"
    echo "  ./deploy-telegram.sh 123456:ABCxyz123"
    echo "  ./deploy-telegram.sh 123456:ABCxyz123 -1001234567890"
    echo ""
    echo "Get token from: https://t.me/botfather"
    exit 1
fi

print_header "Telegram Bot Deployment"

# Validate token format
if [[ ! "$BOT_TOKEN" =~ ^[0-9]+:[A-Za-z0-9_-]+$ ]]; then
    print_error "Invalid token format!"
    echo "Token should be: numbers:letters-numbers-underscore-dash"
    exit 1
fi

print_info "Token format: Valid ✓"

# Test token with curl (if available)
if command -v curl &> /dev/null; then
    print_info "Testing token connectivity..."
    RESPONSE=$(curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getMe" || echo "")
    
    if echo "$RESPONSE" | grep -q '"ok":true'; then
        BOT_NAME=$(echo "$RESPONSE" | grep -o '"username":"[^"]*' | cut -d'"' -f4)
        print_success "Token is valid! Bot: @${BOT_NAME}"
    else
        print_info "Could not verify token (network issue or invalid token)"
    fi
fi

# Create/update .env file
print_info "Setting up environment file: ${ENV_FILE}"

cat > "$ENV_FILE" << EOF
# Hermes Agent - Telegram Configuration
# Generated: $(date)

# Required
TELEGRAM_BOT_TOKEN=${BOT_TOKEN}

# Optional
TELEGRAM_REQUIRE_MENTION=false
TELEGRAM_REPLY_TO_MODE=first
GROUP_SESSIONS_PER_USER=true
THREAD_SESSIONS_PER_USER=false
EOF

if [ -n "$HOME_CHAT" ]; then
    echo "TELEGRAM_HOME_CHANNEL=${HOME_CHAT}" >> "$ENV_FILE"
    print_success "Home channel configured: ${HOME_CHAT}"
fi

print_success ".env file created"

# Check for docker
if command -v docker-compose &> /dev/null; then
    print_info "Docker Compose found!"
    
    read -p "$(echo -e ${YELLOW})Start with docker-compose? (y/n): $(echo -e ${NC})" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Starting Hermes Gateway with Docker..."
        docker-compose up -d
        print_success "Gateway started!"
        echo ""
        echo "View logs:"
        echo "  docker-compose logs -f"
        echo ""
        echo "Stop gateway:"
        echo "  docker-compose down"
        exit 0
    fi
fi

# Check for Python
if command -v python3 &> /dev/null; then
    print_info "Python3 found!"
    
    read -p "$(echo -e ${YELLOW})Start with Python? (y/n): $(echo -e ${NC})" -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        print_info "Starting Hermes Gateway..."
        source "$ENV_FILE"
        python3 -m gateway.run
        exit 0
    fi
fi

# Manual instructions
print_header "Setup Complete"
print_success "Environment file: ${ENV_FILE}"
echo ""
echo "Next steps:"
echo "  1. Review configuration:"
echo "     cat ${ENV_FILE}"
echo ""
echo "  2. Start gateway (choose one):"
echo "     Option A (Docker):"
echo "       docker-compose up -d"
echo ""
echo "     Option B (Python):"
echo "       source ${ENV_FILE}"
echo "       python3 -m gateway.run"
echo ""
echo "     Option C (Hermes CLI):"
echo "       source ${ENV_FILE}"
echo "       hermes gateway run"
echo ""
echo "  3. Test in Telegram:"
echo "     Send a message to @${BOT_TOKEN%%:*} or search by @BotFather"
echo ""
print_success "Ready to deploy!"
