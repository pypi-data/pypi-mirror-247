import re

class Validator:
    @staticmethod
    def _print_message(template_type, value, is_valid):
        status = "соответствует" if is_valid else "не соответствует"
        print(f"Номер {template_type} {value} {status} шаблону.")

    @staticmethod
    def validate_number(phone_number):
        phone_pattern = re.compile(r'^\+998\d{9}$')
        is_valid = bool(re.fullmatch(phone_pattern, phone_number))
        Validator._print_message("телефона", phone_number, is_valid)
        return is_valid

    @staticmethod
    def validate_passport_number(passport_number):
        passport_pattern = re.compile(r'^[A-Z]{2}\d{7}$')
        is_valid = bool(re.fullmatch(passport_pattern, passport_number))
        Validator._print_message("паспорта", passport_number, is_valid)
        return is_valid

