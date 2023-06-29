from functools import wraps
from django.shortcuts import redirect, reverse

def admin_login_required(f):
    @wraps(f)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Redirect to admin login pag if not authenticated
            return redirect(reverse('admin:login'))
        elif not request.user.is_superuser:
            # Redirect to admin login page if the user is not an admin
            return redirect(reverse('admin:login'))
        else:
            return f(request, *args, **kwargs)
            
    return wrapper