#!/usr/bin/env python3
"""
Send a message to a Webex space as a bot.

Requires env vars:
  WEBEX_BOT_TOKEN
  WEBEX_ROOM_ID
"""

import argparse
import os
import sys
import requests

API = "https://webexapis.com/v1/messages"


def post_message(text: str) -> None:
    token = os.environ.get("WEBEX_BOT_TOKEN")
    room = os.environ.get("WEBEX_ROOM_ID")
    if not token or not room:
        raise SystemExit("WEBEX_BOT_TOKEN and WEBEX_ROOM_ID must be set")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"roomId": room, "markdown": text}
    r = requests.post(API, json=payload, headers=headers, timeout=15)
    r.raise_for_status()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--status", choices=["success", "failure", "unstable"], required=True)
    p.add_argument("--build-url", required=True)
    p.add_argument("--tests", default="")
    p.add_argument("--error", default="")
    a = p.parse_args()

    icon = {"success": "✅", "failure": "❌", "unstable": "⚠️"}[a.status]
    lines = [
        f"**Jenkins Build: {a.status.upper()} {icon}**",
        f"[Open build]({a.build_url})",
    ]
    if a.tests:
        lines.append(f"Tests: `{a.tests}`")
    if a.error:
        lines.append("\n```")
        lines.append(a.error[:1500])
        lines.append("```")

    post_message("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except requests.HTTPError as e:
        print("[webex] POST failed:", e, file=sys.stderr)
        sys.exit(0)
