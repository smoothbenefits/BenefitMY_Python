from functools import wraps
from django.core.exceptions import PermissionDenied
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.decorators import available_attrs

from app.models.company_user import CompanyUser

ADMIN = 'admin'
EMPLOYEE = 'employee'
BROKER = 'broker'


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
            if not request.user.is_authenticated():
                raise PermissionDenied()

            if test_func(request, **kwargs):
                return view_func(clz, request, *args, **kwargs)
            else:
                raise PermissionDenied()
        return _wrapped_view
    return decorator


def company_employer(request, **kwargs):
    """ check if a user is the admin of a company"""

    if 'pk' not in kwargs:
        return False
    else:
        company_id = kwargs['pk']
        user_id = request.user.id
        return CompanyUser.objects.filter(
            user=user_id,
            company=company_id,
            company_user_type=ADMIN).exists()


def company_broker(request, **kwargs):
    """ check if a user is the broker of a company"""

    if 'pk' not in kwargs:
        return False
    else:
        company_id = kwargs['pk']
        user_id = request.user.id
        return CompanyUser.objects.filter(
            user=user_id,
            company=company_id,
            company_user_type=BROKER).exists()


def company_employer_or_broker(request, **kwargs):
    """ check if a user is the broker or admin of a company"""

    if 'pk' not in kwargs:
        return False
    else:
        company_id = kwargs['pk']
        user_id = request.user.id
        return CompanyUser.objects.filter(
            user=user_id,
            company=company_id,
            company_user_type__in=[BROKER, ADMIN]).exists()
