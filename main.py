import shutil

import cmn
import utl_config
import utl_generate_mask
import glob
import json
import os
import sys
import time
from zipfile import ZipFile
import cli
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





def remover(item):
    iterator = 0
    pick = time.time()
    with ZipFile('/u02/app/oracle/oradata/datastore/logs/odadb1_aud/log.zip', 'w') as zip:
        for file in glob.glob(item["file_mask"]):
            if os.stat(file).st_mtime < pick - item["delay_in_days"] * 86400:
                zip.write(file)
                os.remove(file)
                iterator += 1
                if iterator % 1000 == 0:
                    log('temporary deleted files by mask {mask} is {iterator}'
                        .format(mask=item["file_mask"], iterator=iterator))

    log('deleted files by mask {mask} is {iterator}'.format(mask=item["file_mask"], iterator=iterator))


def checkfile(file):
    cmn.log.debug('found %s',file)

def copyfile(file, dest):
    cmn.log.debug('file %s copy to %s' , file, dest)
    shutil.copy(file, utl_generate_mask.genDate(dest))


def findfiles(action, source, destination,delta):
    cmn.log.debug('findfiles action %s', delta)
    pick = time.time()
    if delta is None: delta = 0
    for file in glob.glob(source):
        if os.stat(file).st_mtime < pick - delta * 86400:
            if action=='check':
                checkfile(file)
            if action == 'cp':

                copyfile(file,destination)







def confIterator():
    cmn.log.debug('confIterator')
    cmn.log.debug(cmn.config)
    for iterKey, iterValue in cmn.config.items():
       if iterValue['action'] in ('check','cp'):
           findfiles(iterValue['action'],iterValue['source'],iterValue.get('dest') ,iterValue.get('delta'))






if __name__ == "__main__":
    cli.read_cli_flags(sys.argv[1:])
    cli.configlogger(filename=cmn.args['logfile'], level='debug')
    utl_config.read_config()
    confIterator()
    # cli.log.debug(utl_generate_mask.genDate('asd%YM%'))


    # utl_config.write_config()

