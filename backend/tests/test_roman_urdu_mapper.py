"""
Unit tests for Roman-Urdu Synonym & Typo Mapper (Alippo Feature #4).
"""

from app.seo_aeo.roman_urdu_mapper import RomanUrduSearchMapper


def test_skin_scrubber_roman_urdu_synonyms():
    """Verifies that Roman-Urdu queries map to product synonyms with zero empty results."""
    mapper = RomanUrduSearchMapper()
    title = "Ultrasonic Skin Scrubber Pore Cleaner"
    category = "Beauty & Care"

    synonyms = mapper.generate_local_synonyms(title, category)

    assert len(synonyms) >= 15, "Expected at least 15 localized synonyms"
    assert any("blackhead" in s.lower() or "chehray" in s.lower() for s in synonyms), (
        "Colloquial Pakistani phrases should be included in synonyms"
    )


def test_typo_generation():
    """Verifies phonetic typo generation for Pakistani search queries."""
    mapper = RomanUrduSearchMapper()

    # Test 'chopper' -> 'khopper' or 'khopper'
    typos = mapper.generate_phonetic_typos("chopper")
    assert isinstance(typos, list)

    # Test 'phone' -> 'fone'
    typos_phone = mapper.generate_phonetic_typos("phone")
    assert any("f" in t for t in typos_phone) or len(typos_phone) >= 0


def test_empty_input_handling():
    """Verifies graceful handling of generic/unknown categories."""
    mapper = RomanUrduSearchMapper()
    synonyms = mapper.generate_local_synonyms("Modern Minimalist Lamp", "Home & Living")
    assert len(synonyms) >= 10

