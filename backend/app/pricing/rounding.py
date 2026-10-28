"""
Psychological PKR price rounding utility.
Enforces nnstore.shop's catalog convention: every sale and regular price
ends in *49 or *99 (e.g., Rs. 649, Rs. 749, Rs. 899, Rs. 1,099, Rs. 1,399).
"""

import math


def round_to_nnstore_ending(raw_price: float, min_floor: float) -> float:
    """
    Rounds raw_price to the nearest psychological ending (*49 or *99)
    such that the returned price is NEVER strictly lower than min_floor.
    """
    # Start checking candidates at hundreds
    base_hundred = int(math.floor(raw_price / 100.0)) * 100

    # Generate candidate prices around the target
    candidates = []
    for h in range(base_hundred - 100, base_hundred + 300, 100):
        c1 = float(h + 49)
        c2 = float(h + 99)
        if c1 >= min_floor:
            candidates.append(c1)
        if c2 >= min_floor:
            candidates.append(c2)

    if not candidates:
        # Guarantee minimum margin floor with 49 or 99
        h = int(math.ceil(min_floor / 100.0)) * 100
        cand = float(h + 49)
        if cand < min_floor:
            cand = float(h + 99)
        return cand

    # Pick the candidate closest to raw_price
    candidates.sort(key=lambda x: (abs(x - raw_price), x))
    return candidates[0]


def compute_strikethrough_regular_price(sale_price: float) -> float:
    """
    Computes a credible higher 'Regular Price' (List / Strikethrough)
    providing a perceived 30% - 40% discount, ending in *49 or *99.
    Example: Sale Rs. 1,399 -> Regular Rs. 2,049 or Rs. 2,199.
    """
    markup_factor = 1.45  # Approx 31% discount
    raw_regular = sale_price * markup_factor
    return round_to_nnstore_ending(raw_regular, min_floor=sale_price + 200.0)

