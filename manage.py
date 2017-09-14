# -*- coding:utf-8 -*-

""" management script of AUN
"""

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from material import app, db
from material.models import *

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("db", MigrateCommand)  # 数据库我迁移命令


def add_and_commit(*items):
    for item in items:
        db.session.add(item)
    db.session.commit()


@manager.option('-n', '--name', dest="name", help='Your name', default="admin")
@manager.option('-p', '--password', dest='password', help="Your password", default="123456")
@manager.option('-e', '--email', dest="email", help="your email", default=None)
@manager.option('--phone', dest="phone", help="your phone", default=None)
def create_super_user(name, password, email, phone):
    """
    create super user
    """
    try:
        user = User(name, password, email, phone)
        user.add_role("超管")
        add_and_commit(user)
        print("successfully create a super user name:%s,password:%s,email:%s,phone:%s" % (
            name, password, email, phone))
    except:
        print("something wrong.please ensure you have created a super role and your name is unique")


@manager.command
def create_super_role():
    """
    create super role
    """
    try:
        role = Role("超管")

        node1 = Node("materialAdmin", 1)
        node2 = Node("materialAction", 1)

        add_and_commit(node1, node2, role)

        role = Role.query.filter(Role.role_name == "超管").first()

        role.add_node("materialAction")
        role.add_node("materialAdmin")

        add_and_commit(role)

        print("successfully create a super role name:超管")
    except:
        print("you can only run it once or something wrong")


if __name__ == '__main__':
    manager.run()
