import json
import decimal
import logging
import traceback
from django.contrib.auth import get_user_model

from app.service.company_personnel_service import CompanyPersonnelService
from app.service.integration.integration_provider_data_service_base import IntegrationProviderDataServiceBase
from app.service.integration.integration_provider_service import (
        INTEGRATION_SERVICE_TYPE_PAYROLL,
        INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL,
        IntegrationProviderService
    )

from app.models.integration.company_integration_provider import CompanyIntegrationProvider
from app.models.integration.company_user_integration_provider import CompanyUserIntegrationProvider

User = get_user_model()


class AdvantagePayrollDataService(IntegrationProviderDataServiceBase):

    def __init__(self):
        super(AdvantagePayrollDataService, self).__init__()
        self.company_personnel_service = CompanyPersonnelService()
        self.integration_provider_service = IntegrationProviderService()

    def _integration_service_type(self):
        return INTEGRATION_SERVICE_TYPE_PAYROLL

    def _integration_provider_name(self):
        return INTEGRATION_PAYROLL_ADVANTAGE_PAYROLL

    def _internal_generate_and_record_external_employee_number(self, employee_user_id):
        # First check whether the said employee already have a number
        # If so, this is an exception state, log it, and skip the operation
        employee_number = self.integration_provider_service.get_employee_integration_provider_external_id(
            employee_user_id,
            self._integration_service_type(),
            self._integration_provider_name())
        if (employee_number):
            logging.error('Invalid Operation: Try to generate external ID for employee (User ID={0}) already has one!'.format(employee_user_id))
            return

        company_id = self.company_personnel_service.get_company_id_by_employee_user_id(employee_user_id)
        next_employee_number = self._get_next_external_employee_number(company_id)
        # Now save the next usable external employee number to the profile
        # of the specified employee
        self.integration_provider_service.set_employee_integration_provider_external_id(
            employee_user_id,
            self._integration_service_type(),
            self._integration_provider_name(),
            next_employee_number)

    def _get_next_external_employee_number(self, company_id):
        employee_number_seed_str = self.integration_provider_service.get_company_integration_provider_employee_external_id_seed(
            company_id,
            self._integration_service_type(),
            self._integration_provider_name())
        employee_number_seed = 0
        if (employee_number_seed_str):
            try: 
                employee_number_seed = int(employee_number_seed_str)
            except ValueError:
                logging.exception('Encountered malformed external employee number seed: "{0}"'.format(employee_number_seed_str))

        max_employee_number = self._get_max_external_employee_number(company_id)
        return max(employee_number_seed, max_employee_number) + 1

    def _get_max_external_employee_number(self, company_id):
        all_employee_data = CompanyUserIntegrationProvider.objects.filter(
                company_user__company=company_id,
                integration_provider__service_type=self._integration_service_type(),
                integration_provider__name=self._integration_provider_name())

        employee_numbers = []
        for employee_data in all_employee_data:
            if (employee_data.company_user_external_id):
                # For AP, it is assumed that all employee numbers 
                # are positive integers. Though just build some 
                # fault tolerence here, to log the exception and
                # let it go, to not block all employee creations
                # if for some reason there is a malformed ID in 
                # system.
                try: 
                    employee_number = int(employee_data.company_user_external_id)
                    employee_numbers.append(employee_number)
                except ValueError:
                    logging.exception('Encountered malformed external employee number: "{0}"'.format(employee_data.company_user_external_id))

        if (len(employee_numbers) > 0):
            return max(employee_numbers)

        return 0
