import platform
from uuid import getnode as get_mac


def get_os_name():
    return platform.system()


def get_mac_address():
    return ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))


