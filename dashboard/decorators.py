from django.http import HttpResponse
from functools import wraps
from django.contrib.auth.decorators import login_required

def role_base(required_role=None):
    def decorator(func):
        @wraps(func)
        @login_required
        def inner(request,*args,**kwargs):
            user = request.user
            if required_role == user.role:
                return func(request,*args,**kwargs)
            else:
                 return HttpResponse('<div> You are not authorized for this page </div>')
        return inner
    return decorator