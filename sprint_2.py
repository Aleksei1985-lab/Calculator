from datetime import datetime as dt, date, timedelta

date_format = '%d.%m.%Y'

class Record:
    """Сохраняет записи за 7 дней."""
    def __init__(self, amount, comment, date_str=None):
        """Инициализирует кол-во калорий или трат, 
        комментарий и дату."""
        self.amount = amount # количество потраченных денег или калорий
        self.comment = comment

        if date_str is None: # если дата не передается
            self.date = date.today() # устанавливается сегодняшняя дата
            # в формате date_format = '%d.%m.%Y' и перевод строки обратно в формат даты
        else: # если дата передается как строка, то дата преобразуется в date_format = '%d.%m.%Y'
            self.date = dt.strptime(date_str, date_format).date() #
        

class Calculator:
    """Родительский класс для обоих калькуляторов.
    Вычисляет общие данные функциями."""
    def __init__(self, limit): # конструктор
        """Инициализирует лимит калорий или трат."""
        self.limit = limit
        self.records = []
    
    def add_record(self, record):
        """Сохраняет новую запись о расходах."""
        self.records.append(record)
        
    def get_today_stats(self):
        """Считает сколько денег потрачено сегодня."""
        today = date.today()
        return sum(r.amount for r in self.records if r.date == today)

    def get_week_stats(self):
        """Считает, сколько денег потрачено 
        за последние 7 дней."""
        today = date.today()
        week_ago = today - timedelta(days=7)

        total = 0
        for r in self.records:
            if week_ago <= r.date <= today:
                total += r.amount

        return total


class CashCalculator(Calculator):
    """Калькулятор денег."""

    def get_today_cash_remained(self, currency):
        """Определяет сколько денег можно потратить
        сегодня в рублях, доллорах или евро."""
        # курс валют
        USD = 78
        EURO = 90
        
        spent_today = self.get_today_stats()

        if currency == 'rub':
            spent_today = spent_today
        elif currency == 'usd':
            spent_today = spent_today * USD
        elif currency == 'euro':
            spent_today = spent_today * EURO
        currency = 'рублей'

        cash_remaind = self.limit - spent_today
        cash_remaind = round(cash_remaind, 2)

        if cash_remaind > 0:
            return (f'На сегодня осталось {cash_remaind} {currency}')
        elif cash_remaind == 0:
            return f'Денег нет, держитись'
        else:
            return (f'Денег нет, держитесь: твой долг: {cash_remaind} {currency} ')


class CaloriesCalc(Calculator):
    """"Калькулятор калорий."""

    def get_calories_remained(self):
        """Определяет, сколько еще калорий можно/нужно
        получить сегодня."""
        remaining = self.limit - self.get_today_stats()
        if remaining > 0:
            return (f'Сегодня можно съесть что-нибудь еще, но с общей калорийностью не более {remaining} кКал')
        else:
            return f'Хватит есть!'
        

# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(5000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=54, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=30, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=35,
                                  comment='бар в Танин др',
                                  date_str='09.04.2025'))

print(cash_calculator.get_today_cash_remained('usd'))
print(cash_calculator.get_today_cash_remained('rub'))
print(cash_calculator.get_today_cash_remained('euro'))
# должно напечататься
# На сегодня осталось 555 руб

cal_calculator = CaloriesCalc(1000)
cal_calculator.add_record(Record(145, "кофе"))
cal_calculator.add_record(Record(321, "обед"))

print(cal_calculator.get_calories_remained())

    