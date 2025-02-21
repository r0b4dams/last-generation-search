from datetime import date


def is_valid(date_str: str):
    try:
        date.fromisoformat(date_str)
        return True
    except ValueError:
        return False
