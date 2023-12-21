##
##

import platform
import os


class SysInfo(object):

    def __init__(self):
        self.os_type = platform.system()

    @staticmethod
    def get_proc_fs(parameter):
        value = None

        path_prefix = '/proc/sys/'
        path_suffix = parameter.replace('.', '/')
        search_path = path_prefix + path_suffix

        try:
            with open(search_path, 'r') as proc_file:
                line = proc_file.read()
                value = line.split()[-1]
            proc_file.close()
        except OSError:
            pass

        return int(value)

    @staticmethod
    def get_mac_sysctl(parameter):
        value = None

        for line in os.popen('sysctl -a'):
            line = line.strip()
            if line.startswith(parameter):
                value = line.split(':')[-1]
                value = value.lstrip()

        return value

    def get_net_buffer(self):
        value = None

        if self.os_type == 'Linux':
            value = self.get_proc_fs('net.ipv4.tcp_wmem')
        elif self.os_type == 'Darwin':
            value = self.get_mac_sysctl('kern.ipc.maxsockbuf')

        if value:
            return int(value)
        else:
            return None
