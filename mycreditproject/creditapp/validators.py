import re
from datetime import date

FIO_PATTERN = re.compile(r'^[\sа-яА-ЯёЁa-zA-Z\-]+$')
DEPT_CODE_PATTERN = re.compile(r'^\d{3}-\d{3}$')
INN_PATTERN = re.compile(r'^\d{12}$')
SNILS_PATTERN = re.compile(r'^\d{3}-\d{3}-\d{3} \d{2}$')

REQUIRED_FIO_FIELDS = ('lastname', 'firstname')
# обычный словарь
FIELD_LABELS = {
    'lastname': 'Фамилия',
    'firstname': 'Имя',
    'middlename': 'Отчество',
    'birthdate': 'Дата рождения',
    'department_code': 'Код подразделения',
    'inn': 'ИНН',
    'snils': 'СНИЛС',
    'loan_amount': 'Сумма кредита',
    'interest_rate': 'Процентная ставка',
    'loan_term': 'Срок кредита',
    'bank_officer_name': 'ФИО сотрудника банка',
}

# чтобы не писать кучу if
def _validate_fio(value, field_name):
    if not value or not value.strip():
        if field_name in REQUIRED_FIO_FIELDS:
            return 'ФИО должно содержать только буквы и пробелы'
        return None
    if not FIO_PATTERN.match(value.strip()):
        return 'ФИО должно содержать только буквы и пробелы'
    return None

# переделать бы, тут я путаюсь но эт с днями рождения
def _validate_birthdate(value):
    if not value:
        return 'Укажите корректную дату рождения'
    try:
        parts = value.split('-')
        birth = date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return 'Укажите корректную дату рождения'
    today = date.today()
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    if age < 18 or age > 120:
        return 'Укажите корректную дату рождения'
    return None

# проверка ошибок осная возращает в словарь
def validate_form_data(data):
    errors = {}

    for field in ('lastname', 'firstname', 'middlename', 'bank_officer_name'):
        if field in data:
            err = _validate_fio(data.get(field, ''), field)
            if err:
                errors[field] = err

    if 'birthdate' in data:
        err = _validate_birthdate(data.get('birthdate', ''))
        if err:
            errors['birthdate'] = err

    dept_code = data.get('department_code', '').strip()
    if dept_code and not DEPT_CODE_PATTERN.match(dept_code):
        errors['department_code'] = 'Код подразделения должен быть в формате xxx-xxx'

    inn = data.get('inn', '').strip()
    if inn and not INN_PATTERN.match(inn):
        errors['inn'] = 'ИНН должен состоять из 12 цифр'

    snils = data.get('snils', '').strip()
    if snils and not SNILS_PATTERN.match(snils):
        errors['snils'] = 'СНИЛС должен быть в формате xxx-xxx-xxx xx'

    loan_amount = data.get('loan_amount', '').strip()
    if loan_amount:
        try:
            if float(loan_amount) <= 0:
                errors['loan_amount'] = 'Сумма кредита должна быть положительным числом'
        except ValueError:
            errors['loan_amount'] = 'Сумма кредита должна быть положительным числом'

    interest_rate = data.get('interest_rate', '').strip()
    if interest_rate:
        try:
            rate = float(interest_rate.replace(',', '.'))
            if rate < 0 or rate > 100:
                errors['interest_rate'] = 'Ставка должна быть от 0 до 100 %'
        except ValueError:
            errors['interest_rate'] = 'Ставка должна быть от 0 до 100 %'

    loan_term = data.get('loan_term', '').strip()
    if loan_term:
        try:
            term = int(loan_term)
            if term < 1 or term > 360:
                errors['loan_term'] = 'Срок кредита — от 1 до 360 месяцев'
        except ValueError:
            errors['loan_term'] = 'Срок кредита — от 1 до 360 месяцев'

    return errors
