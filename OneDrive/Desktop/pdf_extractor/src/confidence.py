# src/confidence.py
def calculate_confidence(extracted_data, validation_rules):
    """Calculate confidence score based on validation rules."""
    score = 0
    for rule in validation_rules:
        if rule(extracted_data):
            score += 1
    return score / len(validation_rules)