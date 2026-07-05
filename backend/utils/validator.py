import re


def is_empty(value):
    return value is None or str(value).strip() == ""


def is_valid_email(email):
    if is_empty(email):
        return False

    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email.strip()) is not None


def is_valid_phone(phone):
    if is_empty(phone):
        return True

    pattern = r"^(0|\+84)[0-9]{9}$"
    return re.match(pattern, phone.strip()) is not None


def validate_todo(title, description=None):
    errors = []

    if is_empty(title):
        errors.append("Tiêu đề công việc không được để trống.")
    elif len(title.strip()) > 120:
        errors.append("Tiêu đề công việc tối đa 120 ký tự.")

    if description and len(description.strip()) > 1000:
        errors.append("Mô tả công việc tối đa 1000 ký tự.")

    return errors