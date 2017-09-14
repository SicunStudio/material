#--coding:UTF-8--
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from material import db

# user models
role_node = db.Table('role_node',  # 角色权限关联表
                     db.Column(
                         'node_id', db.Integer, db.ForeignKey('node.node_id')),
                     db.Column(
                         'role_id', db.Integer, db.ForeignKey('role.role_id')),
                     db.Column(
                         'created_at', db.DateTime, default=datetime.now)
                     )

user_role = db.Table('user_role',  # 用户角色关联表
                     db.Column(
                         'user_id', db.Integer, db.ForeignKey('user.user_id')),
                     db.Column(
                         'role_id', db.Integer, db.ForeignKey('role.role_id')),
                     db.Column(
                         'created_at', db.DateTime, default=datetime.now)
                     )


class User(db.Model, UserMixin):
    """ User table
    """
    __tablename__ = "user"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(40))
    status = db.Column(db.Boolean)
    remark = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    roles = db.relationship(
        "Role", secondary=user_role, backref=db.backref('users', lazy="dynamic"))

    def verify_password(self, password):
        """ verify password
        """
        return check_password_hash(self.password, password)

    def get_id(self):
        return self.user_id

    @property
    def nodes(self):
        """ 
        Return
            user's all permission node
        """
        node = []
        for r in self.role:
            node = node + r.nodes
        return node

    def add_role(self, role_name):
        role = Role.query.filter(Role.role_name == role_name).first()
        self.roles.append(role)

    def __init__(self, user_name, password, email, phone):
        self.user_name = user_name
        self.password = generate_password_hash(password)
        self.email = email
        self.status = True
        self.phone = phone

    def __str__(self):
        return self.user_name

    __repr__ = __str__


class Node(db.Model):
    """ node table
    """
    __tablename__ = "node"
    node_id = db.Column(db.Integer, primary_key=True)
    node_name = db.Column(db.String(30), unique=True)
    remark = db.Column(db.String(30))
    status = db.Column(db.Boolean)
    level = db.Column(db.Integer)

    def __init__(self, node_name, level):
        self.node_name = node_name
        self.status = 1
        self.level = level

    def __str__(self):
        return self.node_name

    __repr__ = __str__


class Role(db.Model):
    """ 
    role table
    """
    __tablename__ = "role"
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30), unique=True)
    status = db.Column(db.Boolean)
    remark = db.Column(db.String(30))

    nodes = db.relationship(
        "Node", secondary=role_node, backref=db.backref('roles', lazy="dynamic"))

    def add_node(self, node_name):
        """ 
        add node for a role
        """
        n = Node.query.filter(Node.node_name == node_name).first()
        self.nodes.append(n)

    def __init__(self, role_name):
        self.role_name = role_name
        self.status = 1

    def __str__(self):
        return self.role_name

    __repr__ = __str__


class LoginLog(db.Model):
    """ login log 
    """
    log_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64))
    login_time = db.Column(db.DateTime)
    login_ip = db.Column(db.String(40))

    def __init__(self, user_name, login_ip):
        self.user_name = user_name
        self.login_time = datetime.utcnow()
        self.login_ip = login_ip

    def __str__(self):
        return self.user_name
    __repr__ = __str__


# material model
class Base(object):
    '''the base of all the apply tables'''
    id = db.Column(db.INT, primary_key=True)
    apply_time = db.Column(db.DateTime)
    approve_time = db.Column(db.DateTime, nullable=True)
    result = db.Column(db.CHAR(1), default='0', nullable=False)
    applicant = db.Column(db.String(10), nullable=False)
    advice = db.Column(db.String(20))
    pre_verify = db.Column(db.String(20))
    is_print = db.Column(db.CHAR(1))
    filename = db.Column(db.VARCHAR(50))
    rand_filename = db.Column(db.VARCHAR(15))

    association = db.Column(db.String(10), nullable=False)
    tel = db.Column(db.String(15))
    date = db.Column(db.DateTime)
    site = db.Column(db.String(10))
    submit_user_id = db.Column(db.Integer)


class Base1(object):
    '''the base of east4,outdoor,sacenter,special'''
    activity = db.Column(db.String(15))
    number = db.Column(db.SMALLINT)
    sponsor = db.Column(db.TEXT)
    opinion = db.Column(db.String(10))
    content = db.Column(db.TEXT)
    resp_person = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(6))


class East4(db.Model, Base, Base1):
    '''model of east4'''
    __tablename__ = 'material_east4'
    site = None


class Outdoor(db.Model, Base, Base1):
    '''model of outdoor'''
    __tablename__ = 'material_outdoor'


class Sacenter(db.Model, Base, Base1):
    '''model of student activity center'''
    __tablename__ = 'material_sacenter'
    is_query = db.Column(db.CHAR(1))
    site_type = db.Column(db.CHAR(1))


class Special(db.Model, Base, Base1):
    '''model of special'''
    __tablename__ = 'material_special'
    is_query = db.Column(db.CHAR(1))


class Colorprint(db.Model, Base):
    '''model of colorprint'''
    __tablename__ = 'material_colorprint'
    finish_date = db.Column(db.DateTime)
    is_sponsor = db.Column(db.CHAR(1))
    remark = db.Column(db.TEXT)
    time = db.Column(db.String(6))
    content = db.Column(db.TEXT)
    resp_person = db.Column(db.String(10), nullable=False)


class Sports(db.Model, Base):
    '''model of sports'''
    __tablename__ = 'material_sports'
    school_id = db.Column(db.String(10))
    remark = db.Column(db.TEXT)
    time = db.Column(db.String(6))
    resp_person = db.Column(db.String(10), nullable=False)
    department = db.Column(db.String(15))
    content = db.Column(db.TEXT)


class Materials(db.Model, Base):
    '''model of material'''
    __tablename__ = 'material_material'
    resp_person = db.Column(db.String(10), nullable=False)
    activity = db.Column(db.String(15))
    opinion = db.Column(db.String(20))
    projector_date = db.Column(db.DATE)
    projector_num = db.Column(db.SMALLINT)
    chair_date = db.Column(db.DATE)
    electricity_num = db.Column(db.SMALLINT)
    desk_num = db.Column(db.SMALLINT)
    chair_num = db.Column(db.SMALLINT)
    trans_desk_num = db.Column(db.SMALLINT)
    trans_chair_num = db.Column(db.SMALLINT)


class Teachingbuilding(db.Model, Base):
    '''model of teachingbuilding'''
    __tablename__ = 'material_teachingbuilding'
    content = db.Column(db.TEXT())
    activity = db.Column(db.String(15))
    signature = db.Column(db.String(10))
    capacity = db.Column(db.SMALLINT)
    number = db.Column(db.SMALLINT)
    week = db.Column(db.String(5))
    person_type = db.Column(db.CHAR(5))
    function = db.Column(db.CHAR(5))
    phone = db.Column(db.String(15))
    section = db.Column(db.CHAR(5))
    activity_type = db.Column(db.CHAR(1))
    host = db.Column(db.String(10))
    unit = db.Column(db.String(20))
    title = db.Column(db.String(10))
    resp_person = db.Column(db.String(10), nullable=False)
