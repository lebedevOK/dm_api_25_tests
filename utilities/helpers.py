import random
import string


def random_string(length: int = 8) -> str:
    """Generate random string of specified length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def random_email() -> str:
    """Generate random email"""
    return f"{random_string()}@{random_string(6)}.com"