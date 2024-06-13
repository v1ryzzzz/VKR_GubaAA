import random
import string


def generate_password_code():
    return ''.join(
        random.choices(
            string.digits,
            k=6
        )
    )
