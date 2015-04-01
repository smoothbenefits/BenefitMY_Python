import urlparse
from functools import wraps

from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import available_attrs

from app.models.company_user import CompanyUser


def user_passes_test(test_func,
                     login_url=None,
                     redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.

    minor changes patches to django source code
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(clz, request, *args, **kwargs):
            if test_func(request, **kwargs):
                return view_func(clz, request, *args, **kwargs)
            path = request.build_absolute_uri()
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                        settings.LOGIN_URL)[:2]
            current_scheme, current_netloc = urlparse.urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(path, login_url, redirect_field_name)
        return _wrapped_view
    return decorator


def check_company_employer(request, **kwargs):
    """ check if a user is the admin of a company"""

    if 'pk' not in kwargs:
        return False
    else:
        company_id = kwargs['pk']
        user_id = request.user.id
        return CompanyUser.objects.filter(
            user=user_id,
            company=company_id,
            company_user_type='admin').exists()
