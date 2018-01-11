# coding:utf-8
from app_core.windows_core.base_core.worker_base import WorkerBase
import re


class WinService(object):

    def __init__(self, name, display_name, service_type, service_state, service_action):
        dollar_index = name.find(u'$')
        if dollar_index != -1:
            self.name = name[dollar_index:]
        else:
            self.name = name
        self.title_name = name
        self.display_name = display_name
        self.check_instance()
        self.title_display_name = display_name
        self.service_type = service_type
        self.service_state = service_state
        self.service_action = service_action

    def check_instance(self):
        if self.display_name.find(u"instance") != -1:
            re_result = re.search(r'\(Instance:(.+)\)', self.display_name, re.M | re.I)
            if re_result is not None:
                self.display_name = re_result.group(1)

    def __str__(self):
        return '%s|%s|%s' % (self.name, self.service_state, self.service_action)

    def get_dict(self):
        return self.__dict__


class WinServiceWorker(WorkerBase):

    def get_list(self):
        result = self.run_command(u'sc query state= all')
        return self.read_sc_query(result)

    def get_one(self, name):
        command_result = self.run_command(u'sc queryex "%s"' % name)
        return self.check_result(command_result)

    def start_one(self, name):
        command_result = self.run_command(u'sc start "%s"' % name)
        return self.check_result(command_result)

    def stop_one(self, name):
        command_result = self.run_command(u'sc stop "%s"' % name)
        return self.check_result(command_result)

    def check_result(self, value):
        result = self.read_sc_query(value, error_pass=True)
        if len(result) == 0:
            raise BaseException(value.encode('utf-8'))
        return result

    def read_sc_query(self, value, error_pass=False):
        result_list = []
        for line in value.split('\n\n'):
            try:
                result_list.append(
                    self.make_win_service_instance(line)
                )
            except:
                if error_pass:
                    pass
                else:
                    raise BaseException(line.encode('utf-8'))
        return result_list

    @staticmethod
    def make_win_service_instance(instance_source):
        re_result = re.search(r'SERVICE_NAME: (.+)\n', instance_source, re.M | re.I)
        name = re_result.group(1)
        re_result = re.search(r'\nDISPLAY_NAME:(.+)\n', instance_source, re.M | re.I)
        display_name = None if re_result is None else re_result.group(1)
        re_result = re.search(r'\n( +)TYPE( +): (.+)\n', instance_source, re.M | re.I)
        service_type = re_result.group(3)
        re_result = re.search(r'\n( +)STATE( +): (.+)\n( +)(.+)\n', instance_source, re.M | re.I)
        service_state = re_result.group(3)
        service_action = re_result.group(5) if re_result.group(5).find('WIN32_EXIT_CODE') == -1 else None
        return WinService(name, display_name, service_type, service_state, service_action)


win_service_worker = WinServiceWorker()

if __name__ == '__main__':
    WinServiceWorker().get_list()
    print WinServiceWorker().get_one('SogouSvc')
    print WinServiceWorker().get_one('SogouSvc')
    print [str(line) for line in WinServiceWorker().get_one('SogouSvc')]
