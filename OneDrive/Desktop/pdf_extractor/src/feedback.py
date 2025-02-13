# src/feedback.py
def collect_feedback(extracted_data, user_correction):
    """Store user corrections for retraining."""
    # Save corrections to a database or file
    with open("feedback.csv", "a") as f:
        f.write(f"{extracted_data},{user_correction}\n")