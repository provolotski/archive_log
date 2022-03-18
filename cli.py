import getopt
import logging
import sys

# managed flags
# -i --ifile - parameter file
# -l --lfile - logfile
# -a --add -add action
# -s --src --source -source
# -d --dest -destination
import cmn


def read_cli_flags(args):
    try:
        opts, args = getopt.getopt(args, "hi:o:a:s:d:", ["ifile=", "add=", "src=", "source=", "dest="])
    except getopt.GetoptError:
        logging.warning("no parameter")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            cmn.args['file'] = arg
        if opt in ("-l", "--lfile"):
            cmn.args['logfile'] = arg
        if opt in ("-a", "--add"):
            if arg in cmn.avail_action:
                cmn.args['action'] = arg
        if opt in ("-s", "--src", "--source"):
            cmn.args['source'] = arg
        if opt in ("-d", "--dest"):
            cmn.args['dest'] = arg
    print(cmn.args)
    # if len(file) < 5:
    #     cmn.log.warning("no parameter")
    #     sys.exit(2)


def configlogger(level, filename):
    fileh = logging.FileHandler(filename, 'a')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fileh.setFormatter(formatter)

    for hdlr in cmn.log.handlers[:]:  # remove all old handlers
        cmn.log.removeHandler(hdlr)
    cmn.log.addHandler(fileh)  # set the new handler
    if level in cmn.log_level:
        cmn.log.setLevel(cmn.log_level[level])
        cmn.log.debug(level)
