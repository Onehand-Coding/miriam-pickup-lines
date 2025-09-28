import argparse
import sys
from .database import MiriamDatabase
from .presentation import present_miriam_wisdom


def main():
    """Main entry point for the Miriam pickup lines CLI"""
    parser = argparse.ArgumentParser(
        description="Miriam Defensor Santiago's Wisdom Generator",
        epilog="Sample usage: miriam-pickup-line --interactive --category pickup_lines",
    )

    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Interactive mode with user-controlled pacing",
    )

    parser.add_argument(
        "-c",
        "--category",
        choices=[
            "politics",
            "pickup_lines",
            "marriage",
            "education",
            "personal",
            "relationship",
        ],
        help="Filter quotes by category",
    )

    parser.add_argument(
        "-d",
        "--difficulty",
        type=int,
        choices=range(1, 11),
        default=10,
        help="Maximum difficulty level (1-10, default: 10)",
    )

    parser.add_argument(
        "-s", 
        "--sound", 
        action="store_true",
        help="Enable sound effects for each typed character"
    )

    parser.add_argument("--stats", action="store_true", help="Show usage statistics")

    parser.add_argument(
        "--reset", action="store_true", help="Reset usage tracking for all quotes"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    # Initialize database
    try:
        db = MiriamDatabase()
    except Exception as e:
        print(f"Error initializing database: {e}")
        sys.exit(1)

    # Handle special commands
    if args.stats:
        show_stats(db)
        return

    if args.reset:
        db.reset_usage()
        print("✅ Usage tracking reset. All quotes are now available again.")
        return

    # Check if sound is enabled
    sound_enabled = bool(args.sound)

    # Get and present a quote
    try:
        quote = db.get_unused_quote(
            category=args.category, max_difficulty=args.difficulty
        )

        if not quote:
            print("😔 No unused quotes found with your criteria.")
            print("Try running with --reset to refresh the pool.")
            return

        # Present the quote with optional sound
        present_miriam_wisdom(quote, interactive=args.interactive, sound_enabled=sound_enabled)

        # Mark as used
        db.mark_as_used(quote["id"])

    except KeyboardInterrupt:
        print("\n\n👋 Salamat! Until next time...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def show_stats(db):
    """Display usage statistics"""
    stats = db.get_stats()

    print("📊 MIRIAM QUOTES STATISTICS")
    print("=" * 30)
    print(f"Total quotes: {stats['total']}")
    print(f"Used quotes: {stats['used']}")
    print(f"Available quotes: {stats['unused']}")
    print("\nBy category:")

    for category, count in stats["by_category"].items():
        print(f"  {category}: {count} quotes")


if __name__ == "__main__":
    main()
