import random
import requests
import os
from dotenv import load_dotenv
from data import get_summary, get_expense_summary

# Load environment variables from .env
load_dotenv()

# Static fallback tips
SAVING_TIPS = [
    "Track your expenses daily to avoid surprises.",
    "Set a weekly food budget and stick to it.",
    "Pause non-essential subscriptions.",
    "Use a 24-hour rule before impulse purchases."
]

# API key for OpenRouter (Qwen model)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
QWEN_URL = "https://openrouter.ai/api/v1/chat/completions"

def get_ai_tip():
    """Fetches AI-powered tip based on summary and expense data using Qwen via OpenRouter."""
    summary_text = get_summary()
    expense_data = get_expense_summary()

    expense_breakdown = "\n".join([f"{cat}: RM{amt:.2f}" for cat, amt in expense_data.items()])

    prompt = (
        f"You are a financial advisor. Here is the user's budget summary:\n"
        f"{summary_text}\n\n"
        f"Expense breakdown:\n{expense_breakdown}\n\n"
        f"Based on this, provide 2-3 personalized budgeting tips."
    )

    # If API key missing, fallback to static tips
    if not OPENROUTER_API_KEY:
        return random.choice(SAVING_TIPS)

    try:
        response = requests.post(
            QWEN_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "qwen/qwen-2.5-7b-instruct",   # ✅ Qwen model
                "messages": [
                    {"role": "system", "content": "You are a helpful financial advisor."},
                    {"role": "user", "content": prompt}
                ]
            }
        )
        response.raise_for_status()
        data = response.json()
        print("DEBUG:", data)  # 👈 for testing, can remove later
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error fetching AI tip:", e)
        return random.choice(SAVING_TIPS)
