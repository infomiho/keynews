#! /usr/bin/env python

import os
from flask_script import Manager, Server
from app import create_app, db
from flask_apscheduler import APScheduler

app = create_app(os.getenv('APP_CONFIG', 'default'))
manager = Manager(app)
manager.add_command("runserver", Server(host='0.0.0.0'))


@manager.command
def create_db():
    print('> Droping db...')
    db.drop_all()
    print('> Creating db...')
    db.create_all()


@manager.shell
def make_shell_context():
    return dict(app=app, db=db)


if __name__ == '__main__':
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    manager.run()
