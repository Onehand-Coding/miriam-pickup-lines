# Miriam Pickup Lines

Miriam Defensor Santiago's witty political and romantic punchlines with dramatic typing effects.

## Installation

```bash
# Clone
git clone https://github.com/Onehand-Coding/miriam-pickup-lines.git
# cd to project's dir
cd miriam-pickup-lines
# Sync using uv to install as package
uv sync
# or use traditional pip and venv method.
python3 -m venv .venv
source .venv/bin/activate # On Windows: .venv\Scripts\activate
pip install -e .
```

## Usage

```bash
# Remove uv if using traditional

# Random quote
uv run miriam-pickup-line

# Interactive mode
uv run miriam-pickup-line --interactive

# Filter by category
uv run miriam-pickup-line --category pickup_lines

# Limit difficulty level
uv run miriam-pickup-line --difficulty 5

# Show statistics
uv run miriam-pickup-line --stats

# Reset usage tracking
uv run miriam-pickup-line --reset
```

## Categories

- `politics` - Political commentary and corruption jokes
- `pickup_lines` - Romantic and flirting lines
- `marriage` - Marriage and relationship observations
- `education` - School and learning humor
- `personal` - Miriam's personal quotes
- `relationship` - General relationship wisdom

## Examples

```bash
# Remove uv if using traditional

# Get a sweet pickup line (difficulty 1-5)
uv run miriam-pickup-line --category pickup_lines --difficulty 5

# Interactive political commentary
uv run miriam-pickup-line --category politics --interactive

# Random wisdom
uv run miriam-pickup-line
```

## Source

You can generate your own `data/punch_line.json` using this template:

```
"miriam_quotes": [
            {"id": 1, "category": "politics", "type": "comparison", "setup": "What is the difference between corruption in the U.S. and corruption in the Philippines?", "punchline": "In the U.S. they go to jail. In the Philippines, they go to the U.S.", "source": "page_unknown", "difficulty_level": 10, "tags": ["corruption", "international", "savage"]}
```
