import platform
import os
import zipfile
from uuid import getnode as get_mac


def get_os_name():
    return platform.system()


def get_mac_address():
    return ':'.join(("%012X" % get_mac())[i:i + 2] for i in range(0, 12, 2))


def extract_archive(name):
    zip_ref = zipfile.ZipFile(name, 'r')
    zip_ref.extractall(".")
    zip_ref.close()

    # delete archive
    os.remove(name)


def file_exists(path):
    return os.path.isfile(path)
