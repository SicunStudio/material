#-*-coding:urf-8-*-
# flask-principal load user's permission into session
from flask_login import login_user, current_user, logout_user
from flask_principal import identity_loaded, RoleNeed, UserNeed, ActionNeed
from flask_principal import Identity, identity_changed

from material import app


@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    try:
        # Set the identity user object
        identity.user = current_user
        # user has the permission of edit himself

        identity.provides.add(EditUserPermission(current_user.id))

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
            for role in current_user.roles:
                identity.provides.add(RoleNeed(role.roleName))

        # Assuming the User model has a list of nodes, update the
        # identity with the nodes that the user provides
        if hasattr(current_user, "roles"):
            for role in current_user.roles:
                for node in role.nodes:
                    if (node.status == 1) and (current_user.status == 1) and (role.status == 1):
                        identity.provides.add(ActionNeed(node.nodeName))
    except:
        pass


@app.route('/login', methods=["POST", "GET"])
def login():
    pass


@app.route('/logout')
@login_required
def logout():
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    return redirect(request.args.get('next') or '/')
