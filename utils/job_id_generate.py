import uuid


def generate_uuid(length):
    """
    Генерирует шестнадцатеричный UUID с заданной длиной.
    Например:d9f3a7e8

    Args:
       length (int): количество цифр uuid
    """
    return str(uuid.uuid4().hex)[:length]
