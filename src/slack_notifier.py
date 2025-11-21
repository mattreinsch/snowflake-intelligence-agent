"""
Slack Notifier Utility

This module provides a lightweight abstraction for Slack notifications.
Inside Snowflake Notebooks, external web requests are not allowed,
so this class gracefully falls back to simulation mode.

In production, you can enable real Slack webhook posting by setting:
    export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/XXXX/YYY/ZZZ"
"""

import os
import json
try:
    import requests  # Optional for real environments
except ImportError:
    requests = None


class SlackNotifier:
    def __init__(self):
        """
        Initialize the Slack notifier.

        If SLACK_WEBHOOK_URL is not set, the notifier runs in simulation mode,
        printing messages instead of sending them.
        """
        self.webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

    def send_notification(self, message: str):
        """
        Sends a notification to Slack via webhook.
        Falls back to simulation mode inside Snowflake.

        Parameters:
            message (str): The message text to send.
        """

        # Simulation mode (default for Snowflake Notebooks)
        if not self.webhook_url:
            print("SLACK_WEBHOOK_URL not set — Simulating Slack Notification:")
            print(f"[SLACK SIMULATION] {message}")
            return

        # Real webhook mode (for external environments)
        if requests is None:
            print("Requests library not available — cannot send real Slack messages.")
            print(f"[SLACK SIMULATION] {message}")
            return

        payload = {"text": message}

        try:
            response = requests.post(self.webhook_url, json=payload)
            if response.status_code == 200:
                print("Slack notification sent successfully.")
            else:
                print(f"Slack webhook error: {response.status_code} — {response.text}")

        except Exception as e:
            print("Exception occurred while sending Slack message:")
            print(str(e))
            print(f"[SLACK SIMULATION] {message}")
