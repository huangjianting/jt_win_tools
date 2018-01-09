# coding: utf-8
from cmd_reader import CmdReader


class WorkerBase(object):

    @staticmethod
    def run_command(cmd_command):
        return CmdReader(cmd_command.encode('gb2312')).run_command_and_read().decode('gbk')