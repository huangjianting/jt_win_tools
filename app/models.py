# coding:utf-8
import time
import datetime
from app import db


def get_time(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S',
                         time.localtime(timestamp)) + '.' + str(int((timestamp-int(timestamp))*1000))


def to_dict(self):
    re = {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
    for line in re:
        if type(re[line]) == datetime.datetime:
            re[line] = re[line].strftime('%Y-%m-%d %H:%M:%S')
    return re

db.Model.to_dict = to_dict


class ServerIp(db.Model):
    __tablename__ = 'ServerIp'

    id = db.Column(db.Integer, primary_key=True)
    server_ip = db.Column(db.String(64), unique=True)
    create_date = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    def __init__(self, server_ip):
        self.server_ip = server_ip

    def __repr__(self):
        return '<ServerIp %r>' % self.server_ip


if __name__ == '__main__':
    from app import create_app
    app = create_app()
    db.create_all(app=app)
