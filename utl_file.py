
import os
import subprocess


# потом возможно уберу, но пока для работы с файлами по сети
def move_to_server(file, user, server, path ):
    cmd = 'scp {file} {user}@{server}:{path}'.format(file=file, user=user, server=server, path=path)
    subprocess.call(cmd, shell=True)
    p = subprocess.run(["scp", file,user+'@'+server+':'+path ])
    sts = os.waitpid(p.pid, 0)


