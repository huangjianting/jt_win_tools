# coding:utf-8
from app_core.windows_core.base_core.worker_base import WorkerBase
import re


class IIS(object):

    def __init__(self, iis_id, name, address, port, iis_state, iis_bind):
        self.iis_id = iis_id
        self.name = name
        self.address = address
        self.port = port
        self.iis_state = iis_state
        self.iis_bind = iis_bind

    def __str__(self):
        return '%s|%s|%s' % (self.name, self.port, self.iis_state)

    def get_dict(self):
        return self.__dict__


class IISWorker(WorkerBase):
    app_cmd_path = ur"C:\Windows\System32\inetsrv"

    def get_list(self):
        result = self.run_command(ur'%s\appcmd list sites' % self.app_cmd_path)
        return self.read(result)

    def get_one(self, name):
        command_result = self.run_command(ur'%s\appcmd list sites "%s"' % (self.app_cmd_path, name))
        return self.check_result(command_result)

    def start_one(self, name):
        command_result = self.run_command(ur'%s\appcmd start site "%s"' % (self.app_cmd_path, name))
        return self.check_result_message(command_result, u'已成功启动')

    def stop_one(self, name):
        command_result = self.run_command(ur'%s\appcmd stop site "%s"' % (self.app_cmd_path, name))
        return self.check_result_message(command_result, u'已成功停止')

    @staticmethod
    def check_result_message(value, message):
        if value.find(message) != -1:
            return value
        else:
            raise BaseException(value.encode('utf-8'))

    def check_result(self, value):
        result = self.read(value, error_pass=True)
        if len(result) == 0:
            raise BaseException(result.encode('utf-8'))
        return result

    def read(self, value, error_pass=False):
        result_list = []
        if value[-1] == '\n':
            value = value[:-1]
        for line in value.split('\n'):
            try:
                result_list.append(
                    self.make_instance(line)
                )
            except:
                if error_pass:
                    pass
                else:
                    raise BaseException(value.encode('utf-8'))
        return result_list

    @staticmethod
    def make_instance(instance_source):
        re_result = re.search(r'SITE "(.+)" \(id:(.+),bindings:(.+),state:(.+)\)', instance_source, re.M | re.I)
        name = re_result.group(1)
        iis_id = re_result.group(2)
        bindings = re_result.group(3)
        iis_state = re_result.group(4)
        address = ''
        port = ''
        iis_bind = ''
        for binding in bindings.split(','):
            if not address == port == iis_bind == '':
                address += '/'
                port += '/'
                iis_bind += '/'
            if binding.find('net.') == 0 or binding.find('msmq.') == 0:
                bind = [binding, '', '']
            else:
                bind = binding.split(':')
            address += bind[0]
            port += bind[1]
            iis_bind += bind[2]
        return IIS(iis_id, name, address, port, iis_state, iis_bind)


iis_worker = IISWorker()

if __name__ == '__main__':
    print [str(line) for line in iis_worker.get_list()]
    print iis_worker.start_one('pos_api')
    print [str(line) for line in iis_worker.get_one('pos_api')]
    print iis_worker.stop_one('pos_api')
    print [str(line) for line in iis_worker.get_one('pos_api')]
    print iis_worker.start_one('pos_api')
    print [str(line) for line in iis_worker.get_list()]
    print iis_worker.start_one('pos_api1')
