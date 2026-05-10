#!/usr/bin/env python3
"""
Telegram Bot Setup Script for Hermes Agent
Quickly configure and start Telegram bot adapter
"""

import os
import sys
import argparse
from pathlib import Path
import subprocess
import json
from typing import Optional

def setup_env_file(token: str, home_channel: Optional[str] = None, output_file: str = ".env") -> bool:
    """Setup .env file with Telegram configuration"""
    try:
        env_content = f"""# Hermes Agent - Telegram Configuration
# Auto-generated: {__import__('datetime').datetime.now().isoformat()}

TELEGRAM_BOT_TOKEN={token}
"""
        if home_channel:
            env_content += f"TELEGRAM_HOME_CHANNEL={home_channel}\n"
        
        env_content += """TELEGRAM_REQUIRE_MENTION=false
TELEGRAM_REPLY_TO_MODE=first
GROUP_SESSIONS_PER_USER=true
THREAD_SESSIONS_PER_USER=false
"""
        
        with open(output_file, 'w') as f:
            f.write(env_content)
        
        print(f"✅ Environment file created: {output_file}")
        return True
    except Exception as e:
        print(f"❌ Error creating env file: {e}")
        return False

def test_token(token: str) -> bool:
    """Test if token is valid by making a simple API call"""
    try:
        import requests
        response = requests.get(
            f"https://api.telegram.org/bot{token}/getMe",
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data.get('result', {})
                print(f"\n✅ Token is VALID!")
                print(f"   Bot Username: @{bot_info.get('username')}")
                print(f"   Bot ID: {bot_info.get('id')}")
                print(f"   Bot Name: {bot_info.get('first_name')}\n")
                return True
        else:
            print(f"❌ Invalid token (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Could not test token: {e}")
        print("   (This might be OK if no internet connection)")
        return False

def start_gateway() -> bool:
    """Start Hermes gateway with Telegram bot"""
    try:
        print("\n🚀 Starting Hermes Gateway with Telegram bot...\n")
        
        # Try different ways to start
        commands = [
            ["python3", "-m", "gateway.run"],
            ["python", "-m", "gateway.run"],
            ["hermes", "gateway", "run"],
        ]
        
        for cmd in commands:
            try:
                subprocess.run(cmd, check=False)
                return True
            except FileNotFoundError:
                continue
        
        print("❌ Could not start gateway. Please start manually:")
        print("   python3 -m gateway.run")
        return False
    except Exception as e:
        print(f"❌ Error starting gateway: {e}")
        return False

def check_dependencies() -> bool:
    """Check if required dependencies are available"""
    try:
        import telegram
        return True
    except ImportError:
        print("⚠️  Optional: Install python-telegram-bot for better compatibility")
        print("   pip install python-telegram-bot")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Setup Telegram bot for Hermes Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 setup-telegram.py YOUR_BOT_TOKEN
  python3 setup-telegram.py YOUR_BOT_TOKEN --home-chat-id -1001234567890
  python3 setup-telegram.py YOUR_BOT_TOKEN --start
  python3 setup-telegram.py YOUR_BOT_TOKEN --test-only
        """
    )
    
    parser.add_argument("token", help="Telegram bot token from @BotFather")
    parser.add_argument("--home-chat-id", help="Default chat ID for home channel")
    parser.add_argument("--output", default=".env", help="Output .env file (default: .env)")
    parser.add_argument("--start", action="store_true", help="Start gateway after setup")
    parser.add_argument("--test-only", action="store_true", help="Only test token, don't setup")
    parser.add_argument("--docker", action="store_true", help="Use docker-compose to start")
    
    args = parser.parse_args()
    
    # Validate token format
    if not args.token or ':' not in args.token:
        print("❌ Invalid token format. Token should contain ':' (e.g., 123456:ABCxyz)")
        sys.exit(1)
    
    print("=" * 60)
    print("Telegram Bot Setup for Hermes Agent")
    print("=" * 60)
    
    # Test token
    print(f"\n🔍 Testing bot token...")
    if not test_token(args.token):
        if not args.test_only:
            response = input("⚠️  Token test failed. Continue anyway? (y/n): ").lower()
            if response != 'y':
                print("❌ Setup cancelled.")
                sys.exit(1)
    
    if args.test_only:
        print("✅ Token test completed.")
        sys.exit(0)
    
    # Setup env file
    print(f"\n📝 Setting up environment file...")
    if not setup_env_file(args.token, args.home_chat_id, args.output):
        print("❌ Setup failed!")
        sys.exit(1)
    
    # Show configuration
    print(f"\n📋 Configuration:")
    print(f"   Token: {args.token[:20]}...")
    if args.home_chat_id:
        print(f"   Home Channel: {args.home_chat_id}")
    print(f"   Output file: {args.output}")
    
    # Check dependencies
    print(f"\n📦 Checking dependencies...")
    check_dependencies()
    
    # Start if requested
    if args.start:
        print(f"\n💾 Loading configuration from {args.output}...")
        
        if args.docker:
            print(f"\n🐳 Starting with Docker Compose...")
            try:
                subprocess.run(["docker-compose", "up", "-d"], check=True)
                print("✅ Docker container started!")
                print("   View logs: docker-compose logs -f")
            except Exception as e:
                print(f"❌ Docker start failed: {e}")
                print("   Try: docker-compose up -d")
        else:
            if not start_gateway():
                print("\n📖 Manual startup guide:")
                print(f"   1. source {args.output}  (if not using docker)")
                print("   2. python3 -m gateway.run")
    else:
        print(f"\n✅ Setup complete!")
        print(f"\n📖 Next steps:")
        print(f"   1. Verify .env file: cat {args.output}")
        print(f"   2. Start gateway: python3 -m gateway.run")
        print(f"      Or with Docker: docker-compose up -d")
        print(f"   3. Send a message to your bot on Telegram!")
    
    print("\n" + "=" * 60)
    print("✨ Telegram bot is ready!")
    print("=" * 60)

if __name__ == "__main__":
    main()
