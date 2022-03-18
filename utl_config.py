# work with config
import json
import cli
import cmn


def read_config():
    cmn.log.debug('read_config')
    with open(cmn.args['file'], "r") as read_file:
        cmn.config = json.load(read_file)
    cmn.log.debug(cmn.config)


def write_config():
    with open(cmn.args['file'], 'w') as file:
        file.write(json.dumps(cmn.config))


def getMaxKey():
    cmn.log.debug(cmn.config)
    if not cmn.config:
        cmn.log.debug('empty')
        return 0
    else:
        return int(max(cmn.config, key=cmn.config.get))


def add_action(value):
    num = 1 + getMaxKey()
    cmn.config[num] = value
