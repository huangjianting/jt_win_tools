# coding: utf-8
import uuid
import os
from app_core.common.time_out import timeout
from logger_helper import logger_runner


class CmdReader(object):

    def __init__(self, cmd_command):
        self.cmd_command = cmd_command
        self.reader_id = str(uuid.uuid1()).replace('-', '')

    @timeout()
    def run_command_and_read(self):
        logger_runner.info(self.cmd_command, self.reader_id)
        p = os.popen(self.cmd_command)
        ret = p.read()
        logger_runner.debug(ret, self.reader_id)
        return ret


if __name__ == '__main__':
    import re
    new_instance = CmdReader("sc query state= all")
    print new_instance.run_command_and_read().decode('gbk')
    for line in new_instance.run_command_and_read().split('\n\n'):
        print [line]
        matchObj = re.search(r'SERVICE_NAME: (.+)\n', line, re.M | re.I)
        # print matchObj.group()
        print matchObj.group(1)
        matchObj = re.search(r'\nDISPLAY_NAME:(.+)\n', line, re.M | re.I)
        # print matchObj.group()
        print matchObj.group(1)
        matchObj = re.search(r'\n( +)TYPE( +): (.+)\n', line, re.M | re.I)
        # print matchObj.group()
        print matchObj.group(3)
        matchObj = re.search(r'\n( +)STATE( +): (.+)\n( +)(.+)\n', line, re.M | re.I)
        # print matchObj.group()
        print matchObj.group(3)
        if matchObj.group(5).find('WIN32_EXIT_CODE') == -1:
            print matchObj.group(5)
