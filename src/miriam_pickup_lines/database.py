import sqlite3
import json
import random
from datetime import datetime
from pathlib import Path
import os

from .config import PROJECT_ROOT


class MiriamDatabase:
    def __init__(self, db_path=None):
        if db_path is None:
            # Create database in user's home directory
            home_dir = PROJECT_ROOT
            db_dir = home_dir / '.miriam_pickup_lines'
            db_dir.mkdir(exist_ok=True)
            self.db_path = db_dir / 'miriam_quotes.db'
        else:
            self.db_path = Path(db_path)

        self.init_database()
        self.populate_initial_data()

    def init_database(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY,
                    category TEXT NOT NULL,
                    type TEXT NOT NULL,
                    setup TEXT,
                    punchline TEXT NOT NULL,
                    source TEXT,
                    difficulty_level INTEGER,
                    tags TEXT,
                    used_count INTEGER DEFAULT 0,
                    last_used TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def populate_initial_data(self):
        """Populate database with initial quotes if empty"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM quotes")
            count = cursor.fetchone()[0]

            if count == 0:
                # Insert the JSON data
                quotes_data = self.get_initial_quotes()
                for quote in quotes_data:
                    cursor.execute('''
                        INSERT INTO quotes
                        (id, category, type, setup, punchline, source, difficulty_level, tags)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        quote['id'],
                        quote['category'],
                        quote['type'],
                        quote.get('setup', ''),
                        quote['punchline'],
                        quote.get('source', ''),
                        quote.get('difficulty_level', 5),
                        ','.join(quote.get('tags', []))
                    ))
                conn.commit()

    def get_unused_quote(self, category=None, max_difficulty=10):
        """Get a random unused quote, optionally filtered by category and difficulty"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = "SELECT * FROM quotes WHERE used_count = 0"
            params = []

            if category:
                query += " AND category = ?"
                params.append(category)

            query += " AND difficulty_level <= ?"
            params.append(max_difficulty)

            cursor.execute(query, params)
            quotes = cursor.fetchall()

            if not quotes:
                # If no unused quotes, reset all and try again
                self.reset_usage()
                cursor.execute(query, params)
                quotes = cursor.fetchall()

            return dict(random.choice(quotes)) if quotes else None

    def mark_as_used(self, quote_id):
        """Mark a quote as used"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                UPDATE quotes
                SET used_count = used_count + 1, last_used = ?
                WHERE id = ?
            ''', (datetime.now(), quote_id))
            conn.commit()

    def reset_usage(self):
        """Reset usage count for all quotes"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE quotes SET used_count = 0, last_used = NULL")
            conn.commit()

    def get_stats(self):
        """Get usage statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM quotes")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM quotes WHERE used_count > 0")
            used = cursor.fetchone()[0]

            cursor.execute("SELECT category, COUNT(*) FROM quotes GROUP BY category")
            by_category = dict(cursor.fetchall())

            return {
                'total': total,
                'used': used,
                'unused': total - used,
                'by_category': by_category
            }

    def get_initial_quotes(self):
        """Return the complete initial quotes data from Miriam's book"""
        return [
            {"id": 1, "category": "politics", "type": "comparison", "setup": "What is the difference between corruption in the U.S. and corruption in the Philippines?", "punchline": "In the U.S. they go to jail. In the Philippines, they go to the U.S.", "source": "page_unknown", "difficulty_level": 10, "tags": ["corruption", "international", "savage"]},
            {"id": 2, "category": "politics", "type": "statement", "setup": "", "punchline": "Politicians never get lost in thought, because it's unfamiliar territory.", "source": "page_4", "difficulty_level": 8, "tags": ["intelligence", "thinking"]},
            {"id": 3, "category": "politics", "type": "statement", "setup": "", "punchline": "Brains aren't everything. In the case of Congress members, they're nothing.", "source": "page_4", "difficulty_level": 9, "tags": ["congress", "intelligence"]},
            {"id": 4, "category": "politics", "type": "statement", "setup": "", "punchline": "Corrupt politicians would be different, if they had enough oxygen at birth.", "source": "page_4", "difficulty_level": 8, "tags": ["corruption", "birth_defect"]},
            {"id": 5, "category": "politics", "type": "statement", "setup": "", "punchline": "Most people live and learn. Politicians just live.", "source": "page_4", "difficulty_level": 7, "tags": ["learning", "growth"]},
            {"id": 6, "category": "politics", "type": "question", "setup": "To politicians accused of plunder:", "punchline": "As an outsider, what do you think of the human race?", "source": "page_4", "difficulty_level": 9, "tags": ["plunder", "humanity"]},
            {"id": 7, "category": "politics", "type": "statement", "setup": "Of her enemy:", "punchline": "Googling him yielded no results.", "source": "page_4", "difficulty_level": 6, "tags": ["irrelevant", "technology"]},
            {"id": 8, "category": "politics", "type": "statement", "setup": "Of her pet peeve:", "punchline": "He is so ugly he should donate his face to the Parks and Wildlife Office in Quezon City.", "source": "page_4", "difficulty_level": 8, "tags": ["ugly", "wildlife"]},
            {"id": 9, "category": "politics", "type": "statement", "setup": "", "punchline": "I don't mind dying for the Filipino youth and nation, but I certainly don't want to die for politicians.", "source": "page_5", "difficulty_level": 7, "tags": ["sacrifice", "youth"]},
            {"id": 10, "category": "politics", "type": "statement", "setup": "", "punchline": "A politician is a man who will double cross that bridge when he comes to it.", "source": "page_8", "difficulty_level": 6, "tags": ["betrayal", "crossing"]},
            {"id": 11, "category": "politics", "type": "comparison", "setup": "What do you call when you throw garbage in the sea?", "punchline": "Pollution. What do you call when you throw corrupt politicians in the sea? Solution.", "source": "page_59", "difficulty_level": 10, "tags": ["environment", "solution", "drowning"]},
            {"id": 12, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Pumupunta ka ba sa gym? Kasi feeling ko, magwo-work out tayo.", "source": "page_26", "difficulty_level": 6, "tags": ["gym", "exercise", "relationship"]},
            {"id": 13, "category": "pickup_lines", "type": "comparison", "setup": "", "punchline": "Ang pagmamahal ko sa'yo ay parang bilbil, pilit ko mang tinatago pero halata pa rin!", "source": "page_26", "difficulty_level": 5, "tags": ["love", "belly_fat", "obvious"]},
            {"id": 14, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Wow, saan gawa ang t-shirt mo? Gawa ba 'yan sa boyfriend material?", "source": "page_26", "difficulty_level": 7, "tags": ["clothing", "material", "boyfriend"]},
            {"id": 15, "category": "pickup_lines", "type": "comparison", "setup": "", "punchline": "Ang pag-ibig ko sa'yo ay parang relo. Parating pakanan, never kakaliwa.", "source": "page_26", "difficulty_level": 6, "tags": ["watch", "direction", "loyalty"]},
            {"id": 16, "category": "pickup_lines", "type": "comparison", "setup": "", "punchline": "Ang ganda mo ay parang PLDT---pang-long distance.", "source": "page_26", "difficulty_level": 8, "tags": ["beauty", "telecom", "distance"]},
            {"id": 17, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Kung magkaroon man ako ng third eye, ilalagay ko ito sa puso ko. Para hindi na ako mabulag sa pag-ibig.", "source": "page_26", "difficulty_level": 7, "tags": ["third_eye", "heart", "blindness"]},
            {"id": 18, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Kapag namatay na ako, huwag na huwag kang pupunta sa libingan ko, baka tumibok ulit ang puso ko.", "source": "page_26", "difficulty_level": 8, "tags": ["death", "cemetery", "heartbeat"]},
            {"id": 19, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Miss, kutsara ka ba? Kasi papalapit ka pa lang, napapanganga na ako.", "source": "page_26", "difficulty_level": 6, "tags": ["spoon", "mouth", "opening"]},
            {"id": 20, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Kung asukal ka, ako naman ay sago. Wala akong kwenta kung wala ang tamis mo.", "source": "page_27", "difficulty_level": 8, "tags": ["sugar", "sago", "sweetness", "title_reference"]},
            {"id": 21, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Suicide. Homicide. Insecticide. Lahat na lang pamatay. Pero kung gusto mo ng pampabuhay, i-try mo ang 'by my side.'", "source": "page_27", "difficulty_level": 9, "tags": ["death", "killing", "life", "wordplay"]},
            {"id": 22, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Malabo na talaga ang mga mata ko. Pwede ba akong humingi sa iyo ng kahit konting pagtingin?", "source": "page_27", "difficulty_level": 7, "tags": ["vision", "eyes", "looking"]},
            {"id": 23, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Laway ka ba? Kasi kahit tulog na ako, ikaw pa rin ang lumalabas sa bibig ko.", "source": "page_27", "difficulty_level": 8, "tags": ["saliva", "sleep", "mouth"]},
            {"id": 24, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Ang lampa mo naman! Tatawid ka na nga lang sa isip ko, nahulog ka pa sa puso ko.", "source": "page_27", "difficulty_level": 8, "tags": ["clumsy", "mind", "heart", "falling"]},
            {"id": 25, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Password ka ba? Hindi kasi kita kayang kalimutan, pero kaya kitang palitan.", "source": "page_28", "difficulty_level": 9, "tags": ["password", "technology", "forget", "replace"]},
            {"id": 26, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Hindi naman tayo naglalaro ng tagu-taguan pero bakit hinahanap-hanap kita?", "source": "page_28", "difficulty_level": 6, "tags": ["hide_and_seek", "searching"]},
            {"id": 27, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Mag-exchange gift tayo? Akin ka at sa iyo naman ako.", "source": "page_28", "difficulty_level": 7, "tags": ["gift", "exchange", "mutual"]},
            {"id": 28, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Pwede ba kitang sabayan pauwi? Kasi sabi sa akin ng magulang ko, 'Follow your dreams.'", "source": "page_28", "difficulty_level": 8, "tags": ["home", "parents", "dreams"]},
            {"id": 29, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Test paper ka ba? Nauubos na kasi oras ko kakatitig sa'yo, ayan tuloy babagsak na yata ako sa'yo!", "source": "page_28", "difficulty_level": 7, "tags": ["exam", "time", "staring", "falling"]},
            {"id": 30, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Dilim ka ba? Kasi nang dumating ka, wala na akong makitang iba.", "source": "page_31", "difficulty_level": 6, "tags": ["darkness", "arrival", "seeing"]},
            {"id": 31, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Alam mo ba, ang bigas, gasolina, pamasahe, tuition fee, isda, karne, lahat sila nagmamahalan? Tayo na lang kaya ang hindi!", "source": "page_31", "difficulty_level": 8, "tags": ["prices", "inflation", "love", "economics"]},
            {"id": 32, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Pangalan mo palang kinikilig na ako, paano kaya kung magka-apelyido na tayo?", "source": "page_32", "difficulty_level": 7, "tags": ["name", "kilig", "surname", "marriage"]},
            {"id": 33, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Ok lang akong mahilo, basta sa iyo lang iikot ang mundo ko.", "source": "page_32", "difficulty_level": 6, "tags": ["dizzy", "world", "revolve"]},
            {"id": 34, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Dalawang beses lang naman kita gustong makasama: now and forever.", "source": "page_32", "difficulty_level": 7, "tags": ["time", "together", "forever"]},
            {"id": 35, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Dahil isa akong judge, pwede kitang hatulan ng habang buhay na pagkakakulong sa puso ko.", "source": "page_32", "difficulty_level": 8, "tags": ["judge", "life_sentence", "heart", "prison"]},
            {"id": 36, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Can you recommend a good bank? Kasi I'm planning to save all my love for you.", "source": "page_33", "difficulty_level": 7, "tags": ["bank", "save", "love", "money"]},
            {"id": 37, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Ang pag-ibig ko sa'yo ay parang LANGKA. LANGKAtupasan.", "source": "page_34", "difficulty_level": 5, "tags": ["jackfruit", "wordplay", "hard_to_reach"]},
            {"id": 38, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Kili-kili ka ba? Malapit ka kasi sa puso ko.", "source": "page_34", "difficulty_level": 6, "tags": ["armpit", "heart", "close"]},
            {"id": 39, "category": "pickup_lines", "type": "comparison", "setup": "", "punchline": "Ang love ay parang bayad sa jeep. Minsan hindi nasusuklian.", "source": "page_34", "difficulty_level": 7, "tags": ["love", "jeepney", "fare", "change"]},
            {"id": 40, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Pwede bang magpa-blood test? Para malaman mo na type kita.", "source": "page_34", "difficulty_level": 8, "tags": ["blood_test", "type", "medical", "wordplay"]},
            {"id": 41, "category": "pickup_lines", "type": "statement", "setup": "", "punchline": "Gusto kitang kasuhan ng trespassing. Basta-basta ka na lang pumapasok sa puso ko.", "source": "page_34", "difficulty_level": 7, "tags": ["lawsuit", "trespassing", "heart", "legal"]},
            {"id": 42, "category": "pickup_lines", "type": "question", "setup": "", "punchline": "Empleyado ka ba? Empleyado rin ako. Pwede tayong magkaroon ng union.", "source": "page_34", "difficulty_level": 6, "tags": ["employee", "union", "work"]},
            {"id": 43, "category": "relationship", "type": "statement", "setup": "", "punchline": "Ang relasyon ay parang gubat. Madalas may ahas.", "source": "page_37", "difficulty_level": 8, "tags": ["relationship", "forest", "snake", "danger"]},
            {"id": 44, "category": "education", "type": "comparison", "setup": "Question: What is the singular form of the word 'binoculars'?", "punchline": "Answer: Telescope.", "source": "page_68", "difficulty_level": 6, "tags": ["grammar", "singular", "telescope"]},
            {"id": 45, "category": "education", "type": "comparison", "setup": "Question: What is the plural form of iced tea?", "punchline": "Answer: Bottomless iced tea.", "source": "page_68", "difficulty_level": 5, "tags": ["grammar", "plural", "restaurant"]},
            {"id": 46, "category": "education", "type": "comparison", "setup": "Question: What is the plural form of rice?", "punchline": "Answer: Extra rice.", "source": "page_68", "difficulty_level": 5, "tags": ["grammar", "plural", "food"]},
            {"id": 47, "category": "education", "type": "statement", "setup": "", "punchline": "Law school is quite easy. It's like a stroll in a park. Pero Jurassic Park.", "source": "page_69", "difficulty_level": 8, "tags": ["law_school", "park", "difficulty", "danger"]},
            {"id": 48, "category": "education", "type": "statement", "setup": "", "punchline": "Gaano katalino ang estudyanteng Pilipino? Common sense pa lang nila, IQ na ng ibang senator.", "source": "page_76", "difficulty_level": 9, "tags": ["intelligence", "common_sense", "senator", "comparison"]},
            {"id": 49, "category": "marriage", "type": "comparison", "setup": "Question: What is the punishment for bigamy?", "punchline": "Answer: Two wives.", "source": "page_94", "difficulty_level": 8, "tags": ["bigamy", "punishment", "wives"]},
            {"id": 50, "category": "marriage", "type": "statement", "setup": "", "punchline": "Scientists have discovered a food that diminishes a woman's sex drive by 90 percent. Ang tawag doon ay wedding cake.", "source": "page_96", "difficulty_level": 8, "tags": ["marriage", "sex_drive", "wedding_cake"]},
            {"id": 51, "category": "marriage", "type": "statement", "setup": "", "punchline": "Marriages are made in heaven. But then again, so are thunder and lightning.", "source": "page_97", "difficulty_level": 7, "tags": ["heaven", "thunder", "lightning", "nature"]},
            {"id": 52, "category": "marriage", "type": "statement", "setup": "", "punchline": "Marriage is love. Love is blind. Therefore, marriage is an institution for the blind.", "source": "page_97", "difficulty_level": 7, "tags": ["love", "blind", "institution", "logic"]},
            {"id": 53, "category": "marriage", "type": "statement", "setup": "", "punchline": "Marriage is not a word. It is a sentence---a life sentence.", "source": "page_97", "difficulty_level": 8, "tags": ["sentence", "life_sentence", "prison"]},
            {"id": 54, "category": "marriage", "type": "statement", "setup": "", "punchline": "The worst thing about being married is having to tolerate the body noises of your spouse, especially as you both grow older.", "source": "page_99", "difficulty_level": 6, "tags": ["body_noises", "aging", "tolerance"]},
            {"id": 55, "category": "personal", "type": "statement", "setup": "", "punchline": "I eat death threats for breakfast!", "source": "page_46", "difficulty_level": 10, "tags": ["death_threats", "breakfast", "courage", "iconic"]},
            {"id": 56, "category": "personal", "type": "statement", "setup": "", "punchline": "Hindi naman ako mataba eh. In fact, I'm so sexy that it overflows.", "source": "page_110", "difficulty_level": 7, "tags": ["sexy", "overflow", "body_image"]},
            {"id": 57, "category": "personal", "type": "statement", "setup": "", "punchline": "Wala naman talagang pangit, sadyang nasobrahan lang ako sa ganda.", "source": "page_110", "difficulty_level": 8, "tags": ["beauty", "excess", "confidence"]},
            {"id": 58, "category": "personal", "type": "statement", "setup": "", "punchline": "Yes, I am intellectually arrogant. All intellectuals are entitled to be arrogant. That's the only way they can educate the non-intellectual. Inggit lang sila.", "source": "page_109", "difficulty_level": 9, "tags": ["intellectual", "arrogant", "education", "envy"]}
        ]
