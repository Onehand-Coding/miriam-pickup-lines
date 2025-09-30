import time
import sys
import os
from pathlib import Path

try:
    import pygame
    from pygame import mixer
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False

from .config import PROJECT_ROOT


# Initialize pygame mixer for sound effects
if PYGAME_AVAILABLE:
    try:
        mixer.init()
    except pygame.error:
        PYGAME_AVAILABLE = False

# Sound effect file paths
SOUND_DIR = PROJECT_ROOT / "data" / "sounds"
KEYPRESS_SOUND = SOUND_DIR / "keypress.wav"
BURN_SOUND = SOUND_DIR / "burn.wav"      # For high difficulty
SAVAGE_SOUND = SOUND_DIR / "savage.wav"  # For medium high difficulty
WIT_SOUND = SOUND_DIR / "wit.wav"        # For medium difficulty
CHARM_SOUND = SOUND_DIR / "charm.wav"    # For low difficulty
POLITICS_SOUND = SOUND_DIR / "politics.wav"        # For politics category
PICKUP_SOUND = SOUND_DIR / "pickup.wav"            # For pickup lines category
MARRIAGE_SOUND = SOUND_DIR / "marriage.wav"        # For marriage category
EDUCATION_SOUND = SOUND_DIR / "education.wav"      # For education category
PERSONAL_SOUND = SOUND_DIR / "personal.wav"        # For personal category
RELATIONSHIP_SOUND = SOUND_DIR / "relationship.wav" # For relationship category

# Preload sound effects if available
keypad_sound = None
burn_sound = None
savage_sound = None
wit_sound = None
charm_sound = None
politics_sound = None
pickup_sound = None
marriage_sound = None
education_sound = None
personal_sound = None
relationship_sound = None
wisdom_sound = None

if PYGAME_AVAILABLE:  # TODO: Download and set suitable sound for each category and difficulty level.
    if KEYPRESS_SOUND.exists():
        keypad_sound = mixer.Sound(str(KEYPRESS_SOUND))
    if BURN_SOUND.exists():
        burn_sound = mixer.Sound(str(BURN_SOUND))
    if SAVAGE_SOUND.exists():
        savage_sound = mixer.Sound(str(SAVAGE_SOUND))
    if WIT_SOUND.exists():
        wit_sound = mixer.Sound(str(WIT_SOUND))
    if CHARM_SOUND.exists():
        charm_sound = mixer.Sound(str(CHARM_SOUND))
    if POLITICS_SOUND.exists():
        politics_sound = mixer.Sound(str(POLITICS_SOUND))
    if PICKUP_SOUND.exists():
        pickup_sound = mixer.Sound(str(PICKUP_SOUND))
    if MARRIAGE_SOUND.exists():
        marriage_sound = mixer.Sound(str(MARRIAGE_SOUND))
    if EDUCATION_SOUND.exists():
        education_sound = mixer.Sound(str(EDUCATION_SOUND))
    if PERSONAL_SOUND.exists():
        personal_sound = mixer.Sound(str(PERSONAL_SOUND))
        wisdom_sound = mixer.Sound(str(PERSONAL_SOUND))  # Share with this sound for now, we have to set all this later.
    if RELATIONSHIP_SOUND.exists():
        relationship_sound = mixer.Sound(str(RELATIONSHIP_SOUND))


def play_sound(sound_obj, volume=0.3):
    """Play a sound effect if available"""
    if PYGAME_AVAILABLE and sound_obj:
        try:
            sound_obj.set_volume(volume)
            sound_obj.play()
        except Exception:
            # If there's an error playing the sound, continue without sound
            pass


def typewriter_effect(text, delay=0.05, end_with_newline=True, sound_enabled=False):
    """Simulate typewriter effect - each character appears one by one with optional sound"""
    for char in text:
        print(char, end="", flush=True)
        
        if sound_enabled and keypad_sound:
            play_sound(keypad_sound)
        
        time.sleep(delay)
    if end_with_newline:
        print()


def typing_with_pauses(text, delay=0.05, pause_chars=",.?!;:", sound_enabled=False):
    """Typewriter effect with dramatic pauses on punctuation with optional sound"""
    for char in text:
        print(char, end="", flush=True)
        
        if sound_enabled and keypad_sound:
            play_sound(keypad_sound)
        
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


def present_miriam_wisdom(quote_data, interactive=False, sound_enabled=False):
    """Main presentation function for Miriam's quotes"""
    print()
    print("=" * 60)
    print("💎 MIRIAM DEFENSOR SANTIAGO'S WISDOM")
    print("=" * 60)
    print()

    # Category and difficulty indicator
    category = quote_data["category"].upper()
    difficulty = quote_data["difficulty_level"]
    fire_level = "🔥" * min(difficulty // 2, 5)

    typewriter_effect(f"📂 CATEGORY: {category} {fire_level}", 0.08, sound_enabled=sound_enabled)
    time.sleep(1)

    if interactive:
        input("\nPress Enter to reveal Miriam's insight...")

    # Present setup if exists
    if quote_data["setup"] and quote_data["setup"].strip():
        print()
        typewriter_effect("📝 SETUP:", 0.08, sound_enabled=sound_enabled)
        time.sleep(0.5)
        typing_with_pauses(quote_data["setup"], 0.08, sound_enabled=sound_enabled)

        if interactive:
            input("\nPress Enter for the punchline...")
        else:
            dramatic_pause(2)

    # Present the punchline
    print()

    # Split long punchlines for dramatic effect
    punchline = quote_data["punchline"]
    if len(punchline) > 80 and ". " in punchline:
        parts = punchline.split(". ")
        for i, part in enumerate(parts):
            if i > 0:
                part = ". " + part
            typing_with_pauses(part, 0.1, sound_enabled=sound_enabled)
            if i < len(parts) - 1:
                time.sleep(1.5)
    else:
        typing_with_pauses(punchline, 0.1, sound_enabled=sound_enabled)

    # Final pause before playing category sounds
    time.sleep(0.3)

    # Play category-specific sound based on the quote category
    category_sound = None
    if quote_data["category"] == "politics":
        category_sound = politics_sound
    elif quote_data["category"] == "pickup_lines":
        category_sound = pickup_sound
    elif quote_data["category"] == "marriage":
        category_sound = marriage_sound
    elif quote_data["category"] == "education":
        category_sound = education_sound
    elif quote_data["category"] == "personal":
        category_sound = personal_sound
    elif quote_data["category"] == "relationship":
        category_sound = relationship_sound
    elif quote_data["category"] == "wisdom":
        category_sound = wisdom_sound

    # Play the category-specific sound if available
    if sound_enabled and category_sound:
        play_sound(category_sound)
    # Fallback to difficulty-based sound if no category-specific sound
    elif sound_enabled:
        if difficulty >= 9:
            if burn_sound:
                play_sound(burn_sound)
        elif difficulty >= 7:
            if savage_sound:
                play_sound(savage_sound)
        elif difficulty >= 5:
            if wit_sound:
                play_sound(wit_sound)
        else:
            if charm_sound:
                play_sound(charm_sound)

    # Wait for the sound to finish playing (up to 3 seconds max)
    if PYGAME_AVAILABLE and sound_enabled:
        import pygame
        while mixer.get_busy():
            pygame.time.wait(100)  # Wait 100ms between checks
    
    print()
    print(f"Page:{quote_data['source']}")
