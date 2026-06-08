from datetime import datetime

MONTHS_RU = [
    '', 'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
    'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря',
]


def capitalize_word(word):
    if not word:
        return ''
    if '-' in word:
        return '-'.join(capitalize_word(part) for part in word.split('-'))
    return word[0].upper() + word[1:].lower() if len(word) > 1 else word.upper()


def format_fio(lastname='', firstname='', middlename=''):
    parts = [lastname, firstname, middlename]
    return ' '.join(capitalize_word(p.strip()) for p in parts if p and p.strip())


def format_date_ru(date_str):
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return f'«{dt.day:02d}» {MONTHS_RU[dt.month]} {dt.year} г.'
    except ValueError:
        return date_str


def format_date_short(date_str):
    if not date_str:
        return ''
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.strftime('%d.%m.%Y')
    except ValueError:
        return date_str


def format_passport(series, number, issue_date, issued_by, dept_code):
    parts = []
    if series or number:
        parts.append(f'серия {series or "____"} № {number or "______"}')
    if issue_date:
        parts.append(f'выдан {format_date_short(issue_date)}')
    if issued_by:
        parts.append(issued_by)
    if dept_code:
        parts.append(f'код подразделения {dept_code}')
    return ', '.join(parts) if parts else ''


def format_currency(amount, currency='RUB'):
    if not amount:
        return ''
    try:
        val = float(str(amount).replace(',', '.').replace(' ', ''))
        formatted = f'{val:,.2f}'.replace(',', ' ').replace('.', ',')
        symbols = {'RUB': 'руб.', 'USD': 'USD', 'EUR': 'EUR'}
        return f'{formatted} {symbols.get(currency, currency)}'
    except ValueError:
        return str(amount)


def build_context(data):
    full_name = format_fio(
        data.get('lastname', ''),
        data.get('firstname', ''),
        data.get('middlename', ''),
    )
    bank_officer = format_fio_from_string(data.get('bank_officer_name', ''))
    collateral_owner = format_fio_from_string(data.get('collateral_owner', ''))

    passport = format_passport(
        data.get('passport_series', ''),
        data.get('passport_number', ''),
        data.get('passport_issue_date', ''),
        data.get('issued_by', ''),
        data.get('department_code', ''),
    )

    birth_info = ''
    if data.get('birthdate') or data.get('birth_place'):
        birth_info = f'{format_date_short(data.get("birthdate", ""))}, {data.get("birth_place", "")}'.strip(', ')

    work_place = ''
    if data.get('employer') or data.get('position'):
        work_place = f'{data.get("employer", "")}, {data.get("position", "")}'.strip(', ')

    credit_history = ''
    if data.get('has_previous_loans') == 'да':
        credit_history = data.get('previous_loans_details', 'Имеются предыдущие кредиты')
    else:
        credit_history = 'Предыдущие кредиты отсутствуют'

    current_date = data.get('current_date') or datetime.now().strftime('%Y-%m-%d')

    return {
        'full_name': full_name,
        'lastname': capitalize_word(data.get('lastname', '')),
        'firstname': capitalize_word(data.get('firstname', '')),
        'middlename': capitalize_word(data.get('middlename', '')),
        'birthdate': format_date_short(data.get('birthdate', '')),
        'birth_place': data.get('birth_place', ''),
        'birth_info': birth_info,
        'citizenship': data.get('citizenship', ''),
        'marital_status': data.get('marital_status', ''),
        'dependents': data.get('dependents', ''),
        'doc_type': data.get('doc_type', 'Паспорт гражданина РФ'),
        'passport_series': data.get('passport_series', ''),
        'passport_number': data.get('passport_number', ''),
        'passport_issue_date': format_date_short(data.get('passport_issue_date', '')),
        'issued_by': data.get('issued_by', ''),
        'department_code': data.get('department_code', ''),
        'passport_full': passport,
        'registration_address': data.get('registration_address', ''),
        'factual_address': data.get('factual_address', '') or data.get('registration_address', ''),
        'phone': data.get('phone', ''),
        'email': data.get('email', ''),
        'inn': data.get('inn', ''),
        'snils': data.get('snils', ''),
        'client_password': data.get('client_password', ''),
        'employer': data.get('employer', ''),
        'position': data.get('position', ''),
        'work_place': work_place,
        'industry': data.get('industry', ''),
        'qualification': data.get('qualification', ''),
        'salary': data.get('salary', ''),
        'other_income': data.get('other_income', ''),
        'mandatory_payments': data.get('mandatory_payments', ''),
        'net_income': data.get('net_income', ''),
        'loan_purpose': data.get('loan_purpose', ''),
        'loan_amount': data.get('loan_amount', ''),
        'loan_amount_fmt': format_currency(data.get('loan_amount', ''), data.get('currency', 'RUB')),
        'currency': data.get('currency', 'RUB'),
        'loan_term': data.get('loan_term', ''),
        'interest_rate': data.get('interest_rate', ''),
        'total_cost_percent': data.get('total_cost_percent', ''),
        'total_cost_rub': data.get('total_cost_rub', ''),
        'overpayment': data.get('overpayment', ''),
        'penalty': data.get('penalty', ''),
        'product_category': data.get('product_category', ''),
        'total_product_cost': data.get('total_product_cost', ''),
        'initial_fee': data.get('initial_fee', ''),
        'collateral_subject': data.get('collateral_subject', ''),
        'collateral_location': data.get('collateral_location', ''),
        'collateral_storage': data.get('collateral_storage', ''),
        'collateral_owner': collateral_owner,
        'guarantor_data': data.get('guarantor_data', ''),
        'has_previous_loans': data.get('has_previous_loans', ''),
        'previous_loans_details': data.get('previous_loans_details', ''),
        'credit_history': credit_history,
        'bki_name': data.get('bki_name', ''),
        'property_list': data.get('property_list', ''),
        'bank_name': data.get('bank_name', ''),
        'bank_location': data.get('bank_location', ''),
        'bank_inn': data.get('bank_inn', ''),
        'bank_bik': data.get('bank_bik', ''),
        'correspondent_account': data.get('correspondent_account', ''),
        'client_account': data.get('client_account', ''),
        'bank_officer_position': data.get('bank_officer_position', ''),
        'bank_officer_name': bank_officer,
        'authority_basis': data.get('authority_basis', ''),
        'current_date': format_date_ru(current_date),
        'current_date_short': format_date_short(current_date),
        'loan_type': data.get('loan_purpose', 'потребительский'),
        'security': data.get('collateral_subject', '') or 'не предусмотрено',
    }


def format_fio_from_string(fio_str):
    if not fio_str or not fio_str.strip():
        return ''
    return ' '.join(capitalize_word(w) for w in fio_str.strip().split())
