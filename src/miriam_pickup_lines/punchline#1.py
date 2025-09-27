import time
import sys

def typewriter_effect(text, delay=0.05, end_with_newline=True):
    """
    Simulate typewriter effect - each character appears one by one
    """
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    if end_with_newline:
        print()  # New line at the end

def typing_with_pauses(text, delay=0.05, pause_on='.?!'):
    """
    Typewriter effect with dramatic pauses on punctuation
    """
    for char in text:
        print(char, end='', flush=True)
        if char in pause_on:
            time.sleep(delay * 10)  # Longer pause for drama
        else:
            time.sleep(delay)
    print()

def miriam_political_wisdom():
    """
    Present Miriam's classic line with proper dramatic timing
    """
    print("=" * 60)
    print("🎭 MIRIAM DEFENSOR SANTIAGO'S POLITICAL WISDOM")
    print("=" * 60)
    print()

    # Setup with anticipation
    typewriter_effect("Preparing to share political insight...", 0.08)
    time.sleep(1.5)

    # The question - slower for emphasis
    print("📝 QUESTION:")
    time.sleep(0.5)
    typing_with_pauses("What is the difference between corruption in the U.S. and corruption in the Philippines?", 0.08)

    # Dramatic pause while "thinking"
    print()
    for i in range(3):
        print(".", end="", flush=True)
        time.sleep(0.8)
    print()
    print()

    # The devastating answer
    print("💡 ANSWER:")
    time.sleep(1)
    typing_with_pauses("In the U.S. they go to jail.", 0.1)
    time.sleep(2)  # Let it sink in
    typing_with_pauses("In the Philippines, they go to the U.S.", 0.1)

    # Final dramatic pause
    time.sleep(2)
    print()
    typewriter_effect("🔥 BURN LEVEL: MIRIAM DEFENSOR SANTIAGO", 0.06)
    print()

def chat_style_presentation():
    """
    Present it like a social media chat conversation
    """
    print("\n" + "="*50)
    print("💬 FB MESSENGER STYLE")
    print("="*50)

    # Simulate typing indicator
    print("Miriam is typing", end="")
    for i in range(4):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print()
    time.sleep(1)

    # First message
    typewriter_effect("Miriam: May tanong ako sa inyo...", 0.08)
    time.sleep(2)

    # Show typing again
    print("Miriam is typing...")
    time.sleep(1.5)

    # The question
    typewriter_effect("Miriam: What is the difference between corruption in the U.S. and corruption in the Philippines?", 0.06)
    time.sleep(3)

    # Show typing one more time
    print("Miriam is typing...")
    time.sleep(2)

    # The punchline
    typewriter_effect("Miriam: In the U.S. they go to jail. In the Philippines, they go to the U.S.", 0.08)
    time.sleep(1)

    # Reactions
    print()
    typewriter_effect("You: 🔥🔥🔥", 0.2)
    typewriter_effect("Friend1: HAHAHAHA SAVAGE!", 0.1)
    typewriter_effect("Friend2: Miriam never misses 😂", 0.1)
    typewriter_effect("Corrupt Politician: *left the chat*", 0.1)

def terminal_hacker_style():
    """
    Present it like a terminal/hacker interface
    """
    print("\n" + "="*60)
    print("🖥️  TERMINAL ACCESS - MIRIAM_WISDOM.exe")
    print("="*60)

    typewriter_effect("$ accessing_political_database...", 0.05)
    time.sleep(1)
    typewriter_effect("$ loading_corruption_analysis.py", 0.05)
    time.sleep(1)
    typewriter_effect("$ initializing_truth_bomb...", 0.05)
    time.sleep(1.5)

    print()
    typewriter_effect(">>> QUERY: corruption_comparison(US, Philippines)", 0.05)
    time.sleep(1)

    typewriter_effect("Processing", end_with_newline=False)
    for i in range(6):
        print(".", end="", flush=True)
        time.sleep(0.4)
    print()
    time.sleep(1)

    typewriter_effect(">>> RESULT:", 0.05)
    time.sleep(0.5)
    typewriter_effect("    US: jail_time = TRUE", 0.08)
    time.sleep(1)
    typewriter_effect("    Philippines: destination = 'United States'", 0.08)
    time.sleep(2)

    typewriter_effect(">>> STATUS: TRUTH_BOMB_DEPLOYED ✅", 0.05)
    typewriter_effect(">>> DAMAGE_LEVEL: CRITICAL 🔥", 0.05)

def interactive_reveal():
    """
    Interactive version where user presses enter to continue
    """
    print("\n" + "="*50)
    print("🎪 INTERACTIVE MIRIAM WISDOM")
    print("="*50)

    input("Press Enter to reveal Miriam's political insight...")
    print()

    typewriter_effect("Setting up the devastating comparison...", 0.08)
    input("\nPress Enter for the question...")

    typing_with_pauses("What is the difference between corruption in the U.S. and corruption in the Philippines?", 0.08)

    input("\nThinking... Press Enter for Miriam's savage answer...")
    print()

    typewriter_effect("MIRIAM'S ANSWER:", 0.1)
    time.sleep(1)

    input("Part 1 - Press Enter...")
    typing_with_pauses("In the U.S. they go to jail.", 0.1)

    input("\nPart 2 - Press Enter for the killing blow...")
    typing_with_pauses("In the Philippines, they go to the U.S.", 0.1)

    time.sleep(2)
    typewriter_effect("💀 POLITICAL CAREERS: ENDED", 0.08)

# Run all presentations
if __name__ == "__main__":
    # Classic typewriter version
    miriam_political_wisdom()

    time.sleep(3)

    # Chat style
    chat_style_presentation()

    time.sleep(3)

    # Terminal hacker style
    terminal_hacker_style()

    print("\n\n🎯 Choose your presentation style!")
    print("Each creates different dramatic impact for maximum viral potential!")
