from django.contrib.auth.decorators import login_required

from app.models.company_user import CompanyUser


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


login_required = login_required


def is_employer(user_id, company_id):
    """ check if a user is the admin of a company"""
    try:
        CompanyUser.objects.get(user=user_id,
                                company=company_id,
                                company_user_type='admin')
        return True
    except CompanyUser.DoesNotExist:
        return False


def is_broker(user_id, company_id):
    """ check if a user is the broker of a company"""
    try:
        CompanyUser.objects.get(user=user_id,
                                company=company_id,
                                company_user_type='broker')
        return True
    except CompanyUser.DoesNotExist:
        return False


def is_employee(user_id, company_id):
    """ check if a user is the employee of a company"""
    try:
        CompanyUser.objects.get(user=user_id,
                                company=company_id,
                                company_user_type='employee')
        return True
    except CompanyUser.DoesNotExist:
        return False
