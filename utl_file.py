 # потом возможно уберу, но пока для работы с файлами по сети
import os
import subprocess

def move_to_server(file, user, server, path ):
    p = subprocess.run(["scp", file,user+'@'+server+':'+path ])
    sts = os.waitpid(p.pid, 0)


