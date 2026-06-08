from datetime import date

AGE_SCORES = [
    (0, 19, 'до 20 лет', 15),
    (20, 29, '20–29 лет', 45),
    (30, 39, '30–39 лет', 75),
    (40, 49, '40–49 лет', 95),
    (50, 59, '50–59 лет', 105),
    (60, 200, '60 лет и старше', 114),
]

MARITAL_SCORES = {
    'женат/замужем': ('Женат/замужем', 115),
    'холост/не замужем': ('Холост/не замужем', 80),
    'разведен(а)': ('Разведен(а)', 60),
    'вдовец/вдова': ('Вдовец/вдова', 30),
}

DEPENDENTS_SCORES = {
    '0': ('Нет', 87),
    '1': ('1', 65),
    '2': ('2', 40),
    '3': ('3', 20),
    '4': ('Более трёх', 4),
}

INDUSTRY_KEYWORDS = [
    (['госслужб', 'государств', 'муниципал'], 'Госслужба', 124),
    (['коммерч', 'бизнес', 'предприним'], 'Коммерческая деятельность', 110),
    (['пенсион'], 'Пенсионер', 50),
    (['военн', 'силов'], 'Силовые структуры', 100),
    (['образован', 'наук'], 'Образование/наука', 95),
    (['медиц', 'здравоохран'], 'Медицина', 105),
    (['строит'], 'Строительство', 70),
    (['сельск', 'агро'], 'Сельское хозяйство', 55),
]

QUALIFICATION_KEYWORDS = [
    (['руковод', 'директор', 'начальник', 'менеджер'], 'Руководитель', 122),
    (['специалист', 'инженер', 'врач', 'юрист'], 'Специалист', 100),
    (['служащ', 'сотрудник', 'работник'], 'Служащий', 80),
    (['рабоч', 'оператор', 'водитель'], 'Рабочий/вспомогательный', 17),
]


def calculate_age(birthdate_str):
    if not birthdate_str:
        return None
    try:
        parts = birthdate_str.split('-')
        birth = date(int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return None
    today = date.today()
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def score_age(age):
    if age is None:
        return 'Не указан', '', 0
    for low, high, label, score in AGE_SCORES:
        if low <= age <= high:
            return 'Возраст', label, score
    return 'Возраст', str(age), 0


def score_marital(status):
    if status in MARITAL_SCORES:
        label, score = MARITAL_SCORES[status]
        return 'Семейное положение', label, score
    return 'Семейное положение', status or 'Не указано', 50


def score_dependents(dependents):
    key = str(dependents).strip() if dependents else '0'
    if key in DEPENDENTS_SCORES:
        label, score = DEPENDENTS_SCORES[key]
        return 'Число лиц на иждивении', label, score
    return 'Число лиц на иждивении', key, 50


def score_industry(industry):
    text = (industry or '').lower()
    for keywords, label, score in INDUSTRY_KEYWORDS:
        if any(kw in text for kw in keywords):
            return 'Сфера деятельности', label, score
    return 'Сфера деятельности', industry or 'Не указана', 70


def score_qualification(qualification):
    text = (qualification or '').lower()
    for keywords, label, score in QUALIFICATION_KEYWORDS:
        if any(kw in text for kw in keywords):
            return 'Квалификация', label, score
    return 'Квалификация', qualification or 'Не указана', 70


def calculate_scoring(data):
    age = calculate_age(data.get('birthdate', ''))

    scores = [
        score_age(age),
        score_marital(data.get('marital_status', '')),
        score_dependents(data.get('dependents', '0')),
        score_industry(data.get('industry', '')),
        score_qualification(data.get('qualification', '')),
    ]

    total = sum(s[2] for s in scores)

    net_income = 0
    try:
        net_income = float(str(data.get('net_income', '0')).replace(',', '.') or 0)
    except ValueError:
        pass
    if net_income == 0:
        try:
            salary = float(str(data.get('salary', '0')).replace(',', '.') or 0)
            other = float(str(data.get('other_income', '0')).replace(',', '.') or 0)
            payments = float(str(data.get('mandatory_payments', '0')).replace(',', '.') or 0)
            net_income = salary + other - payments
        except ValueError:
            net_income = 0

    solvency = max(0, net_income * 0.5)
    max_loan = solvency * 12 * (total / 100) if total > 0 else 0

    return {
        'score_rows': scores,
        'total_score': total,
        'net_income_calc': f'{net_income:,.2f}'.replace(',', ' ').replace('.', ','),
        'solvency': f'{solvency:,.2f}'.replace(',', ' ').replace('.', ','),
        'max_loan_amount': f'{max_loan:,.2f}'.replace(',', ' ').replace('.', ','),
        'conclusion_text': (
            f'На основании анализа предоставленных данных считаю возможным выдачу кредита '
            f'{{full_name}} в размере {{loan_amount_fmt}} для {{loan_purpose}} '
            f'на {{loan_term}} месяцев под {{interest_rate}}% годовых.'
        ),
    }
