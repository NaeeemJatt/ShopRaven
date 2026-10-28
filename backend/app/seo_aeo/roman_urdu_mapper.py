"""
Roman-Urdu Search & Misspelling Synonym Mapper (Alippo Feature #4).
Eliminates '0 search results' on nnstore.shop by generating Pakistani colloquial queries.
"""

import os
import json
import re
from typing import List

CURRENT_DIR = os.path.dirname(__file__)
DICT_PATH = os.path.join(CURRENT_DIR, "roman_urdu_dictionary.json")


class RomanUrduSearchMapper:
    """Maps products to colloquial Roman-Urdu phrases and common Pakistani phonetic typos."""

    def __init__(self):
        self.dictionary = {}
        if os.path.exists(DICT_PATH):
            try:
                with open(DICT_PATH, "r", encoding="utf-8") as f:
                    self.dictionary = json.load(f)
            except Exception:
                self.dictionary = {}

    def generate_phonetic_typos(self, keyword: str) -> List[str]:
        """
        Generates common phonetic substitutions used by Pakistani mobile shoppers:
        - 'ph' <-> 'f'
        - 'c' <-> 'k'
        - 'ee' <-> 'i'
        - 'oo' <-> 'u'
        - 'w' <-> 'v'
        - 'z' <-> 'j' or 's'
        """
        typos = set()
        clean = keyword.lower().strip()
        words = clean.split()

        substitutions = [
            ("ph", "f"), ("f", "ph"),
            ("k", "c"), ("c", "k"),
            ("ee", "i"), ("i", "ee"),
            ("oo", "u"), ("u", "oo"),
            ("w", "v"), ("v", "w"),
            ("sh", "s"), ("s", "sh"),
        ]

        for word in words:
            if len(word) <= 3:
                continue
            for orig, sub in substitutions:
                if orig in word:
                    variant = word.replace(orig, sub)
                    typos.add(clean.replace(word, variant))

        return list(typos)[:6]

    def generate_local_synonyms(self, product_title: str, category: str) -> List[str]:
        """
        Generates 15-20 localized Roman-Urdu phrases, colloquial terms,
        and phonetic misspellings for tag injection and search metadata.
        """
        synonyms = set()
        title_lower = product_title.lower()

        # 1. Search category dictionary for matching keywords
        category_dict = self.dictionary.get(category, {})
        for root_key, phrases in category_dict.items():
            if root_key in title_lower:
                for p in phrases:
                    synonyms.add(p)

        # Cross-category fallback search if not found in primary category
        if len(synonyms) < 2:
            for cat_name, subdict in self.dictionary.items():
                for root_key, phrases in subdict.items():
                    if root_key in title_lower:
                        for p in phrases:
                            synonyms.add(p)

        # 2. Add category-wide Pakistani buyer intent phrases
        cat_lower = category.lower()
        if "kitchen" in cat_lower:
            synonyms.add("kitchen ka saman")
            synonyms.add("kitchen appliances pakistan")
        elif "beauty" in cat_lower or "care" in cat_lower:
            synonyms.add("chehray ki hifazat")
            synonyms.add("beauty tools daraz")
        elif "electronic" in cat_lower or "gadget" in cat_lower:
            synonyms.add("gadgets pakistan")
            synonyms.add("mobile accessories lahore karachi")
        elif "auto" in cat_lower or "tool" in cat_lower:
            synonyms.add("car decor accessories")
            synonyms.add("gari ka saman")
        elif "baby" in cat_lower or "kid" in cat_lower:
            synonyms.add("bacchon ka saman pakistan")
            synonyms.add("baby items cash on delivery")
        elif "pet" in cat_lower:
            synonyms.add("pet accessories pakistan")
            synonyms.add("billi aur kuttay ka saman")
        else:
            synonyms.add("trending gadgets pakistan")
            synonyms.add("online shopping lahore karachi")

        # 3. Add phonetic typo variants
        title_words = [w for w in title_lower.split() if len(w) > 3][:3]
        for w in title_words:
            for typo in self.generate_phonetic_typos(w):
                synonyms.add(typo)

        # 4. Standard buying intent suffixes
        synonyms.add(f"{title_words[0] if title_words else 'product'} sasta price")
        synonyms.add(f"{title_words[0] if title_words else 'product'} cash on delivery")

        # Ensure between 15 and 20 synonyms
        result = list(synonyms)
        if len(result) < 15:
            generic = [
                "sasta aur behtareen", "online shopping pakistan", "cash on delivery saman",
                "original product guarantee", "nn store trending items", "fast delivery pakistan"
            ]
            for g in generic:
                if len(result) >= 18:
                    break
                result.append(g)

        return result[:20]

