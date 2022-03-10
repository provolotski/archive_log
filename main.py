import getopt
import glob
import json
import os
import sys
import time
from zipfile import ZipFile
import utl_generate_mask

log_file = 'zipper.log'


def remove_log():
    global log_file
    with open(log_file, "a+") as f:
        f.write('\n')
        f.write('--------------------------------------------------------------------------------\n')
        f.write('\n')


def log(message):
    global log_file
    strmsg = time.strftime('%Y.%m.%d %T') + ' ' + message + '\n'
    with open(log_file, "a+") as f:
        f.write(strmsg)


def json_load(file_name):
    with open(file_name, "r") as read_file:
        data = json.load(read_file)
    return data


def read_config():
    file = ''
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["ifile=", ])
    except getopt.GetoptError:
        log("no parameter1")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            file = arg
        if opt in ("-l", "--lfile"):
            global log_file
            log_file = arg
    if len(file) < 5:
        log("no parameter")
        sys.exit(2)
    return json_load(file)


def remover(item):
    iterator = 0
    pick = time.time()
    with ZipFile('/u02/app/oracle/oradata/datastore/logs/odadb1_aud/log.zip','w') as zip:
        for file in glob.glob(item["file_mask"]):
            if os.stat(file).st_mtime < pick - item["delay_in_days"] * 86400:
                zip.write(file)
                os.remove(file)
                iterator += 1
                if iterator % 1000 == 0:
                    log('temporary deleted files by mask {mask} is {iterator}'
                        .format(mask=item["file_mask"], iterator=iterator))

    log('deleted files by mask {mask} is {iterator}'.format(mask=item["file_mask"], iterator=iterator))


def main():
    masks = read_config()
    remove_log()
    for item in masks:
        remover(masks[item])


if __name__ == "__main__":
    print(utl_generate_mask.genDate('asd%YM%'))

