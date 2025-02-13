# src/normalize.py
import pandas as pd
from dateutil.parser import parse

def normalize_dates(dates):
    """Normalize date formats."""
    if not dates or not isinstance(dates, (list, tuple)):
        return []
    normalized_dates = []
    for date in dates:
        try:
            normalized_dates.append(parse(date).strftime("%Y-%m-%d"))
        except (ValueError, TypeError):
            continue
    return normalized_dates

def normalize_currency(amounts):
    """Standardize currency values."""
    if not amounts or not isinstance(amounts, (list, tuple)):
        return []
    normalized_amounts = []
    for amount in amounts:
        try:
            cleaned = str(amount).replace("$", "").replace(",", "")
            normalized_amounts.append(float(cleaned))
        except (ValueError, TypeError):
            continue
    return normalized_amounts