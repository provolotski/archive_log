# Command line parameters

# Config file data
import logging

config = {}

# default parameters
args = {'file': 'config.json', 'logfile': 'logfile.log'}

# default logger
log = logging.getLogger('utilityApp')

log_level = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING
}

avail_action = ['del', 'cp', 'scp', 'mv', 'scpm', 'zip', 'check']
# 'del'  - delete files by mask
# 'cp' - copy files by mask
# 'scp' - copy files to remote host
# 'mv' move files
# 'scpm' move files to remote host
# 'zip' packing files
# 'check' print to log files