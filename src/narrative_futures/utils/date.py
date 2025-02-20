from datetime import date


def is_valid(date_str: str):
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        return False
