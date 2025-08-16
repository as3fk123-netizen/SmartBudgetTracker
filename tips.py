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

# API key is now securely loaded from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

def get_ai_tip():
    """Fetches AI-powered tip based on summary and expense data."""
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
    if not GEMINI_API_KEY:
        return random.choice(SAVING_TIPS)

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Error fetching AI tip:", e)
        return random.choice(SAVING_TIPS)
