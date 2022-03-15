# Параметры командной строки

# данные  конфиг файла
import logging

config = {}

# Интерфейс для работы с командной строкой
args = {'file': 'config.json', 'logfile': 'log/logfile.log'}

# логгер для приложения
log = logging.getLogger('utilityApp')

log_level = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING
}

avail_action = ['del', 'cp', 'scp', 'mv', 'scpm', 'zip']
# 'del'  - удалить файлы по  маске
# 'cp' - копировать файлы по маске
# 'scp' - копировать  на удаленный сервер
# 'mv' переместить файлы
# 'scpm' переместить на удаленный сервер
# 'zip' запаковать