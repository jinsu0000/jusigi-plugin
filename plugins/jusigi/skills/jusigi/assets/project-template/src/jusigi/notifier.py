"""Optional Telegram notification without leaking configuration."""

from __future__ import annotations

import os


def notify(message: str) -> bool:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False
    import requests

    response = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={"chat_id": chat_id, "text": message[:3900]},
        timeout=15,
    )
    response.raise_for_status()
    return True
