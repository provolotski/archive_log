import datetime


# Подменяем маску для формирования файлов директорий итп маска для месяца %YM%

def genDate(inStr):
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    varc = lastMonth.strftime("%Y-%m")
    return inStr.replace("%YM%", varc)
