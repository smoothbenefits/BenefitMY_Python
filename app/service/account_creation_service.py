from django.contrib.auth import get_user_model
from django.conf import settings
from app.models.company_user import CompanyUser
from app.models.company import Company
from app.custom_authentication import AuthUserManager
from app.models.person import Person
from app.models.employee_profile import FULL_TIME, PART_TIME
from app.views.util_view import onboard_email
from app.service.user_document_generator import UserDocumentGenerator
from app.dtos.issue import Issue
from app.serializers.person_serializer import PersonSimpleSerializer
from app.serializers.employee_profile_serializer import EmployeeProfilePostSerializer
from app.serializers.employee_compensation_serializer import EmployeeCompensationPostSerializer
from app.service.hash_key_service import HashKeyService
from app.dtos.operation_result import OperationResult

User = get_user_model()

class AccountCreationService(object):

    REQUIRED_RAW_DATA_FIELDS = [
        'first_name',
        'last_name',
        'aaa',
        'bbb'
    ]

    def parse_raw_data(self, batch_account_raw_data):
        result = OperationResult(batch_account_raw_data)

        # check all lines for number of fields
        # if found bad ones, send the main wrapper back without
        # construting the individual ones
        for line in batch_account_raw_data.raw_data.split('\n'):
            tokens = line.split('\t')
            if (len(tokens) != len(self.REQUIRED_RAW_DATA_FIELDS)):
                result.append_issue(
                    'The following line does not have enough information: %s' % line
                )

        return result

    def validate(self, account_info):
        result = OperationResult(account_info)

        if (account_info is None or
            account_info.company_id is None or
            account_info.company_user_type is None or
            account_info.first_name is None or
            account_info.last_name is None or
            account_info.compensation_info is None):
            result.append_issue(
                "Missing necessary information for account creation"
            )

        try:
            Company.objects.get(pk=account_info.company_id)
        except Company.DoesNotExist:
            result.append_issue(
                "Specificed company does not exist"
            )

        company_users = CompanyUser.objects.filter(
            company=account_info.company_id)

        for c in company_users:
            if (c.company_user_type == account_info.company_user_type and
                    c.user.email == account_info.email):
                result.append_issue(
                    "Specified email has already been used"
                )

        if (not account_info.send_email and account_info.password is None):
            result.append_issue(
                "Missing initial password for the new account"
            )

        # Now validate the initial compensation record
        if (account_info.employment_type == PART_TIME):
            if (account_info.compensation_info.hourly_rate is None or 
                account_info.compensation_info.projected_hour_per_month is None):
                result.append_issue(
                    "Compensation record info is incomplete"
                )
        elif (account_info.employment_type == FULL_TIME):
            if (account_info.compensation_info.annual_base_salary is None):
                result.append_issue(
                    "Compensation record info is incomplete"
                )

        result.set_output_data(account_info)

        return result

    def validate_batch(self, account_creation_data_list):
        result = OperationResult(account_creation_data_list)

        if (account_creation_data_list is None or len(account_creation_data_list) <= 0):
            result.append_validation_issue(
                'Did not find any account info to handle'
            )
        else:
            # Also do some batch level validations
            exist_emails = []
            has_invalid = False
            account_validation_results = []

            for account_info in account_creation_data_list:
                if account_info.email not in exist_emails:
                    exist_emails.append(account_info.email)
                else:
                    result.append_validation_issue(
                        'The email specificed is also used on another account in this batch'
                    )
                account_result = self.validate(account_info)
                if (account_result.has_issue()):
                    has_invalid = True
                account_validation_results.append(account_result)

            if (has_invalid):
                result.append_issue(
                    'There are validation issues on some account info.'
                )

            result.set_output_data(account_validation_results)
            return result

    def execute_creation(self, account_info, do_validation=True): 
        result = OperationResult(account_info)
        account_result = None

        # Do validation first, and short circuit if failed
        if (do_validation):
            account_result = self.validate(account_info)
        else:
            # directly construct the result, skipping validation
            account_result = OperationResult(account_info)

        # If the account creation info is not valid to begin with
        # simply short circuit and return it
        if (account_result.has_issue()):
            return account_result

        userManager = AuthUserManager()

        # Create the actual user data
        password = settings.DEFAULT_USER_PW
        if account_info.password:
            password = account_info.password
        User.objects.create_user(account_info.email, password)
        if not userManager.user_exists(account_info.email):
            raise Exception(
                "Failed to create user account"
            )

        user = userManager.get_user(account_info.email)
        user.first_name = account_info.first_name
        user.last_name = account_info.last_name
        user.save()

        # Create the company_user data
        company_user = CompanyUser(company_id=account_info.company_id,
                                   user=user,
                                   company_user_type=account_info.company_user_type)

        if account_info.new_employee is not None:
            company_user.new_employee = account_info.new_employee

        company_user.save()

        # Now create the person object
        person_data = {'first_name': account_info.first_name,
                       'last_name': account_info.last_name,
                       'user': user.id,
                       'relationship': 'self',
                       'person_type': 'primary_contact',
                       'company': account_info.company_id,
                       'email': user.email}

        person_serializer = PersonSimpleSerializer(data=person_data)
        if person_serializer.is_valid():
            person_serializer.save()
        else:
            raise Exception("Failed to create person record")

        # Create the employee profile
        key_service = HashKeyService()
        person_id = key_service.decode_key(person_serializer.data['id'])
        profile_data = {
            'person': person_id,
            'company': account_info.company_id
        }

        if (account_info.annual_base_salary is not None):
            profile_data['annual_base_salary'] = account_info.annual_base_salary

        if (account_info.employment_type is not None):
            profile_data['employment_type'] = account_info.employment_type

        profile_serializer = EmployeeProfilePostSerializer(data=profile_data)

        if profile_serializer.is_valid():
            profile_serializer.save()
        else:
            raise Exception("Failed to create employee profile record")

        # Now check to see send email and create documents
        if company_user.company_user_type == 'employee':
            if account_info.send_email:
                # now try to create the onboard email for this user.
                try:
                    onboard_email("%s %s" % (user.first_name, user.last_name),
                                  account_info.company_id,
                                  account_info.email,
                                  user.id
                                  )
                except StandardError:
                    raise Exception(
                        "Failed to send email to employee"
                    )

            if (account_info.create_docs and
                account_info.doc_fields is not None):

                # Let's create the documents for this new user
                try:
                    doc_gen = UserDocumentGenerator(company_user.company, user)
                    doc_gen.generate_all_document(account_info.doc_fields)
                except Exception:
                    raise Exception(
                        "Failed to generate documents for employee"
                    )

            # Create the initial compensation record
            compensation_data = {
                'person': person_id,
                'company': account_info.company_id,
                'annual_base_salary': account_info.compensation_info.annual_base_salary,
                'projected_hour_per_month': account_info.compensation_info.projected_hour_per_month,
                'hourly_rate': account_info.compensation_info.hourly_rate,
                'effective_date': account_info.compensation_info.effective_date,
                'increase_percentage': None
            }

            compensation_serializer = EmployeeCompensationPostSerializer(data=compensation_data)

            if (compensation_serializer.is_valid()):
                compensation_serializer.save()
            else:
                raise Exception("Failed to create compensation record")

            account_info.user_id = user.id

            account_result.set_output_data(account_info)

        return account_result

    def execute_creation_batch(self, account_creation_data_list):
        result = self.validate_batch(account_creation_data_list)
        if (result.has_issue()):
            return result

        account_results = []

        for account_info in account_creation_data_list:
            account_result = self.execute_creation(account_info, False)
            account_results.append(account_result)

        result.set_output_data(account_results)
        return result
