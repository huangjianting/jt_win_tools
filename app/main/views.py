# coding:utf-8
from . import main
from flask import render_template


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@main.route('/on_line')
def on_line():
    return "hello world"
