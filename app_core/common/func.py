# coding: utf-8
import os


def check_dir(dir_name):
    is_exist = False
    self_cwd = os.getcwd()
    # print os.listdir(self_cwd)
    for line in os.listdir(self_cwd):
        file_path = os.path.join(self_cwd, line)
        if os.path.isdir(file_path):
            if line == dir_name:
                is_exist = True
    if not is_exist:
        new_dir_path = os.path.join(self_cwd, dir_name)
        os.makedirs(new_dir_path)


if __name__ == '__main__':
    check_dir('demo')
