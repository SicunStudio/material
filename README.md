## material
material system for AU website.separated from AUN
## deploy
1. work with AUN(run.py)

```
from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.serving import run_simple
from aun import aun_app 
from material import app as material

application = DispatcherMiddleware(aun_app, {
    '/material':     material
})
run_simple('localhost', 5000, application, use_reloader=True) #or you can use apache through mod_wsgi

```

2. database init
    1. python manage.py db init
    2. python manage.py db migrate
    3. python manage.py db upgrade
3. create super user    
    1. python manage.py create_super_role
    2. python manage.py create_super_user -n name -p password -e email
    