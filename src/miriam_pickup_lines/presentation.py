import time
import sys


def typewriter_effect(text, delay=0.05, end_with_newline=True):
    """Simulate typewriter effect - each character appears one by one"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    if end_with_newline:
        print()


def typing_with_pauses(text, delay=0.05, pause_chars=",.?!"):
    """Typewriter effect with dramatic pauses on punctuation"""
    for char in text:
        print(char, end="", flush=True)
        if char in pause_chars:
            time.sleep(delay * 10)  # Longer pause for drama
        else:
            time.sleep(delay)
    print()


def dramatic_pause(seconds):
    """Standard dramatic pause with dots"""
    for i in range(int(seconds)):
        print(".", end="", flush=True)
        time.sleep(1)
    print()


def present_miriam_wisdom(quote_data, interactive=False):
    """Main presentation function for Miriam's quotes"""
    print("=" * 60)
    print("💎 MIRIAM DEFENSOR SANTIAGO'S WISDOM")
    print("=" * 60)
    print()

    # Category and difficulty indicator
    category = quote_data["category"].upper()
    difficulty = quote_data["difficulty_level"]
    fire_level = "🔥" * min(difficulty // 2, 5)

    typewriter_effect(f"📂 CATEGORY: {category} {fire_level}", 0.08)
    time.sleep(1)

    if interactive:
        input("\nPress Enter to reveal Miriam's insight...")

    # Present setup if exists
    if quote_data["setup"] and quote_data["setup"].strip():
        print()
        typewriter_effect("📝 SETUP:", 0.08)
        time.sleep(0.5)
        typing_with_pauses(quote_data["setup"], 0.08)

        if interactive:
            input("\nPress Enter for the punchline...")
        else:
            dramatic_pause(2)

    # Present the punchline
    print()
    typewriter_effect("💡 MIRIAM'S WISDOM:", 0.08)
    time.sleep(1)

    # Split long punchlines for dramatic effect
    punchline = quote_data["punchline"]
    if len(punchline) > 80 and ". " in punchline:
        parts = punchline.split(". ")
        for i, part in enumerate(parts):
            if i > 0:
                part = ". " + part
            typing_with_pauses(part, 0.1)
            if i < len(parts) - 1:
                time.sleep(1.5)
    else:
        typing_with_pauses(punchline, 0.1)

    # Final dramatic pause and rating
    time.sleep(2)
    print()

    # Determine burn level message
    if difficulty >= 9:
        burn_msg = "💀 POLITICAL CAREERS: ENDED"
    elif difficulty >= 7:
        burn_msg = "🔥 BURN LEVEL: SAVAGE"
    elif difficulty >= 5:
        burn_msg = "😏 WIT LEVEL: SHARP"
    else:
        burn_msg = "😊 CHARM LEVEL: SWEET"

    typewriter_effect(burn_msg, 0.06)

    # Show source and tags
    if quote_data.get("source"):
        print()
        typewriter_effect(f"📖 Source: {quote_data['source']}", 0.03)

    print()
