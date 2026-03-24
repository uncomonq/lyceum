__all__ = ()


def normalize_user_email(email):
    if not email:
        return ""

    local_part, _, domain = email.strip().lower().partition("@")
    local_part = local_part.split("+", maxsplit=1)[0]

    if domain == "ya.ru":
        domain = "yandex.ru"

    if domain == "gmail.com":
        local_part = local_part.replace(".", "")
    elif domain == "yandex.ru":
        local_part = local_part.replace(".", "-")

    return f"{local_part}@{domain}" if domain else local_part
