import getopt
import logging
import sys

# Интерфейс для работы с командной строкой
config_dict = []

# обрабатываемые флаги
# -i --ifile - файл параметра
# -l --lfile - логфайл

def read_cli_flags (args):
    file = ''
    try:
        opts, args = getopt.getopt(args, "hi:o:", ["ifile=", ])
    except getopt.GetoptError:
        logging.warning("no parameter")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            file = arg
            config_dict['file'] = arg
        if opt in ("-l", "--lfile"):
            config_dict['log_file'] = arg
    if len(file) < 5:
        logging.warning("no parameter")
        sys.exit(2)
    return config_dict

