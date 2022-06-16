import shutil
import datetime
import string
import subprocess

import cmn
import glob
import os
import time
from zipfile import ZipFile


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

def copy_file(source, dest):
    # copy file to destination
    cmn.log.debug('file %s copy to %s' , file, dest)
    if dest[-4]=='.':
        make_dir(generate_mask(dest)[0:string.rfind(generate_mask(dest),'/')])
        shutil.copyfile(source, generate_mask(dest))
    else:
        make_dir(generate_mask(dest))
        shutil.copy(source, generate_mask(dest))


def remove_file(file):
    os.remove(file)

def move_file(source, dest):
    # move file to destination
    cmn.log.debug('file %s move to %s' , source, dest)
    make_dir(generate_mask(dest))
    shutil.move(source, generate_mask(dest))

def find_files_by_date( source, delta):
    cmn.log.debug('find_files_by_date action %s', delta)
    pick = time.time()
    res = []
    if delta is None: delta = 0
    for iter_file in glob.glob(source):
        if os.stat(iter_file).st_mtime < pick - delta * 86400:
            res.append(iter_file)
    return res

            # if action=='check':
            #     checkfile(iter_file)
            # if action == 'cp':
            #     copy_file(iter_file, dest)

def findfiles(action, source, destination,delta):
    cmn.log.debug('findfiles action %s', delta)
    pick = time.time()
    if delta is None: delta = 0
    for iter_file in glob.glob(source):
        if os.stat(iter_file).st_mtime < pick - delta * 86400:
            if action=='check':
                checkfile(iter_file)
            if action == 'cp':
                copy_file(iter_file, destination)

def conf_iterator():
    cmn.log.debug('conf_iterator')
    cmn.log.debug(cmn.config)
    for iterKey, iterValue in cmn.config.items():
       if iterValue['action'] in ('check','cp'):
           findfiles(iterValue['action'],iterValue['source'],iterValue.get('dest') ,iterValue.get('delta'))

def generate_mask(mask):
    cmn.log.debug('generate_mask')
    return generate_date(mask)




def make_dir(dir):
    # create directory if not exists
    if not os.path.exists(dir):
        os.makedirs(dir)

def generate_date(input_string):
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    var_char = last_month.strftime("%Y.%m")
    return input_string.replace("%YM%", var_char)

def copy_to_archive(files, archive):
    make_dir(generate_mask(archive)[0:string.rfind(generate_mask(archive), '/')])
    for file in files:
        with ZipFile(generate_mask(archive), 'a') as zip:
            zip.write(file)
            os.remove(file)



def copy_to_server(file, user, server, path ):
    cmd = 'scp {file} {user}@{server}:{path}'.format(file=file, user=user, server=server, path=path)
    subprocess.call(cmd, shell=True)

def move_to_server(file, user, server, path ):
    copy_to_server(file, user, server, path)
    remove_file(file)


if __name__ == "__main__":
    # cli.read_cli_flags(sys.argv[1:])
    # cli.configlogger(filename=cmn.args['logfile'], level='debug')
    # utl_config.read_config()
    # conf_iterator()
    # make_dir(generate_mask('/u02/app/oracle/oradata/datastore/database_logs/test/%YM%/'))
    # copy_file('/u01/app/oracle/diag/rdbms/eisgs00/eisgs001/trace/alert_eisgs001.log', '/u02/app/oracle/oradata/datastore/database_logs/test/odadb1/%YM%/')
    # move_file('/u02/app/oracle/oradata/datastore/database_logs/test/odadb1/2022.05/alert_eisgs001.log', '/u02/app/oracle/oradata/datastore/database_logs/test/odadb2/%YM%/')
    # copy_to_server('/home/oracle/holdi.sql', 'oracle', 'odadb2','/home/oracle/')
    # remove_file('/home/oracle/holdi.sql')
    # copy_file('/home/oracle/holdi.sql','/home/oracle/holdi1.sql')
    # move_to_server('/home/oracle/holdi1.sql', 'oracle', 'odadb2','/home/oracle/')
    filelist  = find_files_by_date('/u01/app/oracle/admin/eisgs03/adump/*.aud', 1)
    copy_to_archive(filelist, '/u02/app/oracle/oradata/datastore/database_logs/odadb1/%YM%/aud.zip')



    # utl_config.write_config()

