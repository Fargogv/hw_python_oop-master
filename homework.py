import datetime as dt
from typing import Optional


class Calculator:
    """Методы."""

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def get_week_stats(self) -> str:
        """Сколько калорий получено за последние 7 дней/
        Cколько денег потрачено за последние 7 дней."""
        it_now = dt.datetime.now().date()
        it_week_ago = it_now - dt.timedelta(days=7)
        amount = (record.amount for record in self.records
                  if it_week_ago < record.date <= it_now)
        return sum(amount)

    def add_record(self, record):
        """Сохранение новой записи о приёме пищи/
        Сохранение новой записи о расходах."""
        self.records.append(record)

    def get_today_stats(self) -> str:
        """Сколько калорий уже съедено сегодня/
        Cколько денег потрачено сегодня."""
        it_now = dt.datetime.now().date()
        amount = ([record.amount for record
                   in self.records if it_now == record.date])
        return sum(amount)

    def get_today_remained(self) -> float:
        """сколько осталось от лимита."""
        total_amount = self.get_today_stats()
        balance = self.limit - total_amount
        return balance


class Record:
    """Запись данных."""

    def __init__(
            self,
            amount: float,
            comment: str,
            date: Optional[str] = None
    ):
        self.amount = amount
        self.comment = comment
        date_format = '%d.%m.%Y'
        if isinstance(date, str):
            self.date = dt.datetime.strptime(date, date_format).date()
        if date is None:
            self.date = dt.datetime.now().date()


class CaloriesCalculator(Calculator):
    """Калькулятор калорий."""

    def get_calories_remained(self) -> str:
        """Сколько ещё калорий можно/
        нужно получить сегодня."""
        if self.get_today_remained() > 0:
            return ('Сегодня можно съесть что-нибудь ещё,'
                    f' но с общей калорийностью не более '
                    f'{self.get_today_remained():.0f} кКал')
        return 'Хватит есть!'


class CashCalculator(Calculator):
    """Калькулятор денег."""

    USD_RATE = 73.0
    EURO_RATE = 85.0
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        """сколько ещё денег можно потратить сегодня
        в рублях, долларах или евро."""
        currencies = {
            'usd': ('USD', self.USD_RATE),
            'eur': ('Euro', self.EURO_RATE),
            'rub': ('руб', self.RUB_RATE),
        }
        currency_na, currency_rate = currencies[currency]
        today_cash_remained = round(self.get_today_remained()
                                    / currency_rate, 2)
        mod = abs(today_cash_remained)
        if today_cash_remained == 0:
            return 'Денег нет, держись'
        if today_cash_remained > 0:
            return f'На сегодня осталось {today_cash_remained} {currency_na}'
        else:
            return (f'Денег нет, держись: твой долг '
                    f'- {mod} '
                    f'{currency_na}')
