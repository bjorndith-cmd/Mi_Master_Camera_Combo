#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mi Master Camera Combo - Telegram Broadcast Tool
Author: borndead
Usage:
    python tools/send_telegram_post.py --type announcement
    python tools/send_telegram_post.py --type release --tag v5.8 --title "Release v5.8" --notes "Changelog..."
"""

import os
import sys
import argparse
import urllib.request
import urllib.error
import json

def normalize_chat_id(chat_id):
    """Normalize chat_id from URL or plain string to Telegram @username format."""
    if not chat_id:
        return "@Mi_Master_Camera_Combo"
    chat_id = chat_id.strip().strip("'\"")
    if chat_id.startswith("https://t.me/"):
        chat_id = "@" + chat_id.replace("https://t.me/", "").strip("/")
    elif chat_id.startswith("t.me/"):
        chat_id = "@" + chat_id.replace("t.me/", "").strip("/")
    elif not chat_id.startswith("@") and not chat_id.startswith("-"):
        chat_id = "@" + chat_id
    return chat_id

def send_telegram_photo(bot_token, chat_id, photo_path, caption):
    """Send photo with caption via Telegram Bot API using multipart/form-data."""
    url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    
    with open(photo_path, "rb") as f:
        file_bytes = f.read()
    
    filename = os.path.basename(photo_path)
    
    body = bytearray()
    # chat_id
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="chat_id"\r\n\r\n{chat_id}\r\n'.encode("utf-8"))
    # parse_mode
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend('Content-Disposition: form-data; name="parse_mode"\r\n\r\nHTML\r\n'.encode("utf-8"))
    # caption
    if caption:
        body.extend(f"--{boundary}\r\n".encode("utf-8"))
        body.extend(f'Content-Disposition: form-data; name="caption"\r\n\r\n{caption}\r\n'.encode("utf-8"))
    # photo file
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(f'Content-Disposition: form-data; name="photo"; filename="{filename}"\r\n'.encode("utf-8"))
    body.extend(b'Content-Type: image/jpeg\r\n\r\n')
    body.extend(file_bytes)
    body.extend(b'\r\n')
    body.extend(f"--{boundary}--\r\n".encode("utf-8"))
    
    req = urllib.request.Request(url, data=bytes(body))
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")
    
    try:
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            if res_data.get("ok"):
                print("[SUCCESS] Photo sent to Telegram successfully!")
                return True
            else:
                print(f"[ERROR] Telegram API error: {res_data}")
                return False
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        print(f"[ERROR] Telegram HTTP {e.code}: {err_msg}")
        if e.code == 403:
            print("[HINT] 403 Forbidden: The Bot is NOT an Administrator of the channel or lacks 'Post messages' permission!")
        elif e.code == 400:
            print(f"[HINT] 400 Bad Request: Check chat_id format '{chat_id}' or HTML formatting.")
        elif e.code == 401:
            print("[HINT] 401 Unauthorized: TELEGRAM_BOT_TOKEN is incorrect or revoked.")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to send photo: {e}")
        return False

def send_telegram_message(bot_token, chat_id, text):
    """Send text message via Telegram Bot API."""
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            res_data = json.loads(resp.read().decode("utf-8"))
            if res_data.get("ok"):
                print("[SUCCESS] Message sent to Telegram successfully!")
                return True
            else:
                print(f"[ERROR] Telegram API error: {res_data}")
                return False
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        print(f"[ERROR] Telegram HTTP {e.code}: {err_msg}")
        if e.code == 403:
            print("[HINT] 403 Forbidden: The Bot is NOT an Administrator of the channel or lacks 'Post messages' permission!")
        elif e.code == 400:
            print(f"[HINT] 400 Bad Request: Check chat_id format '{chat_id}' or HTML formatting.")
        elif e.code == 401:
            print("[HINT] 401 Unauthorized: TELEGRAM_BOT_TOKEN is incorrect or revoked.")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to send message: {e}")
        return False

def get_announcement_text():
    return (
        "📸 <b>Xiaomi Master Camera Combo — Официальный канал проекта</b> ⚡\n\n"
        "Добро пожаловать в официальное сообщество флагманского модульного комплекса "
        "для камер <b>Xiaomi Leica</b>!\n\n"
        "🎯 <b>Поддерживаемые устройства:</b>\n"
        "• <b>Xiaomi 13 Ultra</b> (<code>ishtar</code>) — 1\" IMX989 + 3x IMX858 (Quad-50M, A14 HOS 1.0 & A15/16 HOS 2/3)\n"
        "• <b>Xiaomi 15</b> (<code>dada</code>) & <b>15 Pro</b> (<code>haotian</code>) — Light Hunter 900\n"
        "• <b>Xiaomi 15 Ultra</b> (<code>xuanyuan</code>) — 1\" LYT-900 + HP9 200M (Stock AIO 104)\n"
        "• <b>Xiaomi 17 Ultra</b> (<code>nezha</code>) — 1\" OVX10500U + HP9 200M (Фикс SimpleRom ST)\n\n"
        "✨ <b>Ключевые возможности:</b>\n"
        "✅ <b>Аппаратный DCG / iDCG HDR</b> (считывание с 1 кадра, ноль смазов)\n"
        "✅ <b>50Мп / 200Мп RAW16</b> для стока и Google Камеры (AGC 9.6)\n"
        "✅ <b>George Video MOD</b> (8K 24fps со всех камер, 4K120fps, чистый AISP)\n"
        "✅ Готовые авторские <b>пресеты конфигураций .agc</b>\n"
        "✅ Скрипт автодиагностики <code>check_support.sh</code>\n\n"
        "🔗 <b>Полезные ссылки:</b>\n"
        "🌐 <a href=\"https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo\">Репозиторий на GitHub</a>\n"
        "📦 <a href=\"https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo/tree/main/releases\">Каталог модулей Releases</a>\n"
        "⚙️ <a href=\"https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo/tree/main/configs\">Готовые AGC конфиги</a>\n"
        "💬 <b>Канал и чат:</b> @Mi_Master_Camera_Combo"
    )

def get_release_text(tag, title, notes):
    header = f"🚀 <b>Новый релиз: {title or tag}</b> ⚡\n\n"
    body = ""
    if notes:
        body = f"📝 <b>Что нового:</b>\n{notes}\n\n"
    footer = (
        "📦 <b>Файлы релиза доступны на GitHub:</b>\n"
        f"👉 <a href=\"https://github.com/bjorndith-cmd/Mi_Master_Camera_Combo/releases\">Скачать обновление</a>\n\n"
        "💬 <b>Обсуждение в чате:</b> @Mi_Master_Camera_Combo"
    )
    return header + body + footer

def main():
    parser = argparse.ArgumentParser(description="Send updates to Telegram Channel")
    parser.add_argument("--type", choices=["announcement", "release", "custom"], default="announcement")
    parser.add_argument("--tag", default="")
    parser.add_argument("--title", default="")
    parser.add_argument("--notes", default="")
    parser.add_argument("--text", default="")
    parser.add_argument("--photo", default="assets/LOGO.jpg")
    args = parser.parse_args()

    raw_token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    raw_chat = os.environ.get("TELEGRAM_CHAT_ID", "@Mi_Master_Camera_Combo")

    bot_token = raw_token.strip().strip("'\"")
    chat_id = normalize_chat_id(raw_chat)

    if not bot_token:
        print("[FATAL] TELEGRAM_BOT_TOKEN secret/environment variable is empty!")
        print("Please add TELEGRAM_BOT_TOKEN in GitHub Settings -> Secrets -> Actions.")
        sys.exit(1)

    print(f"[INFO] Target Telegram Chat ID: {chat_id}")

    # Determine photo path
    photo_path = args.photo
    if not os.path.isabs(photo_path):
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        photo_path = os.path.join(root_dir, args.photo)

    if args.type == "announcement":
        content = get_announcement_text()
    elif args.type == "release":
        content = get_release_text(args.tag, args.title, args.notes)
    else:
        content = args.text or "⚡ <b>Обновление Mi Master Camera Combo</b>"

    success = False
    if os.path.exists(photo_path):
        print(f"[INFO] Photo found at {photo_path}, sending with photo...")
        if len(content) <= 1000:
            success = send_telegram_photo(bot_token, chat_id, photo_path, caption=content)
        else:
            short_caption = "📸 <b>Xiaomi Master Camera Combo</b> ⚡\n<i>Официальное обновление проекта</i>"
            p_ok = send_telegram_photo(bot_token, chat_id, photo_path, caption=short_caption)
            m_ok = send_telegram_message(bot_token, chat_id, content)
            success = p_ok or m_ok

        # If sending photo failed, attempt fallback to text-only
        if not success:
            print("[WARN] Photo send failed. Trying text-only fallback...")
            success = send_telegram_message(bot_token, chat_id, content)
    else:
        print("[INFO] Photo not found, sending text-only message...")
        success = send_telegram_message(bot_token, chat_id, content)

    if not success:
        print("[FATAL] Message delivery to Telegram failed. See error log above.")
        sys.exit(1)
    else:
        print("[SUCCESS] All messages delivered successfully!")

if __name__ == "__main__":
    main()
