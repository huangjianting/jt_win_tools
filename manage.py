# coding:utf-8
import os
from app import create_app
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand


# app = create_app('development_home')
app = create_app()
manager = Manager(app)
manager.add_command("runserver", Server(use_debugger=True), port=6000)


def make_shell_context():
    pass


if __name__ == '__main__':
    manager.run()
