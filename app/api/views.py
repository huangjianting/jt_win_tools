# coding: utf-8
from . import api
from flask import *
from data_models.result import JsonResult
from app_core.data_check import check_string
from app_core.windows_core.win_service.win_service_worker import win_service_worker
from app_core.windows_core.iis.iis_worker import iis_worker
from app.models import ServerIp
from app import db


@api.route('/win_service', methods=['GET', 'POST'])
def win_service():
    try:
        if request.method == 'GET':
            name = check_string(request.values.get('name'), ['IsNotEmpty'], error_message=u'name 为空')
            if name is None:
                ret = win_service_worker.get_list()
            else:
                ret = win_service_worker.get_one(name)
        elif request.method == 'POST':
            name = check_string(request.json.get('name'), ['IsNotEmpty', 'NotNone'], error_message=u'name error')
            method = check_string(request.json.get('method'), ['IsNotEmpty', 'NotNone'], error_message=u'method error')
            if method.upper() not in ['START', 'STOP']:
                raise BaseException(u'method is undefined')
            if method.upper() == 'START':
                ret = win_service_worker.start_one(name)
            else:
                ret = win_service_worker.stop_one(name)
        else:
            raise BaseException("method is not access")
        ret = [line.get_dict() for line in ret]
        ret = JsonResult.success(ret).to_json()
    except BaseException, e:
        ret = JsonResult.error(e.message).to_json()
    return ret


@api.route('/server', methods=['GET', 'POST', 'DELETE'])
def server():
    try:
        if request.method == 'GET':
            server_ip = check_string(request.values.get('server_ip'), ['IsNotEmpty'], error_message=u'server_ip 为空')
            if server_ip is None:
                ret = [line.to_dict() for line in ServerIp.query.all()]
            else:
                ret = [line.to_dict() for line in ServerIp.query.filter(ServerIp.server_ip == server_ip).all()]
        elif request.method == 'POST':
            server_ip = check_string(request.json.get('server_ip'), ['IsNotEmpty', 'NotNone'], error_message=u'server_ip error')
            ret = ServerIp.query.filter(ServerIp.server_ip == server_ip).all()
            if ret:
                raise BaseException(u"已存在")
            db.session.add(ServerIp(server_ip))
            db.session.commit()
            ret = u"添加成功"
        elif request.method == 'DELETE':
            server_ip = check_string(request.json.get('server_ip'), ['IsNotEmpty', 'NotNone'],
                                     error_message=u'server_ip error')
            ret = ServerIp.query.filter(ServerIp.server_ip == server_ip).all()
            if not ret:
                raise BaseException(u"不存在")
            for line in ret:
                db.session.delete(line)
            db.session.commit()
            ret = u"删除成功"
        else:
            raise BaseException("method is not access")
        ret = JsonResult.success(ret).to_json()
    except BaseException, e:
        ret = JsonResult.error(e.message).to_json()
    return ret


@api.route('/iis', methods=['GET', 'POST'])
def iis():
    try:
        if request.method == 'GET':
            name = check_string(request.values.get('name'), ['IsNotEmpty'], error_message=u'name 为空')
            if name is None:
                ret = iis_worker.get_list()
            else:
                ret = iis_worker.get_one(name)
            ret = [line.get_dict() for line in ret]
        elif request.method == 'POST':
            name = check_string(request.json.get('name'), ['IsNotEmpty', 'NotNone'], error_message=u'name error')
            method = check_string(request.json.get('method'), ['IsNotEmpty', 'NotNone'], error_message=u'method error')
            if method.upper() not in ['START', 'STOP']:
                raise BaseException(u'method is undefined')
            if method.upper() == 'START':
                ret = iis_worker.start_one(name)
            else:
                ret = iis_worker.stop_one(name)
        else:
            raise BaseException("method is not access")
        ret = JsonResult.success(ret).to_json()
    except BaseException, e:
        ret = JsonResult.error(e.message).to_json()
    return ret
